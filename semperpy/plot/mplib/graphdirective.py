from semperpy.directive.directive import Directive

class GraphDirective(Directive):

    def make_kwargs(self):
        kwargs = {}
        non_keywords = set(self['_non_keywords'] + ['_non_keywords'])
        for k,i in list(self.items()):
            if not k in non_keywords:
                kwargs[k] = i
        return kwargs
