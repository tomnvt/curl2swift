
from curl2swift.processing.request_template.process_query_params import process_query_params
import subprocess
import re

from curl2swift.parsing.parse_content import ParsedContent
from curl2swift.templates.request_templates import REQUEST_TEMPLATE,\
     PATH_PARAM_SETTER, HEADER_PARAM_SETTER, BODY_PARAM_SETTER
from curl2swift.utils.logger import logging
from curl2swift.utils.pprint_color import pprint_color
from curl2swift.constants import TWO_LEVEL_INDENT_SEP


def process_request_template(
    request_name, description, content: ParsedContent, response_model
):
    logging.info('Processing request template')
    processed_template = REQUEST_TEMPLATE
    processed_template = processed_template.replace('<REQUEST_NAME>', request_name)
    processed_template = processed_template.replace('<DESC>', description)
    processed_template = processed_template.replace('<PATH>', content.path)
    processed_template = processed_template.replace('<METHOD>', '.' + content.method.lower())

    processed_template = processed_template\
        .replace('<HEADERS>', TWO_LEVEL_INDENT_SEP.join(content.header_rows))
    processed_template = processed_template\
        .replace('<BODY_PARAMS>', TWO_LEVEL_INDENT_SEP.join(content.body_param_rows))

    processed_template = process_query_params(content.query_params, processed_template)

    processed_template = processed_template\
        .replace('<PATH_PARAMS>', TWO_LEVEL_INDENT_SEP.join(content.path_param_rows))
    if content.path_param_rows:
        processed_template = processed_template\
            .replace('<PATH_PARAM_SETTER>', PATH_PARAM_SETTER)
    else:
        processed_template = re\
            .sub(r'\n\s*enum PathParameter: String \{\n\s*\}', '', processed_template)
        processed_template = re\
            .sub(r'\n\s*<PATH_PARAM_SETTER>', '', processed_template)

    if content.headers:
        processed_template = processed_template\
            .replace('<HEADER_PARAM_SETTER>', HEADER_PARAM_SETTER)
    else:
        processed_template = re.sub(r'\n\s*enum Header: String \{\n\s*\}', '', processed_template)
        processed_template = re.sub(r'\n\s*<HEADER_PARAM_SETTER>', '', processed_template)

    if content.body_param_rows:
        processed_template = processed_template\
            .replace('<BODY_PARAM_SETTER>', BODY_PARAM_SETTER)
    else:
        processed_template = re\
            .sub(r'\n\s*enum BodyParameter: String \{\n\s*\}', '', processed_template)
        processed_template = re.sub(r'\n\s*<BODY_PARAM_SETTER>', '', processed_template)

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
