#### BEGIN MOCKING REDDIT PACKAGE
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

#### END MOCK

class CSSErrorSet(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        retstr = "List of syntax and / or validation errors:\n    "
        retstr += '\n    '.join(
            ['{0}: {1}'.format(e.__class__.__name__, str(e))
             for e in self.errors]
        )
        return retstr

import cssfilter
import os

images = {image.rsplit('.', 1)[0]: os.path.join('./images', image)
          for image in os.listdir('./images')}
          
with open(os.getenv('cssfile'), 'r') as f:
    parsed, errors = cssfilter.validate_css(f.read(), images)
    if errors:
        raise CSSErrorSet(errors)

