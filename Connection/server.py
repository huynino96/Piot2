import socket


'''
This class is used to create a UDP broadcast server
'''


class Server:
    def __init__(self, port, client_port):
        # The procedure is the same for Client class
        self.__port = port
        self.__client_port = client_port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__server.bind(("", port))

    def close(self):
        if self.__server:
            self.__server.close()

    def send_message(self, message):
        message = str.encode(message)
        self.__server.sendto(message, ("<broadcast>", self.__client_port))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # For this method, on_receive will be an function to handle any data
    # that we have received from the socket. User will define this method
    # to be suitable for their own need
    def listening(self, on_receive):
        while True:
            data, address = self.__server.recvfrom(1024)
            if data:
                on_receive(data)
            else:
                break


if __name__ == '__main__':
    def receieved(message):
        print(message)

    with Server(9999, 5555) as server:
        server.listening(receieved)
