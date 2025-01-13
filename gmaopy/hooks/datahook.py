import copy

class DataHook(object):

    register_ = {}

    def splitOnMainVariable(self,main_variable,data):
        new = []
        for d in data:
            for i in range(len(d[main_variable])):
                n = copy.copy(d)
                n[main_variable] = [n[main_variable][i]]
                n['value'] = [n['value'][i]]
                new.append(n)
        return new

    def cleanupData(self,data):
        for d in data:
            for k,i in list(d.items()):
                if len(i) == 1:
                    d[k] = i[0]
                else:
                    d[k] = tuple(i)
        return data

    @classmethod
    def registerHook(self,name,hook):
        DataHook.register_[name] = hook

    @classmethod
    def hookList(self):
        l = list(DataHook.register_.keys())
        l.sort()
        return l

    @classmethod
    def hook(self,name):
        return DataHook.register_[name]
