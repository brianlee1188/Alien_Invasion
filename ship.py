#Ship Class
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, screen, ai_settings): # two parameters, the ship self reference and the place it will be drawn on, in tihs case the screen.
		"""load the ship's image as well as set its starting position"""
		super().__init__()
		self.screen = screen
		
		#load the ship image and get its rect
		self.image = pygame.image.load('images/ship.bmp') #pygame.image.load is method to load images
		self.rect = self.image.get_rect() #getting rect attributes of self.image which is the ship in this case
		self.screen_rect = screen.get_rect() #only screen.get_rect() because the screen is already determined in settings
		self.ai_settings = ai_settings # we add this attribute to have access to settings class attribute which includes the ship speed factor
		
		#start at bottom center
		self.rect.centerx = self.screen_rect.centerx 
		self.rect.bottom = self.screen_rect.bottom
		
		self.center = float(self.rect.centerx)#storing the center of the image in a new variable so it can accept float value
		
		self.moving_right = False
		self.moving_left = False
	

	
	def update(self):
		"""Moving of ship"""
		if self.moving_right and self.rect.right < self.screen_rect.right: #added
			self.center += self.ai_settings.ship_speed 
		if self.moving_left and self.rect.left > self.screen_rect.left: #if this is true
			self.center -= self.ai_settings.ship_speed 
		
		self.rect.centerx = self.center #this is to update self.rect.centerx after all the moving since self.rect.centerx this code represents and control the location of the image ship
			
	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image, self.rect) #can be interpreted as drawn on screen is the self.image(the ship) with respect to its coordination (self.rect)
		
	def center_ship(self):
		self.center = self.screen_rect.centerx #self center here since we defined it in init()
