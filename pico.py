def singleton(cls):
    instance = None
    def ctor(*args, **kwargs):
        nonlocal instance
        if not instance:
            instance = cls(*args, **kwargs)
        return instance
    return ctor

@singleton
class Pico:
    def __init__(self, val):
        self.recipes = []
        self.PID     = []
        self.steps   = []
        self.history = []
        self.valves  = []


pico = Pico.ctor()
