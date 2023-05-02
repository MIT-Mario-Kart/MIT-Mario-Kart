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
#include <time.h>

// #ifndef STASSID
// #define STASSID "IP"
// #define STAPSK "PASS"
// #endif

// #define UDP_SERVER_IP "10.172.10.2"
// #define UDP_PORT 8888

#define START_ORIENTATION M_PI/2            // 90 deg = facing forwards on trig circle
#define ANGLE_UNIT M_PI/100                 // ~ 1.8 deg
#define MAX_TURN_ANGLE 39                   // 39 = maximum turning angle
#define SERVO_SPEED 1                       // How many degrees the servo turns in one iteration
#define MAX_ORIENTATION 2*M_PI              // 0 deg <= orientation <= 360 deg
#define MIN_ORIENTATION 0                   
#define ANGLE_PRECISION 1                   // In degrees (if angle is within ± ANGLE_PRECISION 
                                            // it doesn't get updated)
#define MAX_VELOCITY 0.025
#define STOP_DECEL 0.025
#define ACC_UNIT 0.025
#define MAX_ACC 0.025

#define START_X 0
#define START_Y 0

// --------------------------------
// Test only values

#define START_VELOCITY 0
#define START_DEG_ORIENTATION 90

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

    dir = (START_DEG_ORIENTATION/180.0) * M_PI;
    velocity_x = START_VELOCITY * cos(dir);
    velocity_y = START_VELOCITY * sin(dir);

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
            update_movements(desired_angle, 1);
            send_coords();
            print_info();
        } else if(strcmp(mov_input, STOP) == 0) {

            update_movements(90, -1);

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
//         velocity_x = fmax(0, velocity_x - SLOWDOWN_DECCEL);
//         velocity_y = fmax(0, velocity_y - SLOWDOWN_DECCEL);

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

    double total_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);
    double total_acc = sqrt(acc_x * acc_x + acc_y * acc_y);
    printf("\nAcceleration(x, y) | absolute = (%lf, %lf) | %lf\n", acc_x, acc_y, total_acc);
    printf("Velocity(x, y) | absolute = (%lf, %lf) | %lf\n", velocity_x, velocity_y, total_velocity);
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
//         velocity_x = fmax(0, velocity_x - SLOWDOWN_DECCEL);
//         velocity_y = fmax(0, velocity_y - SLOWDOWN_DECCEL);

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
* @param desired_accel either -1 (slow down), 0 (maintain velocity) or 1 (accelerate)
* Updates the car's coordinate approximation according to the desired parameters
*/
void update_movements(int desired_angle, int desired_accel) {

    if(desired_angle < (MIN_ORIENTATION/M_PI)*180 || desired_angle > (MAX_ORIENTATION/M_PI)*180 
        || desired_accel < -1 || desired_accel > 1) {
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

    // Current total acceleration
    double curr_acc = sqrt(acc_x * acc_x + acc_y * acc_y);

    // Current total velocity (along x and y)
    double curr_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);

    // Movement logic
    if(desired_accel == -1) {
        
        // Slow down

        // Assume that stopping is so quick that the deceleration can be assumed constant
        curr_acc = curr_velocity > 0 ? fmax(-STOP_DECEL, curr_acc - ACC_UNIT) : 0;
        acc_x = curr_acc * cos(dir);
        acc_y = curr_acc * sin(dir);
        // Update velocity
        curr_velocity = fmax(0, curr_velocity + curr_acc);
        velocity_x = curr_velocity * cos(dir);
        velocity_y = curr_velocity * sin(dir);

    } else if(desired_accel == 0) {

        // Maintain speed

        // Don't change total acceleration, update for orientation
        acc_x = curr_acc * cos(dir);
        acc_y = curr_acc * sin(dir);
        // Don't change total velocity, update for orientation
        velocity_x = curr_velocity * cos(dir);
        velocity_y = curr_velocity * sin(dir);

    } else if(desired_accel == 1) {

        // Accelerate 

        // Update acceleration (the higher the speed, the lower the acceleration)
        curr_acc = fmin(MAX_ACC, (MAX_VELOCITY - curr_velocity) * ACC_UNIT);
        acc_x = curr_acc * cos(dir);
        acc_y = curr_acc * sin(dir); 
        // Update velocity
        curr_velocity = fmin(MAX_VELOCITY, curr_velocity + curr_acc);
        velocity_x = curr_velocity * cos(dir);
        velocity_y = curr_velocity * sin(dir);

    }

    // Update coordinates
    coord_x += velocity_x;
    coord_y += velocity_y;
}

// ------------------------------------------------------------------------