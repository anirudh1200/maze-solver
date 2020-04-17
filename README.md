# maze-solver
A shortest path maze solving approach using breadth first search algorithm implemented in python that can even solve in real time using input from a camera

## Usage
1. To solve an input image
```
Format:
$ python3 solver.py [filename]
Example:
$ python3 solver.py examples/maze200.png
```
2. To solve an input image and generate the video
```
Format:
$ python3 solve_video.py [filename] [fps] [rate]
Example:
$ python3 solve_video.py examples/braid200.png 30 100
```
3. To solve a puzzle from a live input
```
$ python3 live_solver.py
```


## Input
Some example mazes are included in the repository. These basic rules were followed during generating them:

- Each maze is black and white. White represents paths, black represents walls.
- All mazes are surrounded entirely by black walls.
- One white square exists on the top row of the image, and is the start of the maze.
- One white square exists on the bottom row of the image, and is the end of the maze.
- For a live input, the maze should have two red circles denoting the start and end point.

## Tools Used
  - OpenCV 3.4
  - Python 3.6
  
## Steps Involved in Real-Time Solving

* Take input from source (like videocam)
* Take the image and convert it into hsv and apply a mask
* Detect contors use erode function to remove unwanted noise
* Detect the start and end points
* Convert the image to black and white by adaptive gaussian thresholding
* Find the shortest path using the Breadth First Search Algorithm
* Trace the path and display it
