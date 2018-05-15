/*
 
 iPhone App for Grocery Product Recognition
 
 This file is adapted from and based on a foundation of code produced for a Swfit iOS Camera tutorial written by Rizwan Mohamed Ibrahim at https://medium.com/@rizwanm/swift-camera-part-2-c6de440a9404. Additional code was written to provide the necessary custom functionality.
 
 This source code is released under the MIT License, as per the terms of Rizwan's original license.
 
*/

// Begin Adapted Code

import UIKit
import AVFoundation
import Alamofire

class ViewController: UIViewController {
    
    @IBOutlet weak var cancelButton: UIButton!
    
    @IBOutlet weak var previewView: UIView!
    @IBOutlet weak var captureButton: UIButton!
    @IBOutlet weak var messageLabel: UILabel!
    
    @IBOutlet weak var MainLabel: UILabel!
    var captureSession: AVCaptureSession?
    var videoPreviewLayer: AVCaptureVideoPreviewLayer?
    var capturePhotoOutput: AVCapturePhotoOutput?
    var qrCodeFrameView: UIView?

    @IBAction func resetAll(_ sender: UIButton) {
        MainLabel.text = "Start Scanning!"
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        captureButton.layer.cornerRadius = captureButton.frame.size.width / 2
        captureButton.clipsToBounds = true
        
        // Get an instance of the AVCaptureDevice class to initialize a device object and provide the video as the media type parameter
        guard let captureDevice = AVCaptureDevice.default(for: AVMediaType.video) else {
            fatalError("No vidoe device found")
        }

        do {
            // Get an instance of the AVCaptureDeviceInput class using the previous deivce object
            let input = try AVCaptureDeviceInput(device: captureDevice)
            
            // Initialize the captureSession object
            captureSession = AVCaptureSession()
            
            // Set the input devcie on the capture session
            captureSession?.addInput(input)
            
            // Get an instance of ACCapturePhotoOutput class
            capturePhotoOutput = AVCapturePhotoOutput()
            capturePhotoOutput?.isHighResolutionCaptureEnabled = true
            
            // Set the output on the capture session
            captureSession?.addOutput(capturePhotoOutput!)
            
            // Initialize a AVCaptureMetadataOutput object and set it as the input device
            let captureMetadataOutput = AVCaptureMetadataOutput()
            captureSession?.addOutput(captureMetadataOutput)

            // Set delegate and use the default dispatch queue to execute the call back
            captureMetadataOutput.setMetadataObjectsDelegate(self, queue: DispatchQueue.main)
            captureMetadataOutput.metadataObjectTypes = [AVMetadataObject.ObjectType.qr]
            
            //Initialise the video preview layer and add it as a sublayer to the viewPreview view's layer
            videoPreviewLayer = AVCaptureVideoPreviewLayer(session: captureSession!)
            videoPreviewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
            videoPreviewLayer?.frame = view.layer.bounds
            previewView.layer.addSublayer(videoPreviewLayer!)
            
            //start video capture
            captureSession?.startRunning()
            
            messageLabel.isHidden = true
            
            //Initialize QR Code Frame to highlight the QR code
            qrCodeFrameView = UIView()
            
            if let qrCodeFrameView = qrCodeFrameView {
                qrCodeFrameView.layer.borderColor = UIColor.green.cgColor
                qrCodeFrameView.layer.borderWidth = 2
                view.addSubview(qrCodeFrameView)
                view.bringSubview(toFront: qrCodeFrameView)
            }
        } catch {
            //If any error occurs, simply print it out
            print(error)
            return
        }
    
    }

    override func viewDidLayoutSubviews() {
        videoPreviewLayer?.frame = view.bounds
        if let previewLayer = videoPreviewLayer ,(previewLayer.connection?.isVideoOrientationSupported)! {
            previewLayer.connection?.videoOrientation = UIApplication.shared.statusBarOrientation.videoOrientation ?? .portrait
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func onTapTakePhoto(_ sender: Any) {
        // Make sure capturePhotoOutput is valid
        guard let capturePhotoOutput = self.capturePhotoOutput else { return }
        
        // Get an instance of AVCapturePhotoSettings class
        let photoSettings = AVCapturePhotoSettings()
        
        // Set photo settings for our need
        photoSettings.isAutoStillImageStabilizationEnabled = true
        photoSettings.isHighResolutionPhotoEnabled = false
        photoSettings.flashMode = .auto
        
        MainLabel.text = "Image Captured!"
        
        // Call capturePhoto method by passing our photo settings and a delegate implementing AVCapturePhotoCaptureDelegate
        capturePhotoOutput.capturePhoto(with: photoSettings, delegate: self)
    }
    
    // End Adapted Code
    
    // Begin code written for this project
    
    /*
     Function to upload image to Web Server API and to parse result returned by the API.
     
     Input Arguments:
     api_address (String): URL of API service to upload image to
     input_imageData (Data): Image to be uploaded, stored as Data
     
     Return Value:
     output_string (String):
     
     
     */
    
    func upload_image(api_address: String, input_imageData: Data?) -> String {
        var return_string :String = "";
        //self.MainLabel.text = "Uploading...";
        
        // Initialise an UIImage with our image data
        let capturedImage = UIImage.init(data: input_imageData! , scale: 1.0);
        let for_upload_imageData = UIImageJPEGRepresentation(capturedImage!, 1.0)!
        
        // Save captured image to photo album
        if let image = capturedImage {
            UIImageWriteToSavedPhotosAlbum(image, nil, nil, nil)
        }
        
        // Initialise string that will contain output
        var output_string = ""
        
        // Use Alamofire to submit HTTP POST Request to Web Server API
        Alamofire.upload(
            multipartFormData: { multipartFormData in
                multipartFormData.append(for_upload_imageData , withName: "my_image", fileName: "image.jpg", mimeType: "image/jpeg")
        },
            to: api_address,
            encodingCompletion: { encodingResult in
                switch encodingResult {
                case .success(let upload, _, _):
                    upload.responseJSON { response in
                        // Parse JSON reponse and add relevant information to output string
                        //debugPrint(response)
                        //debugPrint(response.result.value)
                        let jsonDict = response.result.value as? [String:Any]
                        //debugPrint(jsonDict)
                        //debugPrint(jsonDict!["max_class"])
                        //debugPrint(jsonDict!["max_value"])
                        //var output_string = ""
                        output_string += jsonDict!["max_class"] as! String
                        output_string += ": "
                        output_string += jsonDict!["max_value"] as! String
                        output_string += "%"
                        print("Second Output")
                        print(output_string)
                        self.MainLabel.text = output_string
                        return_string = output_string;
                        print("Third Output");
                        print(return_string);
                    }
                case .failure(let encodingError):
                    print(encodingError)
                }
        }
        )
        
        
        // Return string containing name and confidence of predicted class
        return return_string
    }
    
    // End code written for this project
    
    // Begin Adapted Code
}

extension ViewController : AVCapturePhotoCaptureDelegate {
    func photoOutput(_ captureOutput: AVCapturePhotoOutput,
                     didFinishProcessingPhoto photoSampleBuffer: CMSampleBuffer?,
                     previewPhoto previewPhotoSampleBuffer: CMSampleBuffer?,
                     resolvedSettings: AVCaptureResolvedPhotoSettings,
                     bracketSettings: AVCaptureBracketedStillImageSettings?,
                     error: Error?) {
        // Make sure we get some photo sample buffer
        guard error == nil,
            let photoSampleBuffer = photoSampleBuffer else {
                print("Error capturing photo: \(String(describing: error))")
                return
        }
        
        self.MainLabel.text = "Uploading...";
        
        // Convert photo same buffer to a jpeg image data by using AVCapturePhotoOutput
        guard let imageData = AVCapturePhotoOutput.jpegPhotoDataRepresentation(forJPEGSampleBuffer: photoSampleBuffer, previewPhotoSampleBuffer: previewPhotoSampleBuffer) else {
            return
        }
        
        let output_string = upload_image(api_address: "http://146.169.3.104:5000/api", input_imageData: imageData);
        
        DispatchQueue.main.asyncAfter(deadline: .now() + .seconds(5), execute: {
            // Put your code which should be executed with a delay here
            print("printing output");
            print(self.MainLabel.text);
        })
        
    }
}

extension ViewController : AVCaptureMetadataOutputObjectsDelegate {
    func metadataOutput(_ captureOutput: AVCaptureMetadataOutput,
                       didOutput metadataObjects: [AVMetadataObject],
                       from connection: AVCaptureConnection) {
        // Check if the metadataObjects array is contains at least one object.
        if metadataObjects.count == 0 {
            qrCodeFrameView?.frame = CGRect.zero
            messageLabel.isHidden = true
            return
        }
        
        // Get the metadata object.
        let metadataObj = metadataObjects[0] as! AVMetadataMachineReadableCodeObject
        
        if metadataObj.type == AVMetadataObject.ObjectType.qr {
            // If the found metadata is equal to the QR code metadata then update the status label's text and set the bounds
            let barCodeObject = videoPreviewLayer?.transformedMetadataObject(for: metadataObj)
            qrCodeFrameView?.frame = barCodeObject!.bounds
            
            if metadataObj.stringValue != nil {
                messageLabel.isHidden = false
                messageLabel.text = metadataObj.stringValue
            }
        }
    }
}

extension UIInterfaceOrientation {
    var videoOrientation: AVCaptureVideoOrientation? {
        switch self {
        case .portraitUpsideDown: return .portraitUpsideDown
        case .landscapeRight: return .landscapeRight
        case .landscapeLeft: return .landscapeLeft
        case .portrait: return .portrait
        default: return nil
        }
    }
}

// End Adapted Code



