#! /usr/bin/env python
# -*- coding: utf-8 -*-

from defs import *
from scaner import Scaner
from tree_2 import *

class Diagram():
	def __init__(self, text_file):
		self.scaner = Scaner(text_file) #Инициализация сканера
		self.__tree = Tree()  # инициализация семантического дерева
		self.curType = '' # текущий тип идентификатора для синтаксического дерева

	#Описания
	def S(self):
		_type = '' #Тип лексемы

		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(c_p) #Вернуть старую позицию

		while ( _type == INT or _type == INT64 or _type == VOID ):
			self.T()
			c_p = self.scaner.get_current_position()
			_type = self.scaner.scan()
			self.scaner.set_current_position(c_p)

	#Одно описание
	def T(self):
		_type = '' #Тип лексемы

		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(c_p) #Вернуть старую позицию

		if ( _type == VOID ):
			self.F()
		else:
			self.W()

	#Данные
	def W(self):
		_type = self.scaner.scan() #Получить текущую лексему
		
		if ( _type != INT and _type != INT64 ):
			print(_type)
			self.scaner.printError("ERROR! Expected int or _int64.")

		self.curType = IDENTITY[_type]

		self.D();

		_type = self.scaner.scan() #Получить текущую лексему

		if ( _type != SEMICOLON ):
			self.scaner.printError("ERROR! Expected semicolon (;).")

	#Список
	def D(self):
		_type = '' #Тип лексемы

		self.Z()

		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему

		while ( _type == COMMA ):
			self.Z()
			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему

		self.scaner.set_current_position(c_p) #Вернуть старую позицию

	#Переменная, массив и индекс
	def Z(self):
		_type = self.scaner.scan() #Получить текущую лексему

		if ( _type != ID ):
			self.scaner.printError("ERROR! Expected identifier.")

		# Занесение идентификатора в таблицу с типом curType
		v = self.__tree.semInclude(''.join(self.scaner.get_lex()), self.curType)
		if ( type(v) == str ):
			self.scaner.printError(v)

		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type == SAVE ):
			self.A()
		elif ( _type == LSBRACKET ):
			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
			if ( _type != RSBRACKET ):
				self.scaner.set_current_position(c_p) #Вернуть старую позицию
				self.A()
				#Проверим закрывается ли скобка
				c_p = self.scaner.get_current_position() #Запомнить текущую позицию
				_type = self.scaner.scan() #Получить текущую лексему
				if ( _type != RSBRACKET ):
					self.scaner.printError("ERROR! Expected right square bracket.")
				c_p = self.scaner.get_current_position() #Запомнить текущую позицию
				_type = self.scaner.scan() #Получить текущую лексему
				if ( _type == SAVE ):
					self.A()
				else:
					self.scaner.set_current_position(c_p) #Вернуть старую позицию
		else:
			self.scaner.set_current_position(c_p) #Вернуть старую позицию

	#Функция
	def F(self):
		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != VOID ):
			self.scaner.printError("ERROR! Expected VOID.")

		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != ID ):
			self.scaner.printError("ERROR! Expected identifier.")

		# Занесение имя функции в таблицу
		v = self.__tree.semInclude(''.join(self.scaner.get_lex()), IDENTITY[VOID])
		if ( type(v) == str ):
			self.scaner.printError(v)

		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != LBRACKET ):
			self.scaner.printError("ERROR! Expected left bracket.")

		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != RBRACKET ):
			self.scaner.printError("ERROR! Expected right bracket.")

		self.Q()

	#Составной оператор
	def Q(self):
		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != LBRACE ):
			self.scaner.printError("ERROR! Expected left brace.")
		self.__tree.nextLavel()
		self.O()
		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != RBRACE ):
			self.scaner.printError("ERROR! Expected right brace.")
		self.__tree.prevLavel()

	#Операторы и описания
	def O(self):
		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(c_p) #Вернуть старую позицию

		while ( _type != RBRACE ):
			if ( _type == INT or _type == INT64 ):
				self.W()
			else:
				self.K()
			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
			self.scaner.set_current_position(c_p) #Вернуть старую позицию

	#Оператор и вызов функции
	def K(self):
		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type == LBRACE ):
			self.scaner.set_current_position(c_p) #Вернуть старую позицию
			self.Q()
		elif ( _type == FOR ):
			self.scaner.set_current_position(c_p) #Вернуть старую позицию
			self.H()
		elif ( _type == SEMICOLON ):
			return #пустой оператор
		elif ( _type == ID ):
			# Поиск имени функции и переменной в таблице
			v1 = self.__tree.semGetType(''.join(self.scaner.get_lex()))
			v = self.__tree.semGetFunct(''.join(self.scaner.get_lex()))
			if ( type(v) == str and type(v1) == str ):
				self.__tree.print()
				_type = self.scaner.scan() #Получить текущую лексему
				if ( _type == LBRACKET ):
					self.scaner.printError(v)
				else:
					self.scaner.printError(v1)


			_type = self.scaner.scan() #Получить текущую лексему
			if ( _type == LBRACKET ):
				_type = self.scaner.scan() #Получить текущую лексему
				if ( _type != RBRACKET ):
					self.scaner.printError("ERROR! Expected right bracket.")
			else:
				self.scaner.set_current_position(c_p) #Вернуть старую позицию
				self.U()
		else:
			self.scaner.set_current_position(c_p) #Вернуть старую позицию
			self.U()

	#FOR
	def H(self):
		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != FOR ):
			self.scaner.printError("ERROR! Expected FOR.")

		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != LBRACKET ):
			self.scaner.printError("ERROR! Expected left bracket.")

		self.U()

		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != SEMICOLON ):
			self.scaner.printError("ERROR! Expected semicolon (;).")

		self.A()

		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != SEMICOLON ):
			self.scaner.printError("ERROR! Expected semicolon (;).")

		self.U()

		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != RBRACKET ):
			self.scaner.printError("ERROR! Expected right bracket.")

		self.K()

	#Присваивание, бинарное присваивание и инкрементирование и декрементирование
	def U(self):
		_type = self.scaner.scan() #Получить текущую лексему

		if ( _type != ID and _type != PLUSPLUS and _type != MINUSMINUS ):
			self.scaner.printError("ERROR! Expected assignment (identifier, ++ or --).")

		if ( _type == ID ):
			# Поиск имени идентификатора в таблице
			v = self.__tree.semGetType(''.join(self.scaner.get_lex()))
			if ( type(v) == str ):
				self.scaner.printError(v)

			_type = self.scaner.scan() #Получить текущую лексему

			if ( _type != SAVE and _type != PLUSEQ and _type != MINUSEQ and _type != MULTEQ 
				and _type != DIVEQ and _type != MODEQ and _type != PLUSPLUS and _type != MINUSMINUS ):
				self.scaner.printError("ERROR! Expected assignment (=, +=, -=, *=. %=, /=, ++ or --).")

			if ( _type == SAVE or _type == PLUSEQ or _type == MINUSEQ or _type == MULTEQ 
				or _type == DIVEQ or _type == MODEQ ):
				self.A()
			elif ( _type == PLUSPLUS or _type == MINUSMINUS ):
				return

		elif ( _type == PLUSPLUS or _type == MINUSMINUS ):
			_type = self.scaner.scan() #Получить текущую лексему
			if ( _type != ID ):
				self.scaner.printError("ERROR! Expected identifier.")
			# Поиск имени идентификатора в таблице
			v = self.__tree.semGetType(''.join(self.scaner.get_lex()))
			if ( type(v) == str ):
				self.scaner.printError(v)

	#Выражение
	def A(self):
		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != PLUS and _type != MINUS ):
			self.scaner.set_current_position(c_p) #Вернуть старую позицию

		self.B()
		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему

		while ( (_type >= LT and _type <= NEQ) or _type == RMOVE or _type == LMOVE ):
			self.B()
			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(c_p) #Вернуть старую позицию

	#Слагаемое
	def B(self):
		self.E()

		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		while ( _type == PLUS or _type == MINUS ):
			self.E()
			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(c_p) #Вернуть старую позицию

	#Множитель
	def E(self):
		self.X()

		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		while ( _type == DIV or _type == MOD or _type == MULT ):
			self.X()
			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(c_p) #Вернуть старую позицию

	#Элементарное выражение
	def X(self):
		_type = self.scaner.scan() #Получить текущую лексему

		if ( _type != ID and _type != LBRACKET and _type != CONSTINT16 and _type != CONSTINT ):
			self.scaner.printError("ERROR! Expected identifier, left bracket or integer constant dec or hex.")

		if ( _type == ID ):
			# Поиск имени идентификатора в таблице
			v = self.__tree.semGetType(''.join(self.scaner.get_lex()))
			if ( type(v) == str ):
				self.scaner.printError(v)

			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
			if ( _type != LSBRACKET ):
				self.scaner.set_current_position(c_p) #Вернуть старую позицию
			else:
				self.A()
				_type = self.scaner.scan() #Получить текущую лексему
				if ( _type != RSBRACKET ):
					self.scaner.printError("ERROR! Expected right square bracket.")

		elif ( _type == LBRACKET ):
			self.A()

			_type = self.scaner.scan() #Получить текущую лексему
			if ( _type != RBRACKET ):
				self.scaner.printError("ERROR! Expected right bracket.")
		elif ( _type == CONSTINT or _type == CONSTINT16 ):
			return

	def printTree(self):
		self.__tree.print()