from Graph import Graph

class Modified_Graph(Graph):

    def insert_vertex(self, x):
        """override."""
        for key in self._outgoing.keys():
            if key.element() == x:
                return key
        v = self.Vertex(x)
        self._outgoing[v] = {}
        return v

    def insert_edge(self, u, v, x):
        if self.get_edge(u, v) is not None:
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e

    def incident_edges(self, v, outgoing=True):
        #override
        self._validate_vertex(v)
        return self._outgoing[v].values()

    def iterate(self):
        myStr=""
        for v in self._outgoing.keys():
            myStr+=v.element()+" "
            for v2 in self._outgoing[v].keys():
                myStr+=v2.element()+" "+str(self._outgoing[v].get(v2).element())
                print(myStr)
                myStr=""

    def get_dict(self):
        return self._outgoing



