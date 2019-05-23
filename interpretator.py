from defs import *
from diagram import Diagram
from scaner import Scaner
import numpy

class Interpretator():
	def __init__(self, text_file):
		self.dg = Diagram(text_file) # Инициализация синаксичского анализатора
		self.scaner = Scaner(text_file) #Инициализация сканера
		self.__tree = None # дерево идентификаторов
		self.interpret = False # флаг интепретации
		self.position = 0

	def run(self):
		# Анализируем синтаксис
		self.dg.S()
		self.__tree = self.dg.getTree()

		# Начинаем интепретацию
		self.interpret = True
		self.globalValue() # глобальные переменные

	def globalValue(self):
		_type = '' #Тип лексемы

		self.position = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(self.position) #Вернуть старую позицию

		while ( _type == INT or _type == INT64 or _type == VOID ):
			if ( _type != VOID ):
				self.W()
			self.position = self.scaner.get_current_position()
			_type = self.scaner.scan()
			self.scaner.set_current_position(self.position)

	#Список данных
	def W(self):
		_type = self.scaner.scan() #Получить текущую лексему

		self.Z()

		self.position = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему

		while ( _type == COMMA ):
			self.Z()
			self.position = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему

		self.scaner.set_current_position(self.position) #Вернуть старую позицию

		_type = self.scaner.scan() #Получить текущую лексему

		if ( _type == SEMICOLON ):
			return

	#Переменная, массив и индекс
	def Z(self):
		self.position = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() # Считываем идентификатор
		_type = self.scaner.scan() # Квадратные скобки, запятая или сохранить 
		self.scaner.set_current_position(self.position) #Вернуть старую позицию

		if ( _type == LSBRACKET ):
			pass
		else:
			_type = self.scaner.scan() #Получить текущую лексему			
			currentID = self.__tree.semGetType(''.join(self.scaner.get_lex()))

		self.position = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() # Квадратные скобки, запятая или сохранить 

		if ( _type == SAVE ):
			value = self.expression()

			self.__tree.semSetData(currentID, value)
		elif ( _type == LSBRACKET ):
			pass
		else:
			self.scaner.set_current_position(self.position) #Вернуть старую позицию

	#Выражение
	def expression(self):
		self.position = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		if ( _type != PLUS and _type != MINUS ):
			self.scaner.set_current_position(self.position) #Вернуть старую позицию
		if ( _type == PLUSPLUS or _type == MINUSMINUS ):
			self.position = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему

		self.addend()
		self.position = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему

		if ( _type == PLUSPLUS or _type == MINUSMINUS ):
			return

		while ( (_type >= LT and _type <= NEQ) or _type == RMOVE or _type == LMOVE ):
			self.addend()
			self.position = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(self.position) #Вернуть старую позицию

	#Слагаемое
	def addend(self):
		self.multiplier()

		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		while ( _type == PLUS or _type == MINUS ):
			self.multiplier()
			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(c_p) #Вернуть старую позицию

	#Множитель
	def multiplier(self):
		value, typeValue = self.elementaryExpression()

		c_p = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() #Получить текущую лексему
		while ( _type == DIV or _type == MOD or _type == MULT ):
			value = self.elementaryExpression()
			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
		self.scaner.set_current_position(c_p) #Вернуть старую позицию

	#Элементарное выражение
	def elementaryExpression(self):
		_type = self.scaner.scan() #Получить текущую лексему

		if ( _type == ID ):
			# Поиск имени идентификатора в таблице
			v = self.__tree.semGetType(''.join(self.scaner.get_lex()))
			value = self.__tree.getData(v)		
			typeValue  = self.__tree.getType(v)	

			c_p = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Проверить: не массив ли?
			if ( _type != LSBRACKET ):
				self.scaner.set_current_position(c_p) #Вернуть старую позицию
				return value, typeValue
			else:
				pass

		elif ( _type == LBRACKET ):
			self.expression()
			_type = self.scaner.scan() #Получить закрывающуюся скобку

		elif ( _type == CONSTINT or _type == CONSTINT16 ):
			v = ''.join(self.scaner.get_lex())
			if( len(v) > 11 ):
				self.scaner.printError("int is greater than the range of values")
			value = int(v)
			if ( value > 2147483647 or value < -2147483648 ):
				self.scaner.printError("int is greater than the range of values")
			return value, INT







#Ввод файла в программу
original_file = open('input1.txt')
text_file = original_file.read(MAX_TEXT)
text_file = text_file + '\0' #добавим концевой ноль в конец исходного файла
original_file.close()

i = Interpretator(text_file)
i.run()

