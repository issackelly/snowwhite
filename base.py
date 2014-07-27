
class Pattern(object):

    client = None
    redis_client = None
    camera = None

    def __init__(self, opc_client, redis_client=None, camera=None):
        super(Pattern, self).__init__()
        self.client = opc_client
        self.redis_client = redis_client
        self.camera = camera

    def run(self, **kwargs):
        raise NotImplemented
