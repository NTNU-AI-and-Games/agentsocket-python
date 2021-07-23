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

#TCP_IP = "10.22.41.62"
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
        self.loop()

    def loop(self):
        if len(environment.states) > 0:
            try:
                L = environment.states[-1]['imageValue']
                im = cv2.imdecode(np.array(L, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow("AgentSocket_agent001", im)
                cv2.setWindowProperty("AgentSocket_agent001", cv2.WND_PROP_TOPMOST, 1)
                cv2.waitKey(10)
            except Exception:
                pass

            try:
                reward = environment.rewards[-1]
                print(reward)
            except Exception:
                pass


        try:
            #self.run_command("a") # send it without checking it
            data = {'type': 'action', 'actions':[]}
            data['actions'].append({'type':'action', 'name':'fire'})
            data['actions'].append({'type':'action', 'name':'jump'})
            data['actions'].append({'type':'key', 'key':'s'})
            data['actions'].append({'type':'axis', 'key':'mousex', 'value': '10', 'state':'pressed'})
            self.send_string(json.dumps(data))
        except:
            print(" - Reconnecting...", end="\r")
            self.connect()
            print(" - Reconnected", end="\n")
            #self.run_command(c) # send it without checking it

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
        self.loop()
    
    
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
            action.name = action_args[1]
            action.value = action_args[2]
        elif (len(action_args) > 1):
            if (is_number(action_args[1])):
                action.value = action_args[1]
            else:
                action.name = action_args[1]
        return action

    def send_action(self, action: Action):
        self.action_log.append(action)
        action_id = str(len(self.action_log) - 1)
        data = {'type': 'action'}
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
