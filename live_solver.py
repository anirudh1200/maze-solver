import cv2
import numpy as np
from queue import Queue
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
frame = 0

# Defining various functions
def reachEnd(pos, maze):
	return (maze[pos[1]][pos[0]] == [0, 255, 0]).all()

def isValidPath(path, minx, miny, maxx, maxy, maze):
	[x, y] = path[1]
	if not(minx<= y < maxx and miny<= x < maxy):
		return False
	elif ((maze[y][x] == [0, 0, 255]).all() or (maze[y][x] == [0,0,0]).all()):
		return False
	if not (maze[y][x] == [0, 255, 0]).all():
		maze[y][x] = [0, 0, 255]
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

# To color the pixels of the shortest path
def tracePath(path, xs, ys, maze):
	x, y = xs, ys
	for move in path[0]:
		if move == 'L':
			y -= 1
		elif move == 'R':
			y += 1
		elif move == 'U':
			x -= 1
		elif move == 'D':
			x += 1
		try:
			maze[y][x] = [0, 0, 255]
			maze[y+1][x] = [0, 0, 255]
			maze[y][x-1] = [0, 0, 255]
			maze[y+1][x-1] = [0, 0, 255]
		except IndexError:
			pass
		else:
			pass
	return maze

def solveMaze(xs, ys, xe, ye, maze):
	# Converting image in black & white
	frame = np.copy(maze)
	gray = cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY)
	bwImg = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
	# Defining start and end points
	(maxx, maxy) = bwImg.shape
	minx, miny = 0, 0
	# Creating queue
	paths = Queue()
	currentPath = ['', [xs, ys]]
	paths.put(currentPath)
	# Plotting start and end points
	maze = cv2.cvtColor(bwImg,cv2.COLOR_GRAY2RGB)
	maze = cv2.circle(maze, (xs, ys), 3, (255, 0, 0), 6)
	maze = cv2.circle(maze, (xe, ye), 3, (0, 255, 0), 6)
	# Main Algorithm
	c=0
	while(not reachEnd(currentPath[1], maze) and not paths.empty()):
		currentPath = paths.get()
		for j in ['L', 'R', 'U', 'D']:
			newPath = [currentPath[0] + j, calcXY(currentPath[1], j)]
			if isValidPath(newPath, minx, miny, maxx, maxy, maze):
				paths.put(newPath)
	if(currentPath[0]):
		return currentPath
	else:
		print('Not found')
		return ['']

frameNo = 0
path, xstart, ystart = [''], 0, 0
while True:
	_, frame = cap.read()
	frame = frame[100:500, 100:500]
	if frameNo > 10:
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		lower_red = np.array([40, 110, 180])
		upper_red = np.array([180, 255, 255])

		mask = cv2.inRange(hsv, lower_red, upper_red)
		kernel = np.ones((6, 6), np.uint8)
		mask = cv2.erode(mask, kernel=kernel)
		# Contours detection
		contours= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
		circles = 0
		for cnt in contours:
			area = cv2.contourArea(cnt)
			if area > 20:
				circles+=1
		if(circles == 2):
			xmin = min([contours[0].ravel()[0], contours[1].ravel()[0]])
			for cnt in contours:
				if area > 20:
					x = cnt.ravel()[0]
					y = cnt.ravel()[1]
					if(x <= xmin):
						xmin = x
						pointName = 'Start'
					else:
						pointName = 'End'
			[xstart, ystart] = contours[0].ravel()[0:2]
			[xend, yend] = contours[1].ravel()[0:2]
			path = solveMaze(xstart, ystart, xend, yend, frame)
			frameNo=0
	elif frameNo == 10:
		path, xstart, ystart = [''], 0, 0
	
	frame = tracePath(path, xstart, ystart, frame)
	cv2.imshow("frame", frame)
	# cv2.imshow("Mask", mask)
	frameNo += 1
	key = cv2.waitKey(1)
	if key==27:
		break

cap.release()
cv2.destroyAllWindows()