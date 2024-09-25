import matplotlib.pyplot as plt
import serial
import os
import time
from threading import Event
import math

#Do not edit this program

class CNC_simulator:
    current_x = 0
    current_y = 0
    MARKER_UP = True
    MIN_X = 0
    MAX_X = 200
    MIN_Y = 0
    MAX_Y = 100
    plt.figure(figsize=(10,5))
    plt.xlim((MIN_X, MAX_X))
    plt.ylim((MIN_Y,MAX_Y))

    #Move to a point (X,Y)
    def move_to_point(self, X, Y):
        
        if self.MIN_X <= X <= self.MAX_X and self.MIN_Y <= Y <= self.MAX_Y:

            if self.MARKER_UP==False:
                plt.plot([self.current_x,  X], [self.current_y,Y],'bo', linestyle="--")
            
            self.current_x = X
            self.current_y = Y
        else:
            print("Point out of bounds")

    #Move the marker down so it can draw
    def move_down(self):
        global MARKER_UP
        self.MARKER_UP = False

    #Move the marker up so it can't draw
    def move_up(self):
        global MARKER_UP
        self.MARKER_UP = True

    #Use this method to create a plot of what you've drawn
    def render_drawing(self):
        plt.show()

    #Move in a circular pattern, starting from where you are, with radius R
    #Set clockwise to be True or False to change the direction you want to move
    #def move_in_circle(self, R, clockwise):

class CNC_controller:
    BAUD_RATE = 115200
    SERIAL_PORT_PATH = "COM11" #Serial Port
    X_LOW_BOUND = 0
    X_HIGH_BOUND = 200
    Y_LOW_BOUND = 0
    Y_HIGH_BOUND = 100

    X_OFFSET = 35
    Y_OFFSET = 25

    gcode = ""

    def wait_for_movement_completion(self,ser,cleaned_line):
        Event().wait(1)

        if cleaned_line != '$X' or '$$':

            idle_counter = 0

            while True:
                ser.reset_input_buffer()
                command = str.encode('?' + '\n')
                ser.write(command)
                grbl_out = ser.readline()
                grbl_response = grbl_out.strip().decode('utf-8')

                if grbl_response != 'ok':
                    if grbl_response.find('Idle') > 0:
                        idle_counter += 1
                if idle_counter > 0:
                    break
        return

    def move_down(self):
        self.gcode += f"G0 Z-33.5" + "\n"

    def move_up(self):
        self.gcode += f"G0 Z0" + "\n"

    def move_to_point(self, X, Y):
        if self.coordinates_within_bounds(X,Y):
            self.gcode +=  f"G0 X{X+self.X_OFFSET} Y{Y+self.Y_OFFSET}" + "\n"
        else:
            print(f"Cannot move to {X}, {Y}, coordinates not within bounds")

    #Check if you are within the stage
    def coordinates_within_bounds(self,X,Y):
        within_bounds = False
        if (X >= self.X_LOW_BOUND) and (X<=self.X_HIGH_BOUND) and (Y>=self.Y_LOW_BOUND) and (Y<=self.Y_HIGH_BOUND):
            within_bounds = True
        return within_bounds

    def wake_up(self,ser):
        ser.write(str.encode("\r\n\r\n"))
        time.sleep(1)  # Wait for cnc to initialize
        ser.flushInput()  # Flush startup text in serial input
        print("CNC machine is awake")
        
    def render_drawing(self, buffer=20):
        with serial.Serial(self.SERIAL_PORT_PATH, self.BAUD_RATE) as ser:
            self.wake_up(ser)
            out_strings = []
            commands = self.gcode.split('\n')
            for i in range (0, math.ceil(len(commands)/buffer)):
                try:
                    buffered_commands = commands[i*buffer:(i+1)*buffer]
                except:
                    buffered_commands = commands[i*buffer:]
                buffered_gcode = ""
                for j in range (0, len(buffered_commands)):
                    buffered_gcode += buffered_commands[j] 
                    buffered_gcode += "\n"
                command = str.encode(buffered_gcode)
                ser.write(command)
                self.wait_for_movement_completion(ser, buffered_gcode)
                grbl_out = ser.readline()  # Wait for response
                out_string =grbl_out.strip().decode('utf-8')
                out_strings.append(out_string)
            return out_strings
        
        gcode = ""
