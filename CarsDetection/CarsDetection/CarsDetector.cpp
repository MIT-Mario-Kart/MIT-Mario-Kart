//
//  CarsDetector.cpp
//  CarsDetection

#include "CarsDetector.hpp"

using namespace cv;
using namespace std;


/**
 * Return an image with the cars detected
 */
DetectionResult CarsDetector::detect_cars(Mat image) {
    return detect_cars_f(image);
}

/**
    Return an image with the corners detected
 */
DetectionResult CarsDetector::detect_corners(Mat image) {
    return detect_corners_f(image);
}


/**
    Function used to detect a triangle and it's orientation
 */
std::vector<dataPoint> CarsDetector::detectTriangles(cv::Mat Mask){
    // find contours of shapes in the image
    vector<vector<Point>> contours;
    findContours(Mask, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    std::vector<dataPoint> detectedData;
    detectedData.reserve(contours.size());

    for (const auto& contour : contours) {
        
       double perimeter = arcLength(contour, true);

        vector<cv::Point> approx;
        // approximate the contour as a polygon
       approxPolyDP(contour, approx, 0.04 * perimeter, true);

       // get bounding box coordinates for contour
       cv::Rect boundingBox = boundingRect(contour);
        
       //get rid of small false positive && keep triangles only
       if (boundingBox.area() > 1000 && approx.size() == 3) {
           // get center point of bounding box
           Point centerPoint = Point(boundingBox.x + boundingBox.width / 2, boundingBox.y + boundingBox.height / 2);
           
           double dist1 = norm(approx[0] - approx[1]);
           double dist2 = norm(approx[1] - approx[2]);
           double dist3 = norm(approx[2] - approx[0]);

           // Determine the smallest side of the triangle
           // pt1 && pt2 are the two side points of the smallest side
           // pt3 is the intersection point of the two longest sides
           Point pt1, pt2, pt3;
           if (dist1 <= dist2 && dist1 <= dist3) {
               pt1 = approx[0];
               pt2 = approx[1];
               pt3 = approx[2];
           } else if (dist2 <= dist1 && dist2 <= dist3) {
               pt1 = approx[1];
               pt2 = approx[2];
               pt3 = approx[0];
           } else {
               pt1 = approx[2];
               pt2 = approx[0];
               pt3 = approx[1];
           }
           

           // Calculate the orientation of the line in degrees
           double dx = pt2.x - pt1.x;
           double dy = pt2.y - pt1.y;
           double angle = atan2(dy, dx) * 180.0 / CV_PI;
           angle = -angle;
           if (angle < 0) {
               angle += 360.0;
           }
           
           dataPoint p;
           p.width = boundingBox.width;
           p.height = boundingBox.height;
           p.centerPoint = centerPoint;
           p.frontEndPoint = pt3;
           p.angle = angle;

           detectedData.push_back(std::move(p));
       }
    }
    return detectedData;
}


/**
 Draw a box around a detected shape for a set of given dataPoint
 */
Mat CarsDetector::drawBoxes(cv::Mat Mask, std::vector<dataPoint> p, Scalar color){
    
    for (dataPoint center : p) {
        Point topLeft = center.centerPoint - Point(center.width / 2, center.height / 2);
        Rect boundingBox(topLeft, Size(center.width, center.height));
        rectangle(Mask, boundingBox, color, 2);
    }
    
    return Mask;
}


/**
 Draw a rectangle with as a side each center of the calibrating triangle.
 */
Mat CarsDetector::drawCalibrationRectangle(cv::Mat Mask, std::vector<dataPoint> p, Scalar color){
    // Find point with smaller x and y
    Point pt1;
    pt1.x = std::min(std::min(p[0].centerPoint.x, p[1].centerPoint.x), std::min(p[2].centerPoint.x, p[3].centerPoint.x));
    pt1.y = std::min(std::min(p[0].centerPoint.y, p[1].centerPoint.y), std::min(p[2].centerPoint.y, p[3].centerPoint.y));

    // Find point with bigger x and y
    Point pt2;
    pt2.x = std::max(std::max(p[0].centerPoint.x, p[1].centerPoint.x), std::max(p[2].centerPoint.x, p[3].centerPoint.x));
    pt2.y = std::max(std::max(p[0].centerPoint.y, p[1].centerPoint.y), std::max(p[2].centerPoint.y, p[3].centerPoint.y));
    
    cv::rectangle(Mask, pt1, pt2, color, 2);
    
    return Mask;
}

/**
    Function to detect only yellow equilateral triangles that are used for calibrating
 */
DetectionResult CarsDetector::detect_corners_f(Mat image) {
    DetectionResult result;
    
    Mat hlsColorspacedImage;
    cvtColor(image, hlsColorspacedImage, CV_RGB2HLS);
    
    //Keep only yellow triangles
    
    Mat yellowMask;
    Scalar yellowLower = Scalar(20, 70, 70);
    Scalar yellowUpper = Scalar(40, 255, 255);
     
    
    inRange(hlsColorspacedImage, yellowLower, yellowUpper, yellowMask);
    std::vector<dataPoint> yellowPoints = detectTriangles(yellowMask);
    
    Mat maskedImage;
    bitwise_and(image, image, maskedImage, yellowMask);
    
    if (yellowPoints.size() == 4){
        drawCalibrationRectangle(maskedImage, yellowPoints, Scalar(255, 255, 0));
    }
    
    drawBoxes(maskedImage, yellowPoints, Scalar(255, 255, 0));
    
    std::vector<std::tuple<cv::Point, double>> yP;
    yP.reserve(yellowPoints.size());
    for (const dataPoint& dp : yellowPoints) {
        yP.emplace_back(dp.centerPoint, dp.angle);
    }
    
    
    std::vector<std::tuple<cv::Point, double>> gP;
    std::vector<std::tuple<cv::Point, double>> bP;
    
    result.yellowDP = yP;
    result.maskedImage = maskedImage;
        
    return result;
}

/**
    Function to detect the cars - each being a coloured isosceles triangle (green, yellow or blue)
 
    How it works:
    - For each car color, filter the original image to keep only the range of the car color
      then detect polygones with three sides (triangles) - for each polygon find the center of
      the smallest side and draw a perpendicular line to find the orientation in degrees (0 - 360)
 */
DetectionResult CarsDetector::detect_cars_f(Mat image) {
    DetectionResult result;
    
    Mat hlsColorspacedImage;
    cvtColor(image, hlsColorspacedImage, CV_RGB2HLS);
    
    //YELLOW
    Mat yellowMask;
    Scalar yellowLower = Scalar(20, 70, 70);
    Scalar yellowUpper = Scalar(40, 255, 255);
    inRange(hlsColorspacedImage, yellowLower, yellowUpper, yellowMask);
    std::vector<dataPoint> yellowPoints = detectTriangles(yellowMask);
    
    
    //BLUE
    Mat blueMask;
    //Scalar blueLower = Scalar(90, 50, 200);
    //Scalar blueLower = Scalar(90, 70, 150);
    //Scalar blueUpper = Scalar(130, 255, 255);
    Scalar blueLower = Scalar(100, 70, 150);
    Scalar blueUpper = Scalar(130, 255, 255);
    inRange(hlsColorspacedImage, blueLower, blueUpper, blueMask);
    std::vector<dataPoint> bluePoints = detectTriangles(blueMask);
    
    //GREEN
    Mat greenMask;
    Scalar greenLower = Scalar(50, 40, 50);
    Scalar greenUpper = Scalar(90, 255, 255);
    inRange(hlsColorspacedImage, greenLower, greenUpper, greenMask);
    std::vector<dataPoint> greenPoints = detectTriangles(greenMask);
    
    //ORANGE
    Mat orangeMask;
    Scalar orangeLower = Scalar(0, 70, 100);      // Lower threshold values for the orange color in HLS
    Scalar orangeUpper = Scalar(20, 255, 255);      // Upper threshold values for the orange color in HLS
    inRange(hlsColorspacedImage, orangeLower, orangeUpper, orangeMask);

    // Detect orange points or perform any desired operations
    std::vector<dataPoint> orangePoints = detectTriangles(orangeMask);
    
    //PINK
    Mat pinkMask;
    Scalar pinkLower = Scalar(140, 70, 50);    // Lower threshold values for the purple color in HLS
    Scalar pinkUpper = Scalar(170, 255, 255);  // Upper threshold values for the purple color in HLS
    inRange(hlsColorspacedImage, pinkLower, pinkUpper, pinkMask);

    // Detect orange points or perform any desired operations
    std::vector<dataPoint> pinkPoints = detectTriangles(pinkMask);
    
    //RED
    Mat redMask;
    Scalar redLower = Scalar(170, 70, 50);      // Lower threshold values for the cyan color in HLS
    Scalar redUpper = Scalar(210, 255, 255);    // Upper threshold values for the cyan color in HLS
    inRange(hlsColorspacedImage, redLower, redUpper, redMask);
    
    // Detect orange points or perform any desired operations
    std::vector<dataPoint> redPoints = detectTriangles(redMask);
    
    
    // combine masks into a single image
    Mat colorMask = yellowMask + blueMask + greenMask + orangeMask + pinkMask + redMask;
    Mat maskedImage;
    bitwise_and(image, image, maskedImage, colorMask);
    
    
    drawBoxes(maskedImage, yellowPoints, Scalar(255, 255, 0));
    drawBoxes(maskedImage, bluePoints, Scalar(0, 0, 255));
    drawBoxes(maskedImage, greenPoints, Scalar(0, 255, 0));
    drawBoxes(maskedImage, orangePoints, Scalar(255, 128, 0));
    drawBoxes(maskedImage, pinkPoints, Scalar(160, 32, 240));
    drawBoxes(maskedImage, redPoints, Scalar(255, 0, 0));
    
    // Convert detected points to tuples
    vector<tuple<Point, double>> yP, gP, bP, oP, pP, rP;
    yP.reserve(yellowPoints.size());
    transform(yellowPoints.begin(), yellowPoints.end(), back_inserter(yP),
        [](const dataPoint& dp) {
            return make_tuple(dp.frontEndPoint, dp.angle);
        }
    );
    gP.reserve(greenPoints.size());
    transform(greenPoints.begin(), greenPoints.end(), back_inserter(gP),
        [](const dataPoint& dp) {
            return make_tuple(dp.frontEndPoint, dp.angle);
        }
    );
    bP.reserve(bluePoints.size());
    transform(bluePoints.begin(), bluePoints.end(), back_inserter(bP),
        [](const dataPoint& dp) {
            return make_tuple(dp.frontEndPoint, dp.angle);
        }
    );
    oP.reserve(orangePoints.size());
    transform(orangePoints.begin(), orangePoints.end(), back_inserter(oP),
        [](const dataPoint& dp) {
            return make_tuple(dp.frontEndPoint, dp.angle);
        }
    );
    pP.reserve(pinkPoints.size());
    transform(pinkPoints.begin(), pinkPoints.end(), back_inserter(pP),
        [](const dataPoint& dp) {
            return make_tuple(dp.frontEndPoint, dp.angle);
        }
    );
    rP.reserve(redPoints.size());
    transform(redPoints.begin(), redPoints.end(), back_inserter(rP),
        [](const dataPoint& dp) {
            return make_tuple(dp.frontEndPoint, dp.angle);
        }
    );
    
    result.yellowDP = yP;
    result.greenDP = gP;
    result.blueDP = bP;
    result.orangeDP = oP;
    result.pinkDP = pP;
    result.redDP = rP;
    result.maskedImage = maskedImage;
        
    return result;
}
