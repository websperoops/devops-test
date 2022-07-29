from django.core.cache import cache


class Lock(object):

    def __init__(self, user_iden, integration, expiry=(60*75)):
        self.expiry = expiry
        self.lock_id = '{0}-lock-{1}'.format(integration, user_iden)
        # cache.add will return false if the key already exists (i.e its locked)
        # otherwise it will return True, (it's unlocked, and then will lock it)
        self.unlocked = cache.add(self.lock_id, 1, expiry)


    def release(self):
        cache.delete(self.lock_id)
