#!/usr/bin/python
import unittest
import os
from todo import TodoList, FileTodoList

class ArgumentHolder(object):
	'''A class that maps named arguments into attributes on
	the class. Useful in tests that require "argument" objects
	'''
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

class TodoListTester(unittest.TestCase):
	def setUp(self):
		self.todo = TodoList()
	
	def tearDown(self):
		del self.todo

	def test_add(self):
		args = ArgumentHolder(todo='Hello World')
		self.todo.add(args)
		self.assertEqual(self.todo.get(0), 'Hello World')

	def test_find_uses_digits(self):
		args = ArgumentHolder(todo='Hello World')
		self.todo.add(args)
		self.todo.add(args)
		self.assertEqual(self.todo.find('1'), 1)
	
	def test_find_by_digits_clamps(self):
		self.assertEqual(self.todo.find('2'), -1)

	def test_find_uses_string(self):
		args = ArgumentHolder(todo='Abc')
		self.todo.add(args)
		self.assertEqual(self.todo.find('Abc'), 0)

	def test_fuzzy_find(self):
		args = ArgumentHolder(todo='A Very Long String')
		self.todo.add(args)
		self.assertEqual(self.todo.find('very'), 0)

	def test_list(self):
		args = ArgumentHolder()
		self.assertEqual(self.todo.list_all(args), '')
		args = ArgumentHolder(todo='Hello World')
		self.todo.add(args)
		self.assertEqual(self.todo.list_all(args), 'Hello World')
		self.todo.add(args)
		self.assertEqual(self.todo.list_all(args), '{0:s}\n{0:s}'.format('Hello World'))
	
	def test_move_by_string(self):
		for s in ['a', 'b', 'c']:
			args = ArgumentHolder(todo=s)
			self.todo.add(args)

		args = ArgumentHolder(todo='c', new_location=0)
		self.todo.move(args)
		self.assertEqual(self.todo.find('c'), 0)

	def test_move_by_id(self):
		for s in ['a', 'b', 'c']:
			args = ArgumentHolder(todo=s)
			self.todo.add(args)

		args = ArgumentHolder(todo='2', new_location=0)
		self.todo.move(args)
		self.assertEqual(self.todo.find('c'), 0)

class FileTodoListTester(unittest.TestCase):
	def __safeFileDelete(self,path):
		if os.path.isfile(path):
			os.remove(path)

	def setUp(self):
		self.path = '.TODO_TEST_FILE'
		f = open(self.path, 'w')
		f.write('A\nB\nC')
		f.close()
		self.todo = FileTodoList(path = self.path)

	def test_read(self):
		self.assertEqual(self.todo.find('A'), 0)
		self.assertEqual(self.todo.find('B'), 1)
		self.assertEqual(self.todo.find('C'), 2)

	def test_write(self):
		self.todo.complete(ArgumentHolder(todo='B'))
		self.todo.write()
		s = open(self.path, 'r').read()
		self.assertEqual(s, 'A\nC')

	def test_empty_file(self):
		self.__safeFileDelete(self.path)
		self.todo = FileTodoList(path = self.path)
		self.assertEqual(self.todo.find('A'), -1)

	# blank lines cause extra items to mysteriously appear
	# in the todo list
	def test_blank_lines_filter(self):
		self.__safeFileDelete(self.path)
		self.todo = FileTodoList(path = self.path)
		args = ArgumentHolder(todo='Hello')
		self.todo.add(args)
		self.todo.write()
		self.todo.read()
		self.assertEqual(self.todo.get(0), 'Hello')
		pass

	def tearDown(self):
		self.__safeFileDelete(self.path)
	
if __name__ == '__main__':
	unittest.main()
