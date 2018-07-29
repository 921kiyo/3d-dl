##Software Engineering Processes?

Evaluating how well our division of work, organisation etc has gone.
This might not require another section if we cover it in the components above instead (e.g. data generation was bigger focus than expected so moved more team members to work on it).
Pavel
The Scrum proved to be very effective at keeping the work organised and in the right direction. Stand up meetings along with sprint review and planning meetings allowed us to spot that data generation will be much more time demanding process and allowed us to reallocate resource in time. The division of work was also smooth. During sprint planning meeting a group decision was made as what needs to be done in next sprint. In all cases, people volunteered to take enough tasks that no tasks were left, that would have to be assigned and all group members always stated that they believe they have the right amount of work that is manageable.


## Functional/System testing

How did we ensure code met the specification?
During sprint meetings (every second week) we discuss the overall progress of the project and goals for the next sprint. This always also includes aligning everyone on the requirements of the final product and comparing the specifications with the missing pieces in our product. For example, during our meeting on 14th February, Pavel who is responsible for sprint planning sketched out the overall project on a whiteboard. We discussed pieces which have been done and pieces which are missing compared to report 1 (the specifications). This way, we can be certain that we are not missing any pieces and also, that everyone on the team knows what has to be done.
Furthermore, we keep an issue board and a ‘done’ list on Gitlab which allows us to compare our progress with the specifications at any point.
How did we assess whether the code/product met the customer’s needs?
We arranged for regular feedback with our supervisor to assert that we are delivering on his expectations about the project (Validation). We also arranged a call with the client (Ocado) to discuss our progress and further plans for the project. Through these points of feedback, we were able to assert that we have set our priorities correctly and our work is aligned with their expectations.
Covers Validation (Are we building the right product?) and Verification (Are we building the product right?).
In terms of Verification, we
discuss in the team how to approach certain problems, to make sure we will choose the best and most efficient way to build a certain part of the software
require team members to test code which they contribute

## Pavel notes(I am happy to cut it down, these are just my notes from testing):
There are several components that are based on random number generation and thus there is no single correct output. The library randomLib contains functions such as random_cartesian_coords that generate random cartesian coordinates within certain area. In cases like this, there is a large interval of correct values. For this reason the testing focused on making sure that the specifications are met. We are testing that the correct number, type and shaped variable is returned. The returned values are also tested to be an acceptable input for any function that takes the tested function output as input. Since the output is random, the test checks multiple outputs to decrease the chance of randomly correct output in otherwise wrong function (Have to IMPLEMENT THIS YETs). Where it was possible, we also carried further tests. For example turbulence.smoothNoise  should decrease variation between neighbour pixels. This was verified by asserting that the variance of the returned 2D array is smaller than that of the original one.

The unit tests of image rendering focused on two aspects. One being the specification as constrained by the next element in the pipeline. These tests ensured that the final image has the right size (300*300 pixels), contains three layers (RGB) and has the .jpeg format.  This ensured that the image is a valid input for the next element in the pipeline. For this testing a special testing set of object images and background images was created. Some of the background images were not suitable and were correctly filtered by the function. The second aspect was to check the content of the image itself. The aim was to ensure that the object is visible on the image and the background assignment is random as needed. This would be problematic to automate but easy to inspect visually. For this reason, the images created during the test are not deleted at the end but left for inspection. The deletion occurs at the start of the next run of the test. This allows for quick and more robust check that the content of the image is correct.

## Ong notes:
! Need to describe the relationship between BlenderAPI and Blender.
Specification of image rendering (the BlenderAPI library) involved testing every class in the BlenderAPI, and seeing if the intended effects are reflected in the state of BlenderAPI, as well as the Blender program. Testing proceeds as follows:
Create a clean Blender environment
Create a class instance (if applicable)
Test a single function
Inspect the output and internal state of the object/function for BlenderAPI
Inspect the change the function has had on the Blender environment
Verify that the correct state changes have taken place.


## Swen notes re 4a:
Unit testing for training a classifier is challenging
Output can only be assessed after classifier has been trained
A “correct” outcome is hard to define given that it is typically a certain accuracy measure
What can be done:
When classifier enters training process, the weights of each layer need to change and the validation accuracy on the training set has to increase. If not, we know that there is a bug. (See blog post unit testing for ML)
We can test code before and after the classifier training
Verification: Test input/output of layers


## Others
Overall the project is on track. We have integrated both 3D rendering data generation part and CNN pipeline to test if our approach gives promising results. We tested two classes (Yogurt and cheese) to see if our model correctly classifies these two. However we observe a slightly inconsistent results (e.g while some runs give low-accuracy(TODO insert figure), other runs give more than 80% accuracy on ambient and factory datasets),
Updates to the specifications are summarized in the table below (highlighted in red). The details for each specification is described in “Update on Progress” section.


For example, our custom BlenderAPI runs within a separate Python 2.7 distribution included in the Blender application.


Another problem was that the side of the object in contact with the desk was shown as a black surface in the 3D model. The training images must be generated from angles that do not show this obstructed part. This could lead to the problem of the object not being recognisable from that one side. This will be mitigated by creating a second 3D model, which shows this side unobstructed and generating images from both models.


 An eight-class Keras model has already been successfully trained, and we will shortly be extending this to a 10 class model.
