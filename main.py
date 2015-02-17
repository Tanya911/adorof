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

def usage( ) :
	print "Кластеризация набора данных\n%s <имя набора данных в базе>" % (__file__)
	return -1

if __name__ == '__main__' :
## Если нам передали недостаточно аргументов, оповещаем пользователя
	if len( sys.argv ) < 2 :
		exit( usage( ) )
## Подсоединяемся к базе данных
	with lite.connect( 'db/main.db' ) as con :
## Тестовый сценарий
		cur = con.cursor( )
		cur.execute( """SELECT SQLITE_VERSION( )""" )
		data = cur.fetchone( )
## Вывод
		print "SQLite version: %s" % data

## КОНЕЦ
