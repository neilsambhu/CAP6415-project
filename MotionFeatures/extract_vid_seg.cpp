/*
 * extractShot.cpp
 *
 *  Created on: Oct 10, 2013
 *      Author: fsouza
 */

#include <iostream>
#include <stdlib.h>
#include <cmath>
#include <string>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

//#define DEBUG

using namespace std;
using namespace cv;

int main (int argc, char **argv)
{
	// first element in the list is always the program name
	if (argc < 5) {
		cout << "USAGE:" << endl;
		cout << "./extractShot <input video path> <start time (in sec)> <end time (in sec)> <output path> [<maxResolution>]" << endl;
//		cout << "./extractShot <input video path> <start time (in sec)> <end time (in sec)> <output path> [<maxResolution> <saveFrames=false> <frameOutputPath>]" << endl;
		cout << "\n-- Example:" << endl;
		cout << "./extractShot S07_Brownie_7150991-1431.avi 16.9 23.5 ./" << endl;
		cout << "./ExtractVideoSegments S07_Brownie_7150991-1431.avi 16.9 23.5 ./ 480 1 " << endl;
		exit(1);
	}

	VideoCapture videoReader;
	VideoWriter videoWriter;
	Mat readFrame, writeFrame, grayFrame, newFrame;

	string inputVideoName = argv[1];
	string outputPath = argv[4];
	string framesOutputPath = "./";

	int startTime = atoi(argv[2]);
	int endTime = atoi(argv[3]);
	int maxResolution = 0;
	int width, newWidth;
	int height, newHeight;
	int frameIndex;
	int startFrame;
	long endFrame;

	float fps = 25;
	float resolutionRescaleFactor = 1.0;

	bool changeResolution = false;
	bool saveFrame = false;

	if (!videoReader.open(inputVideoName)) {
		cout << "Error while reading " << inputVideoName << endl;
		cout << "Quitting processing..." << endl;
		exit(1);
	}

	height = static_cast<int>(videoReader.get(CV_CAP_PROP_FRAME_HEIGHT));
	width = static_cast<int>(videoReader.get(CV_CAP_PROP_FRAME_WIDTH));
	fps = static_cast<float>(videoReader.get(CV_CAP_PROP_FPS));

	cout << "WIDTH x HEIGHT, FPS :" << width << "px x " << height << "px, " << fps << endl;

	// Option: Max Resolution
	if (argc > 5) {
		maxResolution = atoi(argv[5]);
		if (maxResolution > 0) {
			changeResolution = true;
			// find rescaling factor for the image
			if (height > width) {
				newHeight = maxResolution;
				resolutionRescaleFactor = newHeight / (float) height;
				newWidth = static_cast<int>(resolutionRescaleFactor * width);
			} else {
				newWidth = maxResolution;
				resolutionRescaleFactor = newWidth / (float) width;
				newHeight = static_cast<int>(resolutionRescaleFactor * height);
			}
			cout << "Rescale factor: " << resolutionRescaleFactor << endl;
			cout << "Original Resolution: " << width << "x" << height << endl;
			cout << "New Resolution: " << newWidth << "x" << newHeight << endl;
			height = newHeight;
			width = newWidth;
		}
	}

	// create video container
	videoWriter.open(outputPath + "output.avi", //CV_FOURCC('I', 'Y', 'U', 'V'), fps, Size(width,height), false);
			CV_FOURCC('D','I','V','X'), fps, Size(width,height), false);

#ifdef DEBUG
	cvNamedWindow("VIDEO DEBUG",CV_WINDOW_AUTOSIZE);
	cvNamedWindow("VIDEO SEGMENT DEBUG",CV_WINDOW_AUTOSIZE);
#endif

	saveFrame = true;
	framesOutputPath = outputPath;

	// Option: Save frames
//	if (argc > 6) {
//		if (atoi(argv[6]) != 0) {
//			saveFrame = true;
//			framesOutputPath = outputPath;
//		}
//
//		if (argc > 7) {
//			framesOutputPath = argv[7];
//		}
//	}

	// If no start time is provided, set the start frame to be frame one
	frameIndex = 1;
	if (startTime == -1) startFrame = 1;
	else startFrame = static_cast<int>(round(startTime * fps));
	cout << "start frame:" << startFrame << endl;

	// If no end time is provided, set the end frame to be the last frame
	if (endTime == -1) endFrame = (int) videoReader.get(CV_CAP_PROP_FRAME_COUNT);
	else endFrame = static_cast<int>(round(endTime * fps));
	cout << "end frame:" << endFrame << endl;

	// Read the video and collect frames
	while (videoReader.read(readFrame) && frameIndex < endFrame+1) {

#ifdef DEBUG
		cout << "frame" << frameIndex << endl;
		imshow("VIDEO DEBUG",readFrame);
		waitKey(30);
#endif

		// check if current frame falls into the desired range of frames
		if (frameIndex > startFrame-1 && frameIndex < endFrame+1) {
			// convert to gray scale if not already set as such
			if (readFrame.channels() > 1) {
				cvtColor(readFrame, grayFrame, CV_RGB2GRAY);
				readFrame.release(); // free unused memory
			} else {
				grayFrame = readFrame;
			}

			if (changeResolution) {
				resize(grayFrame,writeFrame,Size(width,height));
				grayFrame.release(); // free unused memory
			} else {
				writeFrame = grayFrame;
			}

			videoWriter.write(writeFrame);

#ifdef DEBUG
			cout << "Processing frame #" << frameIndex << endl;
			imshow("VIDEO SEGMENT DEBUG",writeFrame);
			waitKey(30);
#endif

			//if (saveFrame) {
			ostringstream num; num << frameIndex;
			imwrite(framesOutputPath + "frame" + num.str() + ".jpg", writeFrame);
			//}

			readFrame.release();
			grayFrame.release();
			writeFrame.release();
		}

		readFrame.release();

		frameIndex++;
	}

	videoReader.release();
	videoWriter.release();

	return 0;
}
