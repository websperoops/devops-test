import abc
from collections.abc import Iterable

from django.db import connection
from django.db.utils import OperationalError

import logging
import time


class Handler(abc.ABC):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, integration_name, name):

        '''
        This class is meant to be inherited to sync integration objects/resources from APIs
        in batch transactions

        The general idea is to load batches of objects into memory, and then perform
        single transactions to optimze efficiancy and reduce creating uneccesary connections at
        high volume

        Args:
            data (dict): API response data
            integration_id (int): the id for the integraion
            user_iden (int): the user's id
            integration_name (str): hardcoded name specifying the integration itself, (i.e shopify or etsy)
            name (str): hardcoded name specifying the core object/resource

        NOTE: When calling the super() function please call it at the end of the object's
        contructor after you've created you neccesary instance data structures to store response data
        '''

        self.data = data
        self.batch_size=len(data)
        self.integration_id = integration_id
        self.user_iden=user_iden
        self.bad_model_fields = ['_state', 'id', '_uncommitted_filefields', '_django_version']
        self.integration_name = integration_name
        self.name=name
        self.__parse_data()
        Handler.log_behavior(f"successfully read in {self.name}, API response data into handler of length {self.batch_size}")


    @staticmethod
    def log_sql():

        '''
        This function can be called by any Handler class and will output the logs for
        MySQL and list all current transactions
        '''

        def dictfetchall(cursor):
            "Return all rows from a cursor as a dict"
            columns = [col[0] for col in cursor.description]
            lst = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            new_lst = []
            for obj in lst:
                string = ""
                for k, v in obj.items():
                    string += str(k) + ":" + str(v) + "\n"
                new_lst.append(string)
            return new_lst

        with connection.cursor() as cursor:
            cursor.execute(r"SHOW ENGINE INNODB STATUS")
            Handler.log_behavior("CURRENT INNODB ENGINE STATUS:\n")
            for log in dictfetchall(cursor):
                Handler.log_behavior(log)

            cursor.execute(r"SELECT * FROM `information_schema`.`innodb_trx` ORDER BY `trx_started`;")
            Handler.log_behavior("CURRENT_RUNNING_TXNS:\n")
            for log in dictfetchall(cursor):
                Handler.log_behavior(log)


    @staticmethod
    def log_behavior(msg):
        '''
        This function can be called by any Handler class and will log debugger output
        '''
        Handler.logger.info(msg)



    def save_all_objects(self):
        Handler.log_behavior(f"trying to save/update {self.batch_size} {self.name} objects...")
        '''
        This function save independent and dependent objects to the database
        and returns a message on the number of objects inserted/updated,
        this should be logged
        '''
        funcs = [
                    {
                        "func":self.__save_independent_objects,
                        "type":"independent"
                    },

                    {
                        "func":self.__save_dependent_objects,
                        "type":"dependent"
                    }
                ]

        for f_obj in funcs:
            growth_factor = 5
            TRIES = 3
            SLEEPTIME = 0.2
            while True:
                start_time = time.time()
                try:
                    f_obj["func"]()

                    type = f_obj["type"]
                    Handler.log_behavior("successfuly saved {0} {1} objects for integration{2}.".format(type, self.name,self.integration_name))
                    break

                except OperationalError as e:
                    code = e.args[0]
                    Handler.log_behavior("time elapsed before failing/catching excpetion: " + str(time.time()-start_time))

                    # Raise exception if ran out of tries OR error is not either a Deadlock Error(1213) or a Lock wait timeout(1205)
                    if TRIES == 0 or code != 1213 or code !=1205:
                        Handler.log_sql()
                        raise e
                    else:
                        TRIES -= 1
                        Handler.logger.warning(f"Encountered an operational error: {str(e)}, \nSLEEPING FOR {SLEEPTIME} seconds and trying again...")
                        Handler.logger.warning(f"{TRIES} tries left!")
                        time.sleep(SLEEPTIME)
                        SLEEPTIME *= growth_factor

                except Exception as e:
                    Handler.log_behavior("time elapsed before failing/catching excpetion: " + str(time.time()-start_time))
                    Handler.log_sql()
                    raise e

        Handler.log_behavior(f"Successfully inserted/updated {len(self)} {self.name} records for the {self.integration_name} integration")


    @abc.abstractmethod
    def __save_independent_objects(self):

        '''
        Save databse objects/records, that are NOT DEPENDENT on the core
        API resource being saved in the database or any other object, in a SINGLE TRANSACTION
        (i.e it should no foriegn key attributes pointing outwards)
        NOTE:
            This can be done by importing the transaction decorater from the django.db
            module, then using the 'with' key board to declare an atomic transaction within
            the function call. ex...

            with transaction.atomic():
                save_objects_to_database()

        If helper methods are needed, please use
        save_[object/table name]() as a naming convention
        '''

        return

    @abc.abstractmethod
    def __save_dependent_objects(self):

        '''
        Save databse objects/records, that are DEPENDENT on the core
        API resource being saved in the database or any other object, in a SINGLE TRANSACTION
        (i.e it should no foriegn key attributes pointing outwards)

        If there are multiple "levels" of dependancy for example,
        There is an object that is dependent on the core resource, and then there is another
        object that is dependent on that ex:

            [obj2] -> fk relation -> [obj1] -> fk relation -> [Core object]

        You can create 2 functions that are both there own transaction and then call them both
        in __save_dependant_objects

        ex:


            def __save_dependent_objects(self):
                self.save_dep_obj_1()
                self.save_dep_obj_2()

            def save_dep_obj_1(self):
                with transaction.atomic():
                    ....

            def save_dep_obj_2(self):
                with transaction.atomic():
                    ....


        NOTE:
            This can be done by importing the transaction decorater from the django.db
            module, then using the 'with' key board to declare an atomic transaction within
            the function call. ex...

            with transaction.atomic():
                save_objects_to_database()

        If helper methods are needed, please use
        save_[object/table name]() as a naming convention
        '''

        return



    @abc.abstractmethod
    def __parse_data(self):
        '''
        This method is called on initialization, and populates data structures attactched to the instance,
        with API response data so that it can be saved in a batch transaction. If helper methods are needed, please use
        the grab_[object/table name]() naming convention
        '''


    def get_instances_if_exists(self, modelType, modelInstance, unique_attr=None):
        '''
        Args:
            modelType: models.Model
            modelInstance: models.Model()
            unique_attr: str or list or dict()


        This method will take a database type,  and instance of that type
        and try to return a QuerySet object of existing records with similar unique attributes if provided,

        If not similar records are found, the None is returned

        '''
        if modelInstance:
            obj = dict(modelInstance.__dict__)

            for fld in self.bad_model_fields:
                try:
                    del obj[fld]
                except Exception:
                    pass

            if not unique_attr:
                objects = modelType.objects.filter(**obj)

            else:
                if type(unique_attr) == type(list()):
                    pk_iden = {}
                    for attr in unique_attr:
                        pk_iden[attr] = getattr(modelInstance, attr, None)

                elif type(unique_attr) == type(dict()):
                    pk_iden = unique_attr

                else:
                    pk_iden = {unique_attr:getattr(modelInstance, unique_attr, None)}

                objects = modelType.objects.filter(**pk_iden)

            if len(objects) > 0:
                return objects

            else:
                return None
        else:
            return None



    def update_or_save_instance(self, modelType, modelInstance, unique_attr=None):
        '''
        Args:
            modelType: models.Model
            modelInstance: models.Model()
            unique_attr: str or list or dict()

        This method will take a database type, and and instance of that type
        and try to update an existing record with similar unique attributes if provided
        if not, it will treat every attribute as unique together. If an existing model
        does not exist with the specified unique attributes then it will save a new database record
        '''

        if modelInstance:
            obj = dict(modelInstance.__dict__)


            for fld in self.bad_model_fields:
                try:
                    del obj[fld]
                except Exception:
                    pass

            dataset = self.get_instances_if_exists(modelType, modelInstance, unique_attr=unique_attr)

            if dataset:
                dataset.update(**obj)
            else:
                modelInstance.save()


    def __str__(self):

        ''' Print method meant for debugging '''

        d = self.__dict__
        string = ""
        for k, v in d.items():
            if k != "data":
                val = ""
                if isinstance(v, Iterable):
                    for obj in v:
                        val += str(obj) +"\n"
                else:
                    val = str(v)
                string += str(k) + " : " + val + "\n"

        return string


    def __len__(self):

        ''' Returns the batch size to be save/inserted to the database '''

        return self.batch_size
