from curl2swift.utils.logger import logging

def prepare_enum_cases(names, enum_type):
    logging.info('Preparing enum cases for enum type ' + enum_type + ' with names ' + str(names))
    result = []

    for name in names:
        if not name[0]:
            continue
        if enum_type == 'param':
            logging.info('Processing param with name ' + str(name))
            if '_' in name[0]:
                if name[0][0] == '_':
                    name[0] = ''.join(name[0][1:])
                if name[0][-1] == '_':
                    name[0] = ''.join(name[0][:-2])

                split = name[0].split('_')
                split[0] = split[0].lower()
                split[1:] = [word[0].upper() + word[1:] for word in split[1:]]
                processed_name = ''.join(split)
                result.append('case ' + processed_name + ' = ' + '"' + name[0] + '"')
            else:
                the_name = name[0]
                processed_name = the_name[0].lower() + the_name[1:]
                result.append('case ' + processed_name + ' = ' + '"' + the_name + '"')
        elif enum_type == 'header':
            split = name.split('-')
            split[0] = split[0].lower()
            split[1:] = [word[0].upper() + word[1:] for word in split[1:]]
            processed_name = ''.join(split)
            result.append('case ' + processed_name + ' = ' + '"' + name + '"')
    
    logging.info('Created body param rows: ' + str(result))
    return result
