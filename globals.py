from builtins import object

class MyGlobals(object):
    '''Dedicated class for global variables'''
    args = {}
    args['hardware_disconnected'] = False
    args['two_tanks'] = False
    pico = None
