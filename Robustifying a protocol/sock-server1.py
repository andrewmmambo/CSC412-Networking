
import threading
from Message_server1 import MessageServer
# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import sys


# CONTRACT
# start_server : string number -> socket
# Takes a hostname and port number, and returns a socket
# that is ready to listen for requests
def start_server (host, port):
  server_address = (host, port)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(server_address)
  sock.listen(1)
  return sock
  
# CONTRACT
# get_message : socket -> Tuple(string, socket)
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.

#<------------------------------------------------------------------------------------------------------------>


#This is get_message() method I implemented in Matt Jadud's server code file - Sher Sanginov

def get_message (sock):
  connection, client_address = sock.accept() # accept client connection , returns a tuple of two values
  print "Client address: [{0}]".format(client_address)
  message=connection.recv(5000)
  tup=(message, connection)
  return tup
  #char=''
  #while char != b'\0': #this loop stops when received character is equal to \0 (delimitor)
  #	char=connection.recv(1)  #receives one character at a time
   #     if char.isalpha()==True or char.isspace()== True or char.isdigit()==True:  #checks validity of a character
    #    	string= str(char) #append char to string
     #   	print "Received byte:", string   #print each string character
#now if you think about that a bit, you'll come to realize : reading ; message must be fixed length
#what must i do to send complete message? you can user delimeters: every message with be delimited with period
# message is not done until the period is sent
#bytes are not strings some_byte=b'x'
  #connection.send("connected\0")


#< ----------------------------------------------------------------------------------------------------------->


# Mail server methods:
"""
Just for reference:
my_library= [{"username":5},{"fotima":6505},{"no":2, "sh":5, "what":99}]
print len(my_library[2])

"""









# CONTRACT
# socket -> boolean
# Shuts down the socket we're listening on.
def stop_server (sock):
  return sock.close()

# CONTRACT
# handle_message : string socket -> boolean
# Handles the message, and returns True if the server
# should keep handling new messages, or False if the 
# server should shut down the connection and quit.
def handle_message (msg, conn):
  print "hello boys"
  if msg.startswith("REGISTER"):
    MessageServer().register(msg, conn)
  elif msg.startswith("MESSAGE"):
    MessageServer().add_message(msg, conn)
  elif msg.startswith("STORE"):
    MessageServer().store(msg, conn)
  elif msg.startswith("COUNT"):
    MessageServer().count(msg, conn)
  elif msg.startswith("DELMSG"):
    MessageServer().delete_message(msg, conn)
  elif msg.startswith("GETMSG"):
    MessageServer().get_client_message(msg, conn)
  elif msg.startswith("DUMP"):
    MessageServer().dump(msg, conn)

  
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
  host = "localhost"
  port = 8885
  sock = start_server(host, port)
  print("Running server on host [{0}] and port [{1}]".format(host, port))
  
  RUNNING = True
  while RUNNING:
    message, connection = get_message(sock)
    print("MESSAGE: [{0}]".format(message))
    t= threading.Thread(target=handle_message, args=(message, connection,)).start()
   # handle_message(message, connection, MessageServer())

    #handle_message(message, connection, MessageServer())
    # This 'if' probably should not be in production.
    # Our template/test code returns "None" for the connection...


  stop_server(sock)



