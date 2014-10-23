'''
Script: caffe_featurize.py
==========================

Description:
------------
	
	This script allows one to add features from a caffe-trained CNN to mongodb.


Usage: 
------

	python format_data.py -i [input_directory] -o [output_directory]

	i.e.

	python format_data.py 	-i ~/data/robobrain/recipewatch/raw_data \
							-o ~/data/robobrain/recipewatch/data


Args:
-----

	-i (--input_dir): path to source data directory on local filesystem
	-o (--output_dir): path to output directory on local filesystem


##############
Jay Hack
Fall 2014
jhack@stanford.edu
##############
'''
from RecipeWatchRelated import *

if __name__ == '__main__':

	net = CaffeCNN()
	net.cnn

	sd = StorageDelegate()
	for video in sd.iter_videos():
		print video
		for ix, frame in enumerate(video.iter_frames()):
			print "---> Featurizing frame #: %d" % ix
			frame.features = net.featurize_frame(frame)




