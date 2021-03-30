from curl2swift.utils.logger import logging
from curl2swift.templates.codable_template import CODABLE_TEMPLATE


submodels = []
DEFAULT_MODEL_NAME = 'Response'


def get_value_type_in_swift(key, value, is_in_list = False):
    if isinstance(value, str):
        return 'String'
    elif isinstance(value, bool):
        return 'Bool'
    elif isinstance(value, int):
        return 'Int'
    elif isinstance(value, float):
        return 'Double'
    elif isinstance(value, list):
        if value:
            return '[' + get_value_type_in_swift(key, value[0], True) + ']'
        return '[Any]'
    elif isinstance(value, dict):
        if is_in_list:
            singular = key[:-1] if key[-1] == 's' else key
            return singular[0].upper() + singular[1:]
        else:
            return key[0].upper() + key[1:]
    else:
        return 'String'



def add_submodel(model_dict, model_name):
    logging.info("Submodel found: " + model_name)
    if model_dict:
        submodels.append(create_response_model(model_dict, model_name))
    else:
        logging.warning("Found empty dictionary in key " + model_name +
                        '. This key will be ignored.')
        return

def create_response_model(response_json, model_name='Response'):
    global submodels
    if model_name == 'Response':
        submodels = []
    model_name = model_name.replace('/', '')
    logging.info("Creating response model for " + model_name)
    properties = []
    coding_keys = []

    for key in response_json:
        value = response_json[key]
        value_type = get_value_type_in_swift(key, value)

        if isinstance(value, dict):
            add_submodel(value, value_type)
        elif isinstance(value, list) and value:
            if isinstance(value[0], dict):
                add_submodel(value[0], value_type[1:-1])

        property_name = key[0].lower() + key[1:]
        property_name = property_name.replace('/', '')
        if "_" in property_name:
            split = property_name.split('_')
            property_name = split[0] + ''.join([word[0].upper() + word[1:] for word in split[1:]])
        properties.append('let ' + property_name + ' : ' + value_type + '?')
        coding_keys.append('case ' + property_name + ' = "' + key + '"')

    processed_response_template = CODABLE_TEMPLATE\
        .replace('<PROPERTIES>', '\n        '.join(properties))

    processed_response_template = processed_response_template\
        .replace('<CODING_KEYS>', '\n            '.join(coding_keys))\
        .replace('<MODEL_NAME>', model_name)
    if model_name == DEFAULT_MODEL_NAME:
        processed_response_template += ''.join(reversed(submodels))
    return processed_response_template
