from modified_graph import Modified_Graph
from modified_dijkstra import Modified_dijkstra
from drawgv import drawMap
from Graph import Graph

class ReadIn:

    def __init__(self):
        #read in "eurail.txt" and store in myGraph
        self.dijkstra=Modified_dijkstra()

        self.drawMap=drawMap()

        myFile=open("eurail.txt",'r')
        for line in myFile:
            if line !='\n':
                line=line.split(",")
                vertex1=self.dijkstra.insert_vertex(line[0])
                vertex2=self.dijkstra.insert_vertex(line[1])
                self.dijkstra.insert_edge(vertex1,vertex2,self.convert_time(line[2]))
                self.dijkstra.insert_edge(vertex2,vertex1,self.convert_time(line[2]))
                #self.drawMap.add_Location(vertex1)
                #self.drawMap.add_Location(vertex2)


    def convert_time(self,time):
        timeList=time.split(":")
        return int(timeList[0])*60+int(timeList[1])


    def user_input(self):
        orig=input("Please enter an origination: ")
        dest=input("Please enter a destination:  ")
        #self.myGraph.iterate()
        self.dijkstra.get_answer(orig, dest)
        self.drawMap.highlight(self.dijkstra.get_pathList(), self.dijkstra.get_edgeList())
        self.drawMap.draw_transport()

