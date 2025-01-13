from read_class import grid

g = grid()
lons = g.x
for i in range(len(lons)-1):
    print(lons[i],lons[i+1]-lons[i])
print(list(lons))
print(lons[169])
print(lons[170])
