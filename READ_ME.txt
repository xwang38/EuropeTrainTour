
1. To run my program, you can type "python Driver.py"

2. Then, program will respectively prompt for user input of origin and destination. 
If you type the name of the city wrong, the program will raise value error and tell you that it isn't in my graph.

3. The program read data from location.txt, which contains longitude and latitude of a city (get from geopy)

4. If there is no path between origin and destination, the program will raise value error and tell you that destination cannot be reached.

5. If there is a path, the map will be poped out.

6. map.gv will draw the entire graph in green and highlight the path from origin to destination in yellow.

requirement:
python3 site-packages include matplotlib, mpl_toolkits.basemap, pillow, numpy