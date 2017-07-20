#Marima Andrew Mambondiumwe
# worked on this with Sher, Daryll and Jonathan
import socket
import sys

MSGLEN = 1

# CONTRACT
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def send (msg, HOST, PORT):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((HOST, PORT))
  length = sock.send(bytes(msg + "\0"))
  print ("SENT MSG: '{0}'".format(msg))
  print ("CHARACTERS SENT: [{0}]".format(length))
  return sock

def receive_message (sock):
  print "Receiving message"
  chars = []
  try:
    while True:
      char = sock.recv(1)
      if char == bytearray('\0'):
        break
      if not char:
        break
      else:
        #print("Appending {0}".format(char))
        chars.append(char.decode("utf-8") )
  finally:
    return ''.join(chars)

def moduli_list_generator(string):
  moduli_list = []
  count = 0
  for character in string:
    count += ord(character)
  moduli = count % 13
  moduli_list.append(moduli)
  return moduli_list


def checksum(input_list):
  count1 = 0
  for x in input_list:
    count1 += x
  result = count1 % 17
  return result



def checksum_output(string):
  return checksum(moduli_list_generator(string))

if __name__ == "__main__":
  # Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  '''
  if len(sys.argv) < 3:
    print ("Usage:")
    print (" python client.py <host> <port>")
    print (" For example:")
    print (" python client.py localhost 8885")
    print 
    sys.exit()
'''
  #host = sys.argv[1]
  #port = int(sys.argv[2])
  host="localhost"
  port= 8885
  Running = True
  while Running:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    #sock.connect((sys.argv[1], int(sys.argv[2])))
    input=int(raw_input("Press 1 for login, 2 for register:"))
    if input==1:
      username=raw_input("Username:")
      password=raw_input("Password")
      user_input= " ".join(["LOGIN", username, password, "\0"])
      crc_number=checksum_output(user_input)
      number=str(crc_number)
      message=" ".join([number, user_input])
      message1=bytearray(message, encoding="utf-8")
      print message1
      length=sock.send(message1)
      #length=send(message1)
      print "Number of bytes sent:", length
      session_cookie=receive_message(sock)
      if session_cookie.startswith("Cookie"):
        print "Success. Login"
        input = int(raw_input("Press:\n 1: Message \n 2: Store \n3: Count \n4: Delete Message \n5 Get Message  \n 6: Dump \n7:Log Out"))
        while input != 7:
           #get message, dump.
          if input==1:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))


            content1=raw_input("What is your message?")
            content="|"+content1+"|"
            user_input = " ".join(["MESSAGE", content, session_cookie, "\0"])
            num=str(checksum_output(user_input))
            user_input=" ".join([num, user_input])
            user_in=bytearray(user_input, encoding="utf-8")
            sock.send(user_in)
            print "your message sent"
            message1=receive_message(sock)
            print message1
            sock.close()
          elif input==2:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            user_input1 = " ".join(["STORE", username, session_cookie, "\0"])
            crc_number = str(checksum_output(user_input1))
            user_input=" ".join([crc_number, user_input1])
            print user_input
            user_in = bytearray(user_input, encoding="utf-8")
            sock.send(user_in)
            print "your message sent"
            message1 = receive_message(sock)
            print message1
            sock.close()

          elif input == 3:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            user_input = " ".join(["COUNT", username, session_cookie, "\0"])
            num = str(checksum_output(user_input))
            print user_input
            user_input1 = " ".join([num, user_input])
            user_in = bytearray(user_input1, encoding="utf-8")
            sock.send(user_in)
            print "your message sent"
            message1 = receive_message(sock)
            print message1
            sock.close()
          elif input == 4:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            user_input = " ".join(["DELMSG", username, session_cookie, "\0"])
            num = str(checksum_output(user_input))
            print user_input
            user_input1 = " ".join([num, user_input])
            user_in = bytearray(user_input1, encoding="utf-8")
            sock.send(user_in)
            print "your message sent"
            message1 = receive_message(sock)
            print message1
            sock.close()
          elif input == 5:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            user_input = " ".join(["GETMSG", username, session_cookie, "\0"])
            num = str(checksum_output(user_input))
            print user_input
            user_input1 = " ".join([num, user_input])
            user_in = bytearray(user_input1, encoding="utf-8")
            sock.send(user_in)
            print "your message sent"
            message1 = receive_message(sock)
            print message1
            sock.close()
          elif input == 6:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            user_input1 = " ".join(["DUMP", username, session_cookie, "\0"])
            num = str(checksum_output(user_input1))
            print user_input
            user_input = " ".join([num, user_input1])
            user_in = bytearray(user_input, encoding="utf-8")
            sock.send(user_in)
            print "your message sent"
            message1 = receive_message(sock)
            print message1
            sock.close()

          input = int(raw_input("Press:\n 1: Message \n 2: Store \n3: Count \n4: Delete Message \n5 Get Message  \n 6: Dump \n 7: Log Out"))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        user_input = " ".join(["LOGOUT", username, session_cookie, "\0"])
        print user_input
        num=str(checksum_output(user_input))
        user_input1 = " ".join([num, user_input])

        user_in = bytearray(user_input1, encoding="utf-8")
        sock.send(user_in)
        print "your message sent"
        message1 = receive_message(sock)
        sock.close()

      else:
        print session_cookie
        sock.close()

    else: #register username
      username = raw_input("Username:")
      password = raw_input("Password")
      user_input = " ".join(["REGISTER", username, password, "\0"])
      crc_number = checksum_output(user_input)
      number = str(crc_number)
      message = " ".join([number, user_input])
      message1=bytearray(message, encoding="utf-8")
      print message1
      length = sock.send(message1)
      session_cookie = receive_message(sock)
      sock.close()

