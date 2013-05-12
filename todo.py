#!/usr/bin/python
import sys
import os

class TodoCommandParser(object):
	def __init__(self, commandLineArgs):
		# split the arguments by space and skip the first (command name)
		A = commandLineArgs.split()
		A = A[1:]
		self.command = ''
		self.arg1 = ''
		self.arg2 = ''
		if len(A) < 1:
			return
		A[0] = A[0].lower()
		if self.__matchSingleArgCommand(A[0]):
			self.arg1 = ' '.join(A[1:])
		elif 'move'.startswith(A[0]):
			self.command = 'move'
			self.arg1 = int(A[1])
			self.arg2 = ' '.join(A[2:])
		else:
			raise Exception('Not an acceptable command: {0:s}'.format(A[0]))
	def __matchSingleArgCommand(self, s):
		matchedSingleArg = False
		for command in ['add', 'complete', 'list']:
			if command.startswith(s):
				self.command = command
				matchedSingleArg = True
				break
		return matchedSingleArg

class TodoList(object):
	def __init__(self):
		self.__todoList = []
		self.read()
	
	def read(self):
		pass
	
	def write(self):
		pass

	def add(self, arg1='', arg2=''):
		self.__todoList.append(arg1)

	def get(self, k):
		return self.__todoList[k]

	def find(self, s):
		s = s.lower()
		lowerTodo = map(lambda x : x.lower(), self.__todoList)
		for k, item in enumerate(lowerTodo):
			if s in item:
				return k
		return -1

	def complete(self, arg1='', arg2=''):
		k = -1
		if type(arg1) == int:
			k = int(arg1)
		else:
			k = self.find(arg1)
		self.__todoList.pop(k)

	def list_all(self, arg1='', arg2=''):
		return '\n'.join(self.__todoList)

	def move(self, arg1='', arg2=''):
		k = -1
		if type(arg2) == int:
			k = int(arg2)
		else:
			k = self.find(arg2)
		s = self.__todoList.pop(k)
		self.__todoList.insert(arg1, s)

class FileTodoList(TodoList):
	def __init__(self, path='.todo'):
		self.path = path 
		super(FileTodoList, self).__init__()
	
	def read(self):
		# create the file if it doesn't exist
		if not os.path.isfile(self.path):
			self.write()
		with open(self.path, 'r') as f:
			for item in f.read().split('\n'):
				if len(item.strip()) > 0:
					self.add(item)
	
	def write(self):
		with open(self.path, 'w') as f:
			f.write(self.list_all())

class TodoRouter(object):
	def __init__(self, todoList):
		self.todo = todoList
	def route(self, cmd):
		routes = {
			'add': self.todo.add,
			'complete': self.todo.complete,
			'list': self.todo.list_all,
			'move': self.todo.move,
		}
		if cmd not in routes:
			return None
		return routes[cmd]

	def process(self, commandLineInput):
		parser = TodoCommandParser(commandLineInput)
		f = self.route(parser.command)
		if f is None:
			return
		return f(parser.arg1, parser.arg2)

if __name__ == '__main__':
	CommandString = ' '.join(sys.argv)
	FileTodo = FileTodoList(path='TODO')
	Router = TodoRouter(FileTodo)
	result = Router.process(CommandString)
	if result != None:
		print result
	FileTodo.write()
