#####################
# Module: StorageDelegate
# =======================
# manages data input/output
#
# Ideal Usage:
# ------------
# 
# 
import os
import sys
import json
import pandas as pd
import numpy as np
from Video import *


class StorageDelegate:

	def __init__ (self, data_dir=os.path.join(os.getcwd(), '../data/cpmc/CPMC')):
		self.data_dir = data_dir
		self.video_dirs = self.get_video_dirs(self.data_dir)
		self.videos = self.get_videos(self.video_dirs)


	def get_video_dirs(self, data_dir):
		"""
			given cpmc_dir, returns list of full paths to individual dirs
		"""
		return {d:os.path.join(data_dir, d) for d in os.listdir(data_dir) if not d.startswith('.')}


	def get_videos(self, video_dirs):
		"""
			returns dict: VideoName -> Video
		"""
		return {name:Video(name, video_dir) for name, video_dir in video_dirs.items()}







	####################################################################################################
	######################[ --- JSON MANAGEMENT --- ]###################################################
	####################################################################################################

	def iter_json_files (self, data_dir):
		"""
			iterates over all json files in the passed directory, 
			returning them as dicts
			TODO: change os.listdir to a generator
		"""
		json_filenames = filter(lambda x: x.endswith('.json'), os.listdir(data_dir))
		json_filenames = [os.path.join(data_dir, f) for f in json_filenames]
		for f in json_filenames:
			try:
				yield json.load(open(f, 'r'))
			except:
				print "*** encountered non-JSON object: %s ***" % f 
				continue


	def dump_block (self, block_data, output_dir):
		"""
			given block_data, containing a list of python dicts, and an output 
			dir, this will create a new block and store the contents there 
		"""
		print "===[ DUMPING BLOCK: %d entries ]===" % len(block_data)
		block_df = pd.DataFrame(block_data)
		block_name = 'block_' + str(time.time()) + '.df'
		block_fullpath = os.path.join(output_dir, block_name)
		block_df.to_pickle(block_fullpath)


	def consolidate_jsons (self, input_dir, output_dir, format_function=lambda x: x):
		"""
			params:
				- input_dir: path to directory containing raw json files 
				- output_dir: path to directory to store blocks in 
				- format_function: function to format raw json with, before 
									storing in blocks 
			description:		
				iterates over all json files in input_dir, then groups and saves them 
				in blocks of size block_size in the output_dir
		"""
		self.clear_directory (output_dir)
		counter = 0
		current_block = []
		for f in self.iter_json_files (input_dir):
			for js in f:
				formatted = format_function (js)
				if not formatted:
					continue
				current_block.append (formatted)
				counter += 1
				if counter % 1000 == 0:
					print len(current_block)
				if counter % self.block_size == 0:
					self.dump_block (current_block, output_dir)
					del current_block
					current_block = []
		if not counter % self.block_size == 0:
			self.dump_block (current_block, output_dir)


	def load_blocks(self, blocks_dir, n_blocks=None):
		"""
			loads the specified number of blocks in and returns them,
			concatenated.
		"""
		assert os.path.exists(blocks_dir)
		block_names = filter(lambda s:s.endswith('.df'), os.listdir(blocks_dir))
		block_filepaths = [os.path.join(blocks_dir, n) for n in block_names]
		if not n_blocks:
			n_blocks = len(block_filepaths)
		blocks = [pd.read_pickle(f) for f in block_filepaths[:n_blocks]]
		return pd.concat(blocks)




	####################################################################################################
	######################[ --- PANDAS MANAGEMENT--- ]##################################################
	####################################################################################################

	def dump_dataframe_raw (self, df, output_dir):
		"""
			dumps the passed dataframe to pandas_raw
		"""
		print "===[ DUMPING DF RAW: %d entries ]===" % len(df)
		block_name = str(time.time()) + '.df'
		df.to_pickle (os.path.join(output_dir, block_name))


	def blocks_to_dfs (self, input_dir, output_dir):
		"""
			converts json_blocks to pandas dataframes 
		"""
		self.clear_directory (output_dir)
		for f in self.iter_json_files ():
			df = pd.DataFrame(f)
			self.dump_dataframe_raw(df, output_dir)


	def pandas_raw_names (self, data_dir):
		"""
			returns a list of filepaths to pandas raw blocks
		"""
		return [os.path.join(data_dir, f) for f in os.listdir(data_dir)]


	def load_pandas_raw (self, input_dir, num_blocks=1):
		"""
			loads 'num_blocks' of pandas dataframes into memory,
			stores them all into a single pandas dataframe via 
			concatenation
		"""
		blocknames = self.pandas_raw_names(input_dir)[:num_blocks]
		dfs = [pd.read_pickle(bn) for bn in blocknames]
		return pd.concat (dfs)







if __name__ == '__main__':

	sd = StorageDelegate()





