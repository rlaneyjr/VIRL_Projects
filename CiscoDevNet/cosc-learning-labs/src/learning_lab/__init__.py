import settings as bootstrap_settings
from importlib import import_module
from inspect import getsource

def doc(script):
    return help(import_module(script, 'learning_lab'))

def main(script):
    m = import_module(script, 'learning_lab')
#     return getsource(import_module(script,'learning_lab').main)
    return getsource(m.main)

assert bootstrap_settings