import subprocess

from curl2swift.parse_content import ParsedContent
from curl2swift.templates import *
import re
from curl2swift.create_request import create_request
from curl2swift.pprint_color import pprint_color


def process_request_template(content: ParsedContent, header_rows, body_param_rows, response_model):
    two_level_indent_sep = '\n        '
    processed_template = REQUEST_TEMPLATE
    processed_template = processed_template.replace('<REQUEST_NAME>', content.request_name)
    processed_template = processed_template.replace('<DESC>', content.description)
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

    processed_template = processed_template.replace('<RESPONSE>', response_model)

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
