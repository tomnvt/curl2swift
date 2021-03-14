def prepare_enum_cases(names, case):
    result = []
    for name in names:
        if not name[0]:
            continue
        if case == 'param':
            if '_' in name[0]:
                split = name[0].split('_')
                split[0] = split[0].lower()
                split[1:] = [word[0].upper() + word[1:] for word in split[1:]]
                processed_name = ''.join(split)
                result.append('case ' + processed_name + ' = ' + '"' + name[0] + '"')
            else:
                the_name = name[0]
                processed_name = the_name[0].lower() + the_name[1:]
                result.append('case ' + processed_name + ' = ' + '"' + the_name + '"')
        elif case == 'header':
            split = name.split('-')
            split[0] = split[0].lower()
            split[1:] = [word[0].upper() + word[1:] for word in split[1:]]
            processed_name = ''.join(split)
            result.append('case ' + processed_name + ' = ' + '"' + name + '"')
    return result
