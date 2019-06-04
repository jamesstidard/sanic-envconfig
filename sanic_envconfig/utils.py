import json


def load_flat_json(path):
    """
    Turns json data from:

    {
        "a": 1,
        "b": {
            "c": 2,
            "d": 3
        }
    }

    to:

    {
        "a": 1,
        "b__c": 2,
        "b__d": 3
    }
    """
    with open(path) as fp:
        data = json.load(fp)

    def dive(obj, prefix=()):
        if isinstance(obj, dict):
            for key, value in obj.items():
                yield from dive(value, prefix=[*prefix, key])
        else:
            yield '__'.join(prefix), obj

    return dict(dive(data))
