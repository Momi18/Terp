from tkinter import *
import tkinter.messagebox as messagebox
import pygame
import sqlite3

import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import time


"""This is the code for the login/signup screen"""

#This checks if there is a userdata database.
con = sqlite3.connect("userdata.db")
cre = con.cursor()

cre.execute("""
CREATE TABLE IF NOT EXISTS userdata (
  id INTEGER PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
)
""")

pygame.init()

#Creates the tkinter window
window = Tk()
window.title("Terp")
window.geometry("600x400")

#This is a simple and insecure hashing algorithm
def hash(password1):
    hvalue = 0

    for char in password1:
        hvalue = (hvalue + ord(char)) * 10

    return hvalue

#But I created a recursive multi-layered hash function to make it more secure
def mhash(password1, rounds=3):
    if rounds == 0:
        return password1.encode('utf-8')
    else:
        havalue = hash(str(mhash(password1, rounds - 1)))
        return havalue


#Finds the username in the database
def search(username1):
    cre.execute("SELECT * FROM userdata WHERE username=?", (username1,))
    r = cre.fetchone()
    return r is not None

#Created a function to destroy the buttons, saves time.
def destroy():
    btn.destroy()
    btn1.destroy()

#Checks the users inputted details when they are signing up.
def signup():
    if not UserEnt.get() or not PassEnt.get() or not RPasEnt.get():
        messagebox.showerror("Error", "Username and passwords cannot be empty.")
    elif PassEnt.get() == RPasEnt.get():
        username1,password1 = UserEnt.get(), mhash(PassEnt.get())
        cre.execute("INSERT INTO  userdata(username, password) VALUES(?,?)",(username1, password1))
        con.commit()
        messagebox.showinfo("Success", "Account created")
        log()
        #Sends the user to the login screen so that they can log in.
    else:
        messagebox.showerror("Error", "Passwords dont match.")

#Checks the users inputted details when they are logging in.
def login():
    global username1
    username1 = UserEnt.get()
    password1 = mhash(PassEnt.get())
    if not username1 or not password1:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return
    if search(username1):
        cre.execute("SELECT * FROM userdata WHERE username=? AND password=?", (username1, password1))
        result = cre.fetchone()
        if result:
            messagebox.showinfo("Login successful", "Welcome!")
            window.destroy()
            #Send the user to the game
        else:
            messagebox.showerror("Login error", "Invalid username or password")
    else:
        messagebox.showerror("Login error", "Invalid username or password")


frame = Frame()

def log():
	destroy()
	btn2 = Button(frame, text="Back", bg="white", fg="black", command=LS)
	btn2.grid(column=0, row=3)
	global UserEnt, PassEnt
	#Creates the variables of each button and textbox.
	LogLab = Label(frame, text="Login", font=("Arial, 30")) 
	UserLab = Label(frame, text="Username", font=("Arial, 13"))
	UserEnt = Entry(frame, font=("Arial, 13"))
	PassLab = Label(frame, text="Password", font=("Arial", 13))
	PassEnt = Entry(frame, show="*", font=("Arial, 13"))
	LogBut = Button(frame, text="Login", font=("Arial", 13), command=login)
	#When you click log in, it will send you to the log in screen.

	#This displays all the buttons and textboxes and texts.
	LogLab.grid(row=0, column=0, columnspan=2, sticky="news", pady=25)
	UserLab.grid(row=1, column=0)
	UserEnt.grid(row=1, column=1, pady=10)
	PassLab.grid(row=2,column=0)
	PassEnt.grid(row=2, column=1, pady=10)
	LogBut.grid(row=3, column=0, columnspan=2, pady=20)

def sign():
	destroy()
	btn2 = Button(frame, text="Back", bg="white", fg="black", command=LS)
	btn2.grid(column=0, row=4)
	global UserEnt, PassEnt, RPasEnt
	#Creates the variables of each button and textbox.
	SignLab = Label(frame, text="Sign up", font=("Arial, 30"))
	UserLab = Label(frame, text="Username", font=("Arial, 13"))
	UserEnt = Entry(frame, font=("Arial, 13"))
	PassLab = Label(frame, text="Password", font=("Arial", 13))
	PassEnt = Entry(frame, show="*", font=("Arial, 13"))
	RPasLab = Label(frame, text="Confirm Password", font=("Arial", 13))
	RPasEnt = Entry(frame, show="*", font=("Arial, 13"))
	SignBut = Button(frame, text="Sign up", font=("Arial", 13), command=signup)
	#When you click sign up, it will send you to the sign up screen.

	#This displays all the buttons and textboxes and texts.
	SignLab.grid(row=0, column=0, columnspan=2, sticky="news", pady=25)
	UserLab.grid(row=1, column=0)
	UserEnt.grid(row=1, column=1, pady=10)
	PassLab.grid(row=2,column=0)
	PassEnt.grid(row=2, column=1, pady=10)
	RPasLab.grid(row=3,column=0)
	RPasEnt.grid(row=3, column=1, pady=10)
	SignBut.grid(row=4, column=0, columnspan=2, pady=20)

def LS():
	global btn, btn1
	#Creates and displatys the beginning screen buttons.
	btn = Button(frame, text="Login", bg="white", fg="violet", command=log)
	btn.grid(column=1, row=0, pady=25)
	btn1 = Button(frame, text="sign up", bg="white", fg="violet", command=sign)
	btn1.grid(column=1, row=2)

frame.pack()
LS()
window.mainloop()





"""This is the code for the actual game"""




#This checks if there is a leaderboard database.
con = sqlite3.connect("leaderboard.db")
cre = con.cursor()

cre.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
  id INTEGER PRIMARY KEY,
  username1 VARCHAR(255) NOT NULL,
  real_score VARCHAR(255) NOT NULL
)
""")

#Inserts the user's username and score into the database when called.
def leader_update(real_score, username1):
	leader, username1 = real_score, username1
	cre.execute("INSERT INTO  leaderboard(real_score, username1) VALUES(?,?)",(leader, username1))
	con.commit()

#Sorts the scores using merge sort.
def sort(arr):
    if len(arr) > 1:
        middle = len(arr) // 2
        right = arr[middle:]
        left = arr[:middle]

        sort(left)
        sort(right)

        p = q = r = 0

        while p < len(left) and q < len(right):
            if float(left[p][2]) > float(right[q][2]):
                arr[r] = left[p]
                p += 1
            else:
                arr[r] = right[q]
                q += 1
            r += 1

        while p < len(left):
            arr[r] = left[p]
            p += 1
            r += 1

        while q < len(right):
            arr[r] = right[q]
            q += 1
            r += 1

#Gets the leaderboard and everything inside it into a variable, 
cre.execute("SELECT * FROM leaderboard")
leadersort = cre.fetchall()

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

fps = 60
clock = pygame.time.Clock()

#Declaring the windows height and width
windowh = 1000
windoww = 1000

#Declaring the window as a variable
window = pygame.display.set_mode((windoww, windowh)) #, pygame.RESIZABLE
#Name of the window
pygame.display.set_caption('Terp')
pic = pygame.image.load("img/pic.png")
pygame.display.set_icon(pic)


#Define font and its score
fontsc = pygame.font.SysFont('Bauhaus 93', 30)
fonts = pygame.font.SysFont('Bauhaus 93', 125)
font = pygame.font.SysFont('Bauhaus 93', 70)


#Define game variables
tilesi = 50
lvl = 1
maxlvl = 7
GameOver = 0
score = 0
#This is the score for timer
time_score = 0
#Actual score
real_score = 0
time = 0
menu = True
menu1 = False
control_menu = False
leader_menu = False
character_menu = False
keybind_menu = False
char = 'MaskDude'

#Define colours
blue = (108, 217, 241)
blueShadow = (39, 116, 252)
white = (255, 255, 255)
green = (0, 212, 0)
red = (213, 50, 80)
yellow = (255, 255, 102)
black = (0, 0, 0)
orange = (230, 97, 29)

#Load images
bg = pygame.image.load('img/bg.png')
sun = pygame.image.load('img/sun.png')
exit = pygame.image.load('img/Btns/exitB.png')
start = pygame.image.load('img/Btns/startB.png')
restart = pygame.image.load('img/Btns/restartB.png')
resume = pygame.image.load('img/Btns/resumeB.png')
returnb = pygame.image.load('img/Btns/returnB.png')
leaderb = pygame.image.load('img/Btns/leaderboardB.png')
settingsb = pygame.image.load('img/Btns/settingsB.png')
characterb = pygame.image.load('img/Btns/charactersB.png')
keybindb = pygame.image.load('img/Btns/keybindsB.png')

#Load player buttons
Mask = pygame.image.load('img/Btns/MaskB.png')
Ninja = pygame.image.load('img/Btns/NinjaB.png')
Virtual = pygame.image.load('img/Btns/VirtualB.png')
Dino = pygame.image.load('img/Btns/DinoB.png')

#Function that can be called to write text on the screen.
def text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	window.blit(img, (x, y))

#Draws/Displays the background
def background():
	window.blit(bg, (-600, 0))
	window.blit(sun, (50, 50))

#load sounds (s at the end means sound)
pygame.mixer.music.load('sfx/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
deaths = pygame.mixer.Sound('sfx/game_over.wav')
deaths.set_volume(0.5)
jumps = pygame.mixer.Sound('sfx/jump.wav')
jumps.set_volume(0.5)
coins = pygame.mixer.Sound('sfx/coin.wav')
coins.set_volume(0.5)
wins = pygame.mixer.Sound('sfx/win.mp3')
wins.set_volume(0.5)


#This is a funciton to reset the level when the user gets to the next level.
def next_lvl(lvl):
	player.reset(100, windowh - 130, char)
	coing.empty()
	sawg.empty()
	platformg.empty()
	lavag.empty()
	doorg.empty()
	spikeg.empty()

	#Loads in the data of each level one after another and creates the world
	if path.exists(f'levels/lvl{lvl}'):
		pickles = open(f'levels/lvl{lvl}', 'rb')#rb stands for read binary
		world = pickle.load(pickles)
	world = World(world)
	#Creates a dummy coin for showing the score
	coinsc = Coin(tilesi // 2, tilesi // 2)
	coing.add(coinsc)

	return world

#Function to create and load the buttons and the players actions.
class Button():
	def __init__(self, x, y, image):
		self.img = image
		self.rect = self.img.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.click = False

	def draw(self):
		action = False
		#Gets the mouse position
		pos = pygame.mouse.get_pos()

		#Checks if the user has clicked onto anything.
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
				action = True
				self.click = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.click = False

		#Draws the buttons
		window.blit(self.img, self.rect)

		return action


#Class for the player attributes.
class Player():
	def __init__(self, x, y, char):
		self.reset(x, y, char)

	def update(self, GameOver):
		dx = 0
		dy = 0
		col_thresh = 20
		wcooldown = 5

		if GameOver == 0:
			#Get keyboard inputs from user.
			key = pygame.key.get_pressed()
			if (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) and self.jump == False and self.air == False:
				jumps.play()
				self.vely = -15
				self.jump = True
			if (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) == False:
				self.jump = False
			if (key[pygame.K_LEFT] or key[pygame.K_a]):
				dx -= 5
				self.counter += 1
				self.direction = -1
			if (key[pygame.K_RIGHT] or key[pygame.K_d]):
				dx += 5
				self.counter += 1
				self.direction = 1
			if (key[pygame.K_LEFT] or key[pygame.K_a]) == False and (key[pygame.K_RIGHT] or key[pygame.K_d]) == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.img = self.Rimg[self.index]
				if self.direction == -1:
					self.img = self.Limg[self.index]


			#Handles the animation
			if self.counter > wcooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.Rimg):
					self.index = 0
				if self.direction == -1:
					self.img = self.Limg[self.index]
				if self.direction == 1:
					self.img = self.Rimg[self.index]


			#Implementing the gravity
			self.vely += 1
			if self.vely > 10:
				self.vely = 10
			dy += self.vely

			#Check for collisions
			self.air = True
			for tile in world.tilel:
				#Check for collision in horizontal direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#Check for collision in vertical direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#Check if the player is below the ground, e.g. jumping
					if self.vely < 0:
						dy = tile[1].bottom - self.rect.top
						self.vely = 0
					#Check if the player is above the ground, e.g. falling
					elif self.vely >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vely = 0
						self.air = False

			#Check for collisions with door
			if pygame.sprite.spritecollide(self, doorg, False):
				GameOver = 1

			#Check for collisions with lava
			if pygame.sprite.spritecollide(self, lavag, False):
				GameOver = -1
				deaths.play()

			#Check for collisions with spikes
			if pygame.sprite.spritecollide(self, spikeg, False):
				GameOver = -1
				deaths.play()

			#check for collision with enemies
			if pygame.sprite.spritecollide(self, sawg, False):
				GameOver = -1
				deaths.play()


			#Check for collisions with the platforms
			for platform in platformg:
				#Collision in the horizontal direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#Collision in the vertical direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#Check if the player is below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vely = 0
						dy = platform.rect.bottom - self.rect.top
					#Check if the player is above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.air = False
						dy = 0
					#Moves the player sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.direction


			#Updates the palyers coordinates.
			self.rect.x += dx
			self.rect.y += dy

		#When the user has died, this occurs.
		elif GameOver == -1:
			self.img = self.death
			text('GAME OVER!', font, blueShadow, (windoww // 2) - 175, windowh // 2 - 100)
			text('GAME OVER!', font, blue, (windoww // 2) - 180, windowh // 2 - 100)
			if self.rect.y > 200:
				self.rect.y -= 5

		#Draws the player onto the screen.
		window.blit(self.img, self.rect)

		return GameOver


	def reset(self, x, y, char):
		#Limg for Left images
		#Rimg is for Right images
		self.Rimg = []
		self.Limg = []
		self.index = 0
		self.counter = 0
		for num in range(1, 9):
			Rimg = pygame.image.load(f'img/Entities/Char/{char}/run{num}.png')
			Rimg = pygame.transform.scale(Rimg, (40, 50))
			Limg = pygame.transform.flip(Rimg, True, False)
			self.Rimg.append(Rimg)
			self.Limg.append(Limg)
		self.death = pygame.image.load('img/Entities/Ghost.png')
		self.death = pygame.transform.scale(self.death, (40, 50))
		self.img = self.Rimg[self.index]
		self.rect = self.img.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.img.get_width()
		self.height = self.img.get_height()
		self.vely = 0
		self.jump = False
		self.direction = 0
		self.air = True


#Class for generating the world.
class World():
	def __init__(self, data = 9):
		self.tilel = []

		#load images
		dirt = pygame.image.load('img/Blocks/dirt.png')
		grass = pygame.image.load('img/Blocks/grass.png')

		#row count
		rowc = 0

		for row in data:
			#column count
			colc = 0
			for tile in row:
				#Dirt
				if tile == 1:
					img = pygame.transform.scale(dirt, (tilesi, tilesi))
					ImgRect = img.get_rect()
					ImgRect.x = colc * tilesi
					ImgRect.y = rowc * tilesi
					tile = (img, ImgRect)
					self.tilel.append(tile)
				#Grass
				if tile == 2:
					img = pygame.transform.scale(grass, (tilesi, tilesi))
					ImgRect = img.get_rect()
					ImgRect.x = colc * tilesi
					ImgRect.y = rowc * tilesi
					tile = (img, ImgRect)
					self.tilel.append(tile)
				#Saw
				if tile == 3:
					saw = Enemy(colc * tilesi, rowc * tilesi + 15)
					sawg.add(saw)
				#Platform in horizontal direction
				if tile == 4:
					platform = Platform(colc * tilesi, rowc * tilesi, 1, 0)
					platformg.add(platform)
				#Platform in vertical direction
				if tile == 5:
					platform = Platform(colc * tilesi, rowc * tilesi, 0, 1)
					platformg.add(platform)
				#Lava
				if tile == 6:
					lava = Lava(colc * tilesi, rowc * tilesi + (tilesi // 2))
					lavag.add(lava)
				#Coins
				if tile == 7:
					coin = Coin(colc * tilesi + (tilesi // 2), rowc * tilesi + (tilesi // 2))
					coing.add(coin)
				#Door
				if tile == 8:
					door = Door(colc * tilesi, rowc * tilesi - (tilesi // 2))
					doorg.add(door)
				#Spikes
				if tile == 9:
					spike = Spike(colc * tilesi, rowc * tilesi + (tilesi // 2))
					spikeg.add(spike)
				colc += 1
			rowc += 1

	#Displays the level onto the screen.
	def draw(self):
		for tile in self.tilel:
			window.blit(tile[0], tile[1])


#Class for enemy and its movement
class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/Entities/Saw/off.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direction = 1
		self.move_counter = 0

	#Enemy's movement
	def update(self):
		self.rect.x += self.direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.direction *= -1
			self.move_counter *= -1

#Class for display of coin
class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('img/Entities/Coin/coin1.png')
		self.image = pygame.transform.scale(image, (tilesi // 2, tilesi // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

#Class for platforms
class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('img/Blocks/platW.png')
		self.image = pygame.transform.scale(image, (50, 15))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_counter = 0
		self.direction = 1
		self.move_x = move_x
		self.move_y = move_y

	#Function for platform's movement
	def update(self):
		self.rect.x += self.direction * self.move_x
		self.rect.y += self.direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.direction *= -1 
			self.move_counter *= -1


#Class for display of door
class Door(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('img/Entities/door.png')
		self.image = pygame.transform.scale(image, (tilesi, int(tilesi * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

#Class for display of lava
class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('img/Entities/lava.png')
		self.image = pygame.transform.scale(image, (tilesi, tilesi // 1.75))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

#Class for display of spike
class Spike(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('img/Entities/Spikes/idle.png')
		self.image = pygame.transform.scale(image, (tilesi, tilesi // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

#Declare the player as a variable
player = Player(100, windowh - 130, char)

#g stands for group
lavag = pygame.sprite.Group()
doorg = pygame.sprite.Group()
sawg = pygame.sprite.Group()
platformg = pygame.sprite.Group()
coing = pygame.sprite.Group()
spikeg = pygame.sprite.Group()


#This creates the images as buttons and inupts their postions on the screen.
startbtn = Button(windoww // 2 - 85, windowh // 2 - 25, start)
exitbtn = Button(windoww // 2 - 85, windowh // 2 + 275, exit)
leaderbtn = Button(windoww // 2 - 85, windowh // 2 + 75, leaderb)
settingsbtn = Button(windoww // 2 - 85, windowh // 2 + 175, settingsb)
restartbtn = Button(windoww // 2 - 215, windowh // 2 + 40, restart)
resumebtn = Button(windoww // 2 - 215, windowh // 2 + 40, resume)
returnbtn1 = Button(windoww // 2 + 300, windowh // 2 + 400, returnb)
returnbtn = Button(windoww // 2 + 55, windowh // 2 + 40, returnb)
keybindbtn = Button(windoww // 2 + 55, windowh // 2 + 40, keybindb)
characterbtn = Button(windoww // 2 - 85, windowh // 2 - 60, characterb)

Maskbtn = Button(windoww // 2 - 185, windowh // 2.2 - 25, Mask)
Ninjabtn = Button(windoww // 2 + 140, windowh // 2.2 - 25, Ninja)
Virtualbtn = Button(windoww // 2 - 185, windowh // 1.5, Virtual)
Dinobtn = Button(windoww // 2 + 140, windowh // 1.5, Dino)

#This is the event loop
run = True
while run:
	key = pygame.key.get_pressed()

	#If menu1 is fasle, then the code below is run.
	if not menu1:
		background()
		milli = clock.tick(fps)
		#This is the start menu that checks if use has clicked any buttons.
		if menu == True:
			text("Terp", fonts, blueShadow, windoww // 2 - 115, windowh // 5)
			text("Terp", fonts, blue, windoww // 2 - 120, windowh // 5)
			if startbtn.draw():
				lvl = 1
				#reset level
				world = []
				world = next_lvl(lvl)
				GameOver = 0
				score = 0
				menu = False
			if leaderbtn.draw():
				sort(leadersort)
				leader_menu = True
			if settingsbtn.draw():
				control_menu = True
			if exitbtn.draw():
				run = False

		else:
			world.draw()

			#This is what happens whilst the game is running and the player hasnt won or died.
			if GameOver == 0:
				sawg.update()
				platformg.update()
				seconds = milli/1000.
				time += seconds
				#This is what happens when the user clicks escape to go into menu whilst playing the game.
				if key[pygame.K_ESCAPE]:
					menu1 = True
				#Updates the score
				#Checks if a coin has been collected
				if pygame.sprite.spritecollide(player, coing, True):
					score += 1
					coins.play()
				text('X ' + str(score), fontsc, white, tilesi - 10, 10)
			
			sawg.draw(window)
			platformg.draw(window)
			lavag.draw(window)
			coing.draw(window)
			doorg.draw(window)
			spikeg.draw(window)

			GameOver = player.update(GameOver)

			#This is what happens when the player has died
			if GameOver == -1:
				if restartbtn.draw():
					if score >= 7:
						world = []
						world = next_lvl(lvl)
						GameOver = 0
						score = score - 7
					if lvl == 1:
						world = []
						world = next_lvl(lvl)
						GameOver = 0
						score = 0
					else:
						continue
						# text("Need at least 5 coins", fontsc, white, tilesi + 350, 480)
				elif returnbtn.draw():
					menu = True
				

			#This is what happens when the player has won
			if GameOver == 1:
				#Reset game and go to next level
				lvl += 1
				if lvl <= maxlvl:
					#Reset level
					world = []
					world = next_lvl(lvl)
					GameOver = 0
				else:
					#Update the scores
					time_score = time*10
					real_score = round((time_score-(score*20)), 3)
					wins.play()
					#Display the scores and win screen
					text('YOU WIN!', font, blueShadow, (windoww // 2) - 135, windowh // 2.5)
					text('YOU WIN!', font, blue, (windoww // 2) - 140, windowh // 2.5)
					text('Score: ' + str(real_score), fontsc, blueShadow, tilesi + 379, 500)
					text('Score: ' + str(real_score), fontsc, blue, tilesi + 375, 500)
					if restartbtn.draw():
						lvl = 1
						#Reset level
						world = []
						world = next_lvl(lvl)
						GameOver = 0
						score = 0
						#Updates leaderboard database.
						leader_update(real_score, username1)
					#This button will be used to return to the start screen.
					elif returnbtn.draw():
						menu = True
						#Updates leaderboard database.
						leader_update(real_score, username1)

	#If the settings menu is false (not open), then the code below is run.
	if not control_menu:
		#This is the menu whilst completing the level and checks if user has clicked any buttons.
		if menu1 == True:
			background()
			text("Menu", fonts, blueShadow, windoww // 2 - 145, windowh // 4)
			text("Menu", fonts, blue, windoww // 2 - 150, windowh // 4)
			if resumebtn.draw():
				menu1 = False
			if returnbtn.draw():
				menu1 = False
				menu = True
			if settingsbtn.draw():
				control_menu = True

	#This is the settings menu and checks if user has clicked any buttons.
	if not character_menu or not keybind_menu:
		if control_menu == True:
			background()
			text("Settings", fonts, blueShadow, windoww // 2 - 180, windowh // 5)
			text("Settings", fonts, blue, windoww // 2 - 185, windowh // 5)
			if keybindbtn.draw():
				keybind_menu = True
			if characterbtn.draw():
				character_menu = True
			if resumebtn.draw():
				control_menu = False

	#The leaderboard screen.
	if leader_menu == True:
		#Sorts it from lowest to highest.
		sort(leadersort)
		background()
		text("Leaderboard", fonts, blueShadow, windoww // 2 - 325, windowh // 20)
		text("Leaderboard", fonts, blue, windoww // 2 - 330, windowh // 20)
		u = 10
		for i, data in enumerate(leadersort, start=1):
			username, score = data[1], data[2]
			text(f"{u}. {username}: {score}", fontsc, blueShadow, windoww // 2 - 82, windowh // 1.3 - (i*40))
			text(f"{u}. {username}: {score}", fontsc, blue, windoww // 2 - 87, windowh // 1.3 - (i*40))
			u = u-1
		if returnbtn1.draw():
			leader_menu = False
			menu = True

	#The Character selection screen.
	if character_menu == True:
		background()
		text("Character Select", font, blueShadow, windoww // 2 - 235, windowh // 5)
		text("Character Select", font, blue, windoww // 2 - 240, windowh // 5)
		if Ninjabtn.draw():
			char = str("NinjaFrog")
			Player(100, windowh - 130, char)
			character_menu = False
		if Maskbtn.draw():
			char = str("MaskDude")
			Player(100, windowh - 130, char)
			character_menu = False
		if Virtualbtn.draw():
			char = str("VirtualGuy")
			Player(100, windowh - 130, char)
			character_menu = False
		if Dinobtn.draw():
			char = str("Dino")
			Player(100, windowh - 130, char)
			character_menu = False

	#The Keybinds screen.
	if keybind_menu == True:
		background()
		text("Keybinds", font, blueShadow, windoww // 2 - 145, windowh // 5)
		text("Keybinds", font, blue, windoww // 2 - 150, windowh // 5)
		text("Note: The only keybinds that can be used are:", fontsc, blueShadow, windoww // 2 - 450, windowh // 1.1)
		text("Note: The only keybinds that can be used are:", fontsc, blue, windoww // 2 - 455, windowh // 1.1)
		text("W/[Space]/UpArrow - A/LeftArrow - D/RightArrow", fontsc, blueShadow, windoww // 2 - 450, windowh // 1.05)
		text("W/[Space]/UpArrow - A/LeftArrow - D/RightArrow", fontsc, blue, windoww // 2 - 455, windowh // 1.05)
		if returnbtn1.draw():
			keybind_menu = False
			menu = True

	#If the user exits out the game, then the game stops running.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()