#! /usr/bin/env python3
''' 
('RU') Данный модуль заменяет стандартные типы данных последовательностей (списки, кортежи, строки) аналогичными типами данных,
в которых индексация идет не с нуля а с единицы. Пример: a = humlist(1,2,3); print(a[2]) выведет 2.

Содержит типы данных: 
	humlist (аналог списков), humtuple (аналог кортежей), humstr (аналог строк)
Содержит функции:
	humrange (аналог range)

Подключение модуля: 
1) Добавим в sys.path расположение каталога (папки) с данным модулем. 
	Пример 1 (простой):
		import sys
		sys.path.append('/home/user/modules')
	Пример 2 (с относительными путями): 
		import os, sys, inspect
		# realpath() will make your script run, even if you symlink it :)
		cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
		if cmd_folder not in sys.path:
		sys.path.insert(0, cmd_folder)
	Пример 3 (с относительными путями):
		# use this if you want to include modules from a subfolder
		cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
		if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
  Можно не добавлять если данный модуль находится в домашнем каталоге (папке). В некоторых ОС домашний каталог это тот, в котором
  расположен файл с выполняемой программой.
2) Импортируем его: from humanity import *
  или: import humanity


('EN') This module replaces the standard sequence data types (lists, tuples, strings) similar types of data,
in which indexation is not from zero but from one. Example: a = humlist(1,2,3); print(a[2]) will print 2.

Contains data types: 
	humlist (similar to lists), humtuple (similar to tuples), humstr (analogue lines)
Contains functions:
	humrange (analogue range)

Importing module: 
1) Add to sys.path to a directory (folder) with this module. 
	Example 1 (simple):
		import sys
		sys.path.append('/home/user/modules')
	Example 2 (with relative paths): 
		import os, sys, inspect
		# realpath() will make your script run, even if you symlink it :)
		cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
		if cmd_folder not in sys.path:
		sys.path.insert(0, cmd_folder)
	Example 3 (with relative paths):
		# use this if you want to include modules from a subfolder
		cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
		if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
		You can not add if the module is in the home directory (folder). In some operating systems the home directory is the one in which
		is a file with the executable program.
2) Import: import from humanity *
or: import humanity

Revision: 6
'''


from decimal import Decimal  # for humdrange







def changeIndexes(keys):
	'''('RU') Функция используется в: __getitem__, __setitem__, __delitem__.
	Она смещает в последовательностях номер первого элемента с [0] на [1].
	если в функц. передается один аргумент, он int и пишется в keys
	если пытаешься брать срез, keys присваивается объект среза вида: slice(1, None, None)'''
	''' В других методах не используется, так как там нету объектов среза: slice(1, None, None), там можно просто отнять 1 от индекса или добавить
	
	rev. 3
	'''
	if isinstance(keys, slice):
	
		'''if keys.start == 0:  # проверки:
			raise IndexError('There is no element under index 0')'''
		if keys.step == 0:
			raise ValueError('slice step cannot be zero')

		# обычный порядок всегда, кроме когда есть и 1 и 2, 2 больше 1
		if (keys.start and (keys.stop != None)) and (keys.start > keys.stop):  # обратный порядок
		
			if keys.step == None:  # проверки:
				raise IndexError('Step cannot be default (positive) while reverse order.')
			elif keys.step > 0:
				raise IndexError('Step cannot be positive while reverse order.')
				
			if keys.start > 0:
				start = keys.start - 1
				if keys.stop >= 2:
					stop = keys.stop - 2
				elif 0 <= keys.stop  <= 1:
					stop = None
				else:
					stop = keys.stop
				keys = slice(start, stop, keys.step)
			
		else:  # прямой порядок
			if keys.start:
				if keys.start > 0:
					keys = slice(keys.start - 1, keys.stop, keys.step)
		

	elif isinstance(keys, int): #если нет slice(), значит int
	
		if keys > 0:
			keys = keys - 1
		elif keys == 0:  # проверки:
			raise IndexError('There is no element under index 0')
	
	return keys







for name in ('list', 'tuple', 'str'):  # __init__ and __new__ methods
	if name == 'list':
		method = '__init__'
		retn = ''
	else:  # tuple, str
		method = '__new__'
		retn = 'return '
	exec(
	"""def hum{name}{method}(self, *something):
		'''('EN') humlist(1,2) > [1, 2]; humlist([1,2]) > [1, 2]; humlist((1,2), (2,3)) > [(1, 2), (2, 3)] 
		('RU') Подобные есть и в humtuple и в humstr, только называется __new__.
		'''	
		
		classname = 'hum{name}'  # потому что у неизменяемых объектов до создания экземпляра еще нету self.__class__
		length = len(something)
		
		if length > 1:
			if classname == 'humstr':
				result = ''
				for some in something:
					result += str(some)
				{retn}{name}.{method}(self, result)  # retn иногда возвращает, иногда - нет
			else:
				{retn}{name}.{method}(self, something)
		
		elif length == 1:
			if something[0].__class__ == tuple:
				{retn}{name}.{method}(self, something[0])  # tuple
			else:
				if classname == 'humstr':
					{retn}{name}.{method}(self, something[0])  # one element
				else:
					{retn}{name}.{method}(self, something)  # tuple with one element
		
		else:  # length == 0
			{retn}{name}.{method}(self, something)""".format(name=name, method=method, retn=retn))
else:
	del method, retn, name




def sequence__getitem__(self, keys):
	keys = changeIndexes(keys)
	return self.__class__.__base__.__getitem__(self, keys)

def sequence__setitem__(self, keys, value):
	'''('EN') Set self[key] to value. If A = [1,2,3], than A[1] = 5 will change A to: [5,2,3]
	'''
	keys = changeIndexes(keys)
	self.__class__.__base__.__setitem__(self, keys, value) # keys - итерируемый объект: (slice(1,2,1), ) или (1, )

def sequence__delitem__(self, keys):
	'''('EN') Delete self[key]. If A = [1,2,3], than A[1] = 5 will change A so: [5,2,3]''' 
	keys = changeIndexes(keys)
	self.__class__.__base__.__delitem__(self, keys)




def sequence_get(self, keys):
	'''Get method for sequences.
	Returns value of element on position (keys). If such element is absent - returns None.
	Used in: humlist, humtuple, humstr.
	rev. 1
	'''
	try:
		value = self.__getitem__(keys)
	except (IndexError, KeyError):
		value = None
	return value


def sequence_index(self, value, *positions):
	'''Index method for sequences.
	Returns index of element with specified value (optional in positions).
	rev. 1
	'''
	
	length = len(positions)
	
	if length >= 3:
		raise TypeError('index() takes at most 3 arguments ({0} given)'.format(length+1))
	elif length == 2:
		start = positions[0] - 1
		end = positions[1]
		return self.__class__.__base__.index(self, value, start, end) + 1
	elif length == 1:
		start = positions[0] - 1
		return self.__class__.__base__.index(self, value, start) + 1
	else:  # если нет вообще позиций
		return self.__class__.__base__.index(self, value) + 1








class humlist(list):
	'''Class, that is the same to list type, but with normal indexes.
	rev. 2
	'''

	# Технические методы:
	
	__init__ = humlist__init__
	
	__getitem__ = sequence__getitem__
	__setitem__ = sequence__setitem__
	__delitem__ = sequence__delitem__
	
	
	# Нетехнические методы:
	
	index = sequence_index
	get = sequence_get
	
	def insert(self, position, value):
		position = changeIndexes(position)
		list.insert(self, position, value)








class humtuple(tuple):
	'''Class, that is the same to tuple type, but with normal indexes.
	rev. 2
	'''
	
	# Технические методы:
	
	__new__ = humtuple__new__  # у неизменяемых типов только __new__() метод
	
	
	__getitem__ = sequence__getitem__
	__setitem__ = sequence__setitem__
	__delitem__ = sequence__delitem__
	
	
	# Нетехнические методы:
		
	index = sequence_index
	get = sequence_get








class humstr(str):
	'''Class, that is the same to string type, but with normal indexes.
	rev. 2
	'''
	
	# Технические методы:	
	
	__new__ = humstr__new__
	
	__getitem__ = sequence__getitem__
	__setitem__ = sequence__setitem__
	__delitem__ = sequence__delitem__
	
	
	# Нетехнические методы:
	
	index = sequence_index
	get = sequence_get
	
	def find(self, value):
		return str.find(self, value) + 1
	# (rfind и так возвращает правильное значение)
	
	
	def rindex(self, value, *positions):
		length = len(positions)
	
		if length >= 3:
			raise TypeError('index() takes at most 3 arguments ({0} given)'.format(length+1))
		elif length == 2:
			start = positions[0] - 1
			end = positions[1]
			return self.__class__.__base__.rindex(self, value, start, end) + 1
		elif length == 1:
			start = positions[0] - 1
			return self.__class__.__base__.index(self, value, start) + 1
		else:  # если нет вообще позиций
			return self.__class__.__base__.index(self, value) + 1
	
	
	def format(self, *args, **kwargs):
		if args:
			return str.format(self, '', *args, **kwargs)
		else:
			return str.format(self, **kwargs)








class humdict(dict):
	'''Same as dict, but with .get() method.
	'''
	
	get = sequence_get  # it's appropriate








def humrange(*n):
	'''Function, that is the same to range() function, but with normal indexes.
	list(humrange(3)) == [1,2,3]; list(humrange(2, 3)) == [2,3]; list(humrange(10, 8, -1)) == [10, 9, 8]
	rev. 2
	'''
	if len(n) >= 4:  # 4 and more arguments
		return range(*n)  # will raise error
		
	elif len(n) == 3:
	
		if n[0] < n[1]:  # straight order
			if n[2] <= 0:
				raise ValueError("Step can't be lesser or equal to zero while straight order.")
			return range(n[0], n[1] + 1, n[2])  # + и - дают включительность
			
		elif n[0] > n[1]:  # reverse order
			if n[2] >= 0:
				raise ValueError("Step can't be larger or equal to zero while reverse order.")
			return range(n[0], n[1] - 1, n[2])
			
		else:  # equal
			if n[2] <= 0:
				raise ValueError("Step can't be lesser or equal to zero while straight order.")
			return range(n[0], n[1] + 1, n[2])
		
	elif len(n) == 2:  # if [0] will be larger than [1] >> [], because range(4,4) and range(4,3) >> []
		if n[0] > n[1]:
			raise ValueError("Start value can't be larger than second while straight order (default step == 1).")
		return range(n[0], n[1] + 1)
		
	elif len(n) == 1:
		if n[0] <= 0:
			raise ValueError("Range from 1 to {0} with step == 1 doesn't exist (default step == 1).".format(n))
		return range(1, n[0] + 1)  # если один аргумент








"""def humfrange(a, b, step):  # old function-generator
	'''Same as humrange, but including float numbers.
	'''
	if a < b:  # straight order
		if step <= 0:
			raise ValueError("Step can't be lesser or equal to zero while straight order.")
		while a <= b:
			yield a
			a += step
		return
	
	elif a > b:  # reverse order
		if step >= 0:  # can't be
			raise ValueError("Step can't be larger or equal to zero while reverse order.")
		while a >= b:
			yield a
			a += step
		return
	
	else:  # a == b
		if step <= 0:
			raise ValueError("Step can't be lesser or equal to zero while straight order.")
		while True:
			yield a
			break
		return"""








class humdrange():  # not a function because of need .__len__() method
	'''Same as humrange, but including decimal (analog to float) numbers.
	Returns Decimal() numbers.
	rev. 3
	'''
	
	def __init__(self, a, b, step, return_type='dec'):
		'''Return type: 'dec' - decimal, 'float' - float, 'str' - string (float, written as string),
		'int' - int.
		rev. 2
		'''
		self.check_type_errors(a, b, step, return_type)
		
		a, b, step = Decimal(a), Decimal(b), Decimal(step)
		
		self.a, self.b, self.step = a, b, step
		self.current = a
		self.return_type = return_type
		
		self.check_logic_errors()
		
		self.length = self.__len__()
	
	
	def check_type_errors(self, a, b, step, return_type):
		'''Is launched from .__init__().
		rev.2
		'''
		# check for float:
		if (a.__class__ == float) or (b.__class__ == float) or (step.__class__ == float):
			raise TypeError('Please, use Decimal(), int, or float, which is written as string (in quotes), because general float type cannot reproduce all numbers - some of them are changed to other, what causes errors.')
		
		# we check a:
		if not ((a.__class__ == int) or (a.__class__ == str) or (a.__class__ == Decimal)):
			raise TypeError('Start value must be int or decimal, written as string, or Decimal.')
		# we check b:
		if not ((b.__class__ == int) or (b.__class__ == str) or (b.__class__ == Decimal)):
			raise TypeError('Start value must be int or float, written as string, or Decimal.')
		# we check step:
		if not ((step.__class__ == int) or (step.__class__ == str) or (step.__class__ == Decimal)):
			raise TypeError('Start value must be int or float, written as string, or Decimal.')
		
		# we check return_type:
		if not (type(return_type) == str):
			raise TypeError('Return type must be specified with appropriate string.')
	
	
	def check_logic_errors(self):
		'''Checks current instance of humdrange for errors.
		Is launched from .__init__().
		rev. 1
		'''
		# we check step
		if self.step == 0:
			raise ValueError("Step can't be equal to zero.")
		
		# we check a and b
		if self.a > self.b:  # reverse order
			if self.step > 0:
				raise ValueError("Step can't be positive while reverse order.")
		else:  # straight order or a == b
			if self.step < 0:
				raise ValueError("Step can't be negative while straight order.")
		
		# we check return type
		if not ((self.return_type == 'dec') or (self.return_type == 'float') or 
				(self.return_type == 'str') or (self.return_type == 'int')):
					raise ValueError("Return type must be one of: 'dec', 'float', 'str', 'int', it was {0}.".format(type(self.return_type)))
	
	
	
	
	def __iter__(self):
		self.first_time = True  # to return a first
		return self
	
	
	def __next__(self):
	
		if self.first_time:  # first time
			self.first_time = False
			return self.return_depending_type(self.a)
		
		self.current += self.step
		
		if self.a < self.b:  # straight order
			if self.current <= self.b:
				return self.return_depending_type(self.current)
			else:
				raise StopIteration()
		
		elif self.a > self.b:  # reverse order
			if self.current >= self.b:
				return self.return_depending_type(self.current)
			else:
				raise StopIteration()
		
		else:  # a == b
			if self.current == self.a:
				return self.return_depending_type(self.a)
			else:
				raise StopIteration()
	
	
	
	
	def __len__(self):
		try:
			self.length
		except AttributeError:  # if no such attribute
			return int((self.b - self.a) / self.step + 1)
		else:
			return self.length
	
	
	
	
	def __getitem__(self, key):
		'''Returns one value if there's one key (it's int),
		or new appropriate humdrange instance, if key is slice.
		rev. 1
		'''
		if type(key) == int:
			self.check_key_for_errors(key)
			if self.a == self.b:
				return self.return_depending_type(self.a)
			else:  # straight or reverse order
				return self.return_depending_type(self.a + (self.step * (key - 1)))
				# key can be only positive
		
		elif type(key) == slice:  # (slice)
			key = self.replace_negative_keys(key)
			self.check_slice_for_errors(key)
			
			backup = self.return_type  # hack. if it'll be float - it'll pass it (float) to new
			self.return_type = 'dec'  # humdrange's .__init__() method - it'll give errors.
			
			if key.start:
				start = self[key.start]
			else:
				start = self.a
			if key.stop:
				stop = self[key.stop]
			else:
				stop = self.b
			if key.step:
				step = key.step * self.step
			else:
				step = self.step
			
			self.return_type = backup  # return back from hack
			
			return humdrange(start, stop, step, self.return_type)
		
		else:
			raise TypeError('Key is not of an appropriate type. It must be int or slice.')
			
		
	def check_key_for_errors(self, key):
		'''Is used in .__getitem__().
		'''
		if not (type(key) == int):
			raise TypeError('Key must be int.')
		
		if not (1 <= key <= self.__len__()):
			raise IndexError('Key index out of range.')
	
	
	def check_slice_for_errors(self, key):
		'''Is used in .__getitem__().
		'''
		# check types
		if not ( (type(key.start) == int) or (key.start == None) ):
			raise TypeError("Start value must be int or omitted (now it is {0}).".format(key.start))
		if not ( (type(key.stop) == int) or (key.stop == None) ):
			raise TypeError('Stop value must be int or omitted (now it is {0}).'.format(key.start))
		if not ( (type(key.step) == int) or (key.step == None) ):
			raise TypeError('Step value must be int or omitted (now it is {0}).'.format(key.start))	
		
		# check start and stop indexes		
		if key.start:
			if not (1 <= key.start <= self.__len__()):
				raise IndexError('Start key index out of range ({0}).'.format(key.start))
		if key.stop:
			if not (1 <= key.stop <= self.__len__()):
				raise IndexError('Stop key index out of range ({0}).'.format(key.stop))
		
		# now we check step
		if key.step:  # because if it's None, than will be error while "key.step > 0"				
			if (key.start and key.stop) and (key.start > key.stop):  # reverse order
				if key.step > 0:
					raise ValueError('Step cannot be positive ({0}) while reverse order.'.format(key.step))
			else:  # straight order
				if key.step < 0:
					raise ValueError('Step cannot be negative ({0}) while straight order.'.format(key.step))
		elif key.step == 0:			
			raise ValueError('Step cannot be zero.')
	
	def replace_negative_keys(self, key):
		'''Replaces negative key's values (which mean counting from the end of range)
		with positive ones (which mean counting from start of range).
		It doesn't return anything - it replaces so it is.
		'''
		if key.start and (key.start < 0):
			start = (self.__len__() + 1) + key.start  # + -key will give - key
		else:
			start = key.start
		if key.stop and (key.stop < 0):
			stop = (self.__len__() + 1) + key.stop
		else:
			stop = key.stop
		
		return slice(start, stop, key.step)
	
	
	
	
	def return_depending_type(self, value):
		'''Returns value, depending on return type, specified in __init__().
		rev. 1
		'''
		if self.return_type == 'dec':
			return value
		elif self.return_type == 'float':
			return float(value)
		elif self.return_type == 'str':
			return str(value)
		else:  # == 'int'
			return int(value)








if __name__ == '__main__':  # temporary checks
	pass
