todo
====

A Simple Python Todo List. Here are the commands
* complete (c) - Finish an item on your todo list
* add (a) - Add an item to the bottom of your todo list
* move (m) - Move an item on your todo list
* list (l) - List all of the things on your todo list

A tiny project for myself, used to try out TDD. Definitely a learning experience!

If you want to use this on your machine, my suggestion to you is to put it in /usr/local/bin, 
and make sure that its in your path. I would modify the FileTodoList instance at the bottom to
point to some local file. In fact, a potential useful fork is to make the program work for all
users and allow each of them to have their own todo list. This can be acheived by choosing the
path for the FileTodoList to be based on the user's home directory (maybe /home/username/.todoList).
