"""Some simple skeleton code for a pygame game/animation

This skeleton sets up a basic 800x600 window, an event loop, and a
redraw timer to redraw at 30 frames per second.
"""
from __future__ import division
import math
import sys
import pygame
import random


class User(object):
	(INITIATE,LEFT,RIGHT) = (0,1,2)
	def __init__(self):
		self.user_car = pygame.image.load('F1 Car.png')
		self.car_x = (336)
		self.car_y = (600 - 160)  
		self.cdelta_x = 100  #Increment by which the car will move
		self.state = self.INITIATE
		
	def u_draw(self,screen):
		self.rect = self.user_car.get_rect()
		self.rect = self.rect.move(self.car_x, self.car_y)
		
		screen.blit(self.user_car,self.rect)
		
class Traffic(object): #oncoming cars
	def __init__(self, img_file, get_x):
		self.car1 = pygame.image.load(str(img_file))
		self.t_x = int(get_x)
		self.t_y = (-128)
		self.tdelta_y = 10
		
	def t_draw(self,screen):
		self.t_rect = self.car1.get_rect()
		self.t_rect = self.t_rect.move(self.t_x, self.t_y)
		
		screen.blit(self.car1,self.t_rect) 
			

class MyGame(object):
	def __init__(self):
		"""Initialize a new game"""
		pygame.mixer.init()
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()
		
		
		self.sound_tires = pygame.mixer.Sound('tires.mp3')#http://soundbible.com/1178-Tires-Squealing.html
		self.sound_crash = pygame.mixer.Sound('crash.mp3')#http://soundbible.com/1757-Car-Brake-Crash.html
		self.sound_loop = pygame.mixer.Sound('loop.wav')
		
		
		# set up a 640 x 480 window
		self.width = 800
		self.height = 600
		self.screen = pygame.display.set_mode((self.width, self.height))

		# use a black background
		self.bg_color = 0, 0, 0
		self.shoulder_color = 205,133,63
		self.red = (255, 0, 0)
		
		self.font1 = pygame.font.Font('airstrikelaser.ttf', 100)
		self.font2 = pygame.font.Font('airstrike.ttf', 40)
		
		self.U_car = User()
		self.T_car1 = Traffic('bcar.png',128)
		
		# self.u_rect = self.U_car.user_car.get_rect()                       #MAKE rectangles for the two cars
		# self.u_rect = self.u_rect.move(self.U_car.car_x, self.U_car.car_y) #For the collision of the two rectangles
		# self.t_rect = self.T_car1.car1.get_rect()
		# self.t_rect = self.t_rect.move(self.T_car1.t_x, self.T_car1.t_y)

		
		
		#Resources:		
		self.ddelta_y = 15 #Lane divider increment
		self.divider_y = (-100)
		
		self.g_state = 'START'
		self.r_state = 'RUN'
		
		self.counter = 0
		self.score = 0
		self.lives = 4
		

		# Setup a timer to refresh the display FPS times per second
		self.FPS = 30
		self.REFRESH = pygame.USEREVENT+1
		pygame.time.set_timer(self.REFRESH, 1000//self.FPS)


	def run(self):
		"""Loop forever processing events"""
		
		running = True
		while running:
			event = pygame.event.wait()

			# player is asking to quit
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and self.U_car.car_x <= (self.width-278): 
					self.U_car.car_x += self.U_car.cdelta_x
				
			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and self.U_car.car_x > (150):
					self.U_car.car_x -= self.U_car.cdelta_x
					
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
					self.g_state = 'PLAY'
					
			
			# time to draw a new frame
			elif event.type == self.REFRESH:
				self.draw()
				
			else:
				pass # an event type we don't handle			

	def draw(self):
		"""Update the display"""
		# everything we draw now is to a buffer that is not displayed
		self.screen.fill(self.bg_color)
		
		self.u_rect = self.U_car.user_car.get_rect()                       #MAKE rectangles for the two cars
		self.u_rect = self.u_rect.move(self.U_car.car_x, self.U_car.car_y) #For the collision of the two rectangles
		self.t_rect = self.T_car1.car1.get_rect()
		self.t_rect = self.t_rect.move(self.T_car1.t_x, self.T_car1.t_y)
		
		self.counter += 1   
		
		if self.g_state == "START": #Game start screen
			self.score = 0
			self.lives = 4
			self.counter = 0     #reset stats
			self.ddelta_y = 15
			self.T_car1.tdelta_y = 10    #resetting all the speed increments
		
			left_shoulder = pygame.draw.rect(self.screen, self.shoulder_color, (0,0,150,self.height))  #these are the borders of the road
			right_shoulder = pygame.draw.rect(self.screen, self.shoulder_color, (self.width-150,0,150,self.height))
			
			Title = self.font1.render("Desert Racer", True, self.red)
			txt_rect = Title.get_rect()
			txt_rect = txt_rect.move((self.width//2)-(txt_rect.width)//2, 
				(self.height//2)-(txt_rect.height//2))
				
			Subtitle = self.font2.render("Press the UP key to start", True, self.red)
			stxt_rect = Subtitle.get_rect()
			stxt_rect = stxt_rect.move((self.width//2)-(stxt_rect.width)//2, 
				(self.height//2)+(stxt_rect.height))
			
			self.screen.blit(Title, txt_rect)
			self.screen.blit(Subtitle, stxt_rect)
		
		
		
		elif self.g_state == "PLAY": #gameplay		
			
			self.sound_loop.play()
		
			if self.counter % 30 == 0:    #every second
				self.score += 10         #adds 100 score
				
			if self.counter %600 == 0:   #every 20 seconds
				self.ddelta_y += 20      #makes car faster
				self.T_car1.tdelta_y +=15 #makes traffic faster
				
			if self.lives == 0:
				self.g_state = 'END'  #When lives are spent
				
				
				
			if self.U_car.state == 0: #Straight
				self.U_car.car_x = self.U_car.car_x
				self.U_car.car_y = self.U_car.car_y
				
				
			if self.U_car.state == 1: #right
				self.U_car.car_x += self.U_car.cdelta_x
			
			if self.U_car.state == 2: #left
				self.U_car.car_x -= self.U_car.cdelta_x
				
			
			if self.u_rect.colliderect(self.t_rect) == True: #when the two rects collide
					self.sound_tires.play()                  
					self.lives -= 1
					self.T_car1.t_y = (-150)
						
			left_shoulder = pygame.draw.rect(self.screen, self.shoulder_color, (0,0,150,self.height))
			right_shoulder = pygame.draw.rect(self.screen, self.shoulder_color, (self.width-150,0,150,self.height))
			
			divider = pygame.draw.rect(self.screen, (255,255,255), (self.width//2-10,self.divider_y,20,150))
			
			
			
			if self.r_state == 'RUN':     #The divider moves, making the car "move"
				self.divider_y += self.ddelta_y
				self.T_car1.t_y += self.T_car1.tdelta_y
				
				if self.T_car1.t_y >= self.height:
					self.T_car1.t_y = (-128)
					self.T_car1.t_x = random.randint(150,self.width-278)  #random traffic
			
			if self.divider_y >= self.height:
				self.divider_y = (-100)
			
			
			#FOLLOWING IS JUST SCREEN STUFF
			
			scoreTitle = self.font2.render('SCORE:', True, self.red) #SCORE title
			sct_rect = scoreTitle.get_rect()
			sct_rect = sct_rect.move((self.width)-(sct_rect.width), 0)
			
			livesTitle = self.font2.render('LIVES: ', True, self.red) #LIVES title
			lvt_rect = livesTitle.get_rect()
			lvt_rect = lvt_rect.move(0,0)
			
			Score = self.font2.render(str(self.score), True, self.red)  #Score display
			score_rect = Score.get_rect()
			score_rect = score_rect.move((self.width)-(score_rect.width), (score_rect.height))
			
			Lives = self.font2.render(str(self.lives), True, self.red) #lives display
			lives_rect = Lives.get_rect()
			lives_rect = lives_rect.move(0, (lives_rect.height))
			
			self.screen.blit(livesTitle, lvt_rect)
			self.screen.blit(Lives, lives_rect)
			
			self.screen.blit(scoreTitle, sct_rect)
			self.screen.blit(Score, score_rect)
			
			self.U_car.u_draw(self.screen)
			self.T_car1.t_draw(self.screen)
			
		elif self.g_state == 'END': #lives spent
			
			self.sound_crash.play()
			
			Endtitle = self.font2.render('GAME OVER', True, self.red)
			etxt_rect = Endtitle.get_rect()
			etxt_rect = etxt_rect.move((self.width//2) -(etxt_rect.width)//2,
				(self.height//2)+(etxt_rect.height))
				
			self.screen.blit(Endtitle, etxt_rect)
			
			if self.counter%120 == 0:
				self.g_state = 'START'
			
		

		# flip buffers so that everything we have drawn gets displayed
		pygame.display.flip()


MyGame().run()
pygame.quit()
sys.exit()

