import pigpio 
import time
import atexit
from flask import Flask, render_template, request
app = Flask(__name__)

# This function maps the angle we want to move the servo to, to the needed PWM value
def pwmSet(pulse):
	return int(pulse)

# Create a dictionary called pins to store the pin number, name, and angle
pins = {
    23 : {'name' : 'pan', 'pwm' : 1500},
    22 : {'name' : 'tilt', 'pwm' : 1500}
    }

# Create two servo objects using the RPIO PWM library
pi = pigpio.pi()
pi.set_mode(22, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)

# Setup the two servos and turn both to 90 degrees


# Cleanup any open objects
def cleanup():
    pi.set_servo_pulsewidth(22, 0)
    pi.set_servo_pulsewidth(23, 0)


# Load the main form template on webrequest for the root page
@app.route("/")
def main():

    # Create a template data dictionary to send any data to the template
    templateData = {
        'title' : 'PiCam'
        }
    # Pass the template data into the template picam.html and return it to the user
    return render_template('picam.html', **templateData)

# The function below is executed when someone requests a URL with a move direction
@app.route("/<direction>")
def move(direction):
    print('now in move')
    # Choose the direction of the request
    if direction == 'left':
	    # Increment the angle by 10 degrees
        np = pins[23]['pwm'] + 100
	print(np)
        # Verify that the new angle is not too great
        if int(np) <= 2400:
            # Change the angle of the servo
            pi.set_servo_pulsewidth(23, np)

            # Store the new angle in the pins dictionary
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

# Function to manually set a motor to a specific pluse width
@app.route("/<motor>/<pulsewidth>")
def manual(motor,pulsewidth):
    if motor == "pan":
        pi.set_servo_pulsewidth(23, int(pulsewidth))
    elif motor == "tilt":
        pi.set_servo_pulsewidth(22, int(pulsewidth))
    return "Moved"

# Clean everything up when the app exits
atexit.register(cleanup)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
