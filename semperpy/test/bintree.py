
class TreeNode(object):
    
    def __init__(self,string):
        self.string_ = string
        self.left_ = None
        self.right_ = None

    def left(self,left):
        self.left_ = left

    def right(self,right):
        self.right_ = right

    def insert(self,string):
        if string < self.string_:
            if self.left_:
                self.left_.insert(string)
            else:
                self.left_ = TreeNode(string)
        elif string > self.string_:
            if self.right_:
                self.right_.insert(string)
            else:
                self.right_ = TreeNode(string)

    def __str__(self):
        return self.str()

    def str(self,indent = 0):
        s = ' ' * indent + self.string_ + '\n'
        if self.left_:
            s += self.left_.str(indent + 3)
        if self.right_:
            s += self.right_.str(indent + 3)
        return s

    def search(self,string):
        found = False
        if self.string_ == string:
            found = True
        else:
            if self.left_:
                found = self.left_.search(string)
            if not found and self.right_:
                found = self.right_.search(string)
        return found

    def visit(self,visitor):
        stop = visitor(self.string_)
        if not stop:
            if self.left_:
                stop = self.left_.visit(visitor)
            if not stop and self.right_:
                stop = self.right_.visit(visitor)
        return stop

tree = TreeNode('if')
tree.insert('it')
tree.insert('is')
tree.insert('no')
tree.insert('one')
tree.insert('for')
tree.insert('me')
tree.insert('try')
tree.insert('not')
tree.insert('cry')
tree.insert('much')
tree.insert('see')
print(tree)
print(tree.search('for'))
print(tree.search('hello'))
print(tree.search('no'))
print(tree.search('world'))

class Search(object):

    def __init__(self,pattern):
        self.pattern = pattern            

    def __call__(self,value):
        return value == self.pattern

print()
print(tree.visit(Search('for')))
print(tree.visit(Search('hello')))
print(tree.visit(Search('no')))
print(tree.visit(Search('world')))

class Count(object):

    def __init__(self,letter):
        self.letter = letter
        self.count = 0

    def __call__(self,value):
        if value[0] == self.letter:
            self.count += 1
        return False  # we don't stop until it's all done

    def get(self):
        return self.count

count = Count('i')
tree.visit(count)
print(count.get())
