import weakref
import threading
from pathlib import Path


class Logger:
    """Base class centralising instance listing and thread-locking for wirting to files"""

    _instances = []

    _locks: dict[Path, threading.Lock] = {}
    _locks_dict_lock = threading.Lock()

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

    @classmethod
    def _get_write_lock(cls, path: Path) -> threading.Lock:
        with Logger._locks_dict_lock:
            return Logger._locks.setdefault(path.resolve(), threading.Lock())
