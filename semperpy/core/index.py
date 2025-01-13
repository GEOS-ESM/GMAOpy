#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, May 2010, dev@synopticview.com
#-------------------------------------------------------------------
from semperpy.core.tools import to_list, is_list

class Dict(dict):
    pass

class Index(Dict):

    def __init__(self,*args,**kargs):
        self.keywords_ = args
        self.unique_keys_ = kargs.get('unique_keys',False)
        self.sort_ = kargs.get('sort',False)
        self.sorting_ = {}
        for keyword in self.keywords_:
            if keyword in kargs:
                self.sorting_[keyword] = kargs[keyword]
                self.sort_ = True

    def keywords(self):
        return self.keywords_

    def insert(self,__value__,**kargs):
        self._insert(self,self.keywords_,__value__,**kargs)

    def _insert(self,entry,keywords,__value__,**kargs):
        if len(keywords) == 0:
            entry.append(__value__)
        else:
            key = keywords[0]
            entry._key = key
            if key in kargs:
                if not kargs[key] in entry:
                    if len(keywords) > 1:
                        entry[kargs[key]] = Dict()
                    else:
                        entry[kargs[key]] = []
                elif len(keywords) == 1 and self.unique_keys_:
                    raise IndexError('There is already a value stored in %s' % (repr(kargs)))
                self._insert(entry[kargs[key]],keywords[1:],__value__,**kargs)

    def access(self,_nolist=False,**kargs):
        result = self._access(self,self.keywords_,**kargs)
        if _nolist and len(result) == 1:
            result = result[0]
        return result

    def sorted_items(self,entry):
        keys = entry.keys()
        if self.sort_ and not getattr(entry,'_sorted',None):
            l = keys
            keyword = entry._key
            if keyword in self.sorting_:
                l = self.sorting_[keyword](l)
            else:
                l.sort()
            setattr(entry,'_sorted',l)
            keys = l
        for k in keys:
            yield k,entry[k]

    def _access(self,entry,keywords,**kargs):
        found = []
        if len(keywords) >= 1:
            key = keywords[0]
            if key in kargs:
                values = to_list(kargs[key])
                for value in values:
                    if value in entry:
                        found += self._access(entry[value],keywords[1:],**kargs)
            else:
                keys = entry.keys()
                if self.sort_ and not getattr(entry,'_sorted',None):
                    l = keys
                    if self._key in self.sorting_:
                        l = self.sorting_[self._key](l)
                    else:
                        l.sort()
                    setattr(entry,'_sorted',l)
                    keys = l
                for key,values in self.sorted_items(entry):
                    found += self._access(values,keywords[1:],**kargs)
        else:
            found = entry
        return found

    def constrained_access(self,_nolist=True,_expect=1,**kargs):
        result = self.access(_nolist=False,**kargs)
        if len(result) != _expect and _expect >= 0:
            raise IndexError('Constrained access failed, expected %d value(s), found %d for: %s' % (_expect,len(result),kargs.__str__()))

        if _nolist and len(result) == 1:
            result = result[0]
        return result

    def index_values(self,entry=None):
        if entry == None:
            entry = self
        if is_list(entry):
            for v in entry:
                yield v
        else:
            for k,i in entry.items():
                for v in self.index_values(i):
                    yield v

    def index_items(self):
        return self._index_items(self,self.keywords_)

    def _index_items(self,entry,keywords,**kargs):
        if is_list(entry):
            for v in entry:
                yield kargs,v
        else:
            args = Dict(kargs)
            for k,i in list(entry.items()):
                args[keywords[0]] = k
                for v in self._index_items(i,keywords[1:],**args):
                    yield v

    def index_keys(self):
        return self._index_keys(self,self.keywords_)

    def _index_keys(self,entry,keywords,**kargs):
        if is_list(entry):
            for v in entry:
                yield kargs
        else:
            args = Dict(kargs)
            for k,i in entry.items():
                args[keywords[0]] = k
                for v in self._index_keys(i,keywords[1:],**args):
                    yield v

    def __str__(self):
        result = []
        self.display(self,result)
        return '\n'.join(result)
    
    def display(self,entry,result,level=0):
        if is_list(entry):
            result.append(' ' * (level * 3) + repr(entry))
        else:
            for k,i in self.sorted_items(entry):
                result.append(' ' * (level * 3) + repr(k))
                self.display(i,result,level+1)
