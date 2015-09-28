from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
#from geopy.geocoders import Nominatim
from Graph import Graph

class drawMap:
    def __init__(self):
        self.colorList=[]
        self.location={}
        self.readin()
        #self.geolocator = Nominatim()
        """
        self.map = Basemap(llcrnrlon=30,llcrnrlat=30,urcrnrlon=60,urcrnrlat=60.,resolution='i', projection='cass', lat_0 = 45, lon_0 = 45.)
        self.map.etopo(scale=0.3)
        self.map.drawcoastlines()
        self.map.drawcountries()
        """
        self._map = Basemap(projection='cyl',llcrnrlon=-15,llcrnrlat=35,urcrnrlon=38,urcrnrlat=70)
        self._map.drawmapboundary(fill_color=(0,0.698039,1,0.5))
        self._map.drawcountries(color=(1,0.4,0.698039,0.8))
        self._map.drawcoastlines(color=(0.8,0.898039,1,0.5 ))
        self._map.fillcontinents(color=(0.4, 0.8,0,0.5),lake_color=(0,0.501961,1))

        for key in self.location.keys():
            x,y=self._map(self.location[key][1],self.location[key][0])
            plt.text(x, y, key,fontsize=5, ha='left',va='bottom',color=(0.878431,0.878431,0.878431,0.7))
            #plt.text(x, y, key,fontsize=5, ha='left',va='bottom',color=(0,0,0,0.7))

    def highlight(self,mylist,mylistE):
        for i in range(len(mylist)-1):
            prev=mylist[i]
            after=mylist[i+1]
            self.colorList.append((prev,after))

        for myTuple in self.colorList:
            #This loop draw all highlighted path
            other_v1,other_v2=myTuple
            locationV1=self.get_location(other_v1)
            locationV2=self.get_location(other_v2)
            self._map.drawgreatcircle(locationV1[1],locationV1[0],locationV2[1],locationV2[0],linewidth=1.4,color=(1,1,0,0.9))

    def draw_transport(self):
        myFile=open("eurail.txt",'r')
        #This loop draw all path
        for line in myFile:
            if line !='\n':
                line=line.split(",")
                vertex1=Graph.Vertex(line[0])
                vertex2=Graph.Vertex(line[1])
                if self.drawn(vertex1,vertex2)==False:
                    locationV1=self.get_location(vertex1)
                    locationV2=self.get_location(vertex2)

                    self._map.drawgreatcircle(locationV1[1],locationV1[0],locationV2[1],locationV2[0],linewidth=1,color="#3CB371")
        plt.show()

    def get_location(self, v):
        #This function returns a tuple of latitude and longitude
        return self.location[v.element()]

    def drawn(self,v1,v2):
        for myTuple in self.colorList:
            existed1=myTuple[0].element()
            existed2=myTuple[1].element()
            if (v1.element() == existed1 and v2.element()==existed2) \
                    or (v1.element()==existed2 and v2.element()==existed1):
                return True
        return False

    # Below two function get latitude and longitude and store in location.txt
    #for every line in location.txt, we have "name latitude lontitude"
    def add_Location(self,v):
        myFile=open("location.txt",'a')
        if v.element() not in self.location.keys():
            print(str(v.element()))
            location = self.geolocator.geocode(str(v.element()))
            self.location[v.element()]=(location.latitude, location.longitude)
            myStr=str(v.element())+" "+str(self.location[v.element()][0])+" "+str(self.location[v.element()][1])+'\n'
            myFile.write(myStr)

    def readin(self):
    # in self.location dictionary, key is city name, value is (latitude longtitude)
        myFile=open("location.txt",'r')
        for line in myFile:
            if line !='\n':
                line=line.split(" ")
                if str(line[0]) not in self.location.keys():
                    self.location[str(line[0])]=(float(line[1]),float(line[2]))
