//
//  CarsDetectorBridge.h
//  CarsDetection

/**
 Our Swift code is not able to consume C++ code (at least not at the time of writing). However Objective-C is. Furthermore we can consume Objective-C code through Swift. So let’s create Objective-C code to bridge between Swift and C++.
 */

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface CarsDetectorBridge : NSObject
    
- (NSDictionary *) detectCarsIn: (UIImage *) image withValues: (NSArray<NSValue *> *) values;

- (NSDictionary *) detectCornersIn: (UIImage *) image;
    
@end
