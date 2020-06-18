#game_functions
import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, stats, ship, ai_settings, screen, bullets, aliens, sb): #parameter bullets have to come at the end as its dependent on screen and ai_settings
	"""when the key is pressed"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True #here its ship. not self. since we are not defining modules within class and the parameter is ship here
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True	
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_p:
		if not stats.game_active:
			ai_settings.initialize_dynamic_settings()
			start_game(stats, bullets, ai_settings, screen, aliens, ship, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
	if len(bullets) < ai_settings.bullets_allowed: # if the len of the bullet is less than 3 in this case, new bullet will be made
		new_bullet = Bullet(ai_settings, screen, ship)#creating a new instance using Bullet Class
		bullets.add(new_bullet) #bullets is a group to contain the bullets, we are now adding 'new_bullet'

		
def check_keyup_events(event, ship):
	"""when the key is released"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False
		

def check_events(ai_settings, screen, stats, play_button, ship, bullets, aliens, sb): #parameter is ship beacuse all the events check is for the ship
	"""Watch for keyboard and mouse events"""
	for event in pygame.event.get(): #this line specifies where event comes from hence the method does not include the event parameter
		if event.type == pygame.QUIT:
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, stats, ship, ai_settings, screen, bullets, aliens, sb)#this method now has more parameters
		
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos() # we don't need to define mouse_x and y in the method parameter since we made the variable here
			check_play_button(ai_settings, screen, ship, aliens, bullets, stats, play_button, mouse_x, mouse_y, sb)
			
def check_play_button(ai_settings, screen, ship, aliens, bullets, stats, play_button, mouse_x, mouse_y, sb):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		start_game(stats, bullets, ai_settings, screen, aliens, ship, sb)

def start_game(stats, bullets, ai_settings, screen, aliens, ship, sb):
	pygame.mouse.set_visible(False) #the line above is if clicked. then we make cursor invisible in this line
	stats.reset_stats()
	stats.game_active = True
	
	sb.prep_score()# we are updating the score images after we have reset the stats
	sb.prep_high_score()# not here that the high score is not in reset but in init(), so this stats wont get reset
	sb.prep_level()
	sb.prep_ships()
		
	aliens.empty()
	bullets.empty()
	create_fleet(ai_settings, screen, aliens, ship)
	ship.center_ship()	

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb): #need the group parameter bullets
	#these are moved from the alien_invasion.py 
	bullets.update() #cut from alien_invasion.py, this function is calling for each sprite in the group which has the bullet class and the update is a method in it, it updates the bullets movement
	
	for bullet in bullets.copy(): #call copy because we dont want to alter the actual group
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score() # this method is to update the score number where as in update screen the show_score is to draw the score on screen
		check_high_score(stats, sb)
		
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level() # create the image and update it 
		
		create_fleet(ai_settings, screen, aliens, ship)

def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
	
				
#IMPORTANT, THE PARAMETER ORDER SHOULD MATCH THE OPERATION ORDER INSIDE IN, OTHERWISE WE WILL GET ATTRIBUTE ERROR
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb): #the last parameter here is not neccessarily to change as it is only the name, it will be the same if it is zoro instead when applied tihs function to alien_invasion
	"""
	As the following attributes suggested. It has 3 parameteres
	screen being the background, a parametere to update the screen
	ai_settings being the screen settings as it has the Settings() attribute which includes sizes of screen
	ship being the ship, in this case it is being drawn
	fillings the screen with a colour
	""" 

	screen.fill(ai_settings.bg_colour)
	ship.blitme()#This comes after we fill the screen, drawing of ship
	aliens.draw(screen) # not blit but draw since we need draw every sprite in the group
	for bullet in bullets.sprites(): # .sprites() return of all sprites in a group as a list
		bullet.draw_bullet() # the method found in bullet class 
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	
# Make the most recently drawn screen visible.
	pygame.display.flip()

def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites(): #for each alien in the group if the method check edges in alien class is true
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens) # we change fleet direction which is defined below
			break #break once it has been activated once until next time edges is touched
			
def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1  
	
	
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
	if stats.ships_left > 0:
		stats.ships_left -= 1
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings, screen, aliens, ship)
		ship.center_ship()	
		sleep(0.5)
	
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)# we show cursor after all ships are destroyed

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
			break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
	check_fleet_edges(ai_settings, aliens)
	aliens.update() #aliens instead of alien here because aliens is a group that contains all instance of alien class which have the alien class attribute.
	
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
		
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)
	

def get_number_aliens_x(ai_settings, alien_width): #just a long equation we will reference later
	"""alien_width is used here to represent the width but we cannot use alien.rect.width here since we have not make an instance of alien here"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, alien_height, ship_height):
	available_space_y = (ai_settings.screen_height -
							(3*alien_height) - ship_height)
	number_rows = int(available_space_y/(2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""create an alien and determine its location in the row and then adding it to the group"""
	alien = Alien(ai_settings, screen)# this alien is only to get the information of the structure we want and hence not be in the for loop for adding alien to the group
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number # first alien index=0 so the coordinate is alien_width, second alien index=1 so it will be 3 alien_width (including spacing between aliens)
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
	
def create_fleet(ai_settings, screen, aliens, ship): #parameter here is aliens because we are dealing with the whole group
	alien = Alien(ai_settings, screen)# this alien is only to get the information of the structure we want and hence not be in the for loop for adding alien to the group
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)# we hav created the alien instance, hence we replace the alien_width variable as alien.rect.width
	number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
	
	
	#creating first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x): # repeating this for loop up to number of aliens we want to make defined above
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

		
