import socket
import json
import datetime
import random
import shlex
import Environment as environment

import time
from MessageReceiver import MessageReceiver

# Client to connect to UE4 tcp server

TCP_IP = "localhost"
TCP_PORT = 11111

def is_number(n):
    is_number = True
    try:
        num = float(n)
        is_number = num == num
    except ValueError:
        is_number = False
    return is_number


def walk_in_circle(client):
    client.send_command("move_forward 1")
    client.send_command("turn 0.5")

def idle(client):
    client.send_command("move_forward 0")
    client.send_command("turn 0")

# Will run the last command only
def example1(client):
    client.send_command("move_forward 0.3")
    client.send_command("move_forward 0.1")


class Client:
    def __init__(self, host=TCP_IP, port=TCP_PORT):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ms = MessageReceiver(self)
        self.run()


    def run(self):
        self.socket.connect((self.host, self.port))
        self.ms.start() # Starts the run() method in ms (in a separate thread)
        print("Your input:")
        while(True):
            c = input().strip()

            if len(c) > 0:
                try:
                    self.send_command(c) #send it without checking it
                except:
                    print(" - Reconnecting...", end="\r")
                    self.connect()
                    print(" - Reconnected", end="\n")
                    self.send_command(c) #send it without checking it
            else:
                print(' - Write proper commands: <ActionType> <ActionState> <value>')


    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        self.ms = MessageReceiver(self)
        self.ms.start()


    def on_disconnect(self):
        self.socket.close()
        print(" - Disconnected")


    def on_server_disconnect(self):
        self.socket.close()
        print(" - Server disconnected")


    def on_receive_message(self, msg):
        try:
            data = json.loads(msg)
            if (data["type"] == "STATE"):
                environment.on_state_received(data)
                print("states:", environment.states)
            elif (data["type"] == "REWARD"):
                environment.on_reward_received(data)
                print("rewards:", environment.rewards)
            elif (data["type"] == "ACK"):
                if (data["Status"] != "OK"):
                    print(data)
        except json.decoder.JSONDecodeError:
            print("Received message is not JSON formatted")
            print(msg)
    
    
    def send_command(self, str:str):
        lst = shlex.split(str.strip())
        data = self.parse_command_to_json_data(lst)
        self.send_string(json.dumps(data))
        

    def send_string(self, string: str):
        self.socket.send(string.encode())

    def parse_command_to_json_data(self, lst: list[str]):
        if (lst[0] == "walk_in_circle"):
            walk_in_circle(self)
            return
        if (lst[0] == "idle"):
            idle(self)
            return

        # Unique id using current time and random number
        id = str(datetime.datetime.now().timestamp()) +"-"+ str(random.randint(1,500))
        data = {'id': id, 'ActionType':lst[0]}

        if (len(lst) > 2):
            data['ActionState'] = lst[1]
            data['value'] = lst [2]
        elif (len(lst) > 1):
            if (is_number(lst[1])):
                data['value'] = lst[1]
            else:
                data['ActionState'] = lst[1]
        return data
 

if __name__ == '__main__':
    try:
        client = Client()
    except ConnectionRefusedError:
        print("Refused connection. Make sure the Unreal Engine game client is running.")
