#marima andrew mambondiumwe
#implemented and written with Sher, Jonathan and Darryl

import base64
import uuid
import threading
# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html
import socket
import sys


class SimpleMailServerProtocol():
    def __init__(self):
        self.IMQ = []  # incoming_message_queue
        self.MBX = {}  # user_mailboxes
        self.login = {} #registered accounts and passwords
        self.ID = {}  #session ids and usernames
        self.assigned_cookies=[] #to check which session cookies has already been assigned


    def moduli_list_generator(self, string):

        count = 0
        for character in string:
            count += ord(character)
        moduli = count % 13
        count=0
        return moduli

    def checksum(self, input_list):
        count1=0
        count1 += input_list
        print "The sum of each moduli in the list:", count1
        result = count1 % 17
        return result

    def checksum_output(self, string):
        return self.checksum(self.moduli_list_generator(string))

    # CONTRACT
    # start_server : string number -> socket
    # Takes a hostname and port number, and returns a socket
    # that is ready to listen for requests
    def start_server (self, host, port):

      server_address = (host, port)
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(server_address)
      sock.listen(1)  #listens for connections on specified port
      return sock


      # CONTRACT
      # socket -> boolean
      # Shuts down the socket we're listening on.
    def stop_server(self, sock):
      return sock.close()
    #<------------------------------------------------------------------------------------------------------------>
    def get_message(self, sock):
      chars = []
      connection, client_address = sock.accept()
      print ("Connection from [{0}]".format(client_address))
      try:
          while True:
              char = connection.recv(1)
              if char == bytearray('\0'):
                  break
              if not char:
                  break
              else:
                  # print("Appending {0}".format(char))
                  chars.append(char.decode("utf-8"))
      finally:
          tuple1= (''.join(chars), connection)
          message=str(tuple1[0])
          crc = int(message.split(" ")[0])
          index=message.find(chr(32))+1
          final_message=message[index:]
          output=self.checksum_output(final_message)
          if crc==output:
              print "worked"
              tuple=(final_message, connection)
              return tuple
          else:
              connection.send(bytearray("Error, resend the message"+"\0", encoding="utf-8"))

    def assign_cookie(self, username, conn):
        '''assigns cookie to the user'''
        if username not in self.ID:  #checking if username doesn't already have a cookie and if cookie is not assigned
            session_id = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
            while session_id in self.assigned_cookies:
                session_id = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
            self.ID[username]=session_id
            self.assigned_cookies.append(session_id)
            cookie= " ".join([b"Cookie:", session_id])
            cooki=bytearray(cookie, encoding='utf-8')
            conn.sendall(cooki)
            conn.close()
        else:
            if self.ID[username] in self.assigned_cookies:
                self.assigned_cookies.remove(self.ID[username])
            del self.ID[username]
            print username, "has session cookie already"
            self.assign_cookie(username, conn)


    def register(self, message, connection):
          '''Register with password.Only username is parsed.Password must be direct'''
          message=str(message)

          username = message.split(" ")[1]   #splitting username from message
          password= message.split(" ")[2]   #splitting password from message

          if username not in self.login:    #if user is not already registered
              self.login[username]=password #register him/her
              if username not in self.MBX:   #if user does not have a mailbox
                  self.MBX[username]=[]     #create mailbox
              connection.send(bytearray("You are registered now. You can login now" + '\0', encoding="utf-8"))
          else:
              connection.send(bytearray("KO. You are registered. You should login now."+'\0',encoding="utf-8"))
              connection.close()
              return False

    def log_out(self, message, connection):
        message=str(message)
        cookie = message.split(" ")[3]
        username=message.split(" ")[1]
        if username in self.ID:      #if user is already registered
            if self.ID[username]==cookie:
                for i in self.assigned_cookies:
                    if i ==cookie:
                        self.assigned_cookies.remove(i)     #delete user session from assigned session list
                del self.ID[username]
                print "Removed session id of user:", username
            connection.send(bytearray('Logged Out' + '\0', encoding="utf-8"))


    def log_in(self,message,connection):
        #content=message.split(" ")[:4] "LOGIN andrew 4"
        message=str(message)
        username = message.split(" ")[1]  # splitting username from message "LOGIN andrew
        password = message.split(" ")[2]  # splitting password from message

        if username in self.login:          #if user is registered
            if self.login[username]==password:  #if user account match user password
                print "Success.", username, "is logged in."
                self.assign_cookie(username, connection)    #assign cookie to logged in user
                print "Success. User logged in"

            else:
                connection.send(bytearray('Failure. Wrong Password' + '\0', encoding="utf-8"))
        else:
            print "he should register first"
            connection.send(bytearray('You should register first.'+'\0',encoding="utf-8"))
            connection.close()


    def add_message(self, content, connection):

      content=str(content)
      message1=content.split("|")
      message=message1[1]
      print message
      cookie=message1[2]
      cookie_str=cookie.split(" ")
      cookie2=cookie_str[2]


      print cookie2
      for i in self.ID:
          if self.ID[i]==cookie2:
              self.IMQ.append(message)
              print "message appended"
              connection.send(bytearray("OK. You message was added."+'\0', encoding="utf-8"))
          else:
              print "not appended"
              connection.send(bytearray("KO"+'\0', encoding='utf-8'))


    def store(self, message, connection):
        message = str(message)
        cookie = message.split(" ")[3]
        username = message.split(" ")[1]
        if username in self.ID:
            if self.ID[username]==cookie:
                if username in self.MBX:
                    recent_message = self.IMQ.pop()
                    self.MBX[username].append(recent_message)
                    connection.send(bytearray("OK. Your recent message has been stored in user's mailbox"+"\0", encoding="utf-8"))

            else:
                connection.send(bytearray("OK. Your message has not been stored"+"\0", encoding="utf-8"))


    def count(self, message, connection):
        message = str(message)
        cookie = message.split(" ")[3]
        username = message.split(" ")[1]
        if username in self.ID:
            if self.ID[username]==cookie:
                if username in self.MBX:
                    count = len(self.MBX[username])
                    count=str(count)
                    connection.send(bytearray("Your total messages COUNTED:"+ "<"+ count+ ">"+"\0", encoding="utf-8"))

                else:
                    connection.send(bytearray("KO. Did not count"+ "\0", encoding="utf-8"))


    def delete_message(self, message, connection):
        message = str(message)
        cookie = message.split(" ")[3]
        username = message.split(" ")[1]
        if username in self.ID:
            if self.ID[username] == cookie:
                if username in self.MBX:
                    self.MBX[username].pop(0)
                    connection.send(bytearray("OK. You first message was deleted from MBX." + "\0", encoding="utf-8"))
                else:
                    connection.send(bytearray("KO. was not deleted" + "\0", encoding="utf-8"))


    def get_client_message(self, message, connection):
        message = str(message)
        cookie = message.split(" ")[3]
        username = message.split(" ")[1]
        if username in self.ID:
            if self.ID[username] == cookie:
                if username in self.MBX:

                    connection.send(bytearray("Your message:"+ message+"\0", encoding="utf-8"))

                else:
                    connection.send(bytearray("KO. did not get client message"+"\0", encoding="utf-8"))



        # return the first message from the user's mailbox queue
        # return KO if no message or user not registered

    def dump(self, msg, conn):
        message = str(msg)
        cookie = message.split(" ")[3]
        username = message.split(" ")[1]
        if username in self.ID:
            if self.ID[username] == cookie:
                print self.MBX
                print self.IMQ
                connection.send(bytearray("OK" + "\0", encoding="utf-8"))

            else:
                print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(message))
                connection.send(bytearray("KO" + "\0", encoding="utf-8"))



# CONTRACT
# handle_message : string socket -> boolean
# Handles the message, and returns True if the server
# should keep handling new messages, or False if the 
# server should shut down the connection andc quit.
    def handle_message (self, msg, conn):
      if msg.startswith("REGISTER"):
        self.register(msg, connection)
      elif msg.startswith("LOGIN"):
        self.log_in(message, conn)
      elif msg.startswith("MESSAGE"):
        self.add_message(msg, conn)
      elif msg.startswith("STORE"):
        self.store(msg, conn)
      elif msg.startswith("COUNT"):
        self.count(msg, conn)
      elif msg.startswith("DELMSG"):
        self.delete_message(msg, conn)
      elif msg.startswith("GETMSG"):
        self.get_client_message(msg, conn)
      elif msg.startswith("LOGOUT"):
        self.log_out(msg, connection)
      elif msg.startswith("DUMP"):
        self.dump(msg, conn)

  
if __name__ == "__main__":
  # Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  '''
  if len(sys.argv) < 3:
    print ("Usage: ")
    print (" python server.py <host> <port>")
    print (" e.g. python server.py localhost 8888")'''
    #sys.exit()

  #host = sys.argv[1]
  #port = int(sys.argv[2])
  host = "localhost" #or you can put ip of 0.0.0.0 (this ip allows any other ip to connect to this server)
  port = 8885
  mail_server=SimpleMailServerProtocol()
  sock = mail_server.start_server(host, port)
  print("Running server on host [{0}] and port [{1}]".format(host, port))
  
  RUNNING = True
  while RUNNING:
    message, connection = mail_server.get_message(sock)

    print("MESSAGE: [{0}]".format(message))
    print "got the message"
    t= threading.Thread(target=mail_server.handle_message, args=(message, connection,)).start()

  #mail_server.stop_server(sock)



