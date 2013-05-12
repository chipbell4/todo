#!/usr/bin/python
import unittest
import os
from todo import TodoCommandParser, TodoList, FileTodoList, TodoRouter

class TodoCommandParserTester(unittest.TestCase):
	def __genericTest(self, commandLineArgs, expectedCommandName, expectedArg1, expectedArg2):
		cmdParser = TodoCommandParser(commandLineArgs)
		self.assertEqual(cmdParser.command, expectedCommandName)
		self.assertEqual(cmdParser.arg1, expectedArg1)
		self.assertEqual(cmdParser.arg2, expectedArg2)

	def __allCasesTest(self, verb, arg1, arg2):
		shortVerb = verb[0]
		bigVerb = verb.upper()
		testCases = [verb, shortVerb, bigVerb]
		for v in testCases:
			commandLineInput = 'todo {0:s} {1:s} {2:s}'.format(str(v), str(arg1), str(arg2))
			self.__genericTest(commandLineInput, verb, arg1, arg2)

	def test_add(self):
		self.__allCasesTest('add', 'A B C', '')

	def test_complete(self):
		self.__allCasesTest('complete', 'A B C', '')

	def test_list(self):
		self.__allCasesTest('list', '', '')

	def test_move(self):
		self.__allCasesTest('move', 1, 'A B C')

	def test_int_only_move(self):
		commandArgs = 'todo move neener A B C'
		with self.assertRaises(Exception):
			TodoCommandParser(commandArgs)

	def test_invalidCommand(self):
		commandArgs = 'todo notACommand A B C'
		with self.assertRaises(Exception):
			TodoCommandParser(commandArgs)

	def test_emptyCommand(self):
		commandArgs = 'todo'
		p = TodoCommandParser(commandArgs)
		self.assertEqual(p.command, '')
		self.assertEqual(p.arg1, '')
		self.assertEqual(p.arg2, '')

class TodoListTester(unittest.TestCase):
	def setUp(self):
		self.todo = TodoList()
	
	def tearDown(self):
		del self.todo

	def test_add(self):
		item = 'Hello World'
		self.todo.add(item)
		self.assertEqual(self.todo.get(0), item)

	def test_find(self):
		item1 = 'ABCD'
		item2 = 'WXYZ'
		self.assertEqual(self.todo.find(item1), -1)
		for i in xrange(10):
			self.todo.add(item1)
		self.todo.add(item2)
		for i in xrange(10):
			self.todo.add(item1)
		self.assertEqual(self.todo.find(item2), 10)
		self.assertEqual(self.todo.find(item2[:2]), 10)
		self.assertEqual(self.todo.find(item2[1:3]), 10)
		self.assertEqual(self.todo.find(item2[2:]), 10)
		self.assertEqual(self.todo.find(item2.lower()), 10)

	def test_get_by_id(self):
		item = 'abcdefg'
		self.todo.add(item)
		self.assertEqual(self.todo.get(0), item)

	def test_complete_by_string(self):
		item = 'Hello World'
		self.todo.add(item)
		self.todo.complete(item)
		self.assertEqual(self.todo.find(item), -1)

	def test_complete_by_id(self):
		item = 'Hello World'
		self.todo.add(item)
		self.todo.complete(0)
		self.assertEqual(self.todo.find(item), -1)

	def test_list(self):
		self.assertEqual(self.todo.list_all(), '')
		item = 'Hello World'
		self.todo.add(item)
		self.assertEqual(self.todo.list_all(), item)
		self.todo.add(item)
		self.assertEqual(self.todo.list_all(), '{0:s}\n{0:s}'.format(item))
	
	def test_move_by_string(self):
		for s in ['a', 'b', 'c']:
			self.todo.add(s)
		self.todo.move(0, 'c')
		self.assertEqual(self.todo.find('c'), 0)

	def test_move_by_id(self):
		for s in ['a', 'b', 'c']:
			self.todo.add(s)
		self.todo.move(0, 2)
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
		self.todo.complete('B')
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
		item = 'Hello'
		self.todo.add(item)
		self.todo.write()
		self.todo.read()
		self.assertEqual(self.todo.get(0), item)
		pass

	def tearDown(self):
		self.__safeFileDelete(self.path)
	
class TodoRouterTester(unittest.TestCase):
	def setUp(self):
		self.todo = TodoList()
		self.router = TodoRouter(self.todo)
		self.dummyItem = 'DO DAT THING'
		self.dummyItem2 = 'ANOTHER THING'

	def test_find_valid_route(self):
		cmds = ['add', 'complete', 'list', 'move']
		funcs = [self.todo.add, self.todo.complete, self.todo.list_all, self.todo.move]
		for cmd, func in zip(cmds, funcs):
			self.assertEqual(self.router.route(cmd), func)
	def test_invalid_route(self):
		cmd = 'blah'
		self.assertEqual(self.router.route(cmd), None)
		pass

if __name__ == '__main__':
	unittest.main()
