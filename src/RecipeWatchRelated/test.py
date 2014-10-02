import numpy as np 
import scipy as sp
import matplotlib.pyplot as plt

from StorageDelegate import *
from Video import *
from Frame import *

if __name__ == '__main__':

	#=====[ Setup ]=====
	sd = StorageDelegate()
	video = sd.get_random_video()
	frame = video.get_random_frame()
	plt.imshow(frame.visualize_mask(1))
	plt.show()

