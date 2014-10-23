'''
Script: gather_caffe_features.py
================================

Description:
------------
	
	This script allows one to assemble a matrix where rows correspond to frames 
	and columns correspond to features gathered by Caffe. It will only include the 
	features that have already been computed and are present on disk, and include a 
	code-book of which row is which mask in which image.

Usage: 
------

	python gather_caffe_features.py


##############
Jay Hack
Fall 2014
jhack@stanford.edu
##############
'''
from RecipeWatchRelated import *

if __name__ == '__main__':

	sd = StorageDelegate()
	for video in sd.iter_videos():
		for frame in video.iter_frames():
			