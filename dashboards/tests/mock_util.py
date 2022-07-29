from decimal import Decimal
import json
from unittest.mock import Mock


def create_object(attributes):
    """
    Create an mock object with the attributes provided
    Args:
        attributes: a dict with keys representing attribute names and values
        representing attribute values

    Returns: the mock object with the attributes

    """
    obj = Mock()
    for key, value in attributes.items():
        if isinstance(value, dict):
            o = create_object(value)
            setattr(obj, key, o)
        elif isinstance(value, list):
            ls = []
            for child in value:
                if isinstance(child, dict):
                    o = create_object(child)
                    ls.append(o)
                else:
                    ls.append(child)
            setattr(obj, key, ls)
        else:
            setattr(obj, key, value)
        obj.mock_add_spec(spec=key)
    return obj


def create_mock_from_json(json_file_path):
    """

    Args:
        json_file_path: filepath to the json file

    Returns:
        a mock object with all the attributes from the json file
    """
    with open(json_file_path) as json_file:
        attributes = json.load(json_file)

    obj = create_object(attributes)
    return obj

def get_decimal(val, decimal_places):
    if val is None:
        return None
    else:
        return Decimal( f'%.{decimal_places}f' % float(val))