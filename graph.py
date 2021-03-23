from pyrsistent import pmap, pset, thaw, freeze, v

#you may want to use PClass, but we want to learn something
class Graph:
    def __init__(self):
        self._incidence = pmap() #map<int, pair<set<pair<int, T2>>, T1>>
        # where pair is a vector of lenght 2
        # where T1 is a vertex Label and T2 is an edge label
        # a label can be anything, e.g. map of vectors

    def _newgraph(self, incidence):
        a = Graph()
        a._incidence = incidence
        return a

    def hasvertex(self, v):
        return v in self._incidence

    def addvertex(self, v, label): # ads also label for vertex v
        if v in self._incidence:
            return self
        else:
            return self._newgraph(self._incidence.set(v, freeze([pset(), label])))

    def hasedge(self, v1, v2): # self._incidence[v][0] is of type set<pair<int, label>
        return True if v2 in [edge[0] for edge in self._incidence[v1][0]] else False

    def neighbours(self, v):
        for el in self._incidence[v][0]:
            yield el[0]

    def _dostuffwithedge(self, v1, v2, fun): # added 0 to deeper extend path in transform
        modifyv1 = fun(v1)
        modifyv2 = fun(v2)
        newinc = self._incidence.transform([v1, 0], modifyv2, [v2, 0], modifyv1)
        return self._newgraph(newinc)

    def addedge(self, v1, v2, label): # same as before except it inserts label for edge v1v2
        return self._dostuffwithedge(v1, v2, lambda v: (lambda x: x.add(freeze([v, label]))))

    def removeedge(self, v1, v2): # same as before except edges are of type "pair<int, label>" instead of "int"
        return self._dostuffwithedge(v1, v2, lambda v: (lambda x: freeze({edge for edge in x if edge[0] != v})))

    def removevertex(self, v):
        newinc = thaw(self._incidence) # newinc is not persistent
        for v2 in [edge[0] for edge in self._incidence[v][0]]:
            newinc[v2][0] = {edge for edge in newinc[v2][0] if edge[0] != v}
        newinc.pop(v)
        return self._newgraph(freeze(newinc))

    ###transformations###

    def __getitem__(self, label_num): # gets either vertex label or edge label
        if type(label_num) == int:
            return self._incidence[label_num][1]
        for edge in self._incidence[label_num[0]][0]:
            if edge[0] == label_num[1]:
                return edge[1]

    def evolver(self):
        return GraphEvolver(self._incidence)

class GraphEvolver(Graph): # using other class for evolver because immutable Graph shouldt have __setitem__
    def __init__(self, incidence):
        self._incidence = thaw(incidence) #incidence in this class is mutable

    def __setitem__(self, label_num, label):
        if type(label_num) == int:
            self._incidence[label_num][1] = label
            return
        self._incidence[label_num[0]][0] = {
            edge for edge in self._incidence[label_num[0]][0] if edge[0] != label_num[1]
            }
        self._incidence[label_num[0]][0].add(v(label_num[1], label))

    def persistent(self):
        return self._newgraph(freeze(self._incidence))
