from defs import *
import copy

MAXK = 100 #Максимальное число вершин дерева
EMPTY = -1 #Признак пустой ссылки

class Node:
	def __init__(self):
		self.type_id = '' #идентификатор переменной
		self.DataType = EMPTY #тип значения
		self.data = None #значение
		self.__lavel = 0 # для печати дерева 

class Tree:
	def __init__(self):
		self.n = [] # данные таблицы
		self.up = [] #родитель,
		self.left = [] #левый и
		self.right = [] #правый потомок

		self.__root = 0 #корень дерева
		self.__next = 0 #следующий заполняемый элемент в массиве
		self.__parent = 0 # следующий родитель
		self.__lavel = 0 # уровень для печати дерева

		self.up.append(EMPTY)
		self.left.append(EMPTY)
		self.right.append(EMPTY)

		first = Node()
		first.type_id = "-"
		first.DataType = EMPTY
		first.__lavel = 1
		self.n.append(first)
		self.__next += 1
		self.__lavel += 1

	# Создать левого потомка от вершины From
	def setLeft(self, From, Data):
		# Установили связь в новой вершине
		self.up.append(From)
		self.left.append(EMPTY)
		self.right.append(EMPTY) 
		# Записали информацию в новую вершину
		self.n.append(copy.copy(Data))

		# Связали From с новой вершиной
		if ( From != EMPTY ):
			self.left[From] = self.__next

		self.__next += 1
		self.__parent += 1

	# Создать левого потомка от вершины From
	def setRight(self, From, Data):
		# Установили связь в новой вершине
		self.up.append(From)
		self.left.append(EMPTY)
		self.right.append(EMPTY) 
		# Записали информацию в новую вершину
		self.n.append(copy.copy(Data))

		# Связали From с новой вершиной
		if ( From != EMPTY ):
			self.right[From] = self.__next

		self.__next += 1
		self.__parent += 1

	# Поиск данных в дереве до его корня вверх по связям
	def findUp(self, From, type_id):
		# Текущая вершина поиска
		i = From
		while ( ( i != EMPTY ) and ( type_id != self.n[i].type_id ) ):
			i = self.up[i] # поднимаемся наверх по связям

		if ( i == EMPTY ):
			return EMPTY
		else:
			return i

	# Получить значение текущего узла дерева
	def getCurrent(self):
		return self.n[__next - 1].type_id

	#Получить тип элемента a под номером num дерева
	def getTreeLeaf(self, a, num):
		return self.n[num].DataType

	# Проверка идентификатора a на повторное описание внутри блока. 
	# поиск вверх от ткущей вершины addr
	def dupControl(self, addr, a):
		if ( self.findUp(addr, a) == EMPTY ):
			return False
		return True

	# Занесение идентификатора a в таблицу с типом t
	def semInclude(self, a, t):
		if ( self.dupControl(self.__next - 1, a) ):
			return "Повторное описание идентификатора " + str(a)
		newID = Node()
		if ( t != IDENTITY[VOID] ):
			newID.type_id = a
			newID.DataType = t
			newID.__lavel = self.__lavel
			self.setLeft(self.__parent, newID)   # создали вершину - переменную
			return self.__next - 1
		else:
			newID.type_id = a
			newID.DataType = t
			newID.__lavel = self.__lavel
			self.setLeft(self.__parent, newID) # создали вершину - функцию
			return self.__next - 1

	# инициализация следующего уровня дерева
	def nextLavel(self):
		newID2 = Node()
		newID2.type_id = "-"
		newID2.DataType = EMPTY
		self.setRight(self.__parent, newID2) # создали пустую вершину
		self.__lavel += 1

	# вернуться на предыдущий уровень дерева
	def prevLavel(self):
		i = self.__parent
		while ( self.n[i].DataType != EMPTY ):
			i = self.up[i] # поднимаемся наверх по связям
		self.__parent = i - 1
		self.__lavel -= 1

	#Установить тип t для переменной по адресу addr
	def semSetType(self, addr, t):
		self.n[addr].type_id = t

	# Найти в таблице переменную с именем a
	# и вернуть ссылку на соответсвующий элемент дерева
	def semGetType(self, a):
		v = self.findUp(self.__next - 1, a)
		if ( v == EMPTY ):
			return "Отсутсвует описание идентификатора " + str(a)
		if ( self.n[v].DataType == IDENTITY[VOID] ):
			return "Неверное использование вызова функции " + str(a)
		return v

	# Найти в таблице функцию с именем a
	# и вернуть ссылку на соответсвующий элемент дерева
	def semGetFunct(self, a):
		v = self.findUp(self.__next - 1, a)
		if ( v == EMPTY ):
			return "Отсутсвует описание функции " + str(a)
		if ( self.n[v].DataType != IDENTITY[VOID] ):
			return "Не является функцией идентификатор " + str(a)
		return v

	def printTree(self):
		for i in self.n:
			if i.type_id == "-":
				continue
			for j in range(i.__lavel * 2):
				print(" ", end="")
			print(str(i.type_id) + ' (' + str(i.DataType) + ')')

