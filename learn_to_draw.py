from cnc_controls import CNC_simulator #This class will control the simulator
from cnc_controls import CNC_controller #This class will control the 

#Define your methods up here
def create_line():
    print("Creating a line...")

marker = CNC_simulator() #Create an object called "marker" which is an instance of the cnc_simulator

'''
Notes for the simulator:
The bounds of the simulator are 0 <= X <= 200 and 0 <= Y <= 100 (cannot go outside this range)
methods:
            move_to_point(X,Y) --> move to point (X,Y)
            move_down() ---> move marker down (required to draw)
            move_up() ---> move marker up (required to stop drawing)
            render_drawing() ---> display what you've made on screen
'''

#draw a line from (10,10) to (10,90)
marker.move_to_point(10,10)
marker.move_down()
marker.move_to_point(10,90)
marker.move_up()

#Coding goal 1: Create a method [see above] that draws a line between (x1, y1) to (x2, y2), then try it out
create_line()

#Coding goal 2: Create a loop that draws 5 lines, each time increasing x1 and x2 by 20
for i in range (0, 5): 
    create_line()

marker.render_drawing()