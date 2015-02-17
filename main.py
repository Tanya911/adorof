#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__date__ 			= "2015-02-17"
__author__ 			= "Makhalova, Nazarov"
__email__ 			= "tpmakhalova@edu.hse.ru, innazarov@edu.hse.ru"
__status__ 			= "Stub"
__version__ 		= "0.0"
__dscription__ 		= """Основной модуль работы по курсу "Структурно-классификационные методы интеллектуального анализа данных и прогнозирования в слабо формализованных системах" """

import sys

import sqlite3 as lite

import numpy as np
import numpy.random as rnd

## Информация об использовании
def usage( ) :
	print "Кластеризация набора данных\n%s <имя набора данных в базе>" % (__file__)
	return -1

## Проверка динамического подключения модулей
def attach( module, procedure ) :
	try:
## ПОдключаем модуль
		return getattr( __import__( "algorithm." + module,
			globals( ), locals( ), [ procedure ], -1 ), procedure )
	except Exception, e:
## Пропускаем ошибку выше
		raise e

def get_dataset( name ):
## Загружаем данные из базы
	return np.empty( shape = (0,3), dtype = np.float )

## Ветка основного модуля
if __name__ == '__main__' :
## Если нам передали недостаточно аргументов, оповещаем пользователя
	if len( sys.argv ) < 2 :
		exit( usage( ) )

	dataset_name = sys.argv[ 1 ]

## Подсоединяемся к базе данных
	with lite.connect( 'db/main.db' ) as con :
## Тестовый сценарий
		cur = con.cursor( )
		cur.execute( """SELECT SQLITE_VERSION( )""" )
		data = cur.fetchone( )
## Вывод
		print "SQLite version: %s" % data

## Подсоединяем модули на лету
	fill_missing = attach( "missing_data", "pass_through" )
	count_classes = attach( "class_count", "user_specified" )
	seed = attach( "initialization", "basic_seed" )
	cluster = attach( "clustering", "dumb_clustering" )
	
	user_params = { "K" : 5 }

## Основная работа модуля
	data_raw = get_dataset( dataset_name )
	data = fill_missing( data_raw, **user_params )
	class_number = count_classes( data, **user_params )
	class_seed = seed( data, class_number, **user_params )

	result = cluster( data, class_number, class_seed )
	print result

## КОНЕЦ
