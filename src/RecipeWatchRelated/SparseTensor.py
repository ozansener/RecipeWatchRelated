#####################
# Class: SparseTensor
# -------------------
# class used to represent a sparse 3D matrix (3rd order tensor)
#####################
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix

class SparseTensor:
	"""
		Used to represent a sparse 3D matrix (3rd order tensor)
		Represented as a list of scipy sparse matrices
		Good for representing masks!
	"""
	def __init__(self, tensor):
		if not len(tensor.shape) == 3:
			raise Exception("Must be a 3rd order tensor")
		self.shape = tensor.shape
		self.matrices = [csr_matrix(tensor[:,:,i]) for i in range(tensor.shape[2])]


	def __getitem__(self, slices):
		"""
			allows one to slice this matrix
			currently only support slicing on the 3rd index.
		"""
		slice_i, slice_j, slice_k = slices
		if slice_i.start or slice_j.start:
			raise NotImplementedError("Only index based on K for now")
		else:
			return self.matrices[slice_k]
