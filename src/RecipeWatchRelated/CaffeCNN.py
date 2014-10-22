####################
# Class: CaffeCNN
# ---------------
# contains everything needed to apply a Caffe CNN
# to images in order to get feature representations
####################
import os
import numpy as np 
import scipy as sp
import caffe

class CaffeCNN:

	def __init__(self):
		"""
			loads the network 
		"""
		if not 'CAFFE_ROOT_PATH' in os.environ.keys():
			raise Exception("Run configure.sh to set environmental variables! Caffe not found")
		self.caffe_root = os.environ['CAFFE_ROOT_PATH']

		self.deploy_prototxt_path = os.path.join(self.caffe_root, 'models/bvlc_reference_caffenet/deploy.prototxt')
		self.model_path = os.path.join(self.caffe_root, 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel')
		self.net = caffe.Classifier(self.deploy_prototxt_path, self.model_path)


