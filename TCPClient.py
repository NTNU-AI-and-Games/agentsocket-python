from Input import Action
import socket
import json
import datetime
import random
import shlex

import queue
import time
import cv2
import numpy as np

import Environment as environment
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
        self.action_log_queue = queue.Queue()

        self.action_log = []
        self.env_log = []

        self.query_log = []
        self.query_result_log = []

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ms = MessageReceiver(self)
        self.run()


    def run(self):
        self.socket.connect((self.host, self.port))
        self.ms.start() # Starts the run() method in ms (in a separate thread)
        print("Your input:")
        while(True):
            c = input().strip()

            # if c == 'a':
            #     L = environment.states[0]['imageValue']
            #     #print(L[-20:])
            #     im = cv2.imdecode(np.array(L, dtype=np.uint8), cv2.IMREAD_COLOR)
            #     cv2.imshow("Hey", im)
            #     cv2.waitKey(100)

            
            if len(environment.states) > 0:
                L = environment.states[-1]['imageValue']
                im = cv2.imdecode(np.array(L, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow("AgentSocket_agent001", im)
                cv2.setWindowProperty("AgentSocket_agent001", cv2.WND_PROP_TOPMOST, 1)
                cv2.waitKey(100)


            if len(c) > 0:
                try:
                    self.run_command(c) # send it without checking it
                except:
                    print(" - Reconnecting...", end="\r")
                    self.connect()
                    print(" - Reconnected", end="\n")
                    self.run_command(c) # send it without checking it
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
        print("received")
        try:
            data = json.loads(msg)
            if (data["type"] == "STEP"):
                environment.on_step_received(data)
                #print("states:", environment.states)
            if (data["type"] == "STATE"):
                environment.on_state_received(data)
                print("states:", environment.states)
            elif (data["type"] == "REWARD"):
                environment.on_reward_received(data)
                print("rewards:", environment.rewards)
            elif (data["type"] == "ACK"):
                if (data["Status"] != "OK"):
                    print(data)
            else:
                print("something is wrong")
        except json.decoder.JSONDecodeError:
            print("Received message is not JSON formatted")
            #print(msg)
    
    
    def run_command(self, str:str):
        lst = shlex.split(str.strip())
        if (lst[0].lower() == "query"):
            pass
        elif (lst[0].lower() == "action"):
            action = self.parse_action(lst[1:])
            self.send_action(action)
        else: # FIXME: For now, we just use this as if it is action
            action = self.parse_action(lst)
            self.send_action(action)
        


    def parse_command_to_json_data(self, lst: list[str]):
        return self.parse_action(lst)

    def parse_action(self, action_args) -> Action:
        '''Return Action object from the input string list'''
        action = Action(action_args[0])
        if (len(action_args) > 2):
            action.type = action_args[1]
            action.value = action_args[2]
        elif (len(action_args) > 1):
            if (is_number(action_args[1])):
                action.value = action_args[1]
            else:
                action.type = action_args[1]
        return action

    def send_action(self, action: Action):
        self.action_log.append(action)
        action_id = str(len(self.action_log) - 1)
        data = {'type': 'action', 'id': action_id}
        data.update(action.to_dict())
        self.send_string(json.dumps(data))

    def send_string(self, string: str):
        self.socket.send(string.encode())


    def send_query(self, action: str):
        action_id = len(self.action_log)
        self.action_log.append(action)
        id = str(action_id)
        data = {'type': 'query', 'id': id, 'actionName':lst[0]}


if __name__ == '__main__':
    try:
        client = Client()
    except ConnectionRefusedError:
        print("Refused connection. Make sure the Unreal Engine game client is running.")
