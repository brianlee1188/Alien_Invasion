import json
from pathlib import Path

class GameStats():
	
	def __init__(self, ai_settings):
		self.ai_settings = ai_settings
		self.reset_stats()
		filename = Path('high_score.json')
		if filename.is_file():	
			with open(filename) as f_obj2:
				self.high_score = json.load(f_obj2)
		else:
			self.high_score = 0

		self.game_active = False # this will put the game to false to begin with
		
	def reset_stats(self):
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
