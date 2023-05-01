// #include <ESP8266WiFi.h>
// #include <WiFiClient.h>
// #include <ESP8266WebServer.h>
// #include <ESP8266mDNS.h>
// #include <WiFiUdp.h>

// #include <uri/UriBraces.h>
// #include <uri/UriRegex.h>
// #include <Servo.h>

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// #ifndef STASSID
// #define STASSID "IP"
// #define STAPSK "PASS"
// #endif

// #define UDP_SERVER_IP "10.172.10.2"
// #define UDP_PORT 8888

#define START_X 0
#define START_Y 0
#define START_ORIENTATION M_PI/2 // 90 deg = facing forwards on trig circle
#define ANGLE_UNIT M_PI/100 // ~ 1.8 deg
#define MAX_ORIENTATION M_PI
#define MIN_ORIENTATION -MAX_ORIENTATION // -180 deg <= orientation <= 180 deg
#define VELOCITY_UNIT 0.1
#define SLOWDOWN_ACCEL 0.03
#define STOP_ACCEL 0.05
#define MAX_VELOCITY 0.1

#define ACC_UNIT 0.01
#define DECEL_UNIT 0.2
#define MAX_ACC 0.01

#define INPUT_SIZE 513
#define CLOSE "close"
#define RESTART "restart"
#define FORWARD "F"
#define FORWARD_LEFT "FL"
#define FORWARD_RIGHT "FR"
#define REVERSE "R"
#define REVERSE_RIGHT "RR"
#define REVERSE_LEFT "RL"
#define STOP "S"
#define CONT "C"

#define ANGLE_PRECISION 1 // In degrees (if angle is within ± ANGLE_PRECISION it doesn't get updated)

// #define STOP 0
// #define FORWARD 1
// #define FORWARD_LEFT 2
// #define FORWARD_RIGHT 3
// #define REVERSE -1
// #define REVERSE_LEFT -2
// #define REVERSE_RIGHT -3

// #define PIN_D2_FORWARD 4
// #define PIN_D1_REVERSE 5
// #define SERVO_PIN 15


// Lite version
// void update_movements(int desired_angle);

// Pro version
void update_movements(int desired_angle, int desired_accel);

void send_coords(void);
void print_info();
int gt(double angle, int desired_angle);
int lt(double angle, int desired_angle);
int eq(double angle, int desired_angle);

// const char *ssid = STASSID;
// const char *password = STAPSK;

// Servo myservo;
// ESP8266WebServer server(80);
// WiFiUDP UDP;

double coord_x = START_X;
double coord_y = START_Y;
double dir = START_ORIENTATION;
double velocity_x = 0;
double velocity_y = 0;
double acc_x = 0;
double acc_y = 0;

int main(void) {
//   pinMode(PIN_D2_FORWARD,OUTPUT); // D2 F
//   pinMode(PIN_D1_REVERSE,OUTPUT); // D1 R
//   myservo.attach(SERVO_PIN); // D8
//   // 172.20.10.5

//   Serial.begin(115200);
//   WiFi.mode(WIFI_STA);
//   WiFi.begin(ssid, password);
//   Serial.println("");

    // Wait for connection
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }
//   Serial.println("");
//   Serial.print("Connected to ");
//   Serial.println(ssid);
//   Serial.print("IP address: ");
//   Serial.println(WiFi.localIP());

//   if (MDNS.begin("esp8266")) { Serial.println("MDNS responder started"); }


// ----------- STRTOD EXAMPLE ---------------

    // char str[30] = "20.30300 Test";
    // char *ptr;
    // double ret;

    // ret = strtod(str, NULL);
    // printf("\nThe number (double) is %lf\n", ret);
    // printf("String part is |%s|\n", ptr);

// -------------------------------------------

// ---------------------------------------------------------------

    int close = 0;

    printf("Starting...\n");
    print_info();

    while(!close) {

        char usr_input[INPUT_SIZE];
        scanf(" %s", usr_input);  
        char* mov_input;
        int desired_angle = (int) strtod(usr_input, &mov_input);

        if(strcmp(mov_input, CLOSE) == 0) {
            close = 1;
            printf("Closing...\n");
            print_info();
        } else if (strcmp(mov_input, RESTART) == 0) {
            printf("Restarting...\n");
            velocity_x = 0;
            velocity_y = 0;
            dir = START_ORIENTATION;
            coord_x = START_X;
            coord_y = START_Y;
            print_info();
        } else if(  strcmp(mov_input, FORWARD) == 0 || strcmp(mov_input, FORWARD_LEFT) == 0 || strcmp(mov_input, FORWARD_RIGHT) == 0
                    || strcmp(mov_input, REVERSE) == 0 || strcmp(mov_input, REVERSE_LEFT) == 0 
                    || strcmp(mov_input, REVERSE_RIGHT) == 0 || strcmp(mov_input, CONT) == 0) {
            // update_movements(desired_angle);
            send_coords();
            print_info();
        } else if(strcmp(mov_input, STOP) == 0) {

            // update_movements(-1);

        } else {
            printf("Invalid input\n");
        }
    }

// ---------------------------------------------------------------


    return 0;
}

// void loop(void) {
//   server.handleClient();
// }

// void update_movements(int desired_angle) {

//     // C tester code only
//     // ---------------------
//     if(desired_angle == -2) {
//         // Continue
//         coord_x += velocity_x;
//         coord_y += velocity_y;

//         return;
//     }
//     // ---------------------


//     double deg_dir = (dir / M_PI) * 180;

//     if(desired_angle == -1) {
//         // Stop
//         velocity_x = fmax(0, velocity_x - SLOWDOWN_ACCEL);
//         velocity_y = fmax(0, velocity_y - SLOWDOWN_ACCEL);

//     } else {

//         // Assume moving forwards for now
//         if(gt(deg_dir, desired_angle)) {
//             printf("%lf > %d\n", deg_dir, desired_angle);
//             dir = fmax(MIN_ORIENTATION, dir - ANGLE_UNIT);
//         } else if(lt(deg_dir, desired_angle)) {
//             printf("%lf < %d\n", deg_dir, desired_angle);
//             dir = fmin(MAX_ORIENTATION, dir + ANGLE_UNIT);
//         } 

//         velocity_x = fmin(MAX_VELOCITY, velocity_x + cos(dir));
//         velocity_y = fmin(MAX_VELOCITY, velocity_y + sin(dir));
//     }


//     coord_x += velocity_x;
//     coord_y += velocity_y;

// }

// if angle > desired_angle
int gt(double angle, int desired_angle) {
    return (angle - desired_angle > ANGLE_PRECISION); 
}

// if angle < desired_angle
int lt(double angle, int desired_angle) {
    return (angle - desired_angle < -ANGLE_PRECISION);
}

// if angle =~ desired_angle
int eq(double angle, int desired_angle) {
    return (fabs(angle - desired_angle) < ANGLE_PRECISION);
}




// Utility functions

void send_coords() {

    int interaction_index = 0;
    int orientation = (int) ((dir/M_PI) * 180);

    char coords[33];
    sprintf(coords, "%d, %d, %d, %d", interaction_index, (int) coord_x, (int) coord_y, orientation);
  

    printf("%s\n", coords);
    // UDP.beginPacket(UDP_SERVER_IP, UDP_PORT);
    // UDP.write(coords);
    // UDP.endPacket();
}




void print_info(void) {

    double absolute_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);
    printf("\nVelocity(x, y) | absolute = (%lf, %lf) | %lf\n", velocity_x, velocity_y, absolute_velocity);
    printf("Pos(x, y) = (%lf, %lf)\n", coord_x, coord_y);
    printf("Orientation = %lf\n\n", (dir/M_PI) * 180);

}



// ------------------------------------------------------------
// Acceleration logic prototype lite (where we only move forward, and moving implies acceleration)

// void update_movements(int desired_angle) {

//     // C tester code only
//     // ---------------------
//     if(desired_angle == -2) {
//         // Continue
//         coord_x += velocity_x;
//         coord_y += velocity_y;

//         return;
//     }
//     // ---------------------

//     double deg_dir = (dir / M_PI) * 180;

//     if(desired_angle == -1) {

//         // Stop
//         // Assume that stopping is so quick that the deceleration can be assumed constant
//         velocity_x = fmax(0, velocity_x - SLOWDOWN_ACCEL);
//         velocity_y = fmax(0, velocity_y - SLOWDOWN_ACCEL);

//     } else {

//         // Assume moving forwards for now
//         double curr_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);
//         double acc = fmin(MAX_ACC, (MAX_VELOCITY - velocity_x) * ACC_UNIT);
//         acc_x = acc * cos(dir);
//         acc_y = acc * sin(dir);

//         if(gt(deg_dir, desired_angle)) {
//             dir = fmax(MIN_ORIENTATION, dir - ANGLE_UNIT);
//         } else if(lt(deg_dir, desired_angle)) {
//             dir = fmin(MAX_ORIENTATION, dir + ANGLE_UNIT);
//         } 

//         velocity_x = fmin(MAX_VELOCITY, velocity_x + acc_x);
//         velocity_y = fmin(MAX_VELOCITY, velocity_y + acc_y);
//     }

//     coord_x += velocity_x;
//     coord_y += velocity_y;

// }

// ------------------------------------------------------------------------

// ------------------------------------------------------------
// Acceleration logic prototype (forwards only, pro)

/*
* @param desired_angle between MIN_ORIENTATION and MAX_ORIENTATION
* @param desired_accel either -2 (full stop), -1 (slow down), 0 (maintain velocity) or 1 (accelerate)
* Updates the car's coordinate approximation according to the desired parameters
*/
void update_movements(int desired_angle, int desired_accel) {

    if(desired_angle < MIN_ORIENTATION || desired_angle > MAX_ORIENTATION 
        || desired_accel < -2 || desired_accel > 1) {
        printf("Bad parameters\n");
        return;
    }

    // Current orientation in degrees
    double deg_dir = (dir / M_PI) * 180;
    // Update current orientation
    if(gt(deg_dir, desired_angle)) {
        dir = fmax(MIN_ORIENTATION, dir - ANGLE_UNIT);
    } else if(lt(deg_dir, desired_angle)) {
        dir = fmin(MAX_ORIENTATION, dir + ANGLE_UNIT);
    } 

    // Current total velocity (along x and y)
    double curr_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);

    // Movement logic
    if(desired_accel == -2) {
        
        // Stop

        // Assume that stopping is so quick that the deceleration can be assumed constant
        double stop_accel = curr_velocity > 0 ? -STOP_ACCEL : 0;
        acc_x = stop_accel * cos(dir);
        acc_y = stop_accel * sin(dir);
        // Update velocity
        velocity_x = fmax(0, velocity_x - acc_x);
        velocity_y = fmax(0, velocity_y - acc_y);

    } else if(desired_accel == -1) {

        // Slow down (for a corner for example)

        // Assume that we slow down at a constant pace
        double slowdown_accel = curr_velocity > 0 ? -SLOWDOWN_ACCEL : 0;
        double slowdown_velocity = fmax(0, curr_velocity - slowdown_accel);
        // Update velocity
        velocity_x = slowdown_velocity * cos(dir);
        velocity_y = slowdown_velocity * sin(dir);

    } else if(desired_accel == 0) {

        // Maintain current velocity
        velocity_x = curr_velocity * cos(dir);
        velocity_y = curr_velocity * sin(dir);

    } else if(desired_accel == 1) {

        // Accelerate
        double acc = fmin(MAX_ACC, (MAX_VELOCITY - curr_velocity) * ACC_UNIT);
        acc_x = acc * cos(dir);
        acc_y = acc * sin(dir); 

        // Update total velocity
        double new_velocity = fmin(MAX_VELOCITY, curr_velocity + acc);

        // Update x/y velocity
        velocity_x = new_velocity * cos(dir);
        velocity_y = new_velocity * sin(dir);

    }

    // Update coordinates
    coord_x += velocity_x;
    coord_y += velocity_y;
}

// ------------------------------------------------------------------------