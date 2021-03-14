import re
from curl2swift.templates import *
from curl2swift.pprint_color import pprint_color
import subprocess


def process_test_template(header_rows, body_param_rows, content):
    header_setters = []
    for index, header in enumerate(content.headers):
        value = content.headers[header]
        enum_case = re.findall('case (.*) =', header_rows[index])[0]
        header_setters.append('.setHeader(.' + enum_case + ', "' + value + '")')
    body_param_setters = []
    for index, param in enumerate(content.param_names):
        value = param[1]
        enum_case = re.findall('case (.*) =', body_param_rows[index])[0]
        body_param_setters.append('.setBodyParameter(.' + enum_case + ', "' + value + '")')

    processed_template = TEST_TEMPLATE
    if content.headers:
        processed_template = processed_template.replace('<HEADER_SETTERS>', '\n            '.join(header_setters))
    else:
        processed_template = re.sub('.+HEADER_SETTERS>\n', '', processed_template)

    processed_template = processed_template.replace('<URL>', content.url)
    processed_template = processed_template.replace('<PATH>', content.path)

    processed_template = processed_template.replace('<REQUEST_NAME>', content.request_name)

    if content.param_names:
        processed_template = processed_template\
            .replace('<BODY_PARAM_SETTERS>', '\n            '.join(body_param_setters))
    else:
        processed_template = re.sub('.+<BODY_PARAM_SETTERS>\n', '', processed_template)

    print('\n' + '- ' * 8)
    print('GENERATED TEST:')
    print('' + '- ' * 8 + '\n')
    pprint_color(processed_template)
    print('\n' + '- ' * 12)
    print('END OF GENERATED OUTPUT')
    print('' + '- ' * 12 + '\n')

    should_copy = input('Copy to clipboard? [y/n]\n')

    if should_copy == 'y':
        subprocess.run("pbcopy", universal_newlines=True, input=processed_template)
