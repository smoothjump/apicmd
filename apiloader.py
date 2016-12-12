#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys, types
import rdsapi

def _get_mod(modulePath):
    try:
        aMod = sys.modules[modulePath]
        if not isinstance(aMod, types.ModuleType):
            raise KeyError
    except KeyError:
        # The last [''] is very important!
        aMod = __import__(modulePath, globals(), locals(), [''])
        sys.modules[modulePath] = aMod
    return aMod

def _get_func(fullFuncName):
    aFunc = None
    aMod = None
    lastDot = fullFuncName.rfind(u".")
    if lastDot != -1:
        funcName = fullFuncName[lastDot + 1:]
        modPath = fullFuncName[:lastDot]
    else:
        print "Illegal class name or function name, your input should be absolute path"
        raise SystemExit
    try:
        aMod = _get_mod(modPath)
        print aMod
        aFunc = getattr(aMod, funcName)
    except ImportError:
        print "No module named %s" %modPath
        raise SystemExit
    except AttributeError:
        print "Module \"%s\" has no attribute named %s" %(modPath,funcName)
        raise SystemExit
    # Return a reference to the function/class itself,
    # not the results of the function or instance of class.
    return aFunc

def applyFuc(obj,strFunc,arrArgs):
    objFunc = getattr(obj, strFunc)
    return apply(objFunc,arrArgs)

def getObject(fullClassName, *args, **kwargs):
    clazz = _get_Class(fullClassName)
    return clazz(*args, **kwargs)
