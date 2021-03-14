import subprocess

from curl2swift.parse_content import ParsedContent
from curl2swift.templates import *
import re
from curl2swift.parse import parse
from curl2swift.pprint_color import pprint_color
import requests

response_json = 'aww'


def process_request_template(curl, parser, content: ParsedContent, header_rows, body_param_rows):
    two_level_indent_sep = '\n        '
    processed_template = REQUEST_TEMPLATE
    processed_template = processed_template.replace('<REQUEST_NAME>', content.request_name)
    processed_template = processed_template.replace('<PATH>', content.path)
    processed_template = processed_template.replace('<METHOD>', '.' + content.method.lower())

    processed_template = processed_template.replace('<HEADERS>', two_level_indent_sep.join(header_rows))
    processed_template = processed_template.replace('<BODY_PARAMS>', two_level_indent_sep.join(body_param_rows))

    processed_template = processed_template.replace('<PATH_PARAMS>', two_level_indent_sep.join(content.path_param_rows))
    if content.path_param_rows:
        processed_template = processed_template.replace('<PATH_PARAM_SETTER>', PATH_PARAM_SETTER)
    else:
        processed_template = re.sub('\n\s*enum PathParameter: String \{\n\s*\}', '', processed_template)
        processed_template = re.sub('\n\s*<PATH_PARAM_SETTER>', '', processed_template)

    if content.headers:
        processed_template = processed_template.replace('<HEADER_PARAM_SETTER>', HEADER_PARAM_SETTER)
    else:
        processed_template = re.sub('\n\s*enum Header: String \{\n\s*\}', '', processed_template)
        processed_template = re.sub('\n\s*<HEADER_PARAM_SETTER>', '', processed_template)

    if body_param_rows:
        processed_template = processed_template.replace('<BODY_PARAM_SETTER>', BODY_PARAM_SETTER)
    else:
        processed_template = re.sub('\n\s*enum BodyParameter: String \{\n\s*\}', '', processed_template)
        processed_template = re.sub('\n\s*<BODY_PARAM_SETTER>', '', processed_template)

    code = parse(curl, parser)
    exec('global response_json\nresponse_json = (' + code + '.json())')

    properties = []
    coding_keys = []
    for key in response_json:
        value = response_json[key]
        if type(value) == str:
            value_type = 'String'
        elif type(value) == int:
            value_type = 'Int'
        elif type(value) == float:
            value_type = 'Double'
        elif type(value) == bool:
            value_type = 'Bool'
        elif type(value) == list:
            # TODO: Get item type
            value_type = '[String]'
        elif type(value) == dict:
            value_type = key[0].upper() + key[1:]
        else:
            value_type = 'String'
        property_name = key[0].lower() + key[1:]
        if "_" in property_name:
            split = property_name.split('_')
            property_name = split[0] + ''.join([word[0].upper() + word[1:] for word in split[:1]])
        properties.append('let ' + property_name + ' : ' + value_type + '?')
        coding_keys.append('case ' + property_name + ' = "' + key + '"')
    processed_response_template = CODABLE_TEMPLATE.replace('<PROPERTIES>', '\n        '.join(properties))
    processed_response_template = processed_response_template\
        .replace('<CODING_KEYS>', '\n            '.join(coding_keys))
    processed_template = processed_template.replace('<RESPONSE>', processed_response_template)

    print('\n' + '- ' * 9)
    print('GENERATED REQUEST:')
    print('' + '- ' * 9 + '\n')
    pprint_color(processed_template)
    print('\n' + '- ' * 12)
    print('END OF GENERATED OUTPUT')
    print('' + '- ' * 12 + '\n')

    should_copy = input('Copy output to clipboard? [y/n]\n')

    if should_copy == 'y':
        subprocess.run("pbcopy", universal_newlines=True, input=processed_template)
