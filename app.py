#!/usr/bin/python3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask_sqlalchemy  import SQLAlchemy
from flask_bootstrap import Bootstrap
from serial.tools import list_ports
from flask_wtf import FlaskForm 
from utils import get_cameras
from pydobot import Dobot
import subprocess
import threading
import datetime
import requests
import imutils
import os.path
import random
import utils
import time
import cv2
import os 

app = Flask(__name__)
port=8000

# output link for webapp
print('\n\n🤖 Pi-Vision 🤖\n')
print('Log in to piEye. Go to:')
print('🏠 http://0.0.0.0:'+ str(port) +'/ if accessing from Raspberry Pi.')
rpi_ip = subprocess.getoutput('hostname -I').split()[0]
print('🏠 http://' + rpi_ip + ':' + str(port) +'/ if accessing from local network.')
# get the external ip of the raspberry pi
public_ip = requests.get('https://api.ipify.org').text
print('🌎 http://' + public_ip + ':'+ str(port) +'/ if accessing from remote network (port forwarding required).')
print('')

# - - - - - - - - - - - - - - - LOG IN MANAGEMENT START - - - - - - - - - - - - - - - - - - - -

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# - - - - - - - - - - - - - - - LOG IN MANAGEMENT END - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - WEB CAMERA START - - - - - - - - - - - - - - - 
available_cams = get_cameras()
print('Cameras: ' + str(available_cams))
# cam = int(input(''))
# print('')


if len(available_cams) >= 1:
    cam = available_cams[0]
    camera = cv2.VideoCapture(cam)
else: 
    camera = cv2.VideoCapture(9)

# generate frame by frame from camera
def gen_frames():  
    while True:
        # read the camera frame
        success, frame = camera.read()  
        frame = imutils.resize(frame, width=300)
        if not success:
            break
        else:
            # dsize = (300, 300)
            # frame = cv2.resize(frame, dsize)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # concat frame one by one and show result
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  

# video streaming route. Put this in the src attribute of an img tag
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# - - - - - - - - - - - - - - WEB CAMERA END - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - WEB CAMERA2 START - - - - - - - - - - - - - - - 

# select camera for stream
if len(available_cams) >= 2:
    cam2 = available_cams[1]
    camera2 = cv2.VideoCapture(cam2)
else: 
    camera2 = cv2.VideoCapture(10)

# generate frame by frame from camera
def gen_frames2():  
    while True:
        # read the camera frame
        success, frame = camera2.read()  
        frame = imutils.resize(frame, width=300)
        if not success:
            break
        else:
            # dsize = (300, 300)
            # frame = cv2.resize(frame, dsize)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # concat frame one by one and show result
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  

# video streaming route. Put this in the src attribute of an img tag
@app.route('/video_feed2')
def video_feed2():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')

# - - - - - - - - - - - - - - WEB CAMERA2 END - - - - - - - - - - - - - - - -


# - - - - - - - - - - - APP PAGES START - - - - - - - - - - - - - - - - -
# user registration page
# disabled sign-up so not everyone can sign up and use the robot
'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form=form)
'''

# login page 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('reta'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

# this thing is not really used, keeping it just in case
'''
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)
'''

# log out function for users
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def reta():
    return render_template('control.html', cams=available_cams)

# RETA Block (page 4)
@app.route('/blockly')
@login_required
def blockly():
    return render_template('blockly.html', cams=available_cams)

# reservation page
@app.route('/reservation')
@login_required
def reservation():
    return render_template('reservation.html')


# - - - - - - - - - - - APP PAGES END - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - DOBOT CONTROLS START - - - - - - - - - - - - -

step = 5.0
cartesian_scalar = 3.0

# joint-1 control: counter-clockwise
@app.route('/counter-clockwise')
def counter_clockwise():
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    j1, j2, j3, j4 = j1 + step, j2, j3, j4
    
    if j1 < 102.00:
        print ("counter-clockwise")
        device.rotate_joint(j1, j2, j3, j4, wait=False) 
    else:
        print('PREVENTING MOVEMENT: Too Far Counter-Clockwise')
    return ("")

# joint-1 control: clockwise
@app.route('/clockwise')
def clockwise():
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    j1, j2, j3, j4 = j1 - step, j2, j3, j4
    if j1 > -102.00:
        print ("clockwise")
        device.rotate_joint(j1, j2, j3, j4, wait=False) 
    else:
        print('PREVENTING MOVEMENT: Too Far Clockwise')
    return ("")

# joint-2 control: extend
@app.route('/j2-plus')
def j2_plus():
    print ("j2-plus")
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    j1, j2, j3, j4 = j1, j2 + step, j3, j4
    device.rotate_joint(j1, j2, j3, j4, wait=False) 
    return ("")

# joint-2 control: retract
@app.route('/j2-minus')
def j2_minus():
    print ("j2-minus")
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    j1, j2, j3, j4 = j1, j2-step, j3, j4
    device.rotate_joint(j1, j2, j3, j4, wait=False) 
    return ("")

# joint-3 control: down
@app.route('/j3-plus')
def j3_plus():
    print ("j3-plus")
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    j1, j2, j3, j4 = j1, j2, j3+step, j4
    # prevent movement if gripper head goes too low
    if z > -25.71:
        device.rotate_joint(j1, j2, j3, j4, wait=False) 
    else:
        print('CANCELING MOVEMENT: Too Low')
    return ("")

# joint-3 control: up
@app.route('/j3-minus')
def j3_minus():
    print ("j3-minus")
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    j1, j2, j3, j4 = j1, j2, j3-step, j4
    # prevent movement if gripper head goes too high
    if z < 177.128:
        device.rotate_joint(j1, j2, j3, j4, wait=False) 
    else:
        print('CANCELING MOVEMENT: Too High')
    return ("")



# X+ control
@app.route('/x-plus')
def x_plus():
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    x, y, z = x + step*cartesian_scalar, y, z

    print ("x-plus")
    device.move_to(x, y, z, r, wait=False) 
    return ("")

# X- control
@app.route('/x-minus')
def x_minus():
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    x, y, z = x - step*cartesian_scalar, y, z

    print ("x-minus")
    device.move_to(x, y, z, r, wait=False) 
    return ("")

# y+ control
@app.route('/y-plus')
def y_plus():
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    x, y, z = x, y + step*cartesian_scalar, z

    print ("y-plus")
    device.move_to(x, y, z, r, wait=False) 
    return ("")

# y- control
@app.route('/y-minus')
def y_minus():
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    x, y, z = x, y - step*cartesian_scalar, z

    print ("y-minus")
    device.move_to(x, y, z, r, wait=False) 
    return ("")

# z+ control
@app.route('/z-plus')
def z_plus():
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    x, y, z = x, y, z + step*cartesian_scalar

    print ("z-plus")
    device.move_to(x, y, z, r, wait=False) 
    return ("")

# z- control
@app.route('/z-minus')
def z_minus():
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    x, y, z = x, y, z - step*cartesian_scalar

    print ("z-minus")
    device.move_to(x, y, z, r, wait=False) 
    return ("")

# gripper control: activate gripper 
@app.route('/grip')
def gripper_grab():
    print ("grip")
    global device
    device.grip(True)
    return ("")

# gripper control: release gripper
@app.route('/release')
def gripper_release():
    print ("release")
    global device
    device.grip(False)
    return ("")

# gripper control: release gripper
@app.route('/disable-gripper')
def disable_gripper():
    print ("gripper disabled")
    global device
    device.suck(False)
    return ("")

# home device control
@app.route('/home')
def home():
    print ("homing device")
    global device
    utils.home(device)
    return ("")

# function for setting the speed of the dobot
@app.route('/set-speed', methods=['POST'])
def set_speed():
    global step
    speed = request.form['speed']
    step = float(speed)
    print(step)
    print('\nRobot speed updated!\n')
    return jsonify({'speed' : speed})

# function for writing and executing blockly python code from blockly.html
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    # import required libraries
    name = 'import time\n' + name
    name = 'from serial.tools import list_ports \nfrom pydobot import Dobot \nport = list_ports.comports()[0].device\ndevice = Dobot(port=port, verbose=False)\n\n' + name
    dobot_command = open("script.py", "w")
    dobot_command.write(name)
    dobot_command.close()
    print('\nExecuting blockly code...\n')
    print('')
    os.system('python3 script.py')
    print('')
    return jsonify({'name' : name})

# - - - - - - - - - - - DOBOT CONTROLS END - - - - - - - - - - - - -

# - - - - - - - - - - DOBOT DEMOS START - - - - - - - - - - - - - - 

@app.route('/joint-1-demo')
def joint_1_demo():
    print("joint-1 demo")
    global device
    utils.home(device)
    # assign joint movement coordinates
    j1b, j2b, j3b, j4b = 30.0, 15.0, 40.0, 0.779
    j1a, j2a, j3a, j4a = -30.0, 15.0, 40.0, 0.779
    # move dobot back and forth
    for i in range(2):
        device.rotate_joint(j1a, j2a, j3a, j4a, wait=True)
        device.rotate_joint(j1b, j2b, j3b, j4b, wait=True)
    utils.home(device)
    return ("")

@app.route('/joint-2-demo')
def joint_2_demo():
    print("joint-2 demo")
    global device
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    utils.home(device)
    # assign movement coordinates
    x1,y1,z1 = 183.0, 0.0, 41.99 # CHANGE
    x2,y2,z2 = 305.68, 0.0, 27.221 # CHANGE
    # move dobot back and forth
    for i in range(2):
        device.move_to(x1, y1, z1, r, wait=True)
        device.move_to(x2, y2, z2, r, wait=True)
    utils.home(device)
    return ("")

# - - - - - - - - - - DOBOT DEMOS END - - - - - - - - - - - - - - 

# - - - - - - - - - - RETA APP START - - - - - - - - - - - - - - - -

# - - - - - - - - - - RESERVATION START - - - - - - - - - - - - -
@app.route('/reservation-handler', methods=['POST'])
def process_reservation():
    print('\nReservation Request Recieved:')
    start = request.form['name'] + ':00'
    start = datetime.datetime.fromisoformat(start)
    end = start + datetime.timedelta(hours = 1)
    start = start.isoformat()
    end = end.isoformat()
    print(start + ' -- ' + end)

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # create a new google calendar event
    event = {
    'summary': 'Dobot Reservation',
    'location': 'www.supertechft.com',
    'description': 'Your robot reservation is confirmed!',
    'start': {
        'dateTime': start,
        'timeZone': 'UTC',
        #'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': end,
        'timeZone': 'UTC',
        #'timeZone': 'America/Los_Angeles',
    },
    'attendees': [
        #{'email': 'ahu@supertechft.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }

    # check if requested time is available
    requested_time =  {
    "items": [ 
        {
        "id": "c_9evtnmj6adkkcbghf93br4md3c@group.calendar.google.com", 
        },
    ],
    "timeMax": end + 'Z', 
    "timeMin": start + 'Z', 
    'timeZone': 'UTC', 
    #'timeZone': 'America/Los_Angeles',
    }
    busy = service.freebusy().query(body=requested_time).execute()

    # create reservation if requested time is available
    if not busy['calendars']['c_9evtnmj6adkkcbghf93br4md3c@group.calendar.google.com']['busy']:
        print('')
        print('\nNew reservation created ✅\n')
        event = service.events().insert(calendarId='c_9evtnmj6adkkcbghf93br4md3c@group.calendar.google.com', body=event).execute()
        success_status = 'true'
    else:
        print('')
        print('Reservation not available ❌\n')
        success_status = 'false'

    return jsonify({'reservation' : success_status})

# - - - - - - - - - - RESERVATION END - - - - - - - - - - - - - -

if __name__ == '__main__':
    # access and activate the dobot 
    dobot_port = 0
    dobot_port = list_ports.comports()[dobot_port].device
    device = Dobot(port=dobot_port, verbose=False)
    # start the app
    app.run(host='0.0.0.0', port=port, debug=False)

