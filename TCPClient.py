import socket
import json
from MessageReceiver import MessageReceiver

# Client to connect to UE4 tcp server
TCP_IP = "localhost"
TCP_PORT = 3462




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
        print(" - Login to your account")
        print(" - Ready to write your commands")
        print("Your input:")
        while(True):
            c = input().strip().split()

            if len(c) > 1:
                quotedStr = " ".join(c[1:]) #possibly quoted
                #print(quotedStr)
                if len(quotedStr) > 2 and quotedStr[0] == '"' and quotedStr[-1] == '"':
                    c = [c[0], quotedStr[1:-1]]
            if len(c) == 1:
                c.append(None)
            if len(c) == 2:
                try:
                    self.send_payload(c) #send it without checking it
                except:
                    print(" - Reconnecting...")
                    self.connect()
                    self.send_payload(c) #send it without checking it
            else:
                print(' - Write proper commands: <cmd> <arg0>')

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        self.ms = MessageReceiver(self)
        self.ms.start()

    def disconnect(self):
        self.socket.close()
        print(" - Disconnected")

    def receive_message(self, msg):
        print(msg)
        data = json.loads(msg) #dictionary
        #print(MessageParser.parse(data))
        #print("Your input:")

    def send_payload(self, lst): # data is a list of string (commands)
        data = {'command':lst[0],'value':lst[1]}
        self.socket.send(json.dumps(data).encode()) #or sendall()

if __name__ == '__main__':
    try:
        client = Client()
    except ConnectionRefusedError:
        print("Refused connection. Make sure the Unreal Engine game client is running.")
