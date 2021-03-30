from curl2swift.utils.logger import logging
import re
from curl2swift.templates.request_templates import QUERY_PARAM_SETTER
from curl2swift.constants import TWO_LEVEL_INDENT_SEP


def process_query_params(query_params, processed_template):
    logging.info('Processing query params: ' + str(query_params))
    if query_params:
        processed_template = processed_template.replace('<QUERY_PARAM_SETTER>', QUERY_PARAM_SETTER)
        query_param_key_cases = ['case ' + key for key in list(query_params.keys())]
        processed_template = processed_template\
            .replace('<QUERY_PARAMS>', TWO_LEVEL_INDENT_SEP.join(query_param_key_cases))
        query_param_init_rows = []
        query_params_dict_entries = []
        for query_param_key in query_params:
            query_params_dict_entries.append('"' + query_param_key + '": "' + query_params[query_param_key] + '"')
        query_param_init_row = 'set(.queryParams([' + ', '.join(query_params_dict_entries) + ']))'
        print(query_param_init_row)
        processed_template = processed_template\
            .replace('<QUERY_PARAMS_INIT>', query_param_init_row)
    else:
        processed_template = re\
            .sub(r'\n\s*enum QueryParam: String \{\n.*\n\s*}\n', '', processed_template)
        processed_template = re\
            .sub(r'\n\s*<QUERY_PARAMS>', '', processed_template)
        processed_template = re\
            .sub(r'\n\s*<QUERY_PARAMS_INIT>', '', processed_template)
        processed_template = re\
            .sub(r'\n\s*<QUERY_PARAM_SETTER>', '', processed_template)

    return processed_template

