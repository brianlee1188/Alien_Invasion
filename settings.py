#Setting class
class Settings():
	"""Setting class to store settings for Alien_invasion"""
	
	def __init__(self):
		"""game's settings including width, height and background colour"""
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_colour = (230, 230, 230)
		 # reason why we put the ship speed here is the same idea as we adjust our cursor speed in game settings
		self.ship_limit = 3
		
		#bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_colour = 60, 60, 60
		self.bullets_allowed = 3
		
		#alien speed settings
		self.fleet_drop_speed = 10
		
				
		self.speed_up_scale = 1.1
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		self.ship_speed = 1.5
		self.bullet_speed_factor = 1.5
		self.alien_speed_factor = 1.5
		self.fleet_direction = 1
		self.alien_points = 50
	
	def increase_speed(self):
		self.ship_speed *= self.speed_up_scale 
		self.bullet_speed_factor *= self.speed_up_scale 
		self.alien_speed_factor *= self.speed_up_scale
		self.alien_points = int(self.alien_points * self.score_scale) 
