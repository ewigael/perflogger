import weakref


class Logger:
    """Base class centralising instance listing and thread-locking for wirting to files"""

    _instances = []

    def __init__(self):
        Logger._instances.append(weakref.ref(self))

    @classmethod
    def get_all_instances(cls):
        """Return a list of all instances of current class in creation order"""
        # Updates weakrefs
        Logger._instances[:] = [ref for ref in Logger._instances if ref() is not None]

        if cls is Logger:
            return [ref() for ref in cls._instances]
        else:
            return [ref() for ref in cls._instances if isinstance(ref(), cls)]
