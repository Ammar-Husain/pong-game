from threading import Thread
from time import sleep
import pygame, sys
from player import Player

from config import BG_COLOR, TEXT_COLOR, BALL_RADIUS, BALL_COLOR, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_PADDLE_COLOR, OP_PADDLE_COLOR, PADDING, HOST_IP

class Game:
  def __init__(self, s_w, s_h):
    self.s_w = s_w
    self.s_h = s_h
    self.ball_radius = BALL_RADIUS * s_w
    self.player_width = PLAYER_WIDTH * s_w
    self.player_height = PLAYER_HEIGHT * s_h
    self.padding = PADDING * s_h
    self.screen = None
    self.clock = None
    self.player = None
    self.sound = None
  
  def start(self):
    self.set_pygame()
    message = "Enjoy!!!"
    # get player option (host or guest) and connect it to the server (server run on host device)
    while True:
      is_player_host = self.is_host(message)
      self.player = Player(is_player_host)
      
      host_ip = HOST_IP
      connected, message = self.connect_player(host_ip)
      if connected: break
    
    # seperate thread for getting player detecting player movements and send them to the server
    thread = Thread(target=self.send_moves)
    thread.start()
    
    # infinite loop for getting data from the server and drawing the game    
    while True:
      data = self.player.get_data() # get ball and players positions data
      
      if not data: # this was temporary solution for the proplem of incomplete packets received from the server
        continue
    
      if len(data) == 3: # len == 3 means regular state update
        ball_x, ball_y, players_pos = data

      elif data[0] == "c": # a message means the ball hit something (player or sidewall)
        self.sound.play()
        continue
      
      elif data[0] == "1" or data[0] == "2": # messages indicate a round end and a player win (player1 or player2)
        self.show_result(data[0]) #show result screen
        
        if self.player.is_host: # the host can decide to either continue or stop the game
          self.decide_if_to_continue()
          continue
        else:
          self.player.wait_for_restart() # the guest await for host decision             
      
      # this will be used to makes each player see his paddle in the bottom and with his color and the oponent paddle in the top (the server does not see or store the position of the player in the y axis)
      if self.player.is_host:
        my_pos = players_pos[0]
        op_pos = players_pos[1]
      else:
        my_pos = players_pos[1]  
        op_pos = players_pos[0]
      
      # create players paddles rects from the received data
      
      my_paddle = pygame.Rect(my_pos*self.s_w, self.s_h-self.player_height-self.padding, self.player_width, self.player_height)
      op_paddle = pygame.Rect(op_pos*self.s_w, self.padding, self.player_width, self.player_height)
      
      # flip the ball position for the guest up down to fit his reversed perspective
      if not self.player.is_host:
        ball_y = 1 - ball_y
        
      # erase last frame
      self.screen.fill(BG_COLOR)
      
      # Draw and blit ball and players paddles
      ball = pygame.draw.circle(self.screen, BALL_COLOR, (ball_x*self.s_w, ball_y*self.s_h), self.ball_radius)
      pygame.draw.rect(self.screen, PLAYER_PADDLE_COLOR, my_paddle, 0, int(self.player_height//2))
      pygame.draw.rect(self.screen, OP_PADDLE_COLOR, op_paddle, 0, int(self.player_height//2))
      pygame.display.flip()
      
      # self.clock.tick(60) # no need for it because server control frame rate by controlling frequency of data packets send putting it will cause extra delay on the game
      
  #initialize vedio and sound systems
  def set_pygame(self):
    pygame.init()
    self.screen = pygame.display.set_mode((self.s_w, self.s_h))
    self.clock = pygame.time.Clock()
    pygame.mixer.init()
    self.sound = pygame.mixer.Sound("beeb.wav")    

  #the first scrren in the game, designed to take player option
  def is_host(self, message):
    font = pygame.font.Font(None, self.s_w//30)
    
    host_option = font.render("To be the host of the game open Hotspot then press 'h'", True, TEXT_COLOR)
    guest_option = font.render("To be the guest of the game connect to host then press 'g'", True, TEXT_COLOR)
    
    
    self.screen.fill(BG_COLOR) #becasue it can be called multiple times until connections succeed
    
    
    self.screen.blit(host_option, (self.s_w//2 - host_option.get_width()//2, self.s_h*.2))
    self.screen.blit(guest_option, (self.s_w//2 - guest_option.get_width()//2, self.s_h*.3))
    
    if message:
      message_text_surface = font.render(message, True, TEXT_COLOR) 
      self.screen.blit(message_text_surface, (self.s_w//2 - message_text_surface.get_width()//2, self.s_h*.5))
    
    developer_message = font.render("Developed by: Ammar Hussein :)", True, TEXT_COLOR) 
    self.screen.blit(developer_message, (self.s_w//2 - developer_message.get_width()//2, self.s_h*.9))
    
    pygame.display.flip()
    
    # getting the option from the player
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          if self.player.is_host: self.exit()
          
        elif event.type == pygame.KEYDOWN:
          if event.unicode == "h" or event.unicode == "H": # H stands for "Host"
            return True
        
          elif event.unicode == "g" or event.unicode == "G": # G stands for "Guest"
            return False
  
  #connect the player to the given host ip and run the server if the user is the Host
  def connect_player(self, host_ip): 
    try:
      self.player.connect(host_ip)
    except OSError as e:
      print(f"Failed to connect to {host_ip}")
      print(e)
      
      if self.player.is_host:
        message = "Make sure the wifi Hotspot is opened in your device."
        print(message)
      
      else:
        message = "Make sure you are connected to wifi Hotspot and the host has joined the game."
        print(message)
      
      return False, message
    
    else:
      return True, "Let's GO!!!"

  #get inputs (right and left movements) from the user and send them to the server
  #it works in a seperate thread
  def send_moves(self):
    try:
      while True:
        for event in pygame.event.get():
          if event.type == pygame.QUIT: self.exit()
        
        keys = list(pygame.key.get_pressed())
        
        if keys[79]:
          self.player.move(1)

        elif keys[80]:
          self.player.move(-1)
          
        sleep(1/60)
        
    except pygame.error: # when pygame closed
      return
      
  # display the result of the round and the session
  def show_result(self, player):
    result = "Player1 Win!!" if player == "1" else "Player2 Win!!"
    
    # preparing fonts
    font1 = pygame.font.Font(None, self.s_w//15) # for result
    font2 = pygame.font.Font(None, self.s_w//30) # for continue or exit options
    
    # preparing text surfaces
    winner_message = font1.render(result, True, TEXT_COLOR)
    restart_option = font2.render("To restart the game the host must press \"Enter\"", True, TEXT_COLOR)
    close_option = font2.render("To Exit the game the host must press \"Shift\"", True, TEXT_COLOR)
    
    # result rect dimensions calculation and creation
    text_height_sum = winner_message.get_height() + restart_option.get_height() + close_option.get_height()
    maximum_width = max(winner_message.get_width(), restart_option.get_width(), close_option.get_width())
    
    result_rect = pygame.Rect(self.s_w//2 - maximum_width*3//4 , self.s_h//2 - text_height_sum, maximum_width*3//2, text_height_sum*2 + winner_message.get_height()-restart_option.get_height())
    
    # result drawing and blitting
    pygame.draw.rect(self.screen, TEXT_COLOR, result_rect, 2)
    
    self.screen.blit(winner_message, (result_rect.x + (result_rect.w-winner_message.get_width())//2, result_rect.y + text_height_sum//2 - winner_message.get_height()//2))
    self.screen.blit(restart_option, (result_rect.x + (result_rect.w-restart_option.get_width())//2, result_rect.y + text_height_sum + winner_message.get_height()//2 - restart_option.get_height()//2))
    self.screen.blit(close_option, (result_rect.x + (result_rect.w-close_option.get_width())//2, result_rect.y + text_height_sum*3/2 + winner_message.get_height()//2 - close_option.get_height()//2))
    
    pygame.display.flip()

  #get host decision (to continue or to exit)
  def decide_if_to_continue(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: self.exit()
        
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN: # means ENTER has been pressed
            # restart the game
            self.player.server.restart()
            return
          if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
            self.exit()

 
  # to exit the game
  def exit(self):
    if self.player.is_host and self.player.server: #close the server if the player is the host
      self.player.server.close_server()
    
    pygame.quit() # close pygame
    sys.exit("See you soon!") # close the app
  
  
  # it will be used in online mode in future   
  # def get_host_ip(self):
  #   font = pygame.font.Font(None, self.s_w//30)
  #   prompt = font.render("Please write down the host ip in the field below, type enter when you finish:", True, (255, 255, 255))
    
  #   rect = pygame.Rect(self.s_w*.3, self.s_h*.4, self.s_w*.1, self.s_h*.1)
    
  #   host_ip = ""
    
  #   while True:
  #     for event in pygame.event.get():
  #       if event.type == pygame.QUIT:
  #         if self.player.is_host: self.exit()
  #       elif event.type == pygame.KEYDOWN:
  #         if event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] or (event.unicode == "." and host_ip[-1]!= "."):
  #           host_ip += event.unicode
  #         elif event.key == pygame.K_BACKSPACE:
  #           host_ip = host_ip[:-1]
  #         elif event.key == pygame.K_RETURN:
  #           return host_ip
      
  #     self.screen.fill(BG_COLOR)
      
  #     self.screen.blit(prompt, (self.s_w//2 - prompt.get_width()//2, self.s_h*.2))
  #     host_text = font.render(host_ip, True, (255, 255, 255))
  #     self.screen.blit(host_text, (rect.x + rect.w//4, rect.y + rect.h//2 - host_text.get_height()//2))
  
  #     width = max(host_text.get_width() + rect.w*.5 + 10, self.s_w/10)
  #     rect.w = width
  #     pygame.draw.rect(self.screen, TEXT_COLOR, rect, 2)
      
  #     pygame.display.flip()