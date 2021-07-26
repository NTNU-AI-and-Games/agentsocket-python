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
TCP_IP = "129.241.110.146"
TCP_PORT = 11111

images = []

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
        self.connect()
        while(True):
            # Receive two messages: Json and
            try:
                self.run_command("fakeAction")  # This can be any string. AgentSocket will interpret it as an invalid action, while still respond with image 
                
                msg = self.socket.recv(80001024) # will be cancelled by connection.shutdown(SHUT_RD)
                if msg == b'': # Indicates disconnection with the server
                    self.on_server_disconnect()
                    break
                else:
                    # Only accept the messages beginning with a PNG header
                    if b'\x89PNG' == msg[:4]:
                        pass
                    else:
                        try:
                            decodeFirst = msg[:5].decode()
                            if decodeFirst[0] == '{':
                                decoded = msg.decode()
                                data = json.loads(decoded)
                                if (data["type"] == "STEP"):
                                    print(data)
                                    environment.on_receive_step_response(data)
                        except Exception:
                            pass
                
            except Exception:
                print("Not connected. Try again..")
                time.sleep(0.5)
                self.connect()
                
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))

    def on_disconnect(self):
        self.socket.close()
        print(" - Disconnected")

    def on_server_disconnect(self):
        self.socket.close()
        print(" - Server disconnected")
    
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
        return action

    def send_action(self, action: Action):
        self.action_log.append(action)
        action_id = str(len(self.action_log) - 1)
        data = {'type': 'action'}
        data.update(action.to_dict())
        self.send_string(json.dumps(data))

    def send_string(self, string: str):
        self.socket.send(string.encode())


if __name__ == '__main__':
    try:
        client = Client()
    except ConnectionRefusedError:
        print("Refused connection. Make sure the Unreal Engine game client is running.")
