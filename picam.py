import pigpio 
import time
import atexit
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Create a dictionary called pins to store the pin number, name, and angle
pins = {
    23 : {'name' : 'pan', 'pwm' : 1200},
    22 : {'name' : 'tilt', 'pwm' : 1200}
    }

# Create initial blank user for website
user = {
	 'name' : ' '
    }


# Initialize pigpio and set pin 22 and 23 to ouput using PIGPIO Library
pi = pigpio.pi()
pi.set_mode(22, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)

# Set servos to neutral position
pi.set_servo_pulsewidth(22, 1200)
pi.set_servo_pulsewidth(23, 1200)


# Cleanup any open objects
def cleanup():
    pi.set_servo_pulsewidth(22, 0)
    pi.set_servo_pulsewidth(23, 0)

# Load login page
@app.route('/picam.html')
def picam():
	if user['name'] == 'admin':
	    return render_template('picam.html')
	else:
	    return redirect('/login.html')

# Load Home page
@app.route('/index.html')
def index():
	if user['name'] == 'admin':
            return render_template('index.html')
	else:
	    return redirect('/login.html')

# Load the main form template on webrequest for the root page
@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
	    user['name'] = 'admin'
	    return render_template('index.html')
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html')

# The function below is executed when someone requests a URL with a move direction
@app.route("/<direction>")
def move(direction):
    # Choose the direction of the request
    if direction == 'left':
	    # Increment the PWM by 100
        np = pins[23]['pwm'] + 100
	print(np)
        # Verify that the new PWM is within safe range
        if int(np) <= 2400:
            # Change the PWM of the servo
            pi.set_servo_pulsewidth(23, np)

            # Store the new PWM in the pins dictionary
            pins[23]['pwm'] = np
        return str(np) + ' ' + str(np)
    elif direction == 'right':
        np = pins[23]['pwm'] - 100
	print(np)
        if np >= 1100:
            pi.set_servo_pulsewidth(23, np)
            pins[23]['pwm'] = np
        return str(np) + ' ' + str(np)
    elif direction == 'down':
        np = pins[22]['pwm'] + 100
	print(np)
        if np <= 1700:
            pi.set_servo_pulsewidth(22, np)
            pins[22]['pwm'] = np
        return str(np) + ' ' + str(np)
    elif direction == 'up':
        np = pins[22]['pwm'] - 100
	print(np)
        if np >= 800:
            pi.set_servo_pulsewidth(22, np)
            pins[22]['pwm'] = np
        return str(np) + ' ' + str(np)

# Attempts to render and templates missed.  Must be logged in to access as with all other templates.
@app.route('/<path>')
def catch_all(path):
        return render_template(path)

# Clean everything up when the app exits
atexit.register(cleanup)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
