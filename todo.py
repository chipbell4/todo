#!/usr/bin/python
import sys
import os
import argparse

class TodoList(object):
	def __init__(self):
		self.__todoList = []
		self.read()

	def add(self, args):
		'''Appends a new todo onto the internal todo list. Expects an object with
		a todo key on it
		'''
		self._pushTodoRaw(args.todo)
		return "Added new todo \"{0}\" at {1}".format(args.todo, len(self.__todoList)-1)

	def find(self, todo):
		'''Attempts to find a todo using text or index, depending on the input.
		If the the input is numeric it will search by index. Otherwise, it will
		search by text
		'''
		todo = str(todo)
		if todo.isdigit():
			return self._findByIndex(todo)
		else:
			return self._findByText(todo)

	def complete(self, args):
		'''Removes an item from the todo list. Expects an object
		with a todo field on it. Attempts to remove the item,
		whether it is an integer or a string
		'''
		index = self.find(args.todo)
		todo = self.__todoList.pop(index)
		return "Marked #{0}: \"{1}\" as completed".format(index, todo)
		
	def _findByIndex(self, index):
		'''Essentially returns the index passed, as an integer. However,
		if the index is out of bounds for the todo list, it will return -1
		'''
		index = int(index)
		if index >= len(self.__todoList):
			return -1
		else:
			return index

	def _findByText(self, text):
		'''Returns the index of a particular todo item, returning -1
		if the todo cannot be found
		'''
		text = text.lower()
		lowerTodo = map(lambda todo : todo.lower(), self.__todoList)
		for index, todo in enumerate(lowerTodo):
			if text in todo:
				return index
		return -1

	def get(self, k):
		'''Gets the todo item at a particular index of the list
		'''
		return self.__todoList[k]

	def list_all(self, args):
		'''Lists all items in the todo list
		'''
		return '\n'.join(self.__todoList)

	def move(self, args):
		'''Moves an item designated by args.todo to the index
		given by args.new_location
		'''
		old_location = self.find(args.todo)
		new_location = int(args.new_location)
		todo = self.__todoList.pop(old_location)
		self.__todoList.insert(new_location, todo)
		return "Todo \"{0}\" has been moved from {1} to {2}".format(todo, old_location, new_location)
	
	def _pushTodoRaw(self, todo):
		''' an inheritable function to allow subclasses to push onto
		the internal todo list with a raw string
		'''
		self.__todoList.append(todo)
	
	def read(self):
		'''A No-op function for reading a todo list from some storage medium
		This method is intended to be overridden by a child class
		'''
		pass
	
	def write(self):
		'''A No-op function for writing a todo list back to some storage medium
		This method is intended to be overridden by a child class
		'''
		pass

class FileTodoList(TodoList):
	def __init__(self, path='.todo'):
		self.path = path 
		self.parent = super(FileTodoList, self)
		self.parent.__init__()
	
	def read(self):
		'''Reads the todo list from a file
		'''
		# create the file if it doesn't exist
		if not os.path.isfile(self.path):
			self.write()
		with open(self.path, 'r') as f:
			for item in f.read().split('\n'):
				if len(item.strip()) > 0:
					super(FileTodoList, self)._pushTodoRaw(item)
	
	def write(self):
		'''Writes the todo list to a file
		'''
		with open(self.path, 'w') as f:
			f.write(self.list_all(None))

# a class to build the command line parser for the todo list
class ArgumentParserFactory:
	@staticmethod
	def make():
		'''Creates a new argument parser for the todo list, handling all of the sub-commands
		'''
		parser = argparse.ArgumentParser(description='A Command-line based todo manager')
		subparser = parser.add_subparsers(dest='todo_command')
		ArgumentParserFactory.createAddCommand(subparser)
		ArgumentParserFactory.createCompleteCommand(subparser)
		ArgumentParserFactory.createListCommand(subparser)
		ArgumentParserFactory.createMoveCommand(subparser)
		return parser

	# builders for the command
	@staticmethod
	def createAddCommand(parser):
		'''Sets up the add command
		'''
		add_parser = parser.add_parser('add', help='Add a new todo item')
		add_parser.add_argument('todo', type=str, help='The todo to add')

	@staticmethod
	def createCompleteCommand(parser):
		'''Sets up the complete command
		'''
		complete_parser = parser.add_parser('complete', help='Mark a todo as complete')
		complete_parser.add_argument('todo', help='The todo to complete (text or index)')

	@staticmethod
	def createListCommand(parser):
		'''Sets up the list command
		'''
		list_parser = parser.add_parser('list', help='Lists every todo')
	
	@staticmethod
	def createMoveCommand(parser):
		'''Sets up the move command
		'''
		move_parser = parser.add_parser('move', help='Moves <todo> (an index or text) to the index provided by <new_location>')
		move_parser.add_argument('todo', help='The todo to move')
		move_parser.add_argument('new_location', help='The new location to move it to')

if __name__ == '__main__':
	parser = ArgumentParserFactory.make()
	args = parser.parse_args()

	# A "mapper" between the todo command name and the function on the todo class
	# Note that list is the only odd case, since list is a built in function in Python
	routes = {
		'add': 'add',
		'list': 'list_all',
		'complete': 'complete',
		'move' : 'move'
			}

	# map the command to a function name
	function_name = routes[ args.todo_command ]

	todo_list = FileTodoList(path='my_todos')

	# get the function corresponding to the command passed
	todo_function = getattr(todo_list, function_name)

	# execute and print the result, if any
	result = todo_function(args)
	if result != None:
		print result

	# save any changes to the todo list
	todo_list.write()
