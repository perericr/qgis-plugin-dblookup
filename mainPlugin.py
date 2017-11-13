from __future__ import unicode_literals

"""
QGIS SQL function for looking up data in another table

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.  
"""

from qgis.utils import iface,qgsfunction
from qgis.core import QgsExpression
from qgis.utils import iface,qgsfunction
from util import memoized

class DBLookupPlugin(object):
    def __init__(self,iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        QgsExpression.registerFunction(dblookup)

    def unload(self):
        pass

def _getLayerSet():
    try:    #qgis 2
        return {layer.name():layer for layer in iface.legendInterface().layers()}
    except: #qgis 3
        return {layer.name():layer for layer in qgis.core.QgsProject.instance().mapLayers().values()}

@qgsfunction(4,"Reference")
def dblookup(values,feature,parent):
    """
        Retrieve data in field from table, from the first row where key=value.
        <h4>Syntax</h4>
        <p>dbvalue(<i>field,table,key,value</i>)</p>
        <h4>Arguments</h4>
        <p><i>table</i> &rarr; the name of a currently loaded layer, for example 'myLayer'.<br>
        <i>field</i> &rarr; a field of targetLayer whom value is needed, for example 'myTargetField'.<br></p>
        <i>key</i> &rarr; a field of targetLayer used to search between features, for example 'myKeyField'. <br></p>
        <i>value</i> &rarr; value used for comparisons with field "key". Note thet the value need to be of the same type of as field "key"<br></p>
        <h4>Note</h4>
        <p>Data is cached for up to 10 seconds for increased performance.</p>
    """
    (table,row,key,value)=values
    try:
        return dblookup_inner(table,field,key,value)
    except AttributeError,e:
        parent.setEvalErrorString(e)
        return

@memoized(10)
def dblookup_inner(targetLayerName,targetFieldName,keyFieldName,value):
    """
    return: value targetFieldName from targetlayerName where keyFieldName=value
    """
    layerSet = _getLayerSet()
    if not (targetLayerName in layerSet.keys()):
        raise AttributeError("invalid table name")

    for feat in layer_by_name(targetLayerName).getFeatures():
        if feat.attribute(keyFieldName) == value:
            try:
                return feat.attribute(targetFieldName)
            except:
                raise AttributeError("invalid field name")

@memoized(10)                    
def layer_name(name):
    """
    return   : features on layer with name
    exception: attribute error if no table with name found
    """

    for layer in iface.legendInterface().layers():
        if layer.name() == targetLayerName:
            return layer
    else:
        raise AttributeError("invalid table name")
