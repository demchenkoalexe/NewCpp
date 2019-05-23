from defs import *
from diagram import Diagram
from scaner import Scaner

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
			#TODO!!!

		self.position = self.scaner.get_current_position() #Запомнить текущую позицию
		_type = self.scaner.scan() # Квадратные скобки, запятая или сохранить 

		if ( _type == SAVE ):
			self.A()
		elif ( _type == LSBRACKET ):
			self.position = self.scaner.get_current_position() #Запомнить текущую позицию
			_type = self.scaner.scan() #Получить текущую лексему
			if ( _type != RSBRACKET ):
				self.scaner.set_current_position(self.position) #Вернуть старую позицию
				self.A()
				#Проверим закрывается ли скобка
				self.position = self.scaner.get_current_position() #Запомнить текущую позицию
				_type = self.scaner.scan() #Получить текущую лексему
				if ( _type != RSBRACKET ):
					self.scaner.printError("ERROR! Expected right square bracket.")
				self.position = self.scaner.get_current_position() #Запомнить текущую позицию
				_type = self.scaner.scan() #Получить текущую лексему
				if ( _type == SAVE ):
					self.A()
				else:
					self.scaner.set_current_position(self.position) #Вернуть старую позицию
		else:
			self.scaner.set_current_position(self.position) #Вернуть старую позицию
















#Ввод файла в программу
original_file = open('input1.txt')
text_file = original_file.read(MAX_TEXT)
text_file = text_file + '\0' #добавим концевой ноль в конец исходного файла
original_file.close()

i = Interpretator(text_file)
i.run()

