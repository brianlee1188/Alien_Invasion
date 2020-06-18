import game_functions as gf 
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
# Initialize game and create a screen object.
	pygame.init()
	ai_settings = Settings() 
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
		

#Make a ship
	ship = Ship(screen, ai_settings) #outside of while loop so we dont make a ship every time, note here the parameter screen we are drawing on top is already defined above

#Group to store bullet
	bullets = Group() # a group class attribute stored as the name bullets
	
#Group to store aliens
#this function includes the append function of alien into the aliens group which is why it is a parameter
	aliens = Group()
	gf.create_fleet(ai_settings, screen, aliens, ship) # dependent on ship too because our rows coordinates was dependent on ship as well.

# Start the main loop for the game. While true, every indented code will be in loop
	while True:
		
		play_button = Button(ai_settings, screen, "Play")
		
		gf.check_events(ai_settings, screen, stats, play_button, ship, bullets, aliens, sb)
		
		if stats.game_active:
			ship.update() #this module is now to 'move' the ship
			gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)
			
		gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb)# all these parameteres will be shown on screen
		
		
run_game()

