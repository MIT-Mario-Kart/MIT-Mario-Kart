//
//  ViewController.swift
//  CarsDetection
//
//  Created by Anurag Ajwani on 28/04/2019.
//  Copyright © 2019 Anurag Ajwani. All rights reserved.
//  Modified by Arthur Bigot for our project

import UIKit
import AVFoundation
import Network
import MobileCoreServices
import UserNotifications
//import NetworkExtension
//import SystemConfiguration.CaptiveNetwork


class ViewController: UIViewController, AVCaptureVideoDataOutputSampleBufferDelegate, UNUserNotificationCenterDelegate, AVCapturePhotoCaptureDelegate {
    
        
    //PROCESSUS TO SETUP
    //CONNECT THE PHONE TO THE LOCAL NETWORK ON WHICH THE SERVER IS RUNNING
    //FIND THE SERVER COMPUTER IP'S ADDR AND PORT AND HARCODE IT
    //LAUNCH THE SERVER
    //LAUNCH THE APP
    //PLACE THE 4 YELLOW TRIANGLES TO CALIBRATE THE CIRCUIT
    

    @IBOutlet weak var imageView: UIImageView!
    
    private var captureSession: AVCaptureSession = AVCaptureSession()
    private let videoDataOutput = AVCaptureVideoDataOutput()
    
    private var readyToSend = false;
    private var calibrated = false;
    private var savedCalibrationBody = "";
    
    private var lastCalibrationPoints: [NSValue] = []
    private var lastCalibrationTimestamp: TimeInterval = -1
    private var lastNotificationTimestamp: TimeInterval = -1
    
    var connection: NWConnection!
    var listener: NWListener!
    
    

    // MARK: - UIViewController
    override func viewDidLoad() {
        super.viewDidLoad()
        self.addCameraInput()
        self.getFrames()
        self.captureSession.startRunning()
        self.initTCPConnection(sendCalib: false)
            
        /*
        UNUserNotificationCenter.current().delegate = self
        
        // Request permission to show notifications
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
            if let error = error {
                print("Error requesting authorization: \(error.localizedDescription)")
            }
        }
         */
        
    }

    
    // Handle foreground notifications and display them
    func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification, withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        let options: UNNotificationPresentationOptions = [.banner, .sound]
        completionHandler(options)
    }

    
    // MARkK: - AVCaptureVideoDataOutputSampleBufferDelegate
    func captureOutput(
        _ output: AVCaptureOutput,
        didOutput sampleBuffer: CMSampleBuffer,
        from connection: AVCaptureConnection) {
        
        guard let  imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        CVPixelBufferLockBaseAddress(imageBuffer, CVPixelBufferLockFlags.readOnly)
        let baseAddress = CVPixelBufferGetBaseAddress(imageBuffer)
        let bytesPerRow = CVPixelBufferGetBytesPerRow(imageBuffer)
        let width = CVPixelBufferGetWidth(imageBuffer)
        let height = CVPixelBufferGetHeight(imageBuffer)
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        var bitmapInfo: UInt32 = CGBitmapInfo.byteOrder32Little.rawValue
        bitmapInfo |= CGImageAlphaInfo.premultipliedFirst.rawValue & CGBitmapInfo.alphaInfoMask.rawValue
        let context = CGContext(data: baseAddress, width: width, height: height, bitsPerComponent: 8, bytesPerRow: bytesPerRow, space: colorSpace, bitmapInfo: bitmapInfo)
        guard let quartzImage = context?.makeImage() else { return }
        CVPixelBufferUnlockBaseAddress(imageBuffer, CVPixelBufferLockFlags.readOnly)
        let image = UIImage(cgImage: quartzImage)
          
            
            
            
            if(self.calibrated){
                if let imageWithLaneDetected = CarsDetectorBridge().detectCars(in: image, with: lastCalibrationPoints) {
                    // safely unwrap the dictionary and access its values
                    let maskedImage = imageWithLaneDetected["maskedImage"] as! UIImage
                    
                    // safely unwrap the dictionary and access its values
                    //let imageWidth = imageWithLaneDetected["imageWidth"] as! CGFloat
                    // safely unwrap the dictionary and access its values
                    //let imageHeight = imageWithLaneDetected["imageHeight"] as! CGFloat
                    
                    //list of NSPoints
                    var yellowCenterPoints = imageWithLaneDetected["yellowDP"] as! [NSValue]
                    var greenCenterPoints = imageWithLaneDetected["greenDP"] as! [NSValue]
                    var blueCenterPoints = imageWithLaneDetected["blueDP"] as! [NSValue]
                    var orangeCenterPoints = imageWithLaneDetected["orangeDP"] as! [NSValue]
                    var pinkCenterPoints = imageWithLaneDetected["pinkDP"] as! [NSValue]
                    var redCenterPoints = imageWithLaneDetected["redDP"] as! [NSValue]
                    
                    var yellowCenterAngles = imageWithLaneDetected["yellowAngles"] as! [NSValue]
                    var greenCenterAngles = imageWithLaneDetected["greenAngles"] as! [NSValue]
                    var blueCenterAngles = imageWithLaneDetected["blueAngles"] as! [NSValue]
                    var orangeCenterAngles = imageWithLaneDetected["orangeAngles"] as! [NSValue]
                    var pinkCenterAngles = imageWithLaneDetected["pinkAngles"] as! [NSValue]
                    var redCenterAngles = imageWithLaneDetected["redAngles"] as! [NSValue]
                    
                    
                    //remove points that are outside the calibrated points.
                    var (sY, aY) = filterPoints(points: yellowCenterPoints, angles: yellowCenterAngles);
                    var (sG, aG) = filterPoints(points: greenCenterPoints, angles: greenCenterAngles);
                    var (sB, aB) = filterPoints(points: blueCenterPoints, angles: blueCenterAngles);
                    var (sO, aO) = filterPoints(points: orangeCenterPoints, angles: orangeCenterAngles);
                    var (sP, aP) = filterPoints(points: pinkCenterPoints, angles: pinkCenterAngles);
                    var (sR, aR) = filterPoints(points: redCenterPoints, angles: redCenterAngles);
                    
                    //FORMAT
                    //CAL
                    //{"yellow": "[NSPoint: {930, 1399}, NSPoint: {149, 1372}, NSPoint: {949, 541}, NSPoint: {156, 537}]", "green": "[]", "blue" : "[]"}
                    
                    let dataString = "{\"yellow\": \"" + sY + "\", \"green\":\"" + sG + "\", \"blue\" : \"" + sB + "\", \"orange\" : \"" + sO + "\", \"pink\" : \"" + sP + "\", \"red\" : \"" + sR + "\", \"yellowAngles\": \"" + aY + "\", \"greenAngles\": \"" + aG + "\", \"blueAngles\" : \"" + aB + "\", \"orangeAngles\" : \"" + aO + "\", \"pinkAngles\" : \"" + aP + "\", \"redAngles\" : \"" + aR + "\"}\n"
                    
                    let bodyString = "CAM\n" + dataString
                    
                    sendMSG(messageData: bodyString)
                    
                    /*
                     OpenCV uses a right-handed Cartesian coordinate system, where the positive x-axis points to the right, the positive y-axis points downwards, and the positive z-axis points out of the screen towards the viewer.

                     In OpenCV, images are represented as arrays of pixels, where the origin (0,0) is located at the top-left corner of the image. The x-axis extends horizontally to the right and the y-axis extends vertically downwards, similar to the iOS coordinate system.

                     However, the OpenCV coordinate system is also used to specify the 3D location of points in space, in which case the x-axis points to the right, the y-axis points upwards, and the z-axis points backwards away from the viewer. This convention is commonly used in computer vision and graphics applications, where the z-axis is often used to represent depth or distance.

                     It's worth noting that when working with images in OpenCV, the coordinate system is typically flipped along the y-axis compared to the iOS coordinate system. This means that the y-axis is inverted, with higher values at the bottom of the image and lower values at the top. Therefore, when converting between coordinate systems, you may need to account for this difference in orientation.
                     */
                    
                    // x: 0 -> 1080
                    // y: 0 -> 1920
                    
                    // x and y are in OpenCV coordinate format for now.
                    
                    
                    /*
                     In iOS, the coordinate system is a Cartesian coordinate system with the origin (0,0) located at the top-left corner of the screen. The x-axis extends horizontally to the right and the y-axis extends vertically downwards.

                     The units of measurement in the coordinate system are points, which are abstract units that are roughly equivalent to one pixel on a non-Retina display. On Retina displays, a point corresponds to two pixels in each dimension.

                     The coordinate system is used to specify the location and size of UI elements on the screen, such as views and controls. The coordinates are specified as a CGPoint struct, which contains an x and a y value representing the horizontal and vertical distance from the origin, respectively.

                     Note that the coordinate system is relative to the screen and does not take into account the physical orientation of the device. For example, if the device is in landscape orientation, the x-axis will be horizontal but it will be oriented differently than in portrait orientation.
                     */
                
                    
                    // update UI on the main thread
                    DispatchQueue.main.async {
                        self.imageView.image = maskedImage
                    }
                }
            }else{
                //we want to calibrate here // send the
                if let imageWithLaneDetected = CarsDetectorBridge().detectCorners(in: image) {
                    let maskedImage = imageWithLaneDetected["maskedImage"] as! UIImage
                    //list of NSPoints
                    let yellowCenterPoints = imageWithLaneDetected["yellowDP"] as! [NSValue]
                    let sY = String(describing: yellowCenterPoints)
                    
                    //only in the case we have 4 yellow elements stable for the last 10 seconds
                    //we send the calibration data to the server
                    //print(yellowCenterPoints)
                    
                    //{"yellow": "[NSPoint: {930, 1399}-angle, NSPoint: {149, 1372}, NSPoint: {949, 541}, NSPoint: {156, 537}]", "green": "[]", "blue" : "[]"}
                    if(isCalibrationPointsStable(yellowCenterPoints: yellowCenterPoints)){
                        let dataString = "{\"yellow\": \"" + sY + "\", \"green\": \"[]\", \"blue\" : \"[]\", \"yellowAngles\": \"[]\", \"greenAngles\": \"[]\", \"blueAngles\" : \"[]\"}\n"
                        let bodyString = "CAL\n" + dataString
                        
                        
                        savedCalibrationBody = bodyString
                        
                        print("Sending calibration data to server")
                        
                        sendMSG(messageData: bodyString)
                    }
                    
                    // update UI on the main thread
                    DispatchQueue.main.async {
                        self.imageView.image = maskedImage
                    }
                }
            }
    }
    
    // MARK: - Private functions
    private func addCameraInput() {
        guard let device = AVCaptureDevice.DiscoverySession(
            deviceTypes: [.builtInWideAngleCamera, .builtInDualCamera, .builtInTrueDepthCamera],
            mediaType: .video,
            position: .back).devices.first else {
                fatalError("No back camera device found, run on an iOS device and not a simulator")
        }

        let cameraInput = try! AVCaptureDeviceInput(device: device)
        self.captureSession.addInput(cameraInput)
    }
    
    
    private func getFrames() {
        videoDataOutput.videoSettings = [(kCVPixelBufferPixelFormatTypeKey as NSString) : NSNumber(value: kCVPixelFormatType_32BGRA)] as [String : Any]
        videoDataOutput.alwaysDiscardsLateVideoFrames = true
        videoDataOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "camera.frame.processing.queue"))
        captureSession.sessionPreset = .high;
        self.captureSession.addOutput(videoDataOutput)
        guard let connection = self.videoDataOutput.connection(with: AVMediaType.video),
            connection.isVideoOrientationSupported else { return }
        connection.videoOrientation = .portrait
    }
    
    func filterPoints(points: [NSValue], angles: [NSValue]) -> (String, String) {
        guard lastCalibrationPoints.count == 4 else {
            // If the calibration points are not yet set, return the original list of points.
            return (String(describing: points), String(describing: angles))
        }
        
        let rect = CGRect(points: self.lastCalibrationPoints)
        var filteredPoints = [NSValue]()
        var filteredAngles = [NSNumber]()
            
        for (index, point) in points.enumerated() {
            let cgPoint = point.cgPointValue
            if rect.contains(cgPoint) {
                if let angleValue = angles[index] as? NSNumber {
                            filteredPoints.append(point)
                            filteredAngles.append(angleValue)
                }
            }
        }
            
        return (String(describing: filteredPoints), String(describing: filteredAngles))

    }
    
    
    //function to send a notification on the device
    private func sendNotification(message: String, needToBeSent: Bool) {
        
        if(self.lastNotificationTimestamp == -1 || (Date().timeIntervalSince1970 - lastNotificationTimestamp) >= 1 || needToBeSent){
            // Request permission to show notifications
            let content = UNMutableNotificationContent()
            content.title = "Information"
            content.body = message
            content.sound = UNNotificationSound.defaultCritical
            
            // Set the notification trigger for now
            let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
            
            // Create the notification request
            let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: trigger)
            
            // Schedule the notification
            UNUserNotificationCenter.current().add(request) { error in
                if let error = error {
                    print("Error scheduling notification: \(error.localizedDescription)")
                }
            }
            
            lastNotificationTimestamp = Date().timeIntervalSince1970
        }
    }
    
    private func initTCPConnection(sendCalib: Bool) {
        //port on which the server is listening
        let PORT: NWEndpoint.Port = 8899
        //address of the server on the local network
        let ipAddress :NWEndpoint.Host = "172.20.10.6"
        
        let queue = DispatchQueue(label: "TCP Client Queue")
        let tcp = NWProtocolTCP.Options.init()
        tcp.noDelay = true
        let params = NWParameters.init(tls: nil, tcp: tcp)
        
        connection = NWConnection(to: NWEndpoint.hostPort(host: ipAddress, port: PORT), using: params)
        
        connection.stateUpdateHandler = {(newState) in
            switch (newState) {
                case .ready:
                    print("Connected to the Server.")
                    self.readyToSend = true
                    // create a listener object
                    let listener = try! NWListener(using: .udp, on: 12345)
                    self.listener = listener;

                    // set up the listener's state update handler
                    self.listener.stateUpdateHandler = { newState in
                        switch newState {
                        case .ready:
                            print("Listener started")
                        case .failed(let error):
                            print("Listener failed with error: \(error)")
                        case .cancelled:
                            print("Listener cancelled")
                        default:
                            break
                        }
                    }

                    // set up the listener's new connection handler
                    self.listener.newConnectionHandler = { newConnection in
                        //the hacky way we found is to open a new connection from the server side on a special port to tell the
                        //application we are calibrated
                        print("Server is now calibrated.")
                        self.sendNotification(message: "Server is now calibrated.", needToBeSent: true)
                        self.calibrated = true
                        self.listener.cancel()
                    }

                    // start the listener
                    self.listener.start(queue: .global())
                
                case .cancelled:
                    print("Connection was cancelled")
                    self.readyToSend = false
                    self.calibrated = false
                   
                //case .failed(let error):
                case .failed:
                    //print("Connection failure, error: \(error.localizedDescription)")
                    print("Server crashed. Reconnecting in 500 ms.")
                    self.readyToSend = false
                    self.calibrated = false
                    
                    DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                        self.listener.cancel()
                        self.connection.cancel()
                        self.initTCPConnection(sendCalib: true)
                    }
                
                case .preparing:
                    print("Preparing")
                
                case .waiting:
                    //we will be in this state if we try to connect to the server but we get refused
                    print("Waiting")
                    DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                        self.listener.cancel()
                        self.connection.cancel()
                        self.initTCPConnection(sendCalib: true)
                    }
                    
                    
                default:
                    print("Socket entered state \(String(describing: newState))")
                    self.calibrated = false
                    self.readyToSend = false
                
                    DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                        self.listener.cancel()
                        self.connection.cancel()
                        self.initTCPConnection(sendCalib: true)
                    }
                
            }
        }
        
        connection.receiveMessage { (data, context, isComplete, error) in
            if let data = data {
                let message = String(decoding: data, as: UTF8.self)
                print("Received message: \(message)")
                
                // respond to the message if needed
                if message == "ACK" {
                    let response = "special message received"
                    self.connection.send(content: response.data(using: .utf8), completion: .contentProcessed({ (error) in
                        if let error = error {
                            print("Error sending response: \(error)")
                        } else {
                            print("Response sent")
                        }
                    }))
                }
            }
            if let error = error {
                print("Error receiving message: \(error)")
            }
        }
        
        print("Creating TCP Socket\nTrying to connect to the Server..")
        connection.start(queue: queue)
        
        
        //self.sendNotification(message: "Please calibrate the circuit.", needToBeSent: true)
        
        if(sendCalib){
            print("Sending calibration data to server")
            //sendNotification(message: "Sending calibration data to server.", needToBeSent: false)
            
            sendMSG(messageData: savedCalibrationBody)
        }
    }
    
    //Function to send a message to the Server
    //MessageData needs to be a string
    //If the connection isn't open with the server, message won't be sent
    private func sendMSG(messageData: String){
        //in case the connection isn't open yet, don't try to send anything
        if(!readyToSend){
            print("Can't send data, connection isn't set up!")
            return;
        }
        
        
        let content: Data = messageData.data(using: .utf8)!
        connection.send(content: content, completion: NWConnection.SendCompletion.contentProcessed(({ (NWError) in
            if (NWError != nil) {
                print("ERROR! Error when data (Type: Data) sending. NWError: \n \(NWError!)")
            }
        })))
    }
    
    //function that check if the list of calibration points has been stable for the last 10 seconds
    //if yes, it means we can send calibration data to the server
    private func isCalibrationPointsStable(yellowCenterPoints: [NSValue]) -> Bool{
        if yellowCenterPoints.count != 4 {
            // If we don't have exactly 4 points, return false
            return false
        }
        
        let sortedPoints = yellowCenterPoints.sorted { (value1, value2) -> Bool in
            // Extract CGPoint values from NSValue objects
            let point1 = value1.cgPointValue
            let point2 = value2.cgPointValue
            
            // Compare x coordinates first
            if point1.x != point2.x {
                return point1.x < point2.x
            }
            
            // If x coordinates are equal, compare y coordinates
            return point1.y < point2.y
        }
        
        
        if lastCalibrationPoints.isEmpty {
            // If this is the first time, set the lastCalibrationPoints and start the timer
            self.lastCalibrationPoints = sortedPoints
            self.lastCalibrationTimestamp = Date().timeIntervalSince1970
            return false
        } else {
            var isStable = true
            for i in 0..<sortedPoints.count {
                // Get the CGPoint values of the NSValue objects
                let yellowPoint = sortedPoints[i].cgPointValue
                let lastPoint = self.lastCalibrationPoints[i].cgPointValue
                
                // Check if the distance between the two points is greater than a threshold value
                let distance = sqrt(pow(yellowPoint.x - lastPoint.x, 2) + pow(yellowPoint.y - lastPoint.y, 2))
                if distance > 5 {
                    // If the distance is greater than 5 pixels, set isStable to false and break out of the loop
                    isStable = false
                    break
                }
            }
            
            if(!isStable){
                // If the current points are different from the last points, update the lastCalibrationPoints and lastCalibrationTimestamp
                print("Change of calibration points")
                self.lastCalibrationPoints = sortedPoints
                self.lastCalibrationTimestamp = Date().timeIntervalSince1970
                return false
            }else{
                let currentTimeStamp = Date().timeIntervalSince1970
                if currentTimeStamp - lastCalibrationTimestamp >= 6.0 {
                    // If the difference between the current timestamp and lastCalibrationTimestamp is greater than or equal to 6 seconds, we can start calibrating
                    return true
                } else {
                    return false
                }
            }
        }
    }
    
}

//to avoid sending detected positions outside the rectangle
extension CGRect {
    init(points: [NSValue]) {
        let pointValues = points.map { $0.cgPointValue }
        let minX = pointValues.min(by: { $0.x < $1.x })!.x
        let minY = pointValues.min(by: { $0.y < $1.y })!.y
        let maxX = pointValues.max(by: { $0.x < $1.x })!.x
        let maxY = pointValues.max(by: { $0.y < $1.y })!.y
        self.init(x: minX, y: minY, width: maxX - minX, height: maxY - minY)
    }
}
