#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import math
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


ev3 = EV3Brick()
ev3.speaker.beep()

# Declare the Actuators
gripper = Motor(Port.A, Direction.CLOCKWISE) # Make sure your gripper fingers are opened manually when you first start the program
elbow = Motor(Port.B, Direction.COUNTERCLOCKWISE, gears = [8,40])
base  = Motor(Port.C, Direction.CLOCKWISE, gears = [12,36])
conveyor = Motor(Port.D)

gripper.reset_angle(0) # gripper at open position

# Declare the sensors
eTouch = TouchSensor(Port.S3)
bTouch = TouchSensor(Port.S1)
cDetect = ColorSensor(Port.S2)

# Robot Parameters (all in mm)
# Link Lengths
l0 = 35 # measured
l1 = 50
l2 = 95 
l3 = 185
l4 = 110

# Declare other variables
base_error = 11 # Adjust this value based on your base homing position
base_speed = 60 # speed for base motor
elbow_speed = 50 # speed for elbow motor
conveyor_speed = 200 # speed for conveyor motor

# Station Coordinates
station1 = [100.0, 0.0, 0.0] # x, y, z measured 
station2 = [-100.0, -0.0, 0.0] # x, y, z measured 
station5 = [0.0, -115.0, 55.0] # x, y, z measured 

# -------------------- KINEMATICS --------------------
def theta1(y, x): # theta1 takes y and x as parameters
    """Base rotation angle"""
    return math.degrees(math.atan2(y, x))

def theta2(z):
    """Elbow angle using atan2 (geometric solution)"""
    # Vertical component of elbow link
    opp = z + l4 - l0 - l1 - (l2 * math.cos(math.radians(45)))
    opp = max(-l3, min(l3, opp)) # Protect against numerical errors
    adj = math.sqrt(l3**2 - opp**2)   # Horizontal projection of elbow link
    theta = math.degrees(math.atan2(opp, adj)) - 45
    return theta

# function to open/close gripper
def gripperOpen(): # This will open the gripper
    gripper.run_target(100,0, then=Stop.HOLD, wait=True)
  
def gripperClose(): # This will close the gripper
    gripper.run_target(100,90, then=Stop.HOLD, wait=True)


# HOMING USING TOUCH SENSORS
def homeUsingTouch():
    print("Elbow Homing")
    # Move elbow until touch sensor is pressed
    elbow.run(elbow_speed)
    while not eTouch.pressed():
        pass 
    elbow.hold()    
    elbow.reset_angle(0) # reset elbow angle to 0
    elbow.run_target(20, 0, then=Stop.HOLD, wait=True) # To hold elbow at 0 position

    print("Base Homing")
    # Move base until base touch sensor is pressed
    base.run(base_speed)
    while not bTouch.pressed():
        pass
    base.hold()    
    base.reset_angle(base_error) 
    wait(500)

    base.run_target(20,-base_error, then=Stop.HOLD, wait=True)
    base.reset_angle(0) 
    wait(200)

    # ---------- GRIPPER CHECK ----------
    gripperClose()
    gripperOpen()

    # ---------- STATUS ----------
    print("Robot at Home position")
    print(
        "Current theta 1 (base):", base.angle(),
        "Current theta 2 (elbow):", elbow.angle()
    )

# MOTION FUNCTIONS
def roboHome():  # Initialize the Robot to Home position
    elbow.run_target(elbow_speed, 0, then=Stop.HOLD, wait=True)
    base.run_target(base_speed, 0, then=Stop.HOLD, wait=True)

def moveToStation(station):
    th1 = theta1(station[1], station[0])
    th2 = theta2(station[2])

    print("Moving to station")
    print("Calculated Theta1:", th1, "Calculated Theta2:", th2)

    elbow.run_target(elbow_speed, 0, then=Stop.HOLD, wait=True)
    base.run_target(base_speed, th1, then=Stop.HOLD, wait=True)
    elbow.run_target(elbow_speed, th2, then=Stop.HOLD, wait=True)

    print("Reached station")
    print("Base:", base.angle(), "Elbow:", elbow.angle())


def conveyortoStation5():
    print("Conveyor going to Station 5 position")
    conveyor.run_target(conveyor_speed, -280, then=Stop.HOLD, wait=True)
    conveyor.reset_angle(0)

def conveyortoStation4():
    print("Conveyor going to Station 4 position")
    conveyor.run_target(conveyor_speed, 100, then=Stop.HOLD, wait=True)
    conveyor.reset_angle(0) 

def conveyortoStation3():
    print("Conveyor going to Station 3 position")
    conveyor.run_target(conveyor_speed, -580, then=Stop.HOLD, wait=True)
    conveyor.reset_angle(0) 


print("Current Color Detected:", cDetect.color())

# -------------------- COLOR HANDLING --------------------
def handleBlueBall():
    print("Handling BLUE ball")
    moveToStation(station5)
    gripperClose()
    moveToStation(station1)
    gripperOpen()
    roboHome()

def handleRedBall():
    print("Handling RED ball")
    moveToStation(station5)
    gripperClose()
    moveToStation(station2)
    gripperOpen()
    roboHome()

# -------------------- MAIN PROGRAM --------------------
homeUsingTouch()

while True:
    color = cDetect.color()
    # This condition is to avoid the sensor error and to allow sufficient time for the program to start
    if(color != None):
        wait(500) 
        color = cDetect.color()
        print("Detected:", color)

    if color == Color.BLACK:
        print("Black → Station 3")
        ev3.speaker.say("color detected Black")
        conveyortoStation3()

    elif color == Color.GREEN: 
        print("Green → Station 4")
        ev3.speaker.say("color detected Green")
        conveyortoStation4()

    elif color == Color.BLUE:
        print("Blue → Station 5 → Station 1")
        ev3.speaker.say("color detected Blue")
        conveyortoStation5()
        handleBlueBall()

    elif color == Color.RED:
        print("Red → Station 5 → Station 2")
        ev3.speaker.say("color detected Red")
        conveyortoStation5()
        handleRedBall()

    else:
        print("No valid color detected")
    