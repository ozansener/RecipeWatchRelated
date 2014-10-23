'''
Script: caffe_featurize.py
==========================

Description:
------------
	
	This script allows one to add features from a caffe-trained CNN to the filesystem
	and MongoDB back-end.

Usage: 
------

	python caffe_featurize.py


##############
Jay Hack
Fall 2014
jhack@stanford.edu
##############
'''
from RecipeWatchRelated import *

if __name__ == '__main__':

	net = CaffeCNN()
	net.cnn #loads it for us.

	sd = StorageDelegate()
	for video in sd.iter_videos():
		for frame in video.iter_frames():
			print "---> Featurizing frame #: %d" % frame.index
			if frame.features is None and not frame.masks is None:
				frame.features = net.featurize_frame(frame)





