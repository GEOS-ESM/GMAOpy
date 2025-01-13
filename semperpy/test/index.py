from semperpy.core.index import Index

def rev(l):
    l.sort(reverse=True)
    return l

index = Index('a','b','c','d','e',sort = True,a = rev)
#index.insert(12,a='a1',b='b1',c='c1',d='d1',e='e1')
index[{'a':'a1','b':'b1','c':'c1','d':'d1','e':'e1'}] = 12
index.insert(12,a='a1',b='b1',c='c1',d='d1',e='e1')
index.insert(13,a='a1',b='b1',c='c1',d='d1',e='e1')
index.insert(24,a='a1',b='b1',c='c2',d='d1',e='e1')
index.insert(28,a='a1',b='b1',c='c2',d='d2',e='e1')
index.insert(48,a='a2',b='b1',c='c5',d='d2',e='e2')
index.insert(52,a='a2',b='b1',c='c5',d='d2',e='e2')

print(index)

print(index.access(b='b1',a='a1',e='e2'))
print(index.access(b='b1',a='a1',e='e1'))
print(index.access())
