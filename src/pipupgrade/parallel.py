# imports - standard imports
from   contextlib      import contextmanager
import multiprocessing as mp
from   multiprocessing.pool import Pool

class NoDaemonPool(Pool):
    def __init__(self, *args, **kwargs):
        self.super = super(NoDaemonPool, self)
        self.super.__init__(*args, **kwargs)

    def Process(self, *args, **kwargs):
        process = self.super.Process(*args, **kwargs)

        class NonDaemonProcess(process.__class__):
            @property
            def daemon(self):
                return False

            @daemon.setter
            def daemon(self, val):
                pass

        process.__class__ = NonDaemonProcess

        return process

@contextmanager
def pool(class_ = Pool, *args, **kwargs):
    pool = class_(*args, **kwargs)
    yield pool
    pool.terminate()

@contextmanager
def no_daemon_pool(*args, **kwargs):
    with pool(class_ = NoDaemonPool, *args, **kwargs) as p:
        yield p

        p.close(); p.join()