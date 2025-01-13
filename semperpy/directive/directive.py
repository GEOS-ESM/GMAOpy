#---------------------------- # SemperPy Copyright GMAO 2009-2010 --
#
# Claude Gibert, June 2010, dev@synopticview.com
#-------------------------------------------------------------------
import os
import copy
from collections import defaultdict
from semperpy.core.tools import classname, dictionary, is_list, classof, specialize, is_dict, to_list
from semperpy.core.configure import Configure
from semperpy.directive.jsondirectivereader import JSonDirectiveReader
from semperpy.language.language import Language

class Directive(dictionary):

    def __init__(self,*args,**kargs):
        super(Directive,self).__init__(*args,**kargs)
        self._name = classname(self).lower()
        self.default_ = set()
        self.keywords_ = set()
        self.reader_ = None
        self.keepTrack_ = True
        self.negated_ = set()

    def checkLanguage(self,owner = None):
        self.owner = owner
        name = self.name()
        Language.resolveDirective(self,name,self.languageReader(name))
        Language.resolveCascades(self)
        for name,child in list(self.items()):
            if isinstance(child,Directive):
                child.checkLanguage(self)
            elif is_list(child):
                for v in child:
                    if isinstance(v,Directive):
                        v.checkLanguage(self)

    def __setitem__(self,key,value):
        super(Directive,self).__setitem__(key,value)
        if self.keepTrack_:
            self.clearDefault(key)

    def isDefault(self,name):
        return name in self.default_

    def setDefault(self,name):
        self.default_.add(name)

    def keepTrackOfDefaults(self,on):
        self.keepTrack_ = on

    def clearDefault(self,name):
        try:
            v = self.default_
            self.default_.discard(name)
        except:
            pass

    def defaults(self):
        return self.default_

    def keywords(self):
        return self.keywords_

    def inherit_from(self,other,exclude = []):
        done = set()
        exclude = set(exclude)
        for k,i in list(other.items()):
            if not k[0] == '_':
                if k in self.keywords_ and not k in exclude: 
                    done.add(k)
                    if isinstance(i,Directive):
                        self[k].inherit_from(other[k],exclude=exclude)
                    elif (not k in self) or (k in self and self.isDefault(k) and not other.isDefault(k)):
                        self[k] = i
        return done

    def overwrite_from(self,other,exclude = []):
        done = set()
        exclude = set(exclude)
        for k,i in list(other.items()):
            if not k[0] == '_':
                if k in self.keywords_ and not k in exclude: 
                    done.add(k)
                    if isinstance(i,Directive):
                        self[k].overwrite_from(other[k])
                    elif not k in self or (k in self and self.isDefault(k)):
                        self[k] = i
        return done

    def __str__(self,tab=1):
        l = []
        for key, value in list(self.items()):
            if key[0] != '_':
                if isinstance(value,Directive):
                    s = '\n' + value.__str__(tab+1)
                elif is_list(value):
                    doit = False
                    for v in value:
                        doit |= isinstance(v,Directive)
                    if doit:
                        s = '[\n'
                        for v in value:
                            s += v.__str__(tab+1) + '\n'
                        s += '    ' * tab + ']'
                    else:
                        s = value.__str__()
                else:
                    s = value.__str__()
                l.append('    ' * tab + str(key) + ' = ' + s)
        return '    ' * (tab-1) + self.name() + ':\n' + '\n'.join(l)

    def name(self):
        return self._name

    def languageReader(self,name):
        if self.reader_ == None:
            self.reader_ = JSonDirectiveReader(self.applicationName())
        return self.reader_

    def applicationName(self):
        return 'SemperPy'

    def allDirectives(self,application):
        r = JSonDirectiveReader(application)
        return r.directiveList()

    def language(self,directive_name):
        lang,d,k = Language.validate_language(directive_name,self.languageReader(directive_name),self)
        return lang

    def __copy__(self):
        # I had some trouble with the shallow copy of Directive, this is how
        # I managed to fixed it.
        new = Directive()
        new = specialize(new,classof(self))
        for k,i in list(self.items()):
            new[k] = i
        new.default_ = set(self.default_)
        new.keywords_ = set(self.keywords_)
        new._name = self._name
        new.reader_ = self.reader_
        new.keepTrack_ = self.keepTrack_
        new.negated_ = self.negated_
        return new

    def negate(self,which):
        self.negated_.add(which)

    def negated(self):
        return self.negated_

    def mergeDirective(self,a,overwrite=False):
        info = copy.copy(self)
        intel = defaultdict(set)
        for j,item in enumerate(a):
            for k,i in list(item.items()):
                if k[0] != '_':
                    if overwrite or (not k in info or info.isDefault(k)):
                        i = to_list(i)
                        try:
                            for key in i:
                                if not key in intel[k]:
                                    if not k in info or (j == 0 and overwrite):
                                        info[k] = []
                                        intel[k] = set()
                                    if not is_list(info[k]):
                                        info[k] = to_list(info[k])
                                if not key in intel[k]:
                                    info[k].append(key)
                                intel[k].add(key)
                        except TypeError:
                            pass
        for k,i in list(info.items()):
            if is_list(i) and len(i) == 1:
                info[k] = i[0]
        return info
