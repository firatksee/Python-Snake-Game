import os
from time import *
from pynput import keyboard
import threading
from random import randint

headDirectx = 0
headDirecty = 0
snakeBody = [[5,5],[4,5],[3,5],[2,5],[1,5]]
headPos = snakeBody[0]
snakeSize = len(snakeBody)

HEIGHT = 21
WIDTH = 77



def foodGen():
	while True:
		foodx = randint(1, WIDTH - 2)
		foody = randint(1, HEIGHT - 2)

		if not [foodx,foody] in snakeBody and foodx % 2 == headPos[0] % 2:
			break
	return [foodx,foody]


foodPos = foodGen()
score = 0
highScore = 0

gameOn = True

def readHighScore():
	global highScore
	with open("BasicSnakeGameDB.txt","r") as file:
		highScore = int(file.readline())



def gameBoard():
	for y in range(HEIGHT):
		for x in range(WIDTH):
			if x == 0 or x == WIDTH - 1:
				print("*", end = "")
			elif (y == 0 or y == HEIGHT - 1) and x % 2 == 0:
				print("*", end = "")
			elif [x,y] in snakeBody:
				print("■", end = "")
			elif [x,y] == foodPos:
				print("●", end = "")
			else:
				print(" ", end = "")
		print("")
	print("Score: {}".format(score))
	print("High Score: {}".format(highScore))

	sleep(15/1000)
	os.system("cls" if os.name in ('nt', 'dos') else "clear")
	

def controller():
	
	def on_press(key):
		global headDirectx
		global headDirecty
		try:
			if key.char == 'w' and headDirecty != 1:
				headDirecty = -1
				headDirectx = 0
			elif key.char == 's' and headDirecty != -1:
				headDirecty = 1
				headDirectx = 0
			elif key.char == 'd' and headDirectx != -2:
				headDirecty = 0
				headDirectx = 2
			elif key.char == 'a' and headDirectx != 2:
				headDirecty = 0
				headDirectx = -2

		except: 
			if key == keyboard.Key.up and headDirecty != 1:
				headDirecty = -1
				headDirectx = 0
			elif key == keyboard.Key.down and headDirecty != -1:
				headDirecty = 1
				headDirectx = 0
			elif key == keyboard.Key.right and headDirectx != -2:
				headDirecty = 0
				headDirectx = 2
			elif key == keyboard.Key.left and headDirectx != 2:
				headDirecty = 0
				headDirectx = -2
			elif key == keyboard.Key.space:
				headDirecty = 0
				headDirectx = 0
		

	with keyboard.Listener(on_press=on_press) as listener:
	    listener.join()

	listener = keyboard.Listener(on_press=on_press)
	listener.start()



def update():
	global foodPos
	global snakeSize
	global score
	global gameOn

	if headDirectx != 0 or headDirecty != 0:
		for i in range(snakeSize - 1, 0, -1):
			snakeBody[i][0] = snakeBody[i-1][0]
			snakeBody[i][1] = snakeBody[i-1][1]

		headPos[0] += headDirectx
		headPos[1] += headDirecty

		if headPos[0] >= WIDTH - 1:
			headPos[0] = 1
		elif headPos[0] <= 0:
			headPos[0] = WIDTH - 2 
		if headPos[1] >= HEIGHT - 1:
			headPos[1] = 1
		elif headPos[1] <= 0:
			headPos[1] = HEIGHT - 2

		# food eaten
		if headPos == foodPos:
			foodPos = foodGen()
			snakeBody.append([0,0])
			snakeSize = len(snakeBody)
			score += 1

		# game over
		if headPos in snakeBody[1:]:
			gameOn = False




def gamePlay():
	global gameOn
	global score
	global highScore

	while gameOn:
		gameBoard()
		update()

	print("Game Over!\nScore: {}".format(score))

	if score > highScore:
		with open("BasicSnakeGameDB.txt","w") as file:
			file.write(str(score))
			print("New High Score! Congrats!")
	else:
		print("High Score: {}".format(highScore))



thread_one = threading.Thread(target = controller)
thread_two = threading.Thread(target = gamePlay)

if __name__ == "__main__":
	readHighScore()
	thread_one.start()
	thread_two.start()
