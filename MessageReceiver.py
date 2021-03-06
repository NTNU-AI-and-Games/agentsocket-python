from threading import Thread

class MessageReceiver(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.daemon = True #the thread will die out when the main thread ends

    def run(self):
        print(" - Listening for incoming msgs")
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            # An error will be throw is the connection is not settled (such as if the server is down)
            msg = self.client.socket.recv(8001024) #will be cancelled by connection.shutdown(SHUT_RD)
            if msg == b'': # Indicates disconnection with the server
                self.client.on_server_disconnect()
                break
            else:
                decoded_msg = ""
                try:
                    decoded_msg = msg.decode()
                except:
                    decoded_msg = "(message cannot be decoded)"
                    print("Received message cannot be decoded. Message: ")
                    print(msg)
                #print("inside ms, the message is:", msg)
                #self.client.receivedMessage(msg)
                Thread(target=self.client.on_receive_message, args = (decoded_msg,)).start() #new thread
