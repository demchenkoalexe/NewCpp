#! /usr/bin/env python
# -*- coding: utf-8 -*-

from defs import *
from scaner import Scaner
from diagram import Diagram
from tree_2 import *

def main():
	_type = '' #Тип лексемы

	#Ввод файла в программу
	original_file = open('input.txt')
	text_file = original_file.read(MAX_TEXT)
	text_file = text_file + '\0' #добавим концевой ноль в конец исходного файла
	print(text_file)
	original_file.close()

	# Синтаксический анализатор
	dg = Diagram(text_file)
	dg.S()

	scaner = Scaner(text_file) #Инициализация сканера
	print ("\nScaner: ")
	#Вывод всех лексем (реализация сканера)
	while _type != END:
		_type = scaner.scan()
		print(_type, '-->', ''.join(scaner.get_lex()))

	print('\nTree: ')
	dg.printTree()

if __name__ == "__main__":
	main()