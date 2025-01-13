import types
import inspect
import os
import re
import copy
from collections import defaultdict

#----------------------------------------------------------------------------
# SemperPy Copyright SynopticView 2009-2010
#
# Claude Gibert, December 2009, dev@synopticview.com
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# general python utilities
#----------------------------------------------------------------------------
def specialise(self,newclass):
    self.__class__ = newclass
    return self
specialize = specialise

def classname(self):
    return self.__class__.__name__

def classof(self):
    return self.__class__

#----------------------------------------------------------------------------
# general utilities
#----------------------------------------------------------------------------
def is_string(what):
    return type(what) == str

def to_list(v):
    if type(v) != list and type(v) != tuple:
        v = [v]
    return v

def no_list(v):
    if type(v) == list or type(v) == tuple:
        if len(v) == 1:
            return v[0]
        else:
            raise ValueError("Multiple element list cannot be reduced: %s" % repr(v))
    return v

def is_list(item):
    return type(item) == list

def is_tuple(item):
    return type(item) == tuple

def is_tuple_or_list(item):
    return type(item) == list or type(item) == tuple

def is_dict(item):
    return type(item) == dict

def to_lower(what):
    """
        Transforms strings to lower case in an arbitrary structure.
        Will traverse lists and dictionaries (not keys) to modify strings
    """
    if is_string(what):
        return what.lower()
    elif is_tuple_or_list(what):
        for i in range(len(what)):
            what[i] = to_lower(what[i])
        return what
    elif is_dict(what):
        for k,i in list(what.items()):
            what[k] = to_lower(i)
        return what
    else:
        return what

def apply_type_deep(thisType,what):
    if is_tuple_or_list(what):
        for i in range(len(what)):
            what[i] = apply_type_deep(thisType,what[i])
        return what
    elif is_dict(what):
        for k,i in list(what.items()):
            what[k] = apply_type_deep(thisType,i)
        return what
    else:
        return thisType(what)

def apply_type(thisType,what):
    if is_tuple_or_list(what):
        for i in range(len(what)):
            what[i] = apply_type(thisType,what[i])
        return what
    elif is_dict(what):
        for k,i in list(what.items()):
            what[k] = thisType(i)
            return what
    else:
        return thisType(what)

def resolve_environment_variables(what):
    if is_tuple_or_list(what):
        for i in range(len(what)):
            what[i] = resolve_environment_variables(what[i])
    elif is_dict(what):
        for k,i in list(what.items()):
            what[k] = resolve_environment_variables(i)
    elif is_string(what):
        variables = re.findall('\$\{.*?\}',what)
        for var in variables:
            var = re.sub('\W','',var)
            if var in os.environ:
                what = re.sub('\$\{'+var+'\}',os.environ[var],what)
            else:
                raise NameError("Environment variable '%s' was not found" % var)
    return what

def find_variables(template):
    # match text surrounded by < > which are not backslashed
    return [ re.sub('\W','',x) for x in re.findall('(?<!\\\\)<+.*?(?<!\\\\)>+',template) ]

def substitute_variable_list(variables,template,what):
    for v in variables:
        if v in what:
            if type(what[v]) != bytes:
                what[v] = str(what[v])
            template = re.sub('<' + v + '>',what[v],template)
    template = re.sub('\\\\<','<',re.sub('\\\\>','>',template))
    return template

def substitute_variables(template,what):
    variables = find_variables(template)
    return substitute_variable_list(variables,template,what)

def substitute_unix_dates(template,*args):
    for i in range(0,len(args)-1,2):
        name = args[i]
        thedate = args[i+1]
        dates = re.findall(name + '\(.*?\)',template)
        for date in dates:
            format = re.sub('@','%',date[len(name) + 1:-1])
            date = re.sub('\)','\)',re.sub('\(','\(',date))
            template = re.sub(date,thedate.format(format),template)
    return template

def substitute_unix_calculated_dates(template,date,keyword = 'date'):
    all = re.findall('(%s.*?)\((.*?)\)' % keyword,template)
    for value in all:
        datevar = value[0]
        formatvar = value[1]
        format = re.sub('@','%',formatvar)
        thedate = eval(datevar,None,{keyword:date})
        datevar = re.sub('\+','\+',datevar)
        datevar = re.sub('\-','\-',datevar)
        template = re.sub('%s\(%s\)' % (datevar,formatvar),thedate.format(format),template)
    return template

#----------------------------------------------------------------------------
# a simple dictionary which can display nested dictonaries neatly.
#----------------------------------------------------------------------------
class dictionary(dict):

    def __str__(self):
        result = []
        self.display(self,0,result)
        return '\n'.join(result)

    def display(self,d,lev=0,result=[]):
        s = ""
        if not isinstance(d,dictionary):
            if type(d) == list:
                for v in d:
                    self.display(v,lev+1,result)
            else:
                result.append(s.ljust(lev*4) + d.__str__())
        else:
            for k in list(d.keys()):
                result.append(s.ljust(lev*4) + str(k) + ":")
                self.display(d[k],lev+1,result)

#----------------------------------------------------------------------------
# a simple dictionary which ignores case for the keys
#----------------------------------------------------------------------------
class nocasedict(dictionary):

    def __getitem__(self,indx):
        indx = indx.lower()
        return super(nocasedict,self).__getitem__(indx)

    def __setitem__(self,key,value):
        if is_string(key):
            key = key.lower()
        return super(nocasedict,self).__setitem__(key,value)

#----------------------------------------------------------------------------
# merging dictionaries
#----------------------------------------------------------------------------
def mergedicts_overwrite(a,b):
    return dict(a,**b)

def mergedicts_keep(a,b):
    d = mergedicts_overwrite(a,b)
    for k,i in list(a.items()):
        d[k] = i
    return d

#----------------------------------------------------------------------------
# Generating errors
#----------------------------------------------------------------------------
class ErrorCreator(object):
    def __init__(self,exception,title = ''):
        self.exception = exception
        self.msg = []
        self.title = title

    def __call__(self,msg):
        self.msg.append(msg)

    def check(self):
        if len(self.msg) > 0:
            raise self.exception('\n' + self.title + '\n' + '\n'.join(self.msg))

#----------------------------------------------------------------------------
# Recursive distribution
#----------------------------------------------------------------------------
def __distribute(values,result,current = []):
    if len(values) > 0:
        for v in to_list(values[0]):
            __distribute(values[1:],result,current + [v])
    else:
        result.append(current)

def distribute(values):
    result = []
    __distribute(values,result)
    return result

#----------------------------------------------------------------------------
# Recursive distribution in a dictionay with a list of keys to distribute
#----------------------------------------------------------------------------
def _nestedLoops(directive,keywords,action = None,result = [], current = {}, **kargs):
    if len(keywords) > 0:
        key = keywords[0]
        if key in directive:
            directive[key] = to_list(directive[key])
            for value in directive[key]:
                current[key] = value
                _nestedLoops(directive,keywords[1:],action,result,current,**kargs)
        else:
            _nestedLoops(directive,keywords[1:],action,result,current,**kargs)
    else:
        for k,i in list(directive.items()):
            if k not in current:
                current[k] = i
        current = copy.copy(current)
        result.append(current)
        if action is not None:
            action(directive,current,**kargs)
    return result

def nestedLoops(directive,keywords,action = None,**kargs):
    # if a keyword is in the list twice, it has an effect: the same combination
    # will be generated twice. So we make sure they are unique
    k = set(keywords)
    if len(k) != len(keywords):
        raise ValueError('In function nestedLoops, the list of keywords provided contains duplicates, this could have side-effects.')
    new = copy.copy(directive)
    k = list(new.keys())
    for kk in k:
        del(new[kk])
    return _nestedLoops(directive,keywords,action,[],new,**kargs)

def dirwalk(dir,follow_symlinks = True):
    for f in os.listdir(dir):
        fullpath = os.path.join(dir,f)
        usesym = follow_symlinks and os.path.islink(fullpath)
        ispath = os.path.isdir(fullpath)
        if (usesym and ispath) or ispath:
            for x in dirwalk(fullpath):  # recurse into subdir
                yield x
    yield dir

def dirlist(dir,follow_symlinks = True):
    all = []
    for p in dirwalk(dir,follow_symlinks = follow_symlinks):
        all.append(p)
    return all

class sortedMappingIterator(object):

    def __init__(self,what):
        self.what_ = what
        self.keys_ = sorted(what.keys())

    def __iter__(self):
        self.index_ = 0
        return self

    def __next__(self):
        if self.index_ < len(self.what_):
            k = self.keys_[self.index_]
            v = self.what_[k]
            self.index_ += 1
            return k,v
        else:
            raise StopIteration

    def keys(self):
        return self.keys_

    def values(self):
        return [ self.what_[x] for x in self.keys_ ]

class sortedSequenceIteraror(object):

    def __init__(self,what):
        self.what_ = what
        self.keys_ = sorted(what.keys())

    def __iter__(self):
        self.index_ = 0
        return self

    def __next__(self):
        if self.index_ < len(self.what_):
            k = self.keys_[self.index_]
            self.index_ += 1
            return k
        else:
            raise StopIteration

    def keys(self):
        return self.keys_

def tiles2slices(tiles,shape):
    cols = shape[0]
    rows = shape[1]
    if len(tiles) != cols * rows:
        raise ValueError('The tile array is not the right length (%d) for the dimensions passed (%d,%d)' % (len(tiles),cols,rows))
    known = defaultdict(dict)
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            if tiles[index] != 0:
                if not 'min' in known[tiles[index]]:
                    known[tiles[index]]['min'] = (col,row)
                if 'max' in known[tiles[index]]:
                    col1,row1 = known[tiles[index]]['max']
                    if row >= row1 and col >= col1:
                        known[tiles[index]]['max'] = (col,row)
                else:
                    known[tiles[index]]['max'] = (col,row)
    keys = list(known.keys())
    keys.sort()
    result = []
    for key in keys:
        result.append((slice(known[key]['min'][1],known[key]['max'][1]+1),slice(known[key]['min'][0],known[key]['max'][0]+1)))
    return result
