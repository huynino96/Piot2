import socket

'''
This class creates a udp broadcast client that will be used to send and received messages from a server
'''


class Client:
    def __init__(self, port, server_port):
        self.__port = port
        self.__server_port = server_port
        # We create a UDP socket and then enable the broadcast mode
        # by setting socket option to broadcast
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Bind to the "" host, which will be 127.0.0.1 and port
        self.__client.bind(("", port))

    def __enter__(self):
        return self

    def close(self):
        if self.__client:
            self.__client.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def send_message(self, message):
        message = str.encode(message)   # Encode message to bytes
        # Send message to address <broadcast> instead of a local host
        # to make sure any udp server running with __server_port will receive our message
        self.__client.sendto(message, ("<broadcast>", self.__server_port))

    # This method will wait for a return message from the server
    # the second it receive a message. It will stop running and return that data
    def read_response(self):
        while True:
            # Receive message using 1024 bytes of buffer
            result = self.__client.recv(1024)
            if result:
                data = result[0] if type(result) is tuple else result
                return data
            else:
                break
        return None


if __name__ == '__main__':
    with Client(5555, 9999) as client:
        try:
            client.send_message("Hello")
        except Exception as e:
            print(e)
            client.close()
