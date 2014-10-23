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
from itertools import islice

if __name__ == '__main__':

	sd = StorageDelegate()

	feature_vecs = []
	video_ids = []	
	frame_ids = []
	mask_ids = []

	for video in islice(sd.iter_videos(verbose=True), 2):
		for f in video.iter_frames(verbose=True):
			if not f.features is None:
				feature_vecs += f.features.values()
				video_ids += [video.name]*len(f.features.keys())
				frame_ids += [f.index]*len(f.features.keys())
				mask_ids += f.features.keys()

	feature_vecs = np.matrix(feature_vecs)
	video_ids = np.array(video_ids)
	frame_ids = np.array(frame_ids)
	mask_ids = np.array(mask_ids)

