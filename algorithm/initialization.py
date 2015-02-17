#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np

def basic_seed( data, classes, **user ) :
## Возвращаем векторы принадлежности
	return [ np.zeros( data.shape[ 0 ] , dtype = np.float )
		for c in xrange( classes ) ]