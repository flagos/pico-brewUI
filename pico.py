class Singleton(object):
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__new__(*args, **kwargs)
        return cls.instance

class Pico(Singleton):
    def __init__(self):
        self.recipes = []
        self.PID     = []
        self.steps   = []
        self.history = []
        self.valves  = []

        
