from graph import Graph
from pyrsistent import freeze, v, pvector, pmap

#I do not use unittesting framework on purpose here to show that you can do quite a lot without it

g1 = Graph()
assert(g1.hasvertex(1) is False)
g2 = g1.addvertex(1, {'a':[1, 2, 3], 'b':[4, 5]})
assert(g2.hasvertex(1) is True)
assert(g1.hasvertex(1) is False)
assert(g2.hasvertex(2) is False)

g3 = g2.addvertex(2, {'c':[6, 7, 8], 'd':[9, 3]})
g4 = g3.addvertex(3, {'e':[6, 3, 7], 'f':[9, 0]})
assert(g4.hasedge(1,2) is False)
assert(g4.hasedge(2,1) is False)
g5 = g4.addedge(2,3, {'g':[7, 3, 3], 'h':[7, 2]})
assert(g5.hasedge(1,2) is False)
assert(g5.hasedge(2,1) is False)
assert(g5.hasedge(3,2) is True)
assert(g5.hasedge(2,3) is True)
assert(g4.hasedge(3,2) is False)
assert(g4.hasedge(2,3) is False)
g51 = g5.removeedge(2, 3)
assert(g51.hasedge(3,2) is False)
assert(g51.hasedge(2,3) is False)
g52 = g5.removevertex(3)
assert(g52.hasvertex(3) is False)
assert(g52.hasedge(2,3) is False)

assert(set(g5.neighbours(1)) == set())
assert(set(g5.neighbours(2)) == set({3}))
assert(set(g5.neighbours(3)) == set({2}))

g6 = g5.addedge(3,2, "label1")
assert(set(g6.neighbours(1)) == set())
assert(set(g6.neighbours(2)) == set({3}))
assert(set(g6.neighbours(3)) == set({2}))

g7 = g6.addedge(2,1, "label2")
assert(set(g7.neighbours(1)) == set({2}))
assert(set(g7.neighbours(2)) == set({1,3}))
assert(set(g7.neighbours(3)) == set({2}))

g8 = g7.removeedge(3,2)
assert(set(g8.neighbours(1)) == set({2}))
assert(set(g8.neighbours(2)) == set({1}))
assert(set(g8.neighbours(3)) == set())

g9 = g7.removevertex(2)
assert(g9.hasvertex(1) is True)
assert(g9.hasvertex(2) is False)
assert(set(g9.neighbours(1)) == set())
assert(set(g9.neighbours(3)) == set())

g10 = g7.removevertex(1)
assert(g10.hasvertex(1) is False)
assert(g10.hasvertex(2) is True)
assert(set(g10.neighbours(2)) == set({3}))
assert(set(g10.neighbours(3)) == set({2}))

#===================================

ga = g1.addvertex(1, {"temperature":3, "time":12})
gb = ga.addvertex(2, {"temperature":9, "time":18}) # label for vertex 2
gc = gb.addvertex(3, {"temperature":7, "time":4})
gd = gc.addedge(1, 3, {"temperature":6, "time":4}) # label for edge 1-3

vect = v(gd, ga) # pvector of Graphs
assert( gd[(3, 1)] == pmap({"temperature":6, "time":4}) ) # label for edge 1-3
vect2 = vect.transform([0, (3, 1), "temperature"], lambda x: x+4)
ge = vect2[0]
assert( ge[(3, 1)] == pmap({"temperature":10, "time":4}) ) # ge has adjusted temperature
assert( gd[(3, 1)] == pmap({"temperature":6, "time":4}) ) # gd didnt mutate

assert( gd[2] == pmap({"temperature":9, "time":18}) ) # label for vertex 2
vect3 = vect.transform([0, 2], lambda x: {"yesterday_temp":x["temperature"]})
gf = vect3[0]
assert( gf[2] == pmap({"yesterday_temp":9}) ) # label for vertex 2 changed
assert( gd[2] == pmap({"temperature":9, "time":18}) ) # gd didnt mutate
print("Tests complete.")
