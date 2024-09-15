import socket, pickle
from config import PORT
from server import Server

class Player:
  def __init__(self, is_host):
    self.is_host = is_host
    self.client = None # represent the connection between the player and the server and used to send and receive data packets
    
    if is_host:
      self.server = None
      
  def connect(self, host_ip):
    if self.is_host:
      self.server = Server(host_ip)
      self.server.run()
    
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 TCP/Ip socket
    self.client.connect((host_ip, PORT))
  
  def move(self, direction):
    self.client.sendall(pickle.dumps((self.is_host, direction)))
    
  def get_data(self):
    data = self.client.recv(1080) # the number was choosed carefully because it is multiple of 54 the server packet size
    
    if data == "":
      return "sc" # stands for "server closed"
    
    try:
      return pickle.loads(data)
    
    except Exception as e: # incomplete packet was received
      print("a packet has been lost")
      return False