import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self, ai_settings, screen):
		super().__init__() #inheriting parent class
		self.screen = screen
		self.ai_settings = ai_settings
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		#setting location of alien on screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		self.x = float(self.rect.x)
	
	def check_edges(self): #this is not in game_fucntion because every alien sprite should have the ability to check edge
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		if self.rect.left <= screen_rect.left:
			return True
	
	def update(self): #need an update method since the aliens now move
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x
	
	def blitme(self):
		self.screen.blit(self.image, self.rect) #describe what is drawn on screen and the two parameters is whats being drawn and coordindates
		
