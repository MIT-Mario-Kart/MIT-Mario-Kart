# MIT - Mario Kart

## AI algorithm
### Overview
#### Flowmap

The main goal of this project is having cars controlled by players and cars running by themselves (AI controlled cars). In order for the autonomous cars to do a complete lap, they have to follow predetermined directions i.e a flowmap.

A flowmap is a map of desired orientation across the circuit, which we separated into a 40x40 grid. For greater clarity in the code, we chose to represent these orientation as hours on a watch (h3 => 0 deg, h12 => 90 deg, h6 => 270 deg, etc...). At each step the car's orientation (the attribute Car.orientation) is compared to its desired one indicated by the flowmap and a change of direction is applied accordingly.

We then calculate the desired steering angle to send to the Arduino which lies between 0 and 180, 90 meaning going straight.

(===== ADD PICTURE OF THE FLOW MAP =====)


#### Acceleration

Having cars following orientations is great, but in practice the cars take time to turn and their orientation doesn't change immediately. We needed the cars to slow down when approaching sharp bends.

We designed a zone system where each zone has a maximum speed allowed. These zones are bounded with coloured tape on the circuit. There are 3 types of them (ordered in decreasing speed): Green, Blue and Red.

In the Arduino code, the "currZone" variable is either green for full speed, blue for normal speed or red for low speed. Then the variable "speed_percentage", which is determined by the zones, is either 1.25, 1.00 or 0.75.
When a car drives over some tape, its colour sensor detects it and the above-mentioned variables are updated. 
There is also an "out" zone which corresponds to speed_percentage = 0.00 and white colour for the white tarp below the circuit. When a car steps out of the road, it must be placed back on the circuit to continue.

At each step the server sends the variable "rcvd_acc" to the Arduino. We then multiply this value by speed_percentage and give this value to the analogWrite method for the motor. If rcvd_acc is negative we apply it to the PIN_REVERSE instead of the PIN_FORWARD.

#### Powerups

In addition to the red, green and blue tape, we put brown tape on the circuit for powerups. When the sensor detects it, the variable "isPowerupd" is set to 1 and sent to the server. When the server receives it, a random powerup generator is started.

Powerups can have positive or negative effects : 
The first one is to increase your speed by changing Car.acc, the second one is to slow down every other cars and the last one is to invert the commands of all players (not AI) by changing Car.inverted.
The circuit was too narrow so we couldn't implement the last one.

Each powerup lasts 5 seconds as shown below : 


        if self.isOnPowerUp(car):
            if car.startTime == -1:
                pu.powerUp(car, self.cars)

        if car.startTime != -1 and (datetime.datetime.now() - car.startTime).seconds >= POWERUP_TIME:
            car.startTime = -1
            car.acc = pu.NORMAL
            print("STOP POWERUP")
            

With POWERUP_TIME = 5.

Note: since there were times when testing where the color sensors weren't fully calibrated or times where they produced false positives, we added on the server the same logic described above for powerups and acceleration to use if we wanted to disregard the input from the color sensor. However, in the final version of the project we didn't need to do so but still we left this code commented out (so you could see what how we used it).

##### Overtake

With the powerups and the zone system, cars can have different speed across the map. We didn't want them to bump each other (at least not the AI ones) so we had to implement an overtake system.

At first we thought about delimiting a semi-circle behing each cars. When another car drivees into this area, it starts changing its orientation (car.delta) to overtake. This change is proportional to the distance between the two cars. If they are really close, the overtake needs to be more brutal than if they were far away.

But we had problems with Matplotlib (which we used for the semi circles) and the circuit was too narrow to overtake smoothly. So we implemented an slowdown method which calculates a rectangle behind each car and forces the other cars to slow down (changes car.acc) when they are in it.


### AI Simulation
#### Update Movement
Update movement is a method that we used in order to test the flowmap in a simulation. We made it possible to simulate the way a car would (in theory) follow the flowmap in the GUI. This method wasn't used in the final server, but it proved to be very useful in calibrating a first version of the flowmap. The "orientation" around the flowmap uses the classic trig circle: 0 degrees points to the right of the circuit, 90 degrees to the top, 180 to the left and 270 to the bottom.
The way the method works is very simple - it takes a desired velocity and angle as parameters, and computes the next speed, acceleration and coordinates the car would have and stores them in the car's corresponding attributes. 
At first the car's orientation is updated. If the desired angle is negative, this means that the car should turn right (think of it as a negative angle difference on the trig circle, so clockwise), otherwise it should turn left. If the absolute angle difference between the desired angle and the current angle is smaller than ANGLE_PRECISION (an aribitrarily defined constant, to be tweaked as you see fit), then the car won't turn. Whenever it turns, it does so by ANGLE_UNIT every time the method is called.
Next, the method checks which is the desired velocity and updates the car's acceleration and velocity accordingly using basic kinematic equations, implemented in a very naive way. Technically, the way it's coded you can simulate the car's acceleration changing over time, but we tweaked the constants to give it an almost constant acceleration because we didn't need the added precision (if ACC_UNIT = MAX_ACC, then you will get a constant acceleration). Next, the car's speed gets updated according to its acceleration. Both the acceleration and speed are upper bounded (respectively MAX_ACC and MAX_VELOCITY).
Finally, the car's coordinates get updated according to the car's speed, previous position and current orientation. Keep in mind, this method will never be 100% precise, but it works well enough with the constants calibrated to the right values.

## Server 
### Overview
Everything in this project was connected to our main server. It controlled the AI driven cars and processed the input from the remote controllers and sent it to the player cars. It also took input from the camera to know where the cars were on the circuit which was then displayed on the GUI and used for the AI algorithm displayed above.

We used the ThreadedTCPServer library to open a thread for each new connection and then defined a method that was used to handle all newly received information and send back the information needed by the cars or the camera.

The Control class is used to process the information sent to the server and is responsible for figure out the information to send back to each connection.

### Camera connection 
The server receives from the camera, the position and orientation of each cars. Each car object on the server has a `color` attribute, which corresponds to the color of the triangle on top of the car which is detected by the camera. 
#### ID system
The server recognises that the input is from the camera because the camera precedes all its messages by an id "CAM". The same technique is used by the cars to identify themselves: each car has a specific id. This makes it so that the only IP address necessary to know is the server's (the camera and cars need to know where to connect to). The server will then reply to connections from the camera and cars but we don't need to input their IP in the server before hand.
#### Updating the cars based on the information from the camera
The server then stores the coordinates of each car and its orientation and calls `moveCar` which will look at the flowmap to find the desired orientation of the car, calculate the delta sent to the car (angle that needs to be applied by the servo) based on that information and will figure out the acceleration that needs to be sent to the car based on the zone it currently is in (if we are not using the color sensor).
#### Grid system
Since the coordinates sent by the camera are originally within 1080x1920, we need to translate to the actual coordinates in real life. To do so, we use the coordinates of the 4 yellow triangles sent by the camera when it is in calibration mode and use this info to establish a grid. Then, for all future coordinates sent by the camera, we use this grid to translate them to real life positions. Once the server is calibrated, it connects back to the camera to tell it to exit calibration mode.

### Car Connection
Each car connects to the server with a car id. The server uses this id to get its corresponding car object on the server and sends back to the car, the correct information. Either the orientation and acceleration found using the algorithm if it's an AI driven car or the information processed using the controllers for player cars.
#### Server connection
The ESP8266 boards each connect to the main server over wifi, which must all be connected to the same wifi. For this we used the personal hotspot of the phone acting as the camera, which proved a little unreliable as it sometimes decided to become undiscoverable on its own. We often had to resort to yelling "hey Siri, open hotspot settings" while standing on a chair in order to be closer to the phone. 
Once the boards were connected to wifi, we had them connect to the server using WifiClient from the ESP8266WiFi.h library. The boards would send colour sensor information in the form of an integer between 0 and 5, indicating what kind of checkpoint the car has passed (while it isn't passing a checkpoint, it perpetually sends a 0):
0 = circuit, 1 = powerup, 2 = red tape, 3 = green tape, 4 = blue tape, 5 = car is off the circuit
The boards then received all movement data straight from the server, in the form of 2 integers. The first received integer indicated the value to be weitten to the car's servo (between 0 and 180, inclusive). The second indicated the car's speed: a negative integer meant that the car should drive backwards, a positive integer meant that the car should drive forwards and 0 meant stop. 
To separate these two integers from the received string, we used strtok() to separate the string and atoi() to convert the numbers in the string to the int type.
Two important elements we overlooked that probably greatly contributed to server-board latency were the heat produced by the motor on the car (which probably greatly slowed the board down) and the interference caused by other electronic devices in the near vicinity. There were never that many people around us before the demo day, but when people started arriving the day of the demo, the cars connected to the personal hotspot but never to the server.
#### Joystick
We faced more challenges than we had anticipated for the joystick controlling the car. First, we tried using Blynk, except that we couldn't get the Arduino to connect to Blynk's servers and to our server both at once, and we still don't know why. 
Next, we tried reusing and adapting the code one of us had written to control the cars we each made for the personal project (different cars to this project). It worked by hosting a webserver directly on the Arduino using the ESP8266WebServer.h library and then connecting to that webserver using a phone (with the Arduino connected to that phone's personal hotspot). The joystick worked perfectly while not connected to the server, but had terrible latency issues when connected to the server at the same time as hosting the webserver.
In an attempt to fix this, we tried using the car's second board (the ESP32-Cam-AI-Thinker). The idea was to have the ESP8266 host the webserver and have the ESP32 communicate with the main server, and then transmit any data received from the main server over the two boards' Serial ports, using the RX/TX pins and the SoftwareSerial.h library. Unfortunately, we again ran into high latency issues. Anyone who wants to use the SoftwareSerial.h library should know that it takes a lot of processing power and therefore slows the board down. In theory, it's possible to communicate over Serial without using this library, but by this point we were running out of time. Serial communication is painful and long to debug, because you can't send messages to another board over Serial and print received messages to the console at the same time, so you need to be a little creative (to test it out, we connected both boards to a dummy server that just prints messages and had each board transmit any received from the other board). Therefore, we were forced to downgrade to a system where powerups could only affect one car at a time until we came up with our final solution: console controllers connecting to the computer hosting the main server, and the main server sending on the movement data the the ESP8266.

This final solution was implemnted using pygame because it already had a way of detecting a controller once it has been connected to the computer using bluetooth. So what we ended up assigning to our car object a controller from the Controller class if a JOYDEVICEADDED event from pygame was added and if the car was a player driven car. Then we updated each car object constantly by looking at the joystick position to figure out the angle to send to the car and if the forward or backwards button were pressed, to figure out what acceleration to send the car. As described above, the same arduino code was used for player and AI cars so we send that information to the cars in the same way as we did for the AI car. This lets us decide for a given round what cars will be AI or player driven without reuploading arduino code, this is done by simply changing the `ai` attribute of the car when initialising the car object.
