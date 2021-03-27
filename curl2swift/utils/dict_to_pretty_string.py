import json


def dict_to_pretty_string(the_dict, indent=4):
    if not the_dict:
        return "{}"

    return ("\n" + " " * indent).join(
        json.dumps(the_dict, sort_keys=True, indent=indent, separators=(',', ': ')).splitlines())
