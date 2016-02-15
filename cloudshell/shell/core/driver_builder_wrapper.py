import json
import os
import random
from threading import Thread
import sys
import threading
import time
import traceback
import uuid

__author__ = 'eric.r'
import functools
import inspect

# @DriverFunction annotation
# Base classes to use when creating a class callable from Driver Builder
# See ../examples/example_drivers.py

def json_loads(s):
    try:
        return json.loads(s)
    except Exception as e:
        raise Exception('JSON parse exception: {0}. Input: {1}'.format(unicode(e), s))


# Based on http://blog.dscpl.com.au/2014/01/decorators-which-accept-arguments.html
# Don't delete ee!
def ee(w1):
    def d(f):
        def w2(*args2):
            return f(*args2)
        w2.qargspec=inspect.getargspec(f)
        return w2
    return d


def DriverFunction(zapped=None, tags="", alias="", description="", extraMatrixRows={}, category="", order=0):
    if zapped is None:
        return functools.partial(DriverFunction, tags=tags, alias=alias, description=description, extraMatrixRows=extraMatrixRows, category=category, order=order)

    @ee
    def w3(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)
    rv=w3(zapped)
    rv.tags=tags
    rv.alias=alias
    rv.description=description
    rv.extraMatrixRows=extraMatrixRows
    rv.category=category
    rv.order=order
    return rv


logfile = None
if 'PROGRAMDATA' not in os.environ.keys():
    os.environ['PROGRAMDATA'] = "/tmp"

logfilename = os.environ['PROGRAMDATA'].replace('\\', '/')+'/QualiSystems/python_driver_trace.log'
try:
    logfile = open(logfilename, 'a')
except:
    newfn = os.environ['PROGRAMDATA'].replace('\\', '/')+'/QualiSystems/'+str(uuid.uuid4())+'.log'
    logfile = open(newfn, 'a')


def log(s):
    if logfile is None:
        return
    for i in range(10):
        try:
            logfile.write(s.encode('utf-8') + '\n')
            return
        except:
            time.sleep(random.randint(1, 5))


def sevenbitclean(s):
    rv = ''
    for c in s:
        if ord(c) < 128:
            rv += c
        else:
            rv += '?'
    return rv


def tracefunc(frame, event, arg, level=[0]):
    if 'qualipy' in frame.f_code.co_filename:
        tabs = '  ' * level[0]
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        if event == 'call':
            call = '{1}  {0}: {3}::{2}('.format(tabs, t, frame.f_code.co_name, frame.f_code.co_filename)
            for i in range(frame.f_code.co_argcount):
                argname = frame.f_code.co_varnames[i]
                argval = frame.f_locals[argname]
                if i > 0:
                    call += ', '
                if isinstance(argval, unicode):
                    argval = argval.encode('utf-8', errors='ignore')
                else:
                    try:
                        argval = str(argval)
                    except:
                        argval = '<error getting string>'
                argval = sevenbitclean(argval)
                call += '{0}={1}'.format(argname, argval)
            call += ')'
            log(call)
            level[0] += 1
        elif event == 'return':
            argval = arg
            if isinstance(argval, unicode):
                argval = argval.encode('utf-8', errors='ignore')
            else:
                try:
                    argval = str(argval)
                except:
                    argval = '<error getting string>'
            argval = sevenbitclean(argval)
            call = '{1}{0}: {2} returned {3}'.format(tabs, t, frame.f_code.co_name, argval)
            level[0] -= 1
            log(call)
    return tracefunc


def init_trace():
    # sys.settrace(tracefunc)
    # threading.settrace(tracefunc)
    pass


class BaseDriver:
    sessionid2instance={}


class BaseResourceDriver(BaseDriver):
    def __init__(self, sessionid, matrix_json):
        init_trace()
        self.sessionid=sessionid
        BaseDriver.sessionid2instance[sessionid] = self
        # print "base resource driver constructor: "+str(BaseDriver.sessionid2instance)
        self.Init(matrix_json)

    def getSessionId(self):
        return self.sessionid

    @DriverFunction
    def Init(self, matrix_json):
        pass

    @DriverFunction
    def ResetDriver(self, matrix_json):
        pass

    @DriverFunction
    def EndSession(self, matrix_json):
        pass


class BaseServiceDriver(BaseDriver):
    def __init__(self, sessionid, matrix_json):
        init_trace()
        self.sessionid=sessionid
        BaseDriver.sessionid2instance[sessionid] = self
        self.Init(matrix_json)

    @DriverFunction
    def Init(self, matrix_json):
        pass

    @DriverFunction
    def ResetDriver(self, matrix_json):
        pass

    @DriverFunction
    def EndSession(self, matrix_json):
        pass


class BaseTopologyDriver(BaseDriver):
    def __init__(self, sessionid, matrix_json):
        init_trace()
        self.sessionid=sessionid
        BaseDriver.sessionid2instance[sessionid] = self
        self.Init(matrix_json)

    # Note: topology drivers don't have Init but we must generate it
    @DriverFunction
    def Init(self, matrix_json):
        pass

    @DriverFunction
    def Setup(self, matrix_json):
        pass

    @DriverFunction
    def Teardown(self, matrix_json):
        pass

    @DriverFunction
    def EndSession(self, matrix_json):
        pass

