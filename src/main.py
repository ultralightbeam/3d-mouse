"""Build a simple gestures box by running a simple neural net classifier on 3-axis accel data (MPU6050) stream. 

	Force ~15 Hz stream on ide side

	Data flow:
		[mpu6050 raw accel]
		-> feature extraction (e.g. subspacing)
		-> classification (e.g. NN)
		-> [inference result (e.g. shaking the box, drawing a circle with the box)]
	
	(TODO)
	Display rate is lower than stream rate and lagging aggregates 
		- need to put check condition until stream hits most recent value

	Usage:
		$ python main.py /dev/tty.X

"""

import numpy as np
import serial
import sys
import time
import matplotlib.pyplot as plt
import cv2
from sklearn.neural_network import MLPClassifier


IS_DEBUG = 0 # mode for debug plot and print
IS_PRINT_FS = 0
IS_PRINT_STREAM = 0 # mode for printing stream val for training
IS_OUTPUT_BAR = 1 # mode for outputting sample volue

N_BUFFER_DISPLAY = 100 # size of buffer for autogain display
N_BUFFER_COMPUTE = 20 # size of buffer for classifier compute

N_DISPLAY_HEIGHT = 500 # size of image height for display

N_BUFFER_DECISION = 5


# fixed parameters.
BAUDRATE = 9600
N_DIM = 3   # dimension of input stream


def extract_features(M):
	for k in range(M.shape[1]):
		M[:, k] -= np.mean(M[:, k])
	v_feat = M.flatten()
	return v_feat

def round_clean(val):
	"""Round to first dec point.
	"""
	return int(val * 10) / 10.

def autogain(v):
	"""Compress a np vector into [0, 1] for display purposes.
	"""
	return (v - min(v)) / (max(v) - min(v))

def shift_buffer(M, val):
	"""Left-shift a buffer for update values.
	Assume columnwise update.
	"""
	if M.shape[0] != len(val):
		sys.exit('bad dimensions for update')
	M[:, :-1] = M[:, 1:]
	M[:, -1] = val
	return M

def main(argv):
	if N_BUFFER_DISPLAY < N_BUFFER_COMPUTE:
		return -1
	path_device = argv[0]
	# Open up MPU6050 stream.
	ser = serial.Serial(path_device)
	ser.baudrate = BAUDRATE
	M_buffer_display = np.zeros((N_DIM, N_BUFFER_DISPLAY)) + 10**-12 # epsilon for autogain conditioning.
	v_buffer_decision = np.zeros(N_BUFFER_DECISION)
	counter_frame = 0
	time_prev = -1
	time_now = -1
	frame_rate = -1

	N_OUTPUT_BAR = 30

	dict_model = np.load('model.npy').item()
	clf = dict_model['clf']

	plt.figure
	while True:
		line = ser.readline().decode('utf-8')
		accel_line = line.split(', ')
		vals = np.zeros(N_DIM)
		for k in range(N_DIM):
			vals[k] = float(accel_line[k].split('=')[-1])
		M_buffer_display = shift_buffer(M_buffer_display, vals)
		M_buffer_compute = M_buffer_display[:, -N_BUFFER_COMPUTE:]

		if IS_DEBUG:
			# Normalize display data for image plotting.
			M_buffer_display_norm = M_buffer_display.copy()
			for k in range(N_DIM):
				M_buffer_display_norm[k, :] = autogain(M_buffer_display[k, :])
			# Convert display data into image domain.
			M_buffer_display_image = np.zeros((N_DISPLAY_HEIGHT, N_BUFFER_DISPLAY))
			for k in range(N_DIM):
				for k_buf in range(N_BUFFER_DISPLAY):
					M_buffer_display_image[-int(M_buffer_display_norm[0, k_buf] * N_DISPLAY_HEIGHT):, k_buf] = 1
			print(M_buffer_display_norm) # debug raw accel print
			cv2.imshow('raw stream', M_buffer_display_image)
			cv2.waitKey(33)
		if IS_PRINT_FS:
			print('fs = ' + str(round_clean(frame_rate)) + ' Hz')
		if counter_frame == 0:
			time_prev = time.time()
		else:
			time_now = time.time()
			# compute	frame rate
			frame_rate = counter_frame / float(time_now - time_prev)
		if IS_PRINT_STREAM:
			print(str(time.time()) + ':' + str(M_buffer_compute[:, -1]))
		counter_frame += 1
		
		feat_vec = extract_features(M_buffer_compute.T.copy()).reshape(1, -1)
		class_predict = clf.predict(feat_vec)[0]

		v_buffer_decision[:-1] = v_buffer_decision[1:]
		v_buffer_decision[-1] = class_predict
		class_predict_fin = np.median(v_buffer_decision)

		if IS_DEBUG:
			if class_predict_fin == 0:
				print(' ')
			elif class_predict_fin == 1:
				print('clockwise')
			elif class_predict_fin == 2:
				print('anticlockwise')

		if IS_OUTPUT_BAR:
			if class_predict_fin == 1:
				N_OUTPUT_BAR += 1
			elif class_predict_fin == 2:
				N_OUTPUT_BAR -= 1
			print('\n' * 10)
			print(' O ' * N_OUTPUT_BAR)

                        

if __name__ == '__main__':
	main(sys.argv[1:])
	print('terminated.')

