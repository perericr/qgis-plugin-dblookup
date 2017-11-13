from __future__ import unicode_literals

"""
QGIS SQL function for looking up data in another table

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.  
"""

def classFactory(iface):
    from mainPlugin import DBLookupPlugin
    return DBLookupPlugin(iface)
