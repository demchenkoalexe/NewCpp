from defs import *
import sys

class Scaner():
	def __init__(self, t):
		self.current_position = 0 #Указатель текущей позиции в исходном тексте
		self._lex = [] #Локальные переменные типа и изображения лексем

		self.Keyword = ('int', '_int64', 'for', 'void')
		self.IndexKeyword = (INT, INT64, FOR, VOID)

		self.text_file = t

	def printError(self, text):
		line = 1
		symbol = 1
		for i in range(self.current_position):
			if ( self.text_file[i] == '\n' ):
				line += 1
				symbol = 1
			else:
				symbol += 1
		print('String: ' + str(line) + '; Symbol: ' + str(symbol) + '\n' )
		sys.exit(text)

	def endScaning(self):
		print('End of scaning! Thanks!') #Конец сканирования

	def get_lex(self):
		return self._lex

	def get_current_position(self):
		return self.current_position
	def set_current_position(self, c_p):
		self.current_position = c_p

	#Сканер
	def scan(self):
		_type = 0 #Тип лексемы

		self._lex = [] #Очищаем лексему

		#Флаг пропуска ненужных символов
		f = True

		while (f):
			f = False

			#Пропуск пробелов, табуляций и переносов строки
			while (self.text_file[self.current_position] == ' ' or self.text_file[self.current_position] == '\t' or self.text_file[self.current_position] == '\n'):
				self.current_position += 1

			"""
				Многострочные комментарии - их пропускаем. 
				Если комментарий начался, но не закончился весь код считаем ошибкой.
			"""
			if (self.text_file[self.current_position] == '/' and self.text_file[self.current_position + 1] == '*'):
				self.current_position += 2
				_type = ERROR #Если комментарий так и не закончится, вернём ошибку лексемы
				while (not (self.text_file[self.current_position] == '*' and self.text_file[self.current_position + 1] == '/')):
					self.current_position += 1
					if self.text_file[self.current_position + 1] == '\0':
						self.printError('ERROR! Endless comment!')
						self.current_position += 1
						return _type
				self.current_position += 2
				_type = 0
				f = True
				continue

			#Пропуск однострочного комментария
			if (self.text_file[self.current_position] == '/' and self.text_file[self.current_position + 1] == '/'):
				self.current_position += 2
				while self.text_file[self.current_position] != '\n':
					self.current_position += 1
				f = True
				continue
				
		#Конец файла. Конец сканирования.
		if self.text_file[self.current_position] == '\0':
			_lex = self.text_file[self.current_position]
			return END
		#16-ричные числа
		elif ( self.text_file[self.current_position] == '0' and ( self.text_file[self.current_position + 1] == 'x' or self.text_file[self.current_position + 1] == 'X' ) ):
			self._lex.append(self.text_file[self.current_position])
			self._lex.append(self.text_file[self.current_position + 1])
			self.current_position += 2
			while ( ( self.text_file[self.current_position] <= '9' and self.text_file[self.current_position] >= '0' ) 
				or ( self.text_file[self.current_position] <= 'F' and self.text_file[self.current_position] >= 'A' ) 
				or ( self.text_file[self.current_position] <= 'f' and self.text_file[self.current_position] >= 'a' ) ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
			return CONSTINT16
		#10-ричные числа
		elif ( ( self.text_file[self.current_position] <= '9' and self.text_file[self.current_position] >= '0' ) ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			while ( ( self.text_file[self.current_position] <= '9' and self.text_file[self.current_position] >= '0' ) ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
			return CONSTINT
		#Идентификатор
		elif ( ( self.text_file[self.current_position] >= 'a' and self.text_file[self.current_position] <= 'z' ) 
			or ( self.text_file[self.current_position] >= 'A' and self.text_file[self.current_position] <= 'Z' ) 
			or self.text_file[self.current_position] == '_' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			while ( ( self.text_file[self.current_position] <= '9' and self.text_file[self.current_position] >= '0' ) 
				or ( self.text_file[self.current_position] >= 'a' and self.text_file[self.current_position] <= 'z' ) 
				or ( self.text_file[self.current_position] >= 'A' and self.text_file[self.current_position] <= 'Z' ) 
				or self.text_file[self.current_position] == '_' ):
				#Исключаем длинный идентификатор
				if len(self._lex) < MAX_LEX - 1:
					self._lex.append(self.text_file[self.current_position])
					self.current_position += 1
				else:
					self.current_position += 1

			#Проверка на ключевое слово
			for i in range(len(self.Keyword)):
				if ''.join(self._lex) == self.Keyword[i]:
					return self.IndexKeyword[i]
			return ID
		#Запятая
		elif ( self.text_file[self.current_position] == ',' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return COMMA
		#Точка с запятой
		elif ( self.text_file[self.current_position] == ';' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return SEMICOLON
		#Левая круглая скобка
		elif ( self.text_file[self.current_position] == '(' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return LBRACKET
		#Правая круглая скобка
		elif ( self.text_file[self.current_position] == ')' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return RBRACKET
		#Левая фигурная скобка
		elif ( self.text_file[self.current_position] == '{' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return LBRACE
		#Правая фигурная скобка
		elif ( self.text_file[self.current_position] == '}' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return RBRACE
		#Левая квадратная скобка
		elif ( self.text_file[self.current_position] == '[' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return LSBRACKET
		#Правая квадратная скобка
		elif ( self.text_file[self.current_position] == ']' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return RSBRACKET
		#Больше
		elif ( self.text_file[self.current_position] == '>' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			#Больше или равно
			if ( self.text_file[self.current_position] == '=' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return GE
			#Сдвиг вправо
			elif ( self.text_file[self.current_position] == '>' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return RMOVE
			return GT
		#Меньше
		elif ( self.text_file[self.current_position] == '<' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			#Меньше или равно
			if ( self.text_file[self.current_position] == '=' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return LE
			#Сдвиг влево
			elif ( self.text_file[self.current_position] == '<' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return LMOVE
			return LT
		#Присваивание
		elif ( self.text_file[self.current_position] == '=' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			#Равно
			if ( self.text_file[self.current_position] == '=' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return EQ
			return SAVE
		#Не равно
		elif ( self.text_file[self.current_position] == '!' and self.text_file[self.current_position + 1] == '=' ):
			self._lex.append(self.text_file[self.current_position])
			self._lex.append(self.text_file[self.current_position + 1])
			self.current_position += 2
			return NEQ
		#Плюс
		elif ( self.text_file[self.current_position] == '+' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			#Плюс-равно
			if ( self.text_file[self.current_position] == '=' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return PLUSEQ
			#Плюс-плюс
			elif ( self.text_file[self.current_position] == '+' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return PLUSPLUS
			return PLUS
		#Минус
		elif ( self.text_file[self.current_position] == '-' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			#Минус-равно
			if ( self.text_file[self.current_position] == '=' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return MINUSEQ
			#Минус-минус
			elif ( self.text_file[self.current_position] == '-' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return MINUSMINUS
			return MINUS
		#Деление
		elif ( self.text_file[self.current_position] == '/' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			#Деление-равно
			if ( self.text_file[self.current_position] == '=' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return DIVEQ
			return DIV
		#Остаток от деления
		elif ( self.text_file[self.current_position] == '%' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			#Остаток от деления-равно
			if ( self.text_file[self.current_position] == '=' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return MODEQ
			return MOD
		#Умножение от деления
		elif ( self.text_file[self.current_position] == '*' ):
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			#Умножение-равно
			if ( self.text_file[self.current_position] == '=' ):
				self._lex.append(self.text_file[self.current_position])
				self.current_position += 1
				return MULTEQ
			return MULT
		else:
			self.printError('ErorrLex!')
			self._lex.append(self.text_file[self.current_position])
			self.current_position += 1
			return ERROR