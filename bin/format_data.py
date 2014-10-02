'''
Script: format_data.py
======================

Description:
------------
	
	This script allows one to convert data as it appears in the raw (original) 'cpmc' directory 
	to the format that the RecipeWatch program will use. Concretely, it goes from the original 
	storage format:

		cpmc/CPMC/data/
			cpmc_video_name_0/
				JPEGImages/
					frame_name_0.jpg
					...
				Masks/
					mask_name_0.mat
					...
			...

	to the desired format:

		data/videos/
			video_name_0/
				frame_name_0/
					image.jpeg 
					scores.pkl
					masks.pkl
				...
			...

	This allows for easier indexing and faster loading; most notably, it decouples the masks and 
	'objectness scores' for object candidates found within the image, so that they can be loaded 
	independently.



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
import os
import shutil
import sys
import argparse
import pickle
from pprint import pprint
from scipy.io import loadmat
import numpy as np

from SparseTensor import SparseTensor

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


################################################################################
####################[ Setup	Input/Output]#######################################
################################################################################

def make_video_dir(videos_dir, video_name):
	"""
		given a path, makes a video directory there in the following structure:
		video_name/
			frames/
		returns path to that video dir
	"""
	video_dir = os.path.join(videos_dir, video_name)
	if not os.path.isdir(video_dir):
		os.mkdir(video_dir)
	os.mkdir(os.path.join(video_dir, 'frames'))
	return video_dir


def setup_output_dir(output_dir, video_names):
	"""
		sets up the output directory to have one directory 
		for each video; returns a dict mapping video name -> video dir 
		path 
	"""
	#=====[ Step 1: make a clean 'video' folder]=====
	videos_dir = os.path.join(output_dir, 'videos')
	if os.path.exists(videos_dir):
		shutil.rmtree(videos_dir)
	os.mkdir(videos_dir)

	#=====[ Step 2: make individual video dirs	]=====
	output_video_dirs = {}
	for video_name in video_names:
		video_dir = make_video_dir(videos_dir, video_name)
		output_video_dirs[video_name] = video_dir
	return output_video_dirs


def get_video_dirs(video_names):
	"""
		given the video names, this will format the output directory and 
		return a dict mapping video name to a dict containing input path 
		and output path 
	"""
	input_video_dirs = {video_name:os.path.join(input_dir, video_name, 'data') for video_name in video_names}
	output_video_dirs = setup_output_dir(output_dir, video_names)
	video_dirs = {video_name:{} for video_name in video_names}
	for video_name in video_names:
		video_dirs[video_name]['input'] = input_video_dirs[video_name]
		video_dirs[video_name]['output'] = output_video_dirs[video_name]
	return video_dirs





################################################################################
####################[ Transfer Data ]###########################################
################################################################################

def get_frame_names(input_dir):
	"""
		given a video input dir, returns a list of all frame names,
		sorted.
	"""
	return sorted(os.listdir(os.path.join(input_dir, 'JPEGImages')))


def get_frame_index(frame_name):
	"""
		returns the frame index from a frame name 
	"""
	return int(frame_name.split('.')[0][-5:])


def make_frame_dir(video_paths, frame_index):
	"""
		given a video's directories and a frame index, this will make 
		a directory for it. returns a path to this frame directory
	"""
	frame_dir_path = os.path.join(video_paths['output'], 'frames', str(frame_index))
	os.mkdir(frame_dir_path)
	return frame_dir_path


def get_frame_input_paths(video_paths, frame_name):
	"""
		given a video's paths and a frame name, this will return 
		paths to it's "JPEGImages" data and its "masks" data
	"""
	jpeg_path = os.path.join(video_paths['input'], 'JPEGImages', frame_name)
	masks_path = os.path.join(video_paths['input'], 'Masks', frame_name[:-4] + '.mat')
	if not os.path.exists(masks_path):
		masks_path = None
	return jpeg_path, masks_path


def get_frame_output_paths(frame_output_dir):
	"""
		given a frame output dir, returns jpeg, masks, scores paths 
	"""
	fod = frame_output_dir
	return os.path.join(fod, 'image.jpg'), os.path.join(fod, 'masks.npy'), os.path.join(fod, 'scores.npy')


def transfer_frame(frame_name, video, paths):
	"""
		given the name of a frame, it's video, and that video's paths,
		this will transfer the named frame over to the output directory 
	"""
	#=====[ Step 1: make the frame directory, get path to it ]=====
	frame_index = get_frame_index(frame_name)
	frame_output_dir = make_frame_dir(paths, frame_index)

	#=====[ Step 2: get input/output locations	]=====
	jpeg_input_path, masks_input_path = get_frame_input_paths(paths, frame_name)
	jpeg_output_path, masks_output_path, scores_output_path = get_frame_output_paths(frame_output_dir)

	#####[ DEBUG OUTPUT	]#####
	# print '	##[ Transferring Frame: %s ]##' % frame_name
	# print '		frame_index: %s' % frame_index 
	# print '		frame_output_dir: %s' % frame_output_dir
	# print '		jpeg_input_path: %s' % jpeg_input_path
	# print '		jpeg_output_path: %s' % jpeg_output_path
	# print '		masks_input_path: %s' % masks_input_path
	# print '		masks_output_path: %s' % masks_output_path	
	# print '		scores_output_path: %s' % scores_output_path

	#=====[ Step 3: do the copying	]=====
	shutil.copy(jpeg_input_path, jpeg_output_path)
	if masks_input_path:
		masks_scores_coupled = loadmat(open(masks_input_path, 'r'))
		masks = SparseTensor(masks_scores_coupled['masks'])
		scores = masks_scores_coupled['scores']
		np.save(open(masks_output_path, 'w'), masks)
		pickle.dump(open(scores_output_path, 'w'), scores)






def transfer_video(name, paths):
	"""
		given a video name and its input/output paths contained in the dict 
		'paths', this will transfer relevant information over
	"""
	input_dir, output_dir = paths['input'], paths['output']
	frame_names = get_frame_names(input_dir)
	num_frames = len(frame_names)
	for frame_name in frame_names:
		frame_index = get_frame_index(frame_name)
		print '	Transferring Frame: %d/%d' % (frame_index, num_frames)
		transfer_frame(frame_name, name, paths)




if __name__ == '__main__':

	#==========[ ARGPARSING	]==========
	parser = argparse.ArgumentParser(description="Parse format_data.py arguments")
	parser.add_argument(	'-i', '--input_dir',
							metavar='I', type=str, nargs=1, dest='input_dir', required=True,
							help='path to source data (local filesystem)', 
							action='store')
	parser.add_argument(	'-o', '--output_dir',
							metavar='O', type=str, nargs=1, dest='output_dir', required=True,
							help='path to output directory (local filesystem)', 
							action='store')
	args = parser.parse_args ()
	input_dir,output_dir = args.input_dir[0], args.output_dir[0]
	if not os.path.exists(input_dir) and os.path.exists(output_dir):
		raise Exception("make sure that input and output directories are actual paths")
	input_dir = os.path.join(input_dir, 'CPMC')


	#=====[ Step 1: get video_dirs ]=====
	"""
		video_dirs is a dict as follows:
			video_dirs: video_names -> (input_dir, output_dir)
	"""
	video_names = os.listdir(input_dir)
	video_dirs = get_video_dirs(video_names)

	#=====[ Step 2: for each frame, transfer over the information	]=====
	for name, paths in video_dirs.iteritems():
		print '---> Transferring Video: %s...' % name
		transfer_video(name, paths)










