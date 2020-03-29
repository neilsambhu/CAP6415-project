Computing Features for Describing Actions

There three pieces of code that you are gonna need to use to accomplish this task. If your videos are already segmented as you wish, then you will not need to do the first step, i.e. to use the first code. The three parts of this task are the following:

1. Extracting video segments (or the basic unit of data that you want to work with);
2. Extracting optic flow features from the video segments;
3. Computing histogram of optic flow

# Requirements

You need to have OpenCV 2.0 or later versions (2.X.X) installed (never tested with OpenCV 3.0).

1 -- Extracting video segments

Code: extract_vid_seg.cpp

Steps:
a. Compile the code on your machine (make sure all requirements are fulfilled)

    $ g++ -O3 -Wall extract_vid_seg.cpp -o extract_vid_seg -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_video

[Optional] To compile for the debugging mode (visualize the video segment):

    $ g++ -O3 -Wall -DDEBUG extract_vid_seg.cpp -o extract_vid_seg -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_video

b. Execute the program with input data

    $ ./extract_vid_seg <input video path> <start time (in sec)> <end time (in sec)> <frames output path> [<max resolution>]

    <max resolution> is shown enclosed with square brackets to indicate that it is an optional parameter.

    Demo Ex.: 
    $ mkdir output_path
    $ ./extract_vid_seg S07_Brownie_7150991-1431.avi 16.9 23.5 ./output_path/ 480

    The demo above outputs all (grayscale) frames going from second 16.9 to second 23.5 from the video S07_Brownie_7150991-1431.avi at the folder "output_path". It also outputs the video segmented being extracted at "output_path". Both the video and the image frames's  resolutions are rescaled proportionally while keeping the size of the largest dimension (width or height) equal to 480px. In short the outputs are: output_path/output.avi and output_path/frame*.jpg.

2 -- Extracting optic flow features

Code: dense_flow.cpp

Steps:
a. Compile the code:

    $ g++ -O3 -Wall dense_flow.cpp -o dense_flow -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_video

b. Use the output generated in step one (Extracting video segment) as input to this code. Run the following command:

    $ ./dense_flow <inputFramesPath> <fileNamePrefix> <fileExtension> <startFrame> <endFrame> <outputOpticalFlowPath>

    Continuing the process with the example using the S07_Brownie_7150991-1431.avi:

    $ ./dense_flow ./output_path/ frame jpg 480 690 ./output_path/

    The outputs are ./output_path/frame*.xml files containing the computed optic flow per pixel between every consecutive ./output_path/frame*.jpg and the metadata.xml containing information about the optic flow computation (video resolution and the frame interval). These outputs will be used in the next step.
    
3 -- Computing the histograms of optic flow

Code: compute_hof.cpp

Steps:
a. Compile the code:

    $ g++ -O3 -Wall compute_hof.cpp -o compute_hof -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_video
    
    # Debug mode compilation:
    
    $ g++ -O3 -Wall -DDEBUG compute_hof.cpp -o compute_hof -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_video

b. Use the output data generated at step 2, namely "Extracting optic flow", and run the following command (it needs both metadata.xml and frame*.xml files): 

    $ ./compute_hof <inputPath> <outputPath> <idname> [<flow points output path>]
    
    Continuing the running example above, we run
    
    $ mkdir hof
    $ ./compute_hof output_path/ hof/ s07_brownie_480_690_take-bowl
    
    It outputs a histogram of optic flow at hof/s07_brownie_480_690_take-bowl.hof. In the DEBUG mode it also outputs a demo video at hof/s07_brownie_480_690_take-bowl.avi.