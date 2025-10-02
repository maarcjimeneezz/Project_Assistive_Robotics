import os
import time
import socket
import tkinter as tk
from tkinter import messagebox
from math import radians, degrees, pi
import numpy as np
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
tool = RDK.Item('Hand')

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
robot.setSpeed(20)


# ----------------------------
# Robot Constants
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6
timel = 6

# URScript TCP
set_tcp = "set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"


# ----------------------------
# Utils for URScript
def joints_to_movej(target, accel=accel_mss, speed=speed_ms, time=timej, blend=blend_r):
    j1, j2, j3, j4, j5, j6 = np.radians(target.Joints()).tolist()[0]
    return f"movej([{j1},{j2},{j3},{j4},{j5},{j6}],{accel},{speed},{time},{blend})"

def pose_to_movel(target, accel=accel_mss, speed=speed_ms, time=timel, blend=blend_r):
    X, Y, Z, Roll, Pitch, Yaw = Pose_2_TxyzRxyz(target.Pose())
    return f"movel(p[{X},{Y},{Z},{Roll},{Pitch},{Yaw}], a={accel}, v={speed}, t={time}, r={blend})"


# ----------------------------
# Connection check
def check_robot_port(ip, port):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    
# Send URScript command
def send_ur_script(command):
    robot_socket.send((command + "\n").encode())


# ----------------------------
# Movements
def move_to_init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")
    if robot_is_connected:
        send_ur_script(set_tcp)
        time.sleep(1)
        send_ur_script(joints_to_movej(Init_target))
        time.sleep(timel)

def hello():
    print("Hello!")
    robot.MoveL(Hello_start_target, True)
    for i in range(2):
        robot.MoveL(Hello_left_target, True)
        robot.MoveL(Hello_right_target, True)
    print("Hello FINISHED")
    if robot_is_connected:
        send_ur_script(set_tcp)
        time.sleep(1)
        send_ur_script(pose_to_movel(Hello_start_target))
        time.sleep(timel)
        for i in range(2):
            send_ur_script(pose_to_movel(Hello_left_target))
            time.sleep(timel)
            send_ur_script(pose_to_movel(Hello_right_target))
            time.sleep(timel)
        time.sleep(1)

def bye():
    print("Bye!")
    robot.setSpeed(300)
    robot.MoveL(Bye_start_target, True)
    for i in range(2):
        robot.MoveL(Bye_left_target, True)
        robot.MoveL(Bye_right_target, True)
    robot.setSpeed(20)
    print("Bye FINISHED")
    if robot_is_connected:
        send_ur_script(set_tcp)
        time.sleep(1)
        send_ur_script(pose_to_movel(Bye_start_target))
        time.sleep(timel)
        for i in range(2):
            send_ur_script(pose_to_movel(Bye_left_target))
            time.sleep(timel)
            send_ur_script(pose_to_movel(Bye_right_target))
            time.sleep(timel)
        time.sleep(1)

def come_here():
    print("Come here!")
    robot.setSpeed(300)
    for i in range(2):
        robot.MoveL(Come_start_target, True)
        robot.MoveL(Come_up_target, True)
        robot.MoveL(Come_start_target, True)
    robot.setSpeed(20)
    print("Come here FINISHED")
    if robot_is_connected:
        send_ur_script(set_tcp)
        for i in range(2):
            send_ur_script(pose_to_movel(Come_start_target))
            time.sleep(timel)
            send_ur_script(pose_to_movel(Come_up_target))
            time.sleep(timel)
            send_ur_script(pose_to_movel(Come_start_target))
            time.sleep(timel)
        time.sleep(1)


# ----------------------------
# Main function
def main():
    global robot_is_connected
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)

    move_to_init()
    hello()
    come_here()
    move_to_init()
    bye()
    move_to_init()

    if robot_is_connected:
        robot_socket.close()

    print("Program completed.")


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
        
if __name__ == "__main__":
    main()
    #confirm_close()