import os
import time
import tkinter as tk
from tkinter import messagebox
from robodk.robolink import *
from robodk.robomath import *

# ----------------------------
# Load RoboDK project
relative_path = "src/roboDK/Custom_Social_Task.rdk"
absolute_path = os.path.abspath(relative_path)
RDK = Robolink()
RDK.AddFile(absolute_path)


# ----------------------------
# Retrieve items from the RoboDK station
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item("Hand")

Init_target = RDK.Item("Init")
Hello_start_target = RDK.Item("Hello start")
Hello_left_target = RDK.Item("Hello left")
Hello_right_target = RDK.Item("Hello right")
Bye_start_target = RDK.Item("Bye start")
Bye_left_target = RDK.Item("Bye left")
Bye_right_target = RDK.Item("Bye right")
Come_start_target = RDK.Item("Come start")
Come_up_target = RDK.Item("Come up")


# ----------------------------
# Robot setup
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(50)


# ----------------------------
# Connection (real robot or simulate)
def robot_online(online):
    if online:
        robot.setConnectionParams('192.168.1.5', 30000, '/', 'anonymous', '')
        time.sleep(5)
        success = robot.ConnectSafe('192.168.1.5')
        time.sleep(5)
        status, status_msg = robot.ConnectedState()
        if status != ROBOTCOM_READY:
            raise Exception("Failed to connect: " + status_msg)
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        print("Connection to UR5e Successful!")
    else:
        RDK.setRunMode(RUNMODE_SIMULATE)
        print("Simulation mode activated.")


# ----------------------------
# Robot movements
def move_to_init():
    print("Moving to Init")
    robot.MoveL(Init_target, True)
    print("nit_target REACHED")

def hello():
    print("Hello!")
    robot.MoveL(Hello_start_target, True)
    for i in range(2):
        robot.MoveL(Hello_left_target, True)
        robot.MoveL(Hello_right_target, True)
    print("Hello FINISHED")

def bye():
    print("Bye!")
    robot.setSpeed(300)
    robot.MoveL(Bye_start_target, True)
    for i in range(2):
        robot.MoveL(Bye_left_target, True)
        robot.MoveL(Bye_right_target, True)
    robot.setSpeed(50)
    print("Bye FINISHED")

def come_here():
    print("Come here!")
    robot.setSpeed(300)
    for i in range(2):
        robot.MoveL(Come_start_target, True)
        robot.MoveL(Come_up_target, True)
        robot.MoveL(Come_start_target, True)
    robot.setSpeed(50)
    print("Come here FINISHED")


# ----------------------------
# Confirmation dialog to close RoboDK
def confirm_close():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askquestion(
        "Close RoboDK",
        "Do you want to save changes before closing RoboDK?",
        icon='question'
    )
    if response == 'yes':
        RDK.Save()
        RDK.CloseRoboDK()
        print("RoboDK saved and closed.")
    else:
        RDK.CloseRoboDK()
        print("RoboDK closed without saving.")


# ----------------------------
# Main sequence
def main():
    robot_online(False)   # True = real robot, False = simulation
    move_to_init()
    hello()
    come_here()
    move_to_init()
    bye()
    move_to_init()
    print("🎯 Program completed.")


# ----------------------------
if __name__ == "__main__":
    main()
    #confirm_close()