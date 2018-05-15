/*
 
 iPhone App for Grocery Product Recognition
 
 Unit Tests
 
 */

import XCTest
@testable import Camera

class CameraTests: XCTestCase {
    
    var testingNow: ViewController!;
    
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
        testingNow = ViewController();
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
        testingNow = ViewController();
    }
    
    // Test for upload_image function
    // Uploads image and checks result obtained from server by verifying that product type is one of the 10 classes in the model and that the accuracy obtained is a number between 0 and 100
    
    func testUpload(){
        let test_image = UIImage(named: "anchor_test_image");
        let jpeg_image = UIImageJPEGRepresentation(test_image!, 1.0 );
        
        let output_string = testingNow.upload_image(api_address: "146.169.3.104:5000/api", input_imageData: jpeg_image);
        
        DispatchQueue.main.asyncAfter(deadline: .now() + .seconds(5), execute: {
            // Put your code which should be executed with a delay here
            let output_string_array = self.testingNow.MainLabel.text?.components(separatedBy: ": ");
            
            print(output_string_array);
            
            let product_result: String = output_string_array![0];
            var accuracy_result: String = output_string_array![1];
            
            
            let all_product_types: [String] = ["Anchor", "Coconut Water", "Cottage Cheese", "Halloumi", "Liberte", "Mango Yogurt", "Soup", "Soymilk", "Squashums", "Strawberry Yogurt"];
            
            var product_valid: Bool = false;
            
            for p in all_product_types {
                if (product_result == p){
                    product_valid = true;
                }
            }
            
            let accuracy_array = output_string.components(separatedBy: "%");
            accuracy_result = accuracy_array[0];
            let accuracy_num: Float = Float(accuracy_result)!;
            var accuracy_valid: Bool = false;
            
            if (accuracy_num >= 0 && accuracy_num <= 100){
                accuracy_valid = true;
            }
            
            XCTAssertTrue(product_valid);
            XCTAssertTrue(accuracy_valid);
        })
        
        
    }
}
