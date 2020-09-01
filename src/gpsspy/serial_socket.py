import socket

class SerialSocket(object):
    """
    SerialSocket

    This class provides some ducktypeing to allow the ubxtranslator to use an ethernet port that is broadcasting serial data

    Args: 
        eth_port (int): The port number to open a socket server on
    """

    def __init__(self, eth_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', eth_port))
        self.socket.listen()

        self.conn, self.addr = self.socket.accept()

    def read(self, read_data=1):
        """
        Reads a byte or bytes of data from the network port. 

        args:
            read_data (int, default 1): the number of bytes requested

        returns bytes[]: The requested bytes
        """
        data = self.conn.recv(read_data)
        return data

    def write(self, data):
        """
        Writes a byte or bytes of data to the network port.

        args:
            data (bytes[]): The data to write to the socket
        return (bool): True on completion

        """
        self.conn.send(data)
        return True

    def close(self):
        """
        Closes the open sockets
        """
        self.conn.close()
        self.socket.close()
