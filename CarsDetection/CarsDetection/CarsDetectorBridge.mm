//
//  CarsDetectorBridge.m
//  CarsDetection

#import <opencv2/opencv.hpp>
#import <opencv2/imgcodecs/ios.h>
#import <Foundation/Foundation.h>
#import "CarsDetectorBridge.h"
#include "CarsDetector.hpp"

#include <stdio.h>
#include <stdlib.h>
#include <opencv2/core/core_c.h>
#include <opencv2/calib3d/calib3d_c.h>

@implementation CarsDetectorBridge

/**
 CarsDetectorBridge converts UIImages into OpenCV image representation. Then it runs cars detection which returns an image with cars overlayed on top of it. And finally converts the OpenCV image representation back to UIImage.
 */


//Camera matrix value found out via calibration & slightly manually modified to perfectly fit the conditions we are in
//Used to fight lens distorsion so that our coordinates are perfectly linearly distributed
cv::Mat cameraMatrix = (cv::Mat_<double>(3, 3) << 2.90467004e+03, 0.00000000e+00, 0,
                                                     0.00000000e+00, 2.91313128e+03, 0,
                                                     0.00000000e+00, 0.00000000e+00, 1.00000000e+00);



//Distorsion coefficiants found via calibration & slightly manually modified to perfectly fit the conditions we are in
//Used to fight lens distorsion so that our coordinates are perfectly linearly distributed

//The first three parameters are radial distortion coefficients.
//The next two parameters are tangential distortion coefficients (supposed to be zero here as the phone is perfectly parallel to the circuit).
cv::Mat distCoeffs = (cv::Mat_<double>(1, 5) << -0.41882023e-01, 0, 0, 0, 0);

/**
    C interface that takes the UIImage undistort it to revert effects of lens distorsion and pass it to the CarsDetector in the correct format to detect the cars.
 */
- (NSDictionary *) detectCarsIn: (UIImage *) image withValues: (NSArray<NSValue *> *) values{
    // convert uiimage to mat
    cv::Mat opencvImage;
    UIImageToMat(image, opencvImage, true);
    cv::Mat convertedColorSpaceImage;
    cv::cvtColor(opencvImage, convertedColorSpaceImage, CV_RGBA2RGB);
    
    
    cv::Mat rectifiedImage;
    cv::undistort(convertedColorSpaceImage, rectifiedImage, cameraMatrix, distCoeffs);
    
    // Run cars detection
    CarsDetector carsDetector;
    //DetectionResult imageWithCarsDetected = carsDetector.detect_cars(convertedColorSpaceImage);
    DetectionResult imageWithCarsDetected = carsDetector.detect_cars(rectifiedImage);
    
    // convert mat to uiimage
    UIImage *maskedImage = MatToUIImage(imageWithCarsDetected.maskedImage);
    
    // Convert the detected points to arrays of NSValue objects
    NSMutableArray *yellowDP = [self convertPointsToNSValues:imageWithCarsDetected.yellowDP];
    NSMutableArray *greenDP = [self convertPointsToNSValues:imageWithCarsDetected.greenDP];
    NSMutableArray *blueDP = [self convertPointsToNSValues:imageWithCarsDetected.blueDP];
    NSMutableArray *orangeDP = [self convertPointsToNSValues:imageWithCarsDetected.orangeDP];
    NSMutableArray *pinkDP = [self convertPointsToNSValues:imageWithCarsDetected.pinkDP];
    NSMutableArray *redDP = [self convertPointsToNSValues:imageWithCarsDetected.redDP];
    
    // Convert the detected angles to arrays of NSNumber objects
    NSMutableArray *yellowAngles = [self convertAnglesToNSNumbers:imageWithCarsDetected.yellowDP];
    NSMutableArray *greenAngles = [self convertAnglesToNSNumbers:imageWithCarsDetected.greenDP];
    NSMutableArray *blueAngles = [self convertAnglesToNSNumbers:imageWithCarsDetected.blueDP];
    NSMutableArray *orangeAngles = [self convertAnglesToNSNumbers:imageWithCarsDetected.orangeDP];
    NSMutableArray *pinkAngles = [self convertAnglesToNSNumbers:imageWithCarsDetected.pinkDP];
    NSMutableArray *redAngles = [self convertAnglesToNSNumbers:imageWithCarsDetected.redDP];
    
    // return maskedImage and detectedPoints
    return @{@"maskedImage": maskedImage,
             @"yellowDP": yellowDP,
             @"greenDP": greenDP,
             @"blueDP": blueDP,
             @"orangeDP":orangeDP,
             @"pinkDP":pinkDP,
             @"redDP":redDP,
             @"yellowAngles": yellowAngles,
             @"greenAngles": greenAngles,
             @"blueAngles": blueAngles,
             @"orangeAngles": orangeAngles,
             @"pinkAngles": pinkAngles,
             @"redAngles": redAngles
    };
}
    
/**
    C interface that takes the UIImage undistort it to revert effects of lens distorsion and pass it to the CarsDetector in the correct format to detect corners used for calibration.
 */
- (NSDictionary *) detectCornersIn: (UIImage *) image {
    
    // convert uiimage to mat
    cv::Mat opencvImage;
    UIImageToMat(image, opencvImage, true);
    cv::Mat convertedColorSpaceImage;
    cv::cvtColor(opencvImage, convertedColorSpaceImage, CV_RGBA2RGB);
    
    // Rectify the image using the distortion parameters
    cv::Mat rectifiedImage;
    cv::undistort(convertedColorSpaceImage, rectifiedImage, cameraMatrix, distCoeffs);
    
    // Run cars detection
    CarsDetector carsDetector;
    DetectionResult imageWithCarsDetected = carsDetector.detect_corners(rectifiedImage);
    
    UIImage *maskedImage = MatToUIImage(imageWithCarsDetected.maskedImage);
    
    //FOR DEBUGGING: (see the effect of the calibration matrix)
    //UIImage *maskedImage = MatToUIImage(rectifiedImage);
    
    NSMutableArray *yellowDP = [self convertPointsToNSValues:imageWithCarsDetected.yellowDP];
    NSMutableArray *greenDP = [[NSMutableArray alloc] init];
    NSMutableArray *redDP = [[NSMutableArray alloc] init];
    
    // return maskedImage and detectedPoints
    return @{@"maskedImage": maskedImage,
             @"yellowDP": yellowDP,
             @"greenDP": greenDP,
             @"redDP": redDP};
}

/**
    Helper method to convert a std::vector<std::tuple<cv::Point, double>> to an NSMutableArray of NSValue, each NSValue corresponding to a Point
 */
- (NSMutableArray *)convertPointsToNSValues:(const std::vector<std::tuple<cv::Point, double>> &)points {
    NSMutableArray *result = [NSMutableArray arrayWithCapacity:points.size()];
    for (const std::tuple<cv::Point, double> &tuple : points) {
        cv::Point point = std::get<0>(tuple);
        NSValue *value = [NSValue valueWithCGPoint:CGPointMake(point.x, point.y)];
        [result addObject:value];
    }
    return result;
}

/**
    Helper method to convert a std::vector<std::tuple<cv::Point, double>> to an NSMutableArray  of NSNumber, each NSNumber corresponding to an angle
 */
- (NSMutableArray *)convertAnglesToNSNumbers:(const std::vector<std::tuple<cv::Point, double>> &)points {
    NSMutableArray *result = [NSMutableArray arrayWithCapacity:points.size()];
    for (const std::tuple<cv::Point, double> &tuple : points) {
        double angle = std::get<1>(tuple);
        NSNumber *angleNumber = [NSNumber numberWithDouble:angle];
        [result addObject:angleNumber];
    }
    return result;
}

@end
