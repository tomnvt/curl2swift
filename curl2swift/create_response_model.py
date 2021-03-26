import logging
from curl2swift.templates import CODABLE_TEMPLATE


def get_value_type_in_swift(key, value):
    if type(value) == str:
        return 'String'
    elif type(value) == int:
        return 'Int'
    elif type(value) == float:
        return 'Double'
    elif type(value) == bool:
        return 'Bool'
    elif type(value) == list:
        if value:
            return '[' + get_value_type_in_swift(key, value[0]) + ']'
        return '[Any]'
    elif type(value) == dict:
        return key[:-1] if key[-1] == 's' else key
    else:
        return 'String'



def add_submodel(model_dict, model_name):
    submodels.append(create_response_model(model_dict, model_name))


submodels = []
DEFAULT_MODEL_NAME = 'Response'

def create_response_model(response_json, model_name='Response'):
    logging.info("Creating response model")
    properties = []
    coding_keys = []
    for key in response_json:
        value = response_json[key]
        value_type = get_value_type_in_swift(key, value)
        if type(value) == dict:
            add_submodel(value, value_type)
        elif type(value) == list and value:
            if type(value[0]) == dict:
                add_submodel(value[0], value_type[1:-1])
        property_name = key[0].lower() + key[1:]
        if "_" in property_name:
            split = property_name.split('_')
            property_name = split[0] + ''.join([word[0].upper() + word[1:] for word in split[1:]])
        properties.append('let ' + property_name + ' : ' + value_type + '?')
        coding_keys.append('case ' + property_name + ' = "' + key + '"')
    processed_response_template = CODABLE_TEMPLATE.replace('<PROPERTIES>', '\n        '.join(properties))
    processed_response_template = processed_response_template\
        .replace('<CODING_KEYS>', '\n            '.join(coding_keys))\
        .replace('<MODEL_NAME>', model_name)
    if model_name == DEFAULT_MODEL_NAME:
        processed_response_template += ''.join(reversed(submodels))
    return processed_response_template
