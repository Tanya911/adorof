#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__date__            = "2015-03-15"
__author__          = "Makhalova, Nazarov"
__email__           = "tpmakhalova@edu.hse.ru, innazarov@edu.hse.ru"
__status__          = "Alpha"
__version__         = "0.5"
__dscription__      = """Основной модуль работы по курсу "Структурно-классификационные методы интеллектуального анализа данных и прогнозирования в слабо формализованных системах" """

import sys
import time as tm

try :
    import tkinter as tk
    from tkinter.ttk import Combobox
    from tkinter import filedialog as file_dlg
except :
    import Tkinter as tk
    from ttk import Combobox
    import tkFileDialog as file_dlg

import matplotlib
matplotlib.use( 'TkAgg' )

##########################################################################################
class Combox( Combobox ):
    def __init__( self, values, labels, **kwargs ) :
        self.values, self.labels = values, labels
        Combobox.__init__( self, values = labels, **kwargs )
    def current( self ) :
        return self.values[ Combobox.current( self ) ]

##########################################################################################
class Application( tk.Frame ):
    def __init__( self, hWnd, model ) :
        # super( Application, self ).__init__( )
        tk.Frame.__init__( self, hWnd )
        self.option_add( '*tearOff', False )
        self.__wnd = hWnd
        self.__menubar = None
        self.__menuitems = {}
        self.__model = model.register( self )
    def start( self ) :
## Parent
        self.__wnd.title( "Анализ данных" )
        self.__wnd.geometry( '{}x{}'.format( 600, 150 ) )
        self.__wnd.resizable( False, False )
## Menu bar
        self.__menubar = tk.Menu( self.__wnd, tearoff = 0 )
        self.__wnd.config( menu = self.__menubar )
## Exit
        self.__menubar.add_command( label = "Выход", underline = 0, command = self.__cmd_menu_exit )
## Data
        self.__menuitems[ 'data' ] = m_data = tk.Menu( self.__menubar )
        self.__menubar.add_cascade( label = "Данные", underline = 0, menu = m_data )
        m_data.add_command( label = "Загрузить данные", command = self.__cmd_menu_data_open )
        m_data.add_command( label = "Сохранить данные", command = self.__cmd_menu_data_save )
        # m_data.entryconfig( 0, state = tk.ENABLED )
        # m_data.entryconfig( 1, state = tk.DISABLED )
## Show
        self.__menuitems[ 'show' ] = m_show = tk.Menu( self.__menubar )
        self.__menubar.add_cascade( label = "Просмотр", underline = 0, menu = m_show )
        m_show.add_command( label = "Сырые данные", command = self.__cmd_menu_show_view )
        m_show.add_separator( )
        m_show.add_command( label = "Результаты", command = self.__cmd_menu_show_results )
        # m_show.entryconfig( 0, state = tk.DISABLED )
        # m_show.entryconfig( 1, state = tk.DISABLED )
## clustering : Add to the main bar
        self.__menuitems[ 'clustering' ] = m_clust = tk.Menu( self.__menubar )
        self.__menubar.add_cascade( label = "Кластеризация", underline = 0, menu = m_clust )
        # self.__menubar.entryconfig( 2, state = tk.DISABLED )
        m_clust.add_command( label = "Настройка...", command = self.__cmd_menu_cluster_setup )
        m_clust.add_separator( )
        m_clust.add_command( label = "Запуск", command = self.__cmd_menu_cluster_run )
        # m_show.entryconfig( 0, state = tk.DISABLED )
        # m_show.entryconfig( 1, state = tk.DISABLED )
## Initialize the controller
        self.__model.start( )
## Invoke the dispatcher
        self.__wnd.mainloop( )
## View -- window command routines
    def __cmd_menu_exit( self ) :
        self.quit( )
    def __cmd_menu_data_open( self ) :
        fin = self.__show_open_dialog( )
        # try :
        self.__model.load_datafile( fin )
        self.__display_show_datafile( )
        # except Exception, e:
            # self.__display_error( e.value )
        # finally :
        fin.close( )
    def __cmd_menu_data_save( self ) :
        pass
    def __cmd_menu_show_view( self ) :
        self.__model.show_data( )
    def __cmd_menu_show_results( self ) :
        pass
    def __cmd_menu_cluster_setup( self ) :
        setup_window( tk.Toplevel( self ), self.__model ).start( )
    def __cmd_menu_cluster_run( self ) :
        pass
    def __display_show_datafile( self ) :
        if not self.__moedl.has_data( ) :
            self.__display_error( "NODATA" )
            return
## Show basic info on the loaded datafile
        filename, n, attr = self.__model.get_data_info( )
        tk.Label( self.__wnd, text = "Загруженны данные из файла %s" % filename ).grid( row = 0, sticky = tk.W )
        tk.Label( self.__wnd, text = "Количество объектов: %d" % n ).grid( row = 1, sticky = tk.W )
        tk.Label( self.__wnd, text = "Количество признаков: %d" % attr ).grid( row = 2, sticky = tk.W )
## Enable menu options
        self.__menuitems[ 'show' ].entryconfig( 0, state = tk.ACTIVE )
        self.__menubar.entryconfig( 2,state = tk.ACTIVE )
    def __display_error( self, error ) :
        err_wnd = tk.Toplevel( self )
        err_wnd.geometry( '{}x{}'.format( 300, 40 ) )
        err_wnd.resizable( False, False )
        tk.Label( err_wnd, text = error ).grid( row = 0, sticky = tk.W )
    def __show_open_dialog( self ) :
        return file_dlg.askopenfile(
            filetypes = ( ( "CSV", "*.csv" ), ( "All files", "*.*" ) ) )

##########################################################################################
class log_window( tk.Frame ):
    def __init__(self, hWnd, log ):
        tk.Frame.__init__( self, hWnd )
        self.__wnd = hWnd
        self.__log = log
        self.start( )
    def start( self ) :
        self.__wnd.title( "Лог работы" )
        self.__wnd.geometry( '{}x{}'.format( 300, 100 ) )
        self.__wnd.resizable( False, False )
    def hide( self ) :
        pass
    def show( self ) :
        pass

##########################################################################################
class setup_window( tk.Frame ):
    def __init__(self, hWnd, model, callback = None ):
        tk.Frame.__init__( self, hWnd )
        self.__wnd = hWnd
        self.__callback = None
        self.__model = model
        self.start( )
    def start( self ) :
        if not self.__model.has_data( ) :
            self.__wnd.destroy( )
            return
        self.__wnd.title( "Настройка параметров кластеризации" )
        self.__wnd.geometry( '{}x{}'.format( 300, 100 ) )
        self.__wnd.resizable( False, False )
        self.__wnd.protocol( "WM_DELETE_WINDOW", self.onClose  )
## Put the combobox in its rightful place
        classes = range( *self.__model.get_class_range( ) )
        self.combobox = Combox( classes, [ str( i ) for i in classes ], master = self.__wnd, height = 5 )
        tk.Label( self.__wnd, text = "Количество классов при начальном разбиении:" ).grid( row = 1, sticky = tk.W )
        self.combobox.grid( row = 2, sticky = tk.W )
        self.combobox.set( 2 )
    def onClose( self ) :
        print self.combobox.current( )
        self.__wnd.destroy( )

##########################################################################################
if __name__ == '__main__' :
    from model import model as mdl
    Application( tk.Tk( ), mdl( ) ).start( )
    exit( 0 )
