from random import choice
from time import sleep
import socket, pickle, threading, math

from config import BALL_RADIUS, MAX_BOUNCE_ANGLE, PLAYER_WIDTH, PLAYER_HEIGHT, INITIAL_POS_LEFT_DOWN_CORNER, PADDING, BALL_SPEED, PLAYER_SPEED, PORT

lock = threading.Lock()

class Server:
  def __init__(self, ip):
    self.ip = ip
    # self.players = [] #when allowing more than 2
    self.players = [INITIAL_POS_LEFT_DOWN_CORNER, INITIAL_POS_LEFT_DOWN_CORNER]
    self.ball_x = 1/2
    self.ball_y = 1/2
    self.ball_dx = 0
    self.ball_dy = choice([1, -1]) * BALL_SPEED[1]
    self.server = None 
    self.conns = []
    self.is_running = False
    
  def run(self):
    thread = threading.Thread(target=self.running)
    thread.start()
    
  def running(self):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 TCP/Ip socket
    try:
      self.server.bind((self.ip, PORT))
      self.server.listen()
    except Exception as e:
      print(e)
      return
    else:
      print(f"Server is listening on port {PORT}")
      self.is_running = True
      thread = threading.Thread(target=self.handle_connections)
      thread.start()
      self.send_data()
  
  def handle_connections(self):
    while True:
      try:
        conn, addr = self.server.accept()
      except Exception as e:
        print(e)
        return
      else:
        self.conns.append(conn)
        # self.players.append(INITIAL_POS_LEFT_DOWN_CORNER) #when allowing more than 2
        thread = threading.Thread(target=self.handle_player_input, args=[conn])
        thread.start()
  
  def handle_player_input(self, conn):
    while True:
      try:
        data = pickle.loads(conn.recv(340))
      
      except OSError: # means the server has been closed
        break
      
      else:
        if self.is_running:
          lock.acquire()
          self.update_players(data)
          lock.release()
  
  def update_players(self, data):
    direction = 1 if data[1] > 0 else (0 if not data[1] else -1)
    
    if data[0] and 0 <= self.players[0] + PLAYER_SPEED*direction <= 1 - PLAYER_WIDTH:
      self.players[0] += PLAYER_SPEED*direction
    
    elif not data[0] and 0 <= self.players[1] + PLAYER_SPEED*direction <= 1 - PLAYER_WIDTH:
      self.players[1] += PLAYER_SPEED*direction

  def update_ball(self):
    message = ""   
    #ball hits one of the side walls 
    if self.ball_x <= BALL_RADIUS or self.ball_x + BALL_RADIUS >= 1:
      self.ball_dx *= -1
      message = "c"*39 # c stand for collision
    
    #balls hits one of the players
    #player1
    elif self.ball_y + BALL_RADIUS + PLAYER_HEIGHT + PADDING >= 1 and self.players[0] - BALL_RADIUS <= self.ball_x <= self.players[0] + PLAYER_WIDTH + BALL_RADIUS:
      self.ball_dy = -BALL_SPEED[1]
      self.ball_dx = BALL_SPEED[0]*self.sin_bounce_angle(self.players[0])
      message = "c"*39 # c stand for collision
      
     #player2 
    elif self.ball_y - BALL_RADIUS - PLAYER_HEIGHT - PADDING <= 0 and self.players[1] - BALL_RADIUS <= self.ball_x <= self.players[1] + PLAYER_WIDTH + BALL_RADIUS:
      self.ball_dy = BALL_SPEED[1]
      self.ball_dx = BALL_SPEED[0]*self.sin_bounce_angle(self.players[1])
      message = "c"*39 # c stand for collision
  
    #ball falls down
    elif self.ball_y + BALL_RADIUS >= 1:
      #player 2 win
      message = "2"*39 # mean player 2 win the round
    #ball flies away
    elif self.ball_y <= BALL_RADIUS:
      #player 1 win
      message = "1"*39 # mean player 1 win the round
    
    self.ball_x += self.ball_dx
    self.ball_y += self.ball_dy
    
    return message 
  
  def sin_bounce_angle(self, player_pos):
    paddle_center = player_pos + PLAYER_WIDTH/2
    relative_hit_pos = (self.ball_x - paddle_center) / (PLAYER_WIDTH/2)
    bounce_angle = relative_hit_pos * MAX_BOUNCE_ANGLE
    
    return math.sin(bounce_angle)

  def send_data(self):
    while True:
      
      if self.is_running:
        lock.acquire()
        ball_message = self.update_ball()
        
        if ball_message:
          decoded_ball_message = pickle.dumps(ball_message)
          for player_conn in self.conns:
            try:
              player_conn.sendall(decoded_ball_message)
            except:
              self.conns.remove(player_conn)
              
        data = pickle.dumps((self.ball_x, self.ball_y, self.players))
        for player_conn in self.conns:
          try:
            player_conn.sendall(data)
          except:
            self.conns.remove(player_conn)
        
        lock.release()
      
      sleep(1/60)
      
  def restart(self):
      # lock.acquire()
      self.players = [INITIAL_POS_LEFT_DOWN_CORNER, INITIAL_POS_LEFT_DOWN_CORNER]
      self.ball_x = 1/2
      self.ball_y = 1/2
      self.ball_dx = 0
      self.ball_dy = choice([1, -1]) * BALL_SPEED[1]
      self.is_running = True
      # lock.release()
     
  def close_server(self):
    for conn in self.conns:
      conn.close()
    
    self.server.close()
    print("Server has been closed succefully")