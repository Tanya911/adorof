#! /usr/bin/env python
# -*- coding: UTF-8 -*-

## Common dependencies
import numpy as np

## Private dependencies
from scipy.cluster.hierarchy import linkage
class pi0_hier(object):
	"""Класс (pi0_hier) для порождения начального разбиения
	агломеративной иерархической кластеризацией. Использование:
		pi0 = pi0_hier()
		init_partition = pi0(
			data = данные,
			K = количество классов,
			method = метод подсчёта схожести наборов точек )
	Суть метода: на исходных данных последовательным объедининем пар множеств
	разбиения (снизу--вверх) строится иерархия классов согласно мере близости,
	указанной при вызове. По завершении производится откат на K шагов назад до
	той итерации, когда количество классов уменьшилось до K штук. Существенный
	недостаток методоа состоит в том, при выборе оптимистичного метода оценки
	схожести множеств (single linkage) возможно порождение атомарных классов,
	что не подходит для m-локальной оптимизации."""
	def __init__( self ):
		super(pi0_hier, self).__init__( )
## Scalp off the last iterations of agglomerative clustering
##  to figure out the partition with K classes
	def __call__( self, data, K = 5, **kwargs ) :
		clust = linkage( data, **kwargs )
## Get K least cluster IDs
		C = np.sort( clust[ -K+1:, :2 ].ravel( ) )[ : K ]
		return [ self.__rebuild( clust, c ) for c in C ]
## Rebuild the class synthesized at k-th iteration of
##   agglomerative hierarchical clustering
	def __rebuild( self, clust, iter ) :
		if iter <= clust.shape[ 0 ] : return [ int( iter ) ]
		i, j = clust[ iter - clust.shape[ 0 ] - 1, :2 ]
		return self.__rebuild( clust, i ) + self.__rebuild( clust, j )

## Private dependencies
from itertools import combinations as comb
from scipy.spatial.distance import pdist, squareform
class partition_criterion(object):
	"""Класс реализует оценку качества разбиения исходных данных.
	Параметры инициализации:
	-- $\\alpha$, $p$ параметры трансформации расстояния в меру близости:
		$$K(x,y) = e^{ -\alpha d(x,y)^p }$$
	Использование:
		crit = partition_criterion(
			data = данные,
			alpha = масштаб,
			p = степень )
	## Критерий внутриклассовой близости
		crit.I1( pi = разбиение на классы в формате списка списков )
	## Критерий межклассовой близости
		crit.I2( pi = разбиение на классы в формате списка списков )
	## Комбинированный критерий тербующий похожести внутри класса и
	##  различий между классами
		crit( pi = разбиение на классы в формате списка списков )
	"""
	def __init__(self, data, alpha = .5, p = 2, **kwargs ):
		super(partition_criterion, self).__init__()
		K = np.exp( - alpha * ( pdist( data, **kwargs ) ** p ) )
		self.__pdist = squareform( K )
## Reomve the diagonal, since self-similarity should not contribute to
##  the clustering quality criteria.
		np.fill_diagonal( self.__pdist, 0 )
## Implement average linkage
	def I1( self, pi ) :
## Atomic or empty classes must be heavily penalized, but not so much as to 
##  inhibit any data point transfers.
		if np.any( [ len( i ) < 2 for i in pi ] ) : return 0 ##-np.inf
		return np.mean( np.array( [ np.mean( self.__pdist[ np.ix_( i, i ) ],
			dtype = np.float64 )* len( i ) / ( len( i ) - 1.0 ) for i in pi ] ) )
	def I2( self, pi ) :
		if np.any( [ len( i ) < 2 for i in pi ] ) : return -np.inf
		return np.mean( [ np.mean( self.__pdist[ np.ix_( i, j ) ] )
			for i, j in comb( pi, 2 ) ] ) * len( pi ) / ( len( pi ) - 1.0 )
	def __call__( self, pi ) :
		return self.I1( pi ) / self.I2( pi )

## Private dependencies
from scipy.spatial.distance import cdist
from numpy import argpartition as argtop
class s_local(object) :
	"""Класс m-локальной кластеризации. Использование:
		sloc = s_local(
			data = данные,
			crit = класс критерия качества кластеризации )
		## Полный раунд s-локальной оптимизации. Разбиение изменяется или
		##  не изменяетя автоматически. Возвращает новое значение критерия
		##  кластеризации для полученного нового разбиения. Агрумент pi
		##  передаётся по ссылке и претерпевает изменения!
		sloc.s_local(
			pi = текущее разбиение,
			s = количество перебрасываемых точек,
			I0 = текущее значение критерия )
		## Полная процедура m-локальной оптимизации. Производит m полных
		##  раундов s-локальной оптимизации. Аргумент разбиения передаётся
		##  по ссылке и изменяется в процессе работы процедуры.
		sloc.m_local(
			pi = текущее разбиение,
			m = количество перебрасываемых точек )
	"""
	def __init__(self, data, crit ):
		super(s_local, self).__init__()
		self.__data = data
		self.__crit = crit
## A basic step of the s-local optimisation procedure
	def __xfer( self, pi, src, dst, s = 1, I0 = None ) :
		if I0 is None :
			I0 = self.__crit( pi )
## There is no point in shuffling the data points withing the same class
		if src == dst : return I0
## Keep moving batches of s data points until convergence
		while len( pi[ src ] ) >= s + 2 :
## Compute the current centroid of the dst-class : O( n )
			centroid = np.mean( self.__data[ pi[ dst ] ], axis = 0 )
## Compute the distances to the centroid : O( n )
			distances = cdist( [ centroid ], self.__data[ pi[ src ] ] )
## Find s nearest neighbours using introselect ( min-heap + quickselect ): O( n log s)
			sNN = set( argtop( distances[ 0 ], s )[ :s ] )
## Save the original classes (copies) 
			S0, D0 = list( pi[ src ] ), list( pi[ dst ] )
## Move them from S to D: this modifies the partition pi directly!
			list.extend( pi[ dst ], ( S0[ n ] for n in sNN ) )
			pi[ src ] = list( x for n, x in enumerate( S0 ) if n not in sNN )
## Compute the criterion of the modified partition
			I1 = self.__crit( pi )
## If the criterion has not increased, rollback
			if I1 <= I0 :
				pi[ src ], pi[ dst ] = S0, D0
				break
## Indicate that the partition has been altered and proceed
			I0 = I1
## The partition is updated (or not) automatically
		return I0
	def __cycle( self, pi, src, s = 1, I0 = None ) :
		if I0 is None :
			I0 = self.__crit( pi )
## a full cycle through the classes
		dst = 0
## Pick the class to modify. If we fall off the array, this means stabilization has occurred
		while dst < len( pi ) and len( pi[ src ] ) >= s + 2 :
			I1 = self.__xfer( pi, src, dst, s = s, I0 = I0 )
## Continue if the transfers did not yield significant fittness increase
			if I1 <= I0 :
				dst += 1
				continue
## Otherwise restart
			I0 = I1 ; dst = 0
		return I0
	def s_local( self, pi, s = 1, I0 = None ) :
		if I0 is None :
			I0 = self.__crit( pi )
		src = 0
		while src < len( pi ) :
## If the class is of sufficient volume ( the least volume is 2 points )
			if len( pi[ src ] ) >= s + 2 :
##  begin the s-local point transfer cycle
				I1 = self.__cycle( pi, src, s = s, I0 = I0 )
## If the partition has been modified, restart
				if I1 > I0 :
					I0 = I1 ; src = 0
					continue
## Otherwise continue
			src += 1
## The s-local optimization step is finished when no
##  modification to the partition have been made.
		return I0
## m-local optimization: go through the number of points transferred between
##  classes in succession.
	def m_local( self, pi, m = 5 ) :
		s = 1 ; I0 = self.__crit( pi )
		while s <= m :
			I1 = self.s_local( pi, s = s, I0 = I0 )
			if I1 <= I0 :
## No improvement -- proceed to the next round of point transfers
				s += 1
				continue
## Restart from the very beginning
			I0 = I1 ; s = 1
		return I0
