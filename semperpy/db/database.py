from semperpy.core.tools import to_list
from semperpy.db.sqldriver import SQLDriver, RollBack

def progress(text):
    print(text)

class Database(object):


    def __init__(self,prefix,database,schema,write = False,overwrite = False, buffer_size = 2000):
        self.prefix_ = prefix
        self.dependencies_ = schema['dependencies']
        for k,i in list(self.dependencies_.items()):
            self.dependencies_[k] = to_list(i)
        self.target_ = self.dependencies_['target'][0]
        self.tables_ = schema['tables']
        self.overwrite_ = overwrite
        engine = database.get('engine','psql')
        self.driver_ = SQLDriver.createDriver(engine)
        self.db_ = self.driver_.connect(**database)
        self.buffer_ = []
        self.buffer_size_ = buffer_size
        self.message_count_ = 0

    def store_buffered(self,directive,progress=progress):
        self.buffer_.append(dict(directive))
        self.message_count_ += 1
        if self.message_count_ == self.buffer_size_:
            self.message_count_ = 0
            self.flush(progress)

    def store(self,directives):
        directives = to_list(directives)
        self.driver_.begin_transaction()
        attempts = 3
        done = False
        while not done and attempts > 0:
            try:
                self.write(directives,self.dependencies_,self.target_,self.target_)
                done = True
            except RollBack:
                attempts -= 1
        self.driver_.end_transaction()

    def write(self,directives,dependencies,current,target):
        if current in dependencies:
            for table in dependencies[current]:
                self.write(directives,dependencies,table,target)
        w = self.tables_['w_'+current]
        t = self.tables_['r_'+current]
        if current == target:
            d = self.tables_['d_'+current]
            self.driver_.write(self.prefix_ + '.' + target,w,d,directives,self.overwrite_)
        else:
            for directive in  directives:
                id,old = self.driver_.insert_foreign_key('id',self.prefix_ + '.' + current,w,w,directive)
                directive[current + '_id'] = id
    
    def delete(self,directives,dryrun = False):
        directives = to_list(directives)
        done = False
        actions = []
        self._delete(directives,self.dependencies_,self.target_,self.target_,actions)
        actions.reverse()
        self.driver_.begin_transaction()
        for action in actions:
            can_fail = action[0]
            try:
                self.driver_.delete_id(*action[1:],dryrun=dryrun)
            except SQLDriver.DeleteError:
                if not can_fail:
                    raise
        self.driver_.end_transaction()
        if not dryrun:
            print("done")

    def _delete(self,directives,dependencies,current,target,actions):
        if current in dependencies:
            for table in dependencies[current]:
                self._delete(directives,dependencies,table,target,actions)
        t = set(self.tables_['w_'+current])
        if current == target:
            for directive in directives:
                dir = dict()
                for key, value in list(directive.items()):
                    if key in t:
                        dir[key] = value
                actions.append([False,self.prefix_ + '.' + current,list(dir.keys()),dir])
        else:
            for directive in  directives:
                keys = set(directive.keys())
                if not t.isdisjoint(keys):
                    dir = dict(
                    )
                    for key, value in list(directive.items()):
                        if key in t:
                            dir[key] = value
                    id = self.driver_.find_all_id('id',self.prefix_ + '.' + current,list(dir.keys()),dir)
                    if id is not None:
                        for i in id:
                            dir = dict(dir)
                            dir['id'] = i
                            actions.append([True,self.prefix_ + '.' + current,list(dir.keys()),dir])
                        directive[current + '_id'] = id

    def flush(self,progress=progress):
        if len(self.buffer_) > 0:
            self.store(self.buffer_)
            msg = 'flushed %d in database "%s"' % (len(self.buffer_),self.prefix_)
            if self.overwrite_:
                msg += ' overwrite mode'
            progress(msg)
            self.buffer_ = []

    def retrieve(self,directive,keys_to_retrieve,order_by=[],negated={}):
        order = ''
        if len(order_by) > 0:
            order = 'order by (%s)' % ','.join(order_by)
        if len(directive) > 0:
            #print self.driver_
            #print '\n',self.driver_.select_statement(directive,directive.keys(),negated),'\n'
            #print '\n',self.prefix_,'\n'
            #print '\n',directive,'\n',directive.keys(),'\n'
            query = 'select %s from %s.v_view where %s %s;' % (','.join(to_list(keys_to_retrieve)),self.prefix_,self.driver_.select_statement(directive,list(directive.keys()),negated),order)
        else:
            query = 'select %s from %s.v_view;' % (','.join(to_list(keys_to_retrieve)),self.prefix_)
        cursor = self.driver_.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def query(self,query):
        cursor = self.driver_.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def close(self):
        self.driver_.close()
