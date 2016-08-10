import unittest
import decimal

def decimilify(obj):
    if isinstance(obj, float):
        return decimal.Decimal(obj)
    elif isinstance(obj, list):
        new_list = [decimilify(item) for item in obj]
        return new_list
    elif isinstance(obj, dict):
        for key in obj:
            obj[key] = decimilify(obj[key])
        return obj
    else:
        return obj
