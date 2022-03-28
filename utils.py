import math
import time
import cv2

# this function moves the dobot to the home position
# inputs: 
#   • device: the dobot device to move
def home(device):
    print('Homing device ...')
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    device.rotate_joint(0.0, 0.0, 0.0, j4, wait=True)
    return

# this function returns n equally spaced points on a circle 
# returns two lists: x and y
# x = [x0, x1, x2, ..., xn], y = [y0, y1, y2, ..., yn]
# where (x[i], y[i]) is a point on the circle
# inputs: 
#   • n: number of points on the circle
def circle(n):
    π = 3.141592
    step = (2*π)/n

    θ = []
    θi = 0
    while θi <= 2*π:
        θ.append(θi)
        θi = θi + step

    x = []
    y = []
    for i in range(len(θ)):
        xi, yi = math.cos(θ[i]), math.sin(θ[i])
        x.append(xi)
        y.append(yi)

    return x, y

# this function returns n equally spaced points on parabola along the x-axis
# the parabola is centered at x = 0
# returns two lists: x and y
# x = [x0, x1, x2, ..., xn], y = [y0, y1, y2, ..., yn]
# (x[i], y[i]) is a point on the parabola
# inputs: 
#   • x_min: x0 
#   • x_max: xn
#   • a: y = ax^2 (parabolic equation)
#   • n: number of points on parabola
def parabola(x_min, x_max, a, n):
    step = (x_max - x_min) / n

    x = []
    xi = x_min
    while xi <= x_max:
        x.append(xi)
        xi = xi + step

    y = []
    for i in range(len(x)):
        yi = a*(x[i]**2) + 0*x[i] + 0
        y.append(yi)

    return x, y

# this function scales and shifts coordinates so they fit within the dobot range of drawing motion
# inputs: 
#   • x: list of x-coordinates
#   • y: list of y-coordinates 
# returns: lists x and y of scaled coordinates 
def scale_shift(x, y):
    draw_x_max = 340.00
    draw_x_min = 220.00
    draw_x_range = draw_x_max - draw_x_min

    draw_y_max = 85.00
    draw_y_min = -draw_y_max
    draw_y_range = draw_y_max - draw_y_min 

	# scaling factor 
    x_scale = (draw_x_range / (max(x) - min(x)))
    y_scale = (draw_y_range / (max(y) - min(y)))
    scale = min(x_scale, y_scale)

    # scale coordinates
    for i in range(len(x)):
        x[i] = x[i]*scale
        y[i] = y[i]*scale

    # shift coordinates to fit in dobot range 
    x_dif = min(x) - draw_x_min
    y_dif = min(y) - draw_y_min

    for i in range(len(x)):
        x[i] = (x[i] - x_dif) 
        y[i] = (y[i] - y_dif)

    return x, y

# this function uses the dobot to draw dots on paper of given x,y coordinates
# inputs:
#   • device: dobot device to move 
#   • x: list of x-coordinates
#   • y: list of y-coordinates
#   • z: z-coordinate where pen touches paper (must be calibrated for your device)
def draw_dots(device, x, y, z):
    (xp, yp, zp, r, j1, j2, j3, j4) = device.pose()
    for i in range(len(x)):
        device.move_to(x[i], y[i], -10.00, r, wait=True)
        device.move_to(x[i], y[i], z, r, wait=True) 
        time.sleep(1)
        device.move_to(x[i], y[i], -10.00, r, wait=True)

# this function uses the dobot to draw connecting lines between consective coordinates
# inputs:
#   • device: dobot device to move 
#   • x: list of x-coordinates
#   • y: list of y-coordinates
#   • z: z-coordinate where pen touches paper (must be calibrated for your device)
def draw(device, x, y, z):
    (xp, yp, zp, r, j1, j2, j3, j4) = device.pose()
    for i in range(len(x)):
        device.move_to(x[i], y[i], z, r, wait=True)

def drawbox(device, draw):
    (xp, yp, zp, r, j1, j2, j3, j4) = device.pose()
    # dobot drawing boundaries
    x_min = 220.00
    x_max = 340.00

    y_max = 85.00
    y_min = -y_max

    if draw:
        # draw
        z = -47.00
    else:
        # hover
        z = -17.00

    # roughly, the range of dobot coordinates is:
    # x ∈ (204.0, 367.0), y ∈ (-210.0, 212.0), and z ∈ (-87.0, 176.0)
    device.move_to(x_max, y_max, z, r, wait=True) 
    device.move_to(x_min, y_max, z, r, wait=True) 
    device.move_to(x_min, y_min, z, r, wait=True) 
    device.move_to(x_max, y_min, z, r, wait=True) 
    device.move_to(x_max, y_max, z, r, wait=True)

# returns list of available cameras by index
def get_cameras():
    available_cams = []
    for camera_idx in range(10):
        cap = cv2.VideoCapture(camera_idx)
        if cap.isOpened():
            available_cams.append(camera_idx)
            cap.release()
        else:
            # suppress warnings from cv2
            print ('\033[A' + ' '*158 +  '\033[A')
    return available_cams