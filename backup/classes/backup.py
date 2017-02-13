class Backup:
    name = None
    method = None
    source = None
    destination = None
    compress = False
    encrypt = False
    full = 0
    keep = 0

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.method = kwargs['method']
        self.source = kwargs['source']
        self.destination = kwargs['destination']
        self.compress = kwargs['compress']
        self.encrypt = kwargs['encrypt']
        self.full = kwargs['full']
        self.keep = kwargs['keep']
