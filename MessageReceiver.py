from threading import Thread

class MessageReceiver(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.daemon = True #the thread will die out when the main thread ends

    def run(self):
        print("Listening for incoming msgs")
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            # an error will be throw is the connection is not settled (such as if the server is down)
            msg = self.client.socket.recv(1024) #will be cancelled by connection.shutdown(SHUT_RD)
            print("Received msg")
            if msg == b'': #indicates disconnection
                #print(msg, " - message")
                self.client.disconnect()
                break
            else:
                msg = msg.decode()
                #print("inside ms, the message is:", msg)
                #self.client.receivedMessage(msg)
                Thread(target=self.client.receive_message, args = (msg,)).start() #new thread
