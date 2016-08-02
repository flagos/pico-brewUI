from builtins import object

class MyGlobals(object):
    '''Dedicated class for global variables'''
    args = {}
    args['hardware_disconnected'] = False
    pico = None
