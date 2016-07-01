from __future__ import print_function
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

    _ = N_

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
from pylons.i18n import _

#### END MOCK

def _force_unicode(text):
    if text is None:
        return u''

    if isinstance(text, unicode):
        return text

    try:
        text = unicode(text, 'utf-8')
    except UnicodeDecodeError:
        text = unicode(text, 'latin1')
    except TypeError:
        text = unicode(text)
    return text

class CSSError(object):
    def __init__(self, validation_error):
        self.error = validation_error

    @property
    def message(self):
        return _(self.error.message_key) % self.error.message_params

class CSSErrorSet(Exception):
    def __init__(self, errors):
        self.errors = errors
        self.__format_errors()

    def __str__(self):
        retstr = "List of validation errors:\n    "
        return retstr + '\n    '.join(self.errors)

    def __format_errors(self):
        stringed_errors = []
        for e in self.errors:
            error = []
            if hasattr(e.error, 'line'):
                error.append('[line {0}]'.format(e.error.line))
            error.append(e.message)
            if hasattr(e.error, "offending_line"):
                error.append(e.error.offending_line)
                stringed_errors.append(" ".join(error))
        self.errors = stringed_errors

import cssfilter
import os

images = {image.rsplit('.', 1)[0]: os.path.join('./images', image)
          for image in os.listdir('./images')}
          
with open(os.getenv('cssfile', 'stylesheet.css'), 'r') as f:
    parsed, errors = cssfilter.validate_css(_force_unicode(f.read()), images)
    errors = [CSSError(error) for error in errors]
    if errors:
        raise CSSErrorSet(errors)

