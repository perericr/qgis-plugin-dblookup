from __future__ import unicode_literals

"""
QGIS SQL function for looking up data in another table:
utility functions

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.  
"""

import time

class memoized(object):
    """
    memoization with time limit (in s)
    """
    
    def __init__(self,ttl=2):
        self.cache={}
        self.ttl=ttl

    def __call__(self, func):
        def _memoized(*args):
            self.func = func
            now = time.time()
            try:
                value,last_update=self.cache[args]
                age = now - last_update
                if age > self.ttl:
                    raise AttributeError
                return value

            except(KeyError, AttributeError):
                value = self.func(*args)
                self.cache[args]=(value,now)
                return value

            except TypeError:
                return self.func(*args)
        return _memoized
