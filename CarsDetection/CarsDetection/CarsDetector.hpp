//
//  CarsDetector.hpp
//  CarsDetection


/**
 The bridging header file is important as it will allow us to consume our cars detector algorithm by allowing different languages to talk to each other. 
 */

#include <opencv2/opencv.hpp>
#include <opencv2/core/types.hpp>

using namespace cv;
using namespace std;

struct DetectionResult {
    std::vector<std::tuple<cv::Point, double>> yellowDP;
    std::vector<std::tuple<cv::Point, double>> greenDP;
    std::vector<std::tuple<cv::Point, double>> blueDP;
    std::vector<std::tuple<cv::Point, double>> orangeDP;
    std::vector<std::tuple<cv::Point, double>> pinkDP;
    std::vector<std::tuple<cv::Point, double>> redDP;
    Mat maskedImage;
};

/*
    frontEndPoint is the intersection of the two longer sides of the isocele triangle (front end position of the car)
    centerPoint is the center point of the car (only used for calibrating with the yellow equilateral triangles)
 */
struct dataPoint {
    cv::Point frontEndPoint;
    cv::Point centerPoint;
    int width;
    int height;
    double angle;
};

class CarsDetector {
    
    public:
    
    /**
     Returns image with cars overlay
     */
    DetectionResult detect_cars(Mat image);
    
    /**
     Returns image with corners overlay
     */
    DetectionResult detect_corners(Mat image);

    
    private:
    
    /**
     Filters yellow and white colors on image
     */
    DetectionResult detect_cars_f(Mat image);
    
    /**
     Filters yellow and white colors on image
     */
    DetectionResult detect_corners_f(Mat image);
    
    
    std::vector<dataPoint> detectTriangles(cv::Mat Mask);
    
    Mat drawBoxes(cv::Mat Mask, std::vector<dataPoint> p, Scalar color);
    
    Mat drawCalibrationRectangle(cv::Mat Mask, std::vector<dataPoint> p, Scalar color);
    
};
