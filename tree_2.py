#! /usr/bin/env python
# -*- coding: utf-8 -*-

from defs import *
import collections

class SemTree:
	@staticmethod
	def _int64():
		return 1

	@staticmethod
	def int():
		return 2

	@staticmethod
	def func():
		return 3

	@staticmethod
	def identifier():
		return 4

	@staticmethod
	def get_type_name(sem_type):
		if sem_type == SemTypes._int64():
			return '_int64'
        elif sem_type == SemTypes.int():
            return 'int'
        else:
            raise ValueError("Недопустимое значение параметра: " + str(sem_type))

class Node:
	"""
		name - идентификатор
		type - тип синтаксической конструкции (переменная, ф-ия и.т.д.)
		semtype - семантический тип
	"""

	def __init__(self, name, type, sem_type):
		self.__name = name
		self.__type = type
		self.__sem_type = sem_type