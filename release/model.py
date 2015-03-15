#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__date__            = "2015-03-15"
__author__          = "Makhalova, Nazarov"
__email__           = "tpmakhalova@edu.hse.ru, innazarov@edu.hse.ru"
__dscription__      = """Основной вычислительный модуль"""

##########################################################################################

import matplotlib.pyplot as plotter
import mpl_toolkits.mplot3d

import numpy as np
import FillGaps as fg

################################################################################
class model( object ):
    def __init__( self ):
        super( model, self ).__init__( )
        self.__dataset = self.__original = None
        self.__name = None
        self.__application = None
################################################################################
    def register( self, application ) :
        if self.__application is None :
            self.__application = application
        return self
    def start( self ) :
        pass
################################################################################
    def has_data( self ) :
        return self.__dataset is not None
    def load_datafile( self, fin ) :
        self.__dataset = np.genfromtxt( fin.name, delimiter = ',' )
        self.__original = self.__dataset.copy( )
        self.__name = fin.name
    def __call__( self ) :
        return self.__dataset
    def get_data_info( self ) :
        if self.__dataset is None : return ( '', 0, 0, )
        return ( self.__name, self.__dataset.shape[ 0 ], self.__dataset.shape[ 1 ] )
    def get_class_range( self ) :
        if self.__dataset is None : return ( 0, 0, )
        return ( 2, self.__dataset.shape[ 0 ] // 15 + 1 )
    def show_data( self ) :
        if self.__dataset is None : return
## Do the PCA
        figure = plotter.figure( figsize = ( 8, 4 ), facecolor = 'w' )
        ax = figure.gca( projection = '3d' )
        xLabel = ax.set_xlabel( '\nX', linespacing = 3.2 )
        yLabel = ax.set_ylabel( '\nY', linespacing = 3.1 )
        zLabel = ax.set_zlabel( '\nZ', linespacing = 3.4 )
        if self.__dataset.shape[ 1 ] < 3 :
            zs = np.zeros( self.__dataset.shape[ 0 ] )
        else:
            zs = self.__dataset[ :, 2 ]
        if self.__dataset.shape[ 1 ] < 2:
            ys = np.zeros( self.__dataset.shape[ 0 ] )
        else:
            ys = self.__dataset[ :, 1 ]
        xs = self.__dataset[ :, 0 ]
        ax.scatter( xs, ys, zs, c = 'b', marker = 'o' )
        ax.dist = 10
        plotter.show( )

if __name__ == '__main__':
    pass