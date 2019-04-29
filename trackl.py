
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import PIL
import numpy as np
# for arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())


OPENCV_OBJECT_TRACKERS = {                       # initialize dictionary for trackers
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}

# initialize  tracker
trackers = cv2.MultiTracker_create()

print("If you want to track by marking enter 1")
print("If you want to track by an image press 2")
kll = int(input())

vs = cv2.VideoCapture(args["video"])

# loop over frames from the video stream
if(kll == 1):
		time.sleep(2.0)
		while True:

			frame = vs.read()  # for reading the frame
			frame = frame[1] if args.get("video", False) else frame


			if frame is None:
				break


			frame = imutils.resize(frame, width=600)


			(success, boxes) = trackers.update(frame)


			for box in boxes:               #for bounding boxes in each frame 
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


			cv2.imshow("Frame", frame)
			key = cv2.waitKey(20) & 0xFF


			if key == ord("s"):
				# select the bounding box of the object we want to track (make
				# sure you press ENTER or SPACE after selecting the ROI)
				box = cv2.selectROI("Frame", frame, fromCenter=False,
					showCrosshair=True)
				ki = list(box)
				print(ki)
				
				crop_img = frame[int(ki[1]):int(ki[1])+int(ki[3]), int(ki[0]):int(ki[0])+int(ki[2])]

				cv2.imwrite("frame.jpg",crop_img)
				
				tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
				trackers.add(tracker, frame, box)


			# if the `q` key was pressed, break from the loop
			elif key == ord("q"):
				break

			
		cv2.destroyAllWindows()


if(kll == 2):
	time.sleep(2.0)
	check = 0
	while True:

		if (check == 0):
			frame = vs.read() 
			frame = frame[1]             # for reading the frame
			frame = imutils.resize(frame, width=600)
			img_rgb = frame



			img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

			template = cv2.imread('frame.jpg',0)
			w, h = template.shape[::-1]


			for i in range(6,20):
				res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)       #for template matching
				threshold = i*0.05
				# print(str(threshold))
				loc = np.where( res >= threshold)
				k = 0
				for pt in zip(*loc[::-1]):
					k = k+1
				# print(k)
				if((k)==2):
					for pt in zip(*loc[::-1]):
						# cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
						print(pt[0],pt[1],w,h)
						check = 1
						list11 = (pt[0],pt[1],w,h)
						tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
						trackers.add(tracker, frame, list11)

						# print(threshold)
						break
					break
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(20) & 0xFF		
			if key == ord("q"):
				break






		if (check == 1):
			frame = vs.read()  # for reading the frame
			frame = frame[1]
		


			if frame is None:
				break


			frame = imutils.resize(frame, width=600)


			(success, boxes) = trackers.update(frame)


			for box in boxes:               #for bounding boxes in each frame 
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


			cv2.imshow("Frame", frame)
			key = cv2.waitKey(20) & 0xFF







			
			if key == ord("q"):
				break

			
	cv2.destroyAllWindows()
