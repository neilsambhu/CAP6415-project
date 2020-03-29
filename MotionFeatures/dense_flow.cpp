/*
 * denseFlow.cpp
 *
 *  Created on: Oct 15, 2013
 *      Author: fsouza
 */


#include <iostream>
#include <vector>
#include <string>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/video/video.hpp>

using namespace std;
using namespace cv;

int main(int argc, char **argv)
{
	string inputPath;
	string fileNamePrefix;
	string fileExtension;

	int startFrame;
	int endFrame;

	//string outputPath;
	//string outputIDName;
	string outputOFPath;
	//string BBImagesPath;
	string prevFramePath;
	string nextFramePath;
	string fileName;

	ostringstream number;

	Mat prev;
	Mat next;
	Mat flow;
	Mat mag;
	Mat grad;
	vector<Mat> planes;

	int levels;
	int winsize;
	int iterations;
	int poly_n;

	double pyr_scale;
	double poly_sigma;
	double minVal;
	double maxVal;

	FileStorage OFStreamRecord, fileStream;

	// Read external arguments
	if (argc < 7) {
		cout << "HELP:\n" << endl;
		cout << "./DenseFlow <inputFramesPath> <fileNamePrefix> <fileExtension> <startFrame> <endFrame> <outputOpticalFlowPath>" << endl;
		exit(1);
	}

	inputPath = argv[1];
	fileNamePrefix = argv[2];
	fileExtension = argv[3];
	startFrame = atoi(argv[4]);
	endFrame = atoi(argv[5]);
	outputOFPath = argv[6];


	pyr_scale = 0.5;
	levels = 1;
	winsize = 25;
	poly_n = 11; // 5 or 7
	poly_sigma = 3.5; // 1.1 or 1.5 if poly_n = 7: increases smoothness
	iterations = 10;

	fileName = outputOFPath + "metadata.xml";
	fileStream.open(fileName,FileStorage::WRITE);
	fileStream << "opticalFlowParams" << "[";
	fileStream << "{:" << "pyr_scale" << pyr_scale << "levels" << levels << "winsize" << winsize << "poly_n" << poly_n;
	fileStream << "poly_sigma" << poly_sigma << "iterations" << iterations << "}";
	fileStream << "]";
	fileStream << "startFrame" << (startFrame+1);
	fileStream << "endFrame" << endFrame;

	number << startFrame;
	prevFramePath = inputPath + fileNamePrefix + number.str() + "." + fileExtension;
	prev = imread(prevFramePath,CV_LOAD_IMAGE_GRAYSCALE);
	number.str("");

/*	cout << "frame path: " << prevFramePath << endl;
	cvNamedWindow("test",CV_WINDOW_AUTOSIZE);
	imshow("test",prev);
	waitKey(0);
*/
	fileStream << "frameWidth" << prev.cols;
	fileStream << "frameHeight" << prev.rows;

	fileStream.release();
	prev.release();

	// EXTRACT DENSE OPTICAL FLOW
	for (int i = startFrame; i < endFrame; i++) {
		number << i;
		prevFramePath = inputPath + fileNamePrefix + number.str() + "." + fileExtension;
		prev = imread(prevFramePath,CV_LOAD_IMAGE_GRAYSCALE);
		cout << "prev.channels() = " << prev.channels() << endl;
		number.str("");

		number << i+1;
		nextFramePath = inputPath + fileNamePrefix + number.str() + "." + fileExtension;
		next = imread(nextFramePath, CV_LOAD_IMAGE_GRAYSCALE);
		cout << "next.channels() = " << next.channels() << endl;

		flow = Mat::zeros(prev.rows, next.cols, CV_32FC2);

		// compute optical flow using parameters provided
		calcOpticalFlowFarneback(prev,next,flow,pyr_scale,levels,winsize,
								 iterations,poly_n,poly_sigma,OPTFLOW_FARNEBACK_GAUSSIAN);

		cout << "Convert from Dx and Dy to magnitude and gradient..." << endl;

		split(flow,planes);
		cartToPolar(planes[0],planes[1],mag,grad);
		minMaxLoc(mag,&minVal,&maxVal,NULL,NULL);

		fileName = outputOFPath + "frame" + number.str() + ".xml";

		OFStreamRecord.open(fileName,FileStorage::WRITE);
		OFStreamRecord << "Dx" << planes[0];
		OFStreamRecord << "Dy" << planes[1];
		OFStreamRecord << "mag" << mag;
		OFStreamRecord << "grad" << grad;
		OFStreamRecord << "minMag" << minVal;
		OFStreamRecord << "maxMag" << maxVal;
		OFStreamRecord.release();

		planes[0].release();
		planes[1].release();
		planes.clear();

		mag.release();
		grad.release();
		prev.release();
		next.release();
		flow.release();

		number.str("");
	}

	return 0;
}

