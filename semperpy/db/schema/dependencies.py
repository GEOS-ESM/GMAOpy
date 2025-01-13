from semperpy.core.tools import to_list

class Dependencies(object):

    def __init__(self):
        self.dependencies_ = {}
        self.analysed_ = False

    def __call__(self,table,dependency):
        if not table in self.dependencies_:
            self.dependencies_[table] = []
        self.dependencies_[table] += to_list(dependency)

    def __str__(self):
        self.analyse()
        lines = []
        lines.append('[dependencies]')
        lines.append('target = %s' % self.target_)
        for table,dep in list(self.dependencies_.items()):
            if len(dep) > 0:
                lines.append('%s = %s' % (table,', '.join(dep)))
        return '\n'.join(lines)

    def analyse(self):
        #--------------------------------
        # The table which is not listed
        # in the lists of dependencies
        # is the target table to be
        # built. We make sure we only
        # have one target.
        #--------------------------------
        if self.analysed_:
            return
        self.analysed_ = True
        dependedupon = set()
        for dep in list(self.dependencies_.values()):
            for table in dep:
                dependedupon.add(table)
        target = None
        for table in list(self.dependencies_.keys()):
            if not table in dependedupon:
                if target is not None:
                    raise ValueError('More than one target found')
                target = table
        self.target_ = target

    def ordered(self):
        #--------------------------------
        # First establish the number of 
        # relations for each table
        #--------------------------------
        order = {
        }
        for table,dep in list(self.dependencies_.items()):
            order[table] = self._ordered(self.dependencies_,dep,0)
        #--------------------------------
        # Then sort the list of table in
        # increasing number of relations
        #--------------------------------
        all = list(order.keys())
        all.sort(lambda a,b: cmp(order[a],order[b]))
        return all

    def _ordered(self,all,dep,count):
        for d in dep:
            count = self._ordered(all,all[d],count+1)
        return count
