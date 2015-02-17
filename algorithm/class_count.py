#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np

def user_specified( data, **user ) :
	if not "K" in user :
		raise Exception( "Пользователь не укзал количество классов" )
	return user[ "K" ]