class MessageServer():
    def __init__(self):
        self.IMQ = []  # incoming_message_queue
        self.MBX = {}  # user_mailboxes

    def register(self, message, connection):
        start = message.find("<") + 1
        stop = message.find(">")
        username = message[start:stop]
        if username not in self.MBX:
            self.MBX[username]=[]
            connection.send("OK. You are registered now.")
            print self.MBX
            return True
        else:
            connection.send("KO. You are not registered.")
            return False



    def add_message(self, content, connection):
        start = content.find("<") + 1
        stop = content.find(">")
        message = content[start:stop]
        self.IMQ.append(message)
        connection.send("OK. You message was added.")
        return True


    def store(self, username, connection):
        '''
        if user registered:
          take his recent message off the queue and store in the user's mailbox as a value
        :param username:
        :return:
        '''
        start = username.find("<") + 1
        stop = username.find(">")
        user = username[start:stop]
        if user in self.MBX:
            recent_message= self.IMQ.pop()
            self.MBX[user].append(recent_message)
            connection.send("OK. Your recent message has been stored in user's mailbox")
            return True
        else:
            connection.send("KO. Your message has not been stored")
            return False


    def count(self, username, connection):
        start = username.find("<") + 1
        stop = username.find(">")
        user = username[start:stop]
        if user in self.MBX:
            count=len(self.MBX[user])
            connection.send("Your total messages COUNTED:", "<", count,">")
            return True
        else:
            connection.send("KO. did not count error")
            return False

    def delete_message(self, username, connection):
        start = username.find("<") + 1
        stop = username.find(">")
        user = username[start:stop]
        if user in self.MBX:
            self.MBX[user].pop(0)
            connection.send("OK. You first message was deleted from MBX.")
            return True
        else:
            connection.send("KO. was not deleted")
            return False

    def get_client_message(self, username, connection):
        start = username.find("<") + 1
        stop = username.find(">")
        user = username[start:stop]
        if user in self.MBX:
            connection.send("Your message:",self.MBX[user].pop())
            return True
        else:
            connection.send("KO. did not get client message")
            return False

        #return the first message from the user's mailbox queue
        #return KO if no message or user not registered


    def dump(self, msg, conn):
        if "DUMP" in msg:
            print self.MBX
            print self.IMQ
            conn.sendall(b"OK\0")
            return True
        else:
            print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(msg))
            conn.sendall(b"KO\0")
            return False

'''
        When the server receives a DUMP command, it should print the contents of the IMQ and MBX to its terminal.
        This is a debugging command; it allows the client to ask the server to print its contents,
        which is useful to the server author. It should always return OK. '''
