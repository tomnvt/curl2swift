import os
import shutil
import git

def clone_repo(url, content_type):
    dir_name = url.split('/')[-1].replace('.git', '')
    clone_func = lambda: git.Git(os.getcwd()).clone(url)
    clone_print = lambda: print('Cloning ' + content_type + ' into ' + dir_name)
    if os.path.isdir(os.getcwd() + os.sep + dir_name):
        print('Directory ' + dir_name + ' already exists.')
        response = input('Would you like to delete it and clone again? [y/n]\n')
        if response == 'y':
            print('Deleting ' + dir_name + '.')
            shutil.rmtree(os.getcwd() + os.sep + dir_name)
            clone_print()
            clone_func()
    else:
        clone_print()
        clone_func()
