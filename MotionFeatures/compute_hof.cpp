/*
 * sampleHoFPatterns.cpp
 *
 *  Created on: Dec 3, 2013
 *      Author: fsouza
 */



/*
 * main.cpp
 *
 *  Created on: Sep 22, 2013
 *      Author: fsouza
 */

#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <cmath>
#include <fstream>
#include <ostream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/video/video.hpp>

using namespace std;
using namespace cv;

#define NBINS 72
#define OutMat Mat
#define InMat Mat

//#define DEBUG
#define MAXMAG_PER_FRAME
//#define MAXMAG_WHOLE_VIDEO
//#define CAMERA_MOTION_CORRECTION

void cameraMotionCorrection(Mat &dx, Mat &dy, int _border_size);
float displacementAverage(Mat &im,int border_size);
void computeHistogram(InMat &gradient, InMat &magnitude, OutMat &histogram, Rect ROI, float threshold);
void drawArrow(Mat &img, int x, int y, int u, int v, Scalar color, int size, int thickness);

int main (int argc, char **argv)
{
	FileStorage featuresFS, opticalFlowFS, metadataFS;
	FileNode frameBoundingBoxes;
	FileNodeIterator it;
	Mat gradient, magnitude, Dx, Dy;
	vector<Mat> histogram;
	Rect box;

	//int boxNumber;
	int splits = 3;
	int startFrame, endFrame;
	int width, height;

	vector<string> frames;
	ostringstream number;
	fstream featuresFile;
	fstream flowsPointFile;

	string tagName;
	string opticalFlowFilesPath;
	string boundingBoxesFileName;
	string featureFileName;
	string flowsPointFileName;
	string opticalFlowFileName;
	string inputPath;
	string outputPath;
	string idname;
	string flowsPointOutputPath;

	bool saveFlowPoints = false;

	if (argc < 4) {
		cout << "Arguments are missing.\n"
				"USAGE:\n\n"
				"EX.: ./compute_hof <inputPath> <outputPath> <idname> [<flow points output path>]\n\n"
				"CONTACT: fillipe@mail.usf.edu\n";
		exit(1);
	}

	// READING EXTERNAL ARGUMENTS (INPUT TO THE PROGRAM)
	inputPath = string(argv[1]);
	outputPath = string(argv[2]);
	idname = string(argv[3]);
	if (argc > 4) {
		saveFlowPoints = true;
		flowsPointOutputPath = string(argv[4]);
	}
	//roiOutputPath = string(argv[4]);

	histogram.resize(splits);

	metadataFS.open(inputPath+"metadata.xml", FileStorage::READ);
	metadataFS["startFrame"] >> startFrame;
	metadataFS["endFrame"] >> endFrame;
	metadataFS["frameWidth"] >> width;
	metadataFS["frameHeight"] >> height;
	metadataFS.release();

	cout << inputPath << "metadata.xml" << endl;

	box.x = 0;
	box.y = 0;
	box.width = width;
	box.height = height;

	float fps = 25;
	Mat hist;
	int begin, end;

	// SPLIT THE SEQUENCE OF FRAMES INTO nframes SEGMENTS OF FRAMES
	int nframes = (endFrame - startFrame + 1) / histogram.size();

	vector<float> mags;
	float maxMagnitude = 0.0;

#ifdef MAXMAG_WHOLE_VIDEO
    // FIND GLOBAL MAXIMUM MAGNITUDE THAT IS THE AVERAGE OF THE MAXIMUMS
  	float frmMaxMag = 0.0;
	float avgMag = 0.0;
	for (int frm = startFrame; frm <= endFrame; frm++) {
		number << frm;
		tagName = "frame" + number.str(); number.str("");
		opticalFlowFileName = inputPath + tagName + ".xml";
		opticalFlowFS.open(opticalFlowFileName, FileStorage::READ);
		opticalFlowFS["maxMag"] >> frmMaxMag;
		opticalFlowFS.release();

		if (frmMaxMag > maxMagnitude ) {
			maxMagnitude = frmMaxMag;
		}

		avgMag += frmMaxMag;
		mags.push_back(frmMaxMag);
	}

	maxMagnitude = avgMag / (endFrame - startFrame + 1);
#endif

#ifdef DEBUG
	VideoWriter videoWriter;
	videoWriter.open(outputPath + idname +".avi", CV_FOURCC('D', 'I', 'V', 'X'), fps, Size(width,height), true);
#endif

	for (int k = 0; k < histogram.size(); k++) {
		begin = startFrame + k*nframes;

		if (k < histogram.size()-1) {
			end = begin + nframes - 1;
		} else {
			end = endFrame;
		}

		for (int frm = begin; frm <= end; frm++) {
			ostringstream number;
			number << frm;
			tagName = "frame" + number.str(); //number.str("");
			cout << tagName << endl;

			// READ OPTICAL FLOW DATA
			opticalFlowFileName = inputPath + tagName + ".xml";
			opticalFlowFS.open(opticalFlowFileName, FileStorage::READ);
			opticalFlowFS["Dx"] >> Dx;
			opticalFlowFS["Dy"] >> Dy;
			opticalFlowFS["grad"] >> gradient;
			opticalFlowFS["mag"] >> magnitude;

#ifdef MAXMAG_PER_FRAME
			opticalFlowFS["maxMag"] >> maxMagnitude;
#endif
			//width = gradient.cols;
			//height = gradient.rows;
			opticalFlowFS.release();

#ifdef CAMERA_MOTION_CORRECTION
			cameraMotionCorrection(Dx,Dy,75);
			cartToPolar(Dx,Dy,magnitude,gradient);
//			cout << "finished reading optical flow data..." << endl;
#endif

#ifdef DEBUG
			string imageFilename = inputPath + tagName + ".jpg";
			Mat img = imread(imageFilename);

			Mat vismag = Mat::zeros(magnitude.rows,magnitude.cols,CV_8UC3);
			cv::normalize(magnitude, vismag, 0, 255, NORM_MINMAX, CV_8UC1);
			cvtColor(vismag,vismag,CV_GRAY2BGR);
#endif

			// SAVE THRESHOLDED OPTIC FLOW LOCATION FIELD
			if (saveFlowPoints) {
				flowsPointFileName = flowsPointOutputPath + "frame_" + number.str() + ".txt"; number.str("");
				flowsPointFile.open(flowsPointFileName.c_str(), ofstream::out); // | ofstream::app);

				// FIRST ROW STORES THE IMAGE RESOLUTION
				flowsPointFile << width << "," << height << endl;

				for (int i = 0; i < gradient.rows; i+=1) {
					for (int j = 0; j < gradient.cols; j+=1) {
						if (magnitude.at<float>(i,j) > 0.2*maxMagnitude)
							flowsPointFile << i << "," << j << endl;
					}
				}
				flowsPointFile.close();
			}

/*	UNCOMMENT THIS CODE TOO */
#ifdef DEBUG
			for (int i = 0; i < gradient.rows; i+=10) { //+=10
				for (int j = 0; j < gradient.cols; j+=8) { //+=8
					if (magnitude.at<float>(i,j) > 0.2*maxMagnitude)
						drawArrow(vismag,j,i,round(5*Dx.at<float>(i,j)),round(5*Dy.at<float>(i,j)),Scalar(0,0,255),3,1);
				}
			}

			vismag = 0.5*vismag + 0.5*img;
			videoWriter.write(vismag);

			cvNamedWindow("mag",CV_WINDOW_AUTOSIZE);
			imshow("mag",vismag);
			waitKey(30);
//			cout << "finished reading optical flow data..." << endl;
#endif
			// COMPUTE HISTOGRAM OF OPTIC FLOW
 			computeHistogram(gradient, magnitude, hist, box, 0.2*maxMagnitude);

			if (histogram[k].rows < 1 || histogram[k].cols < 1) {
				histogram[k] = hist.clone();
			} else {
				histogram[k] = histogram[k] + hist;
			}

#ifdef DEBUG
			cout << histogram[k] << endl;
			cout << "finished computing histogram..." << endl;
#endif
			// SAVE FEATURES ON FILE
			/*
			number << boxNumber;
			featureFileName = outputPath + "" + number.str() + ".hof"; number.str("");

			featuresFile.open(featureFileName.c_str(), ofstream::out | ofstream::app);
			featuresFile << histogram.at<float>(0);
			//cout << histogram.at<float>(0);
			for (int k = 1; k < histogram.rows; k++) {
				//cout << " " << histogram.at<float>(k);
				featuresFile << " " << histogram.at<float>(k);
			}
			featuresFile << "\n";
			featuresFile.close();
			 */

			// FREE MEMORY STORAGE
			gradient.release();
			magnitude.release();
#ifdef DEBUG
			vismag.release();
			img.release();
#endif
			hist.release();
			//histogram.release();
//cout << "END OF LOOP" << endl;
		}

	}
/* UNCOMMENT THIS BLOCK LATER */
	// LOCAL NORMALIZATION
	for (int k = 0; k < histogram.size(); k++) {
		float total = 0.0;
		for (int i = 0; i < NBINS; i++)
			total += histogram[k].at<float>(i);

		for (int i = 0; i < NBINS; i++)
			histogram[k].at<float>(i) /= total;
	}

	// GLOBAL NORMALIZATION
/*	float total = 0.0;
	float maxval = 0.0, minval = 0.0;
	for (int k = 0; k < histogram.size(); k++) {
		for (int i = 0; i < NBINS; i++)
			if (histogram[k].at<float>(i) > total) {
				total = histogram[k].at<float>(i);
			}
	}

	for (int k = 0; k < histogram.size(); k++) {
		for (int i = 0; i < NBINS; i++)
			histogram[k].at<float>(i) /= total;
	}
*/
	// SAVE FEATURES ON FILE
/* UNCOMMENT THIS CODE BLOCK LATER */
	featureFileName = outputPath + idname + ".hof";

	featuresFile.open(featureFileName.c_str(), ofstream::out);
	for (int k = 0; k < histogram.size(); k++) {
		//featuresFile << histogram[k].at<float>(0);
		//cout << histogram.at<float>(0);
		for (int i = 0; i < histogram[k].rows; i++) {
			//cout << " " << histogram.at<float>(k);
			featuresFile <<  histogram[k].at<float>(i) << " ";
		}
	}
	featuresFile << "\n";
	featuresFile.close();

	return 0;
}

void computeHistogram(InMat &gradient, InMat &magnitude, OutMat &histogram, Rect ROI, float threshold)
{
	int binSize;
	int lowBin, highBin;
	int distanceToLowBin, distanceToHighBin;

	float angleInDegree; // 0 - 360
	float lowBinWeight, highBinWeight;

	double maxVal = 0;

	binSize = 360 / NBINS;
	histogram = Mat::zeros(NBINS,1,CV_32FC1);

	for (int i = ROI.y; i < ROI.y + ROI.height; i++) {
		for (int j = ROI.x; j < ROI.x + ROI.width; j++) {
			if (magnitude.at<float>(i,j) < threshold)
				continue;

			// CONVERT ANGLE FROM RADIANS TO DEGREES
			angleInDegree = gradient.at<float>(i,j) * (180.0 / M_PI);

			// FIND WEIGHTS
			lowBin = ( (int) round(angleInDegree) / binSize ) * binSize;
			highBin = lowBin + binSize;
			distanceToLowBin = abs(angleInDegree - lowBin);
			distanceToHighBin = abs(angleInDegree - highBin);
			lowBinWeight = distanceToHighBin / static_cast<float>(distanceToLowBin + distanceToHighBin);
			highBinWeight = distanceToLowBin / static_cast<float>(distanceToLowBin + distanceToHighBin);

	/*
			cout << "angle: " << angleInDegree ;
			cout << ", lowBin: " << lowBin << " " << (lowBin % 360) / binSize ;
			cout << ", highBin: " << highBin << " " << ( (highBin % 360) / binSize );
			cout << ", lowBinWeight: " << lowBinWeight ;
			cout << ", highBinWeight: " << highBinWeight << endl;
	*/
			// WEIGH HISTOGRAM BINS
			histogram.at<float>( (lowBin % 360) / binSize ) += lowBinWeight * magnitude.at<float>(i,j);
			histogram.at<float>( (highBin % 360) / binSize ) += highBinWeight * magnitude.at<float>(i,j);
		}
	}

	// NORMALIZE HISTOGRAM
	//minMaxLoc(histogram, 0, &maxVal, 0, 0);

	maxVal = 0.0;
	for (int i = 0; i < NBINS; i++)
			maxVal += histogram.at<float>(i);

	for (int i = 0; i < NBINS; i++)
		histogram.at<float>(i) /= maxVal;

	return ;
}


/*
void globalCameraMotionCorrection(Mat &dx, Mat &dy, int bin_size=10)
{
	float minValue;
	float maxValue;
	float step;
	vector<float> histogram;

	histogram.resize(bin_size);

	return ;
}
*/

float displacementAverage(Mat &im,int border_size)
{
	float displacement = 0.0f;

	// left edge of the image
	for (int k = 0; k < border_size; k++) {
		for (int i = 0; i < im.rows; i++) {
			displacement += im.at<float>(i,k);
			//if (abs(im.at<float>(i,k)) > abs(displacement))
			//	displacement = im.at<float>(i,k);
		}
	}

	// right edge of the image
	for (int k = im.cols-border_size; k < im.cols; k++) {
		for (int i = 0; i < im.rows; i++) {
			displacement += im.at<float>(i,k);
			//if (abs(im.at<float>(i,k)) > abs(displacement))
			//	displacement = im.at<float>(i,k);
		}
	}

	// top edge of the image
	for (int k = 0; k < border_size; k++) {
		for (int i = border_size; i < im.cols-border_size; i++) {
			displacement += im.at<float>(k,i);
			//if (abs(im.at<float>(k,i)) > abs(displacement))
			//	displacement = im.at<float>(k,i);
		}
	}

	// bottom edge of the image
	for (int k = im.rows-border_size; k < im.rows; k++) {
		for (int i = border_size; i < im.cols-border_size; i++) {
			displacement += im.at<float>(k,i);
			//if (abs(im.at<float>(k,i)) > abs(displacement))
			//	displacement = im.at<float>(k,i);
		}
	}

	float number_of_pixels = 2*border_size*(im.rows + im.cols - 2*border_size);

	return displacement/number_of_pixels;
}

void cameraMotionCorrection(Mat &dx, Mat &dy, int _border_size=5)
{
	float avgDispAtX = displacementAverage(dx,_border_size);
	float avgDispAtY = displacementAverage(dy,_border_size);

	printf("Estimated Camera Motion Flow: dx=%f,dy=%f\n",avgDispAtX,avgDispAtY);

	for (int i = 0; i < dx.rows; i++) {
		for (int j = 0; j < dx.cols; j++) {
			dx.at<float>(i,j) -= avgDispAtX;
			dy.at<float>(i,j) -= avgDispAtY;
		}
	}

	return ;
}


void drawArrow(Mat &img, int x, int y, int u, int v, Scalar color, int Size, int thickness)
{
	cv::Point pt1,pt2;
	double Theta;
	double PI = 3.1416;

	if(u == 0)
	    Theta=PI/2;
	else
	    Theta=atan2(double(v),(double)(u));


	pt1.x=x;
	pt1.y=y;

	pt2.x=x+u;
	pt2.y=y+v;

	cv::line(img,pt1,pt2,color,thickness,8);  //Draw Line

	Size=(int)(Size*0.707);

	if(Theta==PI/2 && pt1.y > pt2.y){
	    pt1.x=(int)(Size*cos(Theta)-Size*sin(Theta)+pt2.x);
	    pt1.y=(int)(Size*sin(Theta)+Size*cos(Theta)+pt2.y);
	    cv::line(img,pt1,pt2,color,thickness,8);  //Draw Line

	    pt1.x=(int)(Size*cos(Theta)+Size*sin(Theta)+pt2.x);
	    pt1.y=(int)(Size*sin(Theta)-Size*cos(Theta)+pt2.y);
	    cv::line(img,pt1,pt2,color,thickness,8);  //Draw Line
	} else {
	    pt1.x=(int)(-Size*cos(Theta)-Size*sin(Theta)+pt2.x);
	    pt1.y=(int)(-Size*sin(Theta)+Size*cos(Theta)+pt2.y);
	    cv::line(img,pt1,pt2,color,thickness,8);  //Draw Line

	    pt1.x=(int)(-Size*cos(Theta)+Size*sin(Theta)+pt2.x);
	    pt1.y=(int)(-Size*sin(Theta)-Size*cos(Theta)+pt2.y);
	    cv::line(img,pt1,pt2,color,thickness,8);  //Draw Line
	}
}

