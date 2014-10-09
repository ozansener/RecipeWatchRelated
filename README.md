Projects related to the Recipe Watch project including
===================

- [Anticipating the next object by Jay Hack](#anticipating-the-next-object)


### Anticipating the next object

Dependencies:
-------------
Note: easiest way to satisfy these dependencies is through installing Anaconda. This will contain python,
ipython and everything else you will need.

Here are the packages:
- numpy
- scipy
- pillow (formerly PIL)
- mongodb, pymongo
- scikit-image


Setup:
------
~$: cd RecipeWatchRelated
~$: source ./configure.sh
~$: mongodb --dbpath=$MONGODB_DBPATH
~$: ipython
In [1]: from RecipeWatchRelated import *
...

