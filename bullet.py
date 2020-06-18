import pygame
from pygame.sprite import Sprite #the Sprite class

class Bullet(Sprite): #inheriting parent class which is a group element
	def __init__(self, ai_settings, screen, ship):# ai settings as parameter for sizes of bullet
		super().__init__()
		self.screen = screen
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
			
		#location of where bullet will be
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		#Specs of bullet
		self.y = float(self.rect.y) #saving as a float for more refined movement for all y coordinates
		self.colour = ai_settings.bullet_colour
		self.speed_factor = ai_settings.bullet_speed_factor
	
	def update(self):
		self.y -= self.speed_factor
		self.rect.y = self.y
	
	def draw_bullet(self):
		"""draw the bullet to the screen"""
		pygame.draw.rect(self.screen, self.colour, self.rect) 
		
		
		
