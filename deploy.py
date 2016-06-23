import sys
try:
    import rcssmin
except ImportError:
    raise RuntimeError("rcssmin.py not downloaded from github@reddit/reddit")

class _i18n(object):
    @staticmethod
    def N_(arg):
        return str(arg)

class _pylons(object):
    i18n = _i18n()

class _utils(object):
    @staticmethod
    def tup(item, ret_is_single=False): 
        if hasattr(item, '__iter__'): 
            return (item, False) if ret_is_single else item 
        return ((item,), True) if ret_is_single else (item,) 

class _contrib(object):
    rcssmin = rcssmin
    
class _lib(object):
    utils = _utils()
    contrib = _contrib()

class _r2(object):
    lib = _lib()
    
sys.modules['pylons'] = _pylons()
sys.modules['pylons.i18n'] = sys.modules['pylons'].i18n
sys.modules['r2'] = _r2()
sys.modules['r2.lib'] = sys.modules['r2'].lib
sys.modules['r2.lib.utils'] = sys.modules['r2.lib'].utils
sys.modules['r2.lib.contrib'] = sys.modules['r2.lib'].contrib

