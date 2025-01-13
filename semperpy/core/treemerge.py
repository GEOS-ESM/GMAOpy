import copy
import types
import string

class TreeKeywords(object):

    def __init__(self,fixed,combinable):
        self.fixed_ = fixed
        self.combinable_ = combinable
        self.sfixed_ = set(fixed)
        self.scombinable_ = set(combinable)

class TreeNode(object):

    def __init__(self,keywords,hooks):
        self.keywords_ = keywords
        self.hooks_ = hooks
        self.kids_ = {}
        self.key_ = None

    def insert(self,keywords,directive):
        if len(keywords) == 0:
            return
        keyword = keywords[0]
        self.key_ = keyword
        if self.key_ in self.keywords_.sfixed_:
            self.specialise(FixedNode)
        elif self.key_ in self.keywords_.scombinable_:
            self.specialise(CombinableNode)
        else:
            raise ValueError('TreeMerge: unknown keyword: ' + self.key_)
        vals = [None]
        if keyword in directive:
            if keyword in self.hooks_:
                vals = self.hash_value(self.hooks_[keyword](directive[keyword]))
            else:
                vals = self.hash_value(directive[keyword])
        for value in vals:
            if not value in self.kids_:
                node = TreeNode(self.keywords_,self.hooks_)
                self.kids_[value] = node
            else:
                node = self.kids_[value]
            node.insert(keywords[1:],directive)
        return node

    def remove(self,keywords,directive):
        if len(keywords) == 0:
            return True
        result = False
        keyword = keywords[0]
        vals = [str(None)]
        if self.key_ != keyword:
            raise ValueError('keyword "'+keyword+'" found in the wrong place')
        if keyword in directive:
            if keyword in self.hooks_:
                vals = self.hash_value(self.hooks_[keyword](directive[keyword]))
            else:
                vals = self.hash_value(directive[keyword])
        vals = set(vals)
        all = str(None) in vals
        for kid in list(self.kids_.keys()):
            if (kid in vals) or all:
                if self.kids_[kid].remove(keywords[1:],directive):
                    del(self.kids_[kid])
        return len(self.kids_) == 0

    def hash_value(self,value):
        vals = []
        if type(value) == list or type(value) == tuple:
            for v in value:
                vals.append(str(v))
        else:
            vals.append(str(value))
        return vals

    def __str__(self):
        return string.join(self.dump([],0),'\n')

    def dump(self,lines,tab):
        for key in list(self.kids_.keys()):
            lines.append(' ' * 3 + self.key_ + '=' + key.__str__())
            self.kids_[key].dump(lines,tab+1)
        return lines

    def buildRequests(self,directive = {}):
        return [directive]

    def fill_directive(self,directive):
        pass

    def signature_depth(self,branch,result):
        result.append(branch)    
        return branch

    def signature_breadth(self,*args):
        return ''


class FixedNode(TreeNode):

    def buildRequests(self,directive = {}):
        dirs = []
        for value,child in list(self.kids_.items()):
            d = directive
            if value != None:
                directive[self.key_] = set([value])
            else:
                if self.key_ in directive:
                    del(directive[self.key_])
            if child:
                dirs += child.buildRequests(directive)
                directive = copy.copy(directive)
        return dirs


class CombinableNode(TreeNode):

    def signature_depth(self,branch = [], result = []):
        b = copy.copy(branch)
        for key in list(self.kids_.keys()):
            self.kids_[key].signature_depth(b + [key.__str__()],result)
        return result

    def signature_breadth(self):
        s = []
        for key in list(self.kids_.keys()):
            s.append(key.__str__())
            s.append(self.kids_[key].signature_breadth())
        return ':'.join(s)

    def fill_directive(self,directive):
        if not self.key_ in directive:
            directive[self.key_] = set()
        for key in list(self.kids_.keys()):
            directive[self.key_].add(key)
        
    def buildRequests(self,directive = {}):
        dirs = []
        paths = dict()
        for value,child in list(self.kids_.items()):
            sign = child.signature_breadth()
            if not sign in paths:
                paths[sign] = []
            paths[sign].append({'child': child,
                             'value': value})
        if len(paths) == 0:
            directive[self.key_] = set(self.kids_.keys())
            return [directive]
        else:
            for path in list(paths.values()):
                dir = copy.copy(directive)
                dir[self.key_] = set()
                for value in path:
                    if value['value'] != None:
                        dir[self.key_].add(value['value'])
                if len(path) > 1:
                    newdirs = value['child'].buildRequests(dir)
                    for dir in newdirs:
                        value['child'].fill_directive(dir)
                    dirs += newdirs
                else:
                    dirs += value['child'].buildRequests(dir)
        return dirs


class TreeMerge(object):

    def __init__(self,fixed,combinable):
        self.hooks_ = {}
        self.keywords_ = TreeKeywords(fixed,combinable)
        self.root_ = TreeNode(self.keywords_,self.hooks_)

    def register(self,keyword,action):
        self.hooks_[keyword] = action

    def insert(self,directive):
        d = {}
        for key,item in list(directive.items()):
            d[key.lower()] = item
        self.root_.insert(self.keywords_.fixed_ + self.keywords_.combinable_,d)

    def remove(self,directive):
        d = {}
        for key,item in list(directive.items()):
            d[key.lower()] = item
        self.root_.remove(self.keywords_.fixed_ + self.keywords_.combinable_,d)

    def __str__(self):
        return self.root_.__str__()

    def buildRequests(self):
        result = self.root_.buildRequests()
        for directive in result:
            for key,value in list(directive.items()):
                value = list(value)
                if len(value) == 1:
                    directive[key] = value[0]
                elif len(value) == 0:
                    del(directive[key])
                else:
                    directive[key] = value
        return result

