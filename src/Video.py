####################
# Class: Video
# ------------
# used to contain all information relevant to a single video
import os

class Video:

	def __init__(self, name, video_dir):
		self.name = name
		self.video_dir = video_dir
		self.data_dir = os.path.join(video_dir, 'data')
		self.frames_dir = os.path.join(self.data_dir, 'JPEGImages')
		self.masks_dir = os.path.join(self.data_dir, 'Masks')

		self.frame_paths = sorted([os.path.join(self.frames_dir, name) for name in os.listdir(self.frames_dir)])
		self.mask_paths = sorted([os.path.join(self.masks_dir, name) for name in os.listdir(self.masks_dir)])

		if not len(frame_paths) == len(mask_paths):
			raise Exception("The number of mask paths != number of frame paths in video: %s" % name)





