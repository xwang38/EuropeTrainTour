from shortest_path import shortest_path
from shortest_path import AdaptableHeapPriorityQueue
from modified_graph import Modified_Graph

class Modified_dijkstra(Modified_Graph):
    """This class use Dijkstra to compute shortest path from vertex A to vertex B
    and track that path"""

    def __init__(self):
        self.track_path=[]
        self.parent={}
        self.cloud={}
        self._outgoing = {}

    def shortest_path_lengths(self, src):
        #override method; add "tracking" function
        d = {}
        pq = AdaptableHeapPriorityQueue()
        pqlocator = {}

        for v in self.vertices():
            if v == src:
                d[v] = 0
            else:
                d[v] = float('inf')
            pqlocator[v] = pq.add(d[v], v)

        while not pq.is_empty():
            key, u = pq.remove_min()
            self.cloud[u] = key
            for e in self.incident_edges(u):
                v = e.opposite(u)
                if self.in_dict(self.cloud, v)==False:
                    if self.in_dict(self.parent, v)==False:
                        self.parent[v]=u
                    wgt = e.element()
                    if d[u] + wgt < d[v]:
                        d[v] = d[u] + wgt
                        pq.update(pqlocator[v], d[v], v)
                        self.parent[v]=u


    def in_dict(self,dict, v):
        for ele in dict.keys():
            if ele.element()==v.element():
                return True
        return False

    def get_answer(self, origin_element, destination_element):
        origin, destination= None, None
        for vertex in self.vertices():
            if vertex.element()==origin_element:
                origin=vertex
            if vertex.element()==destination_element:
                destination=vertex
        if destination==None:
            raise ValueError("destination not in graph")
        if origin==None :
            raise ValueError("origin not in graph")
        del self.track_path[:]

        self.shortest_path_lengths(origin)
        total_time=self.convert_time(self.cloud[destination])
        self.myPath=self.get_path(origin, destination)
        print("The shortest travel time is by going through these intermediary stops:")
        for city in self.myPath:
            print(city.element())
        print("Which takes "+str(total_time[0])+" hours and "+str(total_time[1])+" minutes.")

    def convert_time(self,minutes):
        hour=minutes//60
        minute=minutes-hour*60
        return hour,minute

    def get_path(self, origin, destination):
        myPath=[destination]
        if self.in_dict(self.parent, destination)==False:
            raise ValueError("destination cannot be achieved")
        prev=self.parent[destination]
        while prev.element() != origin.element():
            myPath.append(prev)
            prev=self.parent[prev]
        myPath.append(origin)
        reverse=[]
        i=len(myPath)-1
        while (i>=0):
            reverse.append(myPath[i])
            i-=1
        return reverse

    def get_pathList(self):
        return self.myPath

    def get_edgeList(self):
        tupleList=[]
        for i in range(len(self.myPath)-1):
            prev=self.myPath[i]
            after=self.myPath[i+1]
            tupleList.append((prev,after))
        edges=[]
        for myTuple in tupleList:
            myStr=""
            tmpEdge=self.get_edge(myTuple[0],myTuple[1])
            time=self.convert_time(tmpEdge.element())
            myStr+=str(time[0])+":"+str(time[1])
            edges.append(myStr)
        return edges










