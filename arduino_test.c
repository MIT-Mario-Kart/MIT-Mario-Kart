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
#define START_ORIENTATION 270
#define ANGLE_UNIT 1                 
#define MAX_ORIENTATION M_PI
#define MIN_ORIENTATION -MAX_ORIENTATION    // -180 deg <= orientation <= 180 deg
#define ANGLE_PRECISION 1                   // In degrees (if angle is within ± ANGLE_PRECISION 
                                            // it doesn't get updated)
#define MAX_VELOCITY 0.25
#define MAX_ACC MAX_VELOCITY
#define MAX_DECEL -MAX_ACC
#define ACC_UNIT 0.9 

#define GREEN_V MAX_VELOCITY
#define BLUE_V MAX_VELOCITY*0.7
#define RED_V MAX_VELOCITY*0.3
#define USR -1.0
#define BRAKE 0.0

// --------------------------------
// Test only values

#define FLOAT_PRECISION 0.0001

#define START_VELOCITY 0
#define START_X 0
#define START_Y 0

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

void update_movements(double desired_angle, double desired_velocity);
int gtWithin(double a, double b, double within);
int eqWithin(double a, double b, double within);
void print_info();
double radians(double angle);
int modulo(int nb, int base);

double coord_x = START_X;
double coord_y = START_Y;
double dir = START_ORIENTATION;
double velocity = START_VELOCITY;
double acc = 0;

int main(void) {

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
            velocity = 0;
            acc = 0;
            dir = START_ORIENTATION;
            coord_x = START_X;
            coord_y = START_Y;
            print_info();
        } else if(  strcmp(mov_input, FORWARD) == 0 || strcmp(mov_input, FORWARD_LEFT) == 0 || strcmp(mov_input, FORWARD_RIGHT) == 0
                    || strcmp(mov_input, REVERSE) == 0 || strcmp(mov_input, REVERSE_LEFT) == 0 
                    || strcmp(mov_input, REVERSE_RIGHT) == 0 || strcmp(mov_input, CONT) == 0) {


            desired_angle = desired_angle % 360;
            double right = dir - desired_angle;
            double left = desired_angle - dir;
            if(left < 0) left += 360;
            if(right < 0) right += 360;

            if(right < left) {
                // Turn right (negative desired_angle)
                update_movements((double) -abs(desired_angle), USR);
            } else {
                // Turn left (positive desired_angle)
                update_movements((double) abs(desired_angle), USR);
            }

            print_info();

        } else if(strcmp(mov_input, STOP) == 0) {

            update_movements(dir, BRAKE);
            print_info();

        } else {
            printf("Invalid input\n");
        }
    }

    return 0;
}

int gtWithin(double a, double b, double within) {
    return (a - b) > within;
}

int eqWithin(double a, double b, double within) {
    return fabs(a - b) < within;
}

void print_info(void) {

    printf("\nAcceleration: %lf\n", acc);
    printf("Velocity: %lf\n", velocity);
    printf("Pos(x, y) = (%lf, %lf)\n", coord_x, coord_y);
    printf("Orientation = %lf\n\n", dir);

}

double radians(double angle) {
    return (angle/180.0) * M_PI;
}

int modulo(int nb, int base) {
    int remainder = nb % base;
    return remainder < 0 ? remainder + base : remainder;
}
// ---------------------------------------------------------------------------------


/*
* @param desired_angle between MIN_ORIENTATION and MAX_ORIENTATION
* @param desired_velocity either -1 (user accelerate), 0 (brake), RED_V, BLUE_V or GREEN_V
* Updates the car's coordinate approximation according to the desired parameters
*/
void update_movements(double desired_angle, double desired_velocity) {

    // Update orientation

    double aDiff = fabs(dir - desired_angle);

    if (gtWithin(aDiff, 0, ANGLE_PRECISION)) {
        // Turn right if desired_orientation < 0 (i.e. decrement angle)
        if (desired_angle < 0) dir = modulo(dir - ANGLE_UNIT, 360);
        // Else turn left (i.e. increment angle)
        if (desired_angle > 0) dir = modulo(dir + ANGLE_UNIT, 360);
    }

    // Update acceleration, velocity and finally coordinates

    if(eqWithin(desired_velocity, BRAKE, FLOAT_PRECISION)) {

        // Start braking (user control)

        if(velocity > 0) {
            acc = MAX_DECEL;
        } else {
            acc = 0;
        }
            
        velocity = fmax(0, velocity + acc);
    } else if(eqWithin(desired_velocity, RED_V, FLOAT_PRECISION)) {

        double vDiff = RED_V - velocity;
        if(gtWithin(vDiff, 0, FLOAT_PRECISION)) {

            // RED_V is quicker than current velocity => accelerate

            // Update acceleration
            if(acc < 0) {
                acc = 0;
            } else {
                acc = fmin(MAX_ACC, fabs(MAX_VELOCITY - velocity)*ACC_UNIT);
            }

            // Update velocity
            velocity = fmin(RED_V, velocity + acc);
        

            
        } else if(gtWithin(-vDiff, 0, FLOAT_PRECISION)) {

            // RED_V is slower than current velocity => brake

            // Update acceleration
            if(gtWithin(velocity, RED_V, FLOAT_PRECISION)) {
                acc = MAX_DECEL;
            } else {
                acc = 0;
            }

            // Update velocity
            velocity = fmax(RED_V, velocity + acc);
        }


    } else if(eqWithin(desired_velocity, BLUE_V, FLOAT_PRECISION)) {

        double vDiff = BLUE_V - velocity;
        if(gtWithin(vDiff, 0, FLOAT_PRECISION)) {

            // BLUE_V is quicker than current velocity => accelerate

            // Update acceleration
            if(acc < 0) {
                acc = 0;
            } else {
                acc = fmin(MAX_ACC, fabs(MAX_VELOCITY - velocity)*ACC_UNIT);
            }

            // Update velocity
            velocity = fmin(BLUE_V, velocity + acc);
        

            
        } else if(gtWithin(-vDiff, 0, FLOAT_PRECISION)) {

            // BLUE_V is slower than current velocity => brake

            // Update acceleration
            if(gtWithin(velocity, BLUE_V, FLOAT_PRECISION)) {
                acc = MAX_DECEL;
            } else {
                acc = 0;
            }

            // Update velocity
            velocity = fmax(BLUE_V, velocity + acc);
        }


    } else if(eqWithin(desired_velocity, GREEN_V, FLOAT_PRECISION)) {

        double vDiff = GREEN_V - velocity;
        if(gtWithin(vDiff, 0, FLOAT_PRECISION)) {

            // GREEN_V is quicker than current velocity => accelerate

            // Update acceleration
            if(acc < 0) {
                acc = 0;
            } else {
                acc = fmin(MAX_ACC, fabs(MAX_VELOCITY - velocity)*ACC_UNIT);
            }

            // Update velocity
            velocity = fmin(GREEN_V, velocity + acc);
          
        } 

    } else if(eqWithin(desired_velocity, USR, FLOAT_PRECISION)) {
        
        // User only has accelerate/brake controls

        // Update acceleration
        acc = fmin(MAX_ACC, fabs(MAX_VELOCITY - velocity)*ACC_UNIT);

        // Update velocity
        velocity = fmin(MAX_VELOCITY, velocity + acc);
    }

    // Update coordinates after velocity and acceleration have been updated
    coord_x += velocity * cos(radians(dir));
    coord_y += velocity * sin(radians(dir));
}


// ------------------------------------------------------------------------