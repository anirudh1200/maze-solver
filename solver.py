# Importing necessary libraries
import cv2
import sys
import time
import numpy as np
from queue import Queue
from matplotlib import pyplot as plt

# Loading the image and resizing
img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bwImg = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

# Displaying image
plt.imshow(bwImg, cmap = 'gray')
plt.show()

# Defining various functions
def getStart():
	for i in range(len(maze[0])):
		if maze[0][i] == 255:
			return (0, i)
	print('No start found')

def getEnd():
	for i in range(len(maze[0])):
		if maze[len(maze)-1][i] == 255:
			return (len(maze)-1, i)
	print('No end found')

def reachEnd(path):
	x, y = path[1]
	if(x == endx and y == endy):
		return True
	return False

def isValidPath(path):
	[x, y] = path[1]
	if not(minx<= x < maxx and miny<= y < maxy):
		return False
	elif (maze[x][y] == 0 or maze[x][y] == 50):
		return False
	maze[x][y] = 50
	return True

def calcXY(currentXY, move):
	[x, y] = currentXY
	if move == 'L':
		y -= 1
	elif move == 'R':
		y += 1
	elif move == 'U':
		x -= 1
	elif move == 'D':
		x += 1
	return [x, y]

def traceOnce(x,y,xd,yd):
	x += xd
	y += yd
	try:
		img[x][y] = [0, 0, 255]
	except IndexError:
		pass
	else:
		pass
	return [x, y]

# To color the pixels of the shortest path
def tracePath(path):
	x, y = startx, starty
	for move in path[0]:
		if move == 'L':
			[x, y] = traceOnce(x,y,0,-1)
		elif move == 'R':
			[x, y] = traceOnce(x,y,0,1)
		elif move == 'U':
			[x, y] = traceOnce(x,y,-1,0)
		elif move == 'D':
			[x, y] = traceOnce(x,y,1,0)

# Creating queue
paths = Queue()
maze = np.copy(bwImg)

# Defining start and end points
(maxx, maxy) = bwImg.shape
minx, miny = 0, 0
(startx, starty) = getStart()
(endx, endy) = getEnd()
print(startx, starty, endx , endy)

# Setting start point
currentPath = ['', [startx, starty]]
paths.put(currentPath)

# Main Algorithm
print('Starting search...')
while(not reachEnd(currentPath) and not paths.empty()):
	currentPath = paths.get()
	for j in ['L', 'R', 'U', 'D']:
		newPath = [currentPath[0] + j, calcXY(currentPath[1], j)]
		if isValidPath(newPath):
			paths.put(newPath)

if(currentPath[0]):
	print('Shortest Path Found !!!')
	# Tracing the shortest path
	tracePath(currentPath)

	# Displaying solved maze
	plt.imshow(img, cmap = 'gray')
	plt.show()
else:
	print('No path found...')