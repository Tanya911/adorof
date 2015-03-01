#! /usr/bin/env python
# -*- coding: UTF-8 -*-

__date__ 			= "2015-02-17"
__author__ 			= "Makhalova, Nazarov"
__email__ 			= "tpmakhalova@edu.hse.ru, innazarov@edu.hse.ru"
__status__ 			= "Stub"
__version__ 		= "0.0"
__dscription__ 		= """Основной модуль работы по курсу "Структурно-классификационные методы интеллектуального анализа данных и прогнозирования в слабо формализованных системах" """

import sys

import time as tm
import database as db

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

def parse_user_params( argv ) :
	return { "dataset" : argv[ 1 ], "K" : 5 }

## Ветка основного модуля
if __name__ == '__main__' :
## Если нам передали недостаточно аргументов, оповещаем пользователя
	if len( sys.argv ) < 2 :
		exit( usage( ) )

## Проверяем соединение
	db.test( )

## Определяем параметры введённые пользоватлем
	user_params = parse_user_params( sys.argv )

## Подсоединяем модули на лету (здесь можно реализовать
##  выбор алгоритма пользователем, но это потом!)
	fill_missing = attach( "missing_data", "do_nothing" )
	count_classes = attach( "class_count", "user_specified" )
	seed = attach( "initialization", "basic_seed" )
	cluster = attach( "clustering", "dumb_clustering" )

## Основная работа модуля
	try:
## Получаем данные из базы
		data_id, data_raw = db.get_dataset( name = user_params[ "dataset" ] )
## Обрабатываем числовые данные алгоритмами
## Пополняем пропуски
		data = fill_missing( data_raw, **user_params )
## Считаем классы
		class_number = count_classes( data, **user_params )
## Выбираем начальное разбиение
		class_seed = seed( data, class_number, **user_params )
## Кластеризуем
		result = cluster( data, class_number, class_seed )
## Собираем информацию для размещения в БД
		pass
## Сохраянем результаты в базе
		result_id = db.store_result( data_id, result )
## Вызываем модуль отрисовки
		# execfile( 'report.py', result_id )
	except Exception, e:
## Обработка исключений: просто выводи и выходим с кодом -2
		print e
		exit( -2 )

## КОНЕЦ
