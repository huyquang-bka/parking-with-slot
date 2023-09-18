from PyQt5.QtWebSockets import QWebSocketServer, QWebSocket
from PyQt5.QtCore import QUrl


class SocketServer(QWebSocketServer):
    def __init__(self, parent=None):
        super(SocketServer, self).__init__(
            "SocketServer", QWebSocketServer.NonSecureMode, parent)
        self.clients = []

    def reconnect(self, port):
        self.listen(QUrl("ws://localhost:{}".format(port)))
        print("Connected to port {}".format(port))
        self.newConnection.connect(self.on_new_connection)
        return True

    def on_new_connection(self):
        client = self.nextPendingConnection()
        self.clients.append(client)

    def on_client_disconnect(self, client):
        self.clients.remove(client)
        print("Client disconnected")

    def on_message(self, message):
        print("Message received: {}".format(message))

    def on_error(self, error_code):
        print("Error: {}".format(error_code))

    def send_message(self, message):
        for client in self.clients:
            client.sendTextMessage(message)

    def close(self):
        self.close()
        print("Closed connection")
        return True

    def get_clients(self):
        return self.clients

    def get_client(self, index):
        return self.clients[index]


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    server = SocketServer()
    server.reconnect(1234)
    app.exec_()
