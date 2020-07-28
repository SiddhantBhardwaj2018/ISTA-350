'''
Name - Vibhor Mehta
Section Leader -
ISTA 350 HW5
Date - 4/1/2020
Collaborators - Siddhant Bhardwaj
'''

class Node:
	def __init__(self,data):
		'''
		This constructor initializes the instance variable datum to the data
		and the instance variables left and right to None.
		'''
		self.datum = data
		self.left = None
		self.right = None

	def __add__(self,value):
		'''
		This magic method inserts a new item with self as root,if 
		the item is not already in the tree.
		'''
		if self:
			if value < self.datum:
				if self.left is None:
					self.left = Node(value)
				else:
					self.left  + value
			elif value > self.datum:
				if self.right is None:
					self.right = Node(value)
				else:
					self.right  + value

	def __contains__(self,item):
		'''
		This magic method takes an item and returns True if it is in the subtree, else
		returns False.
		'''
		if self:
			if item > self.datum and self.right:
				return item in self.right
			if item < self.datum and self.left:
				return item in self.left
			if item == self.datum:
				return True
		return False
			
	def sort(self,lst):
		'''
		This method takes items from a tree and appends them to a list in an ordered fashion.
		'''
		if self.left:
			self.left.sort(lst)
		lst.append(self.datum)
		if self.right:
			self.right.sort(lst)

	def __eq__(self,other):
		'''
		This magic method takes 2 Node objects and checks if their roots have the same shape
		and the same datums.
		'''
		if (self.datum != other.datum) or (self.right and not other.right) or (self.left and not other.left) or (other.right and not self.right) or (other.left and not self.left):
			return False
		if (self.left and self.right) and (other.left and other.right):
			return self.left == other.left and self.right == other.right
		if self.left and other.left :
			return self.left == other.left
		if self.right and other.right:
			return self.right == other.right
		return True
	
		


class BST:
	def __init__(self,item = None):
		'''
		This constructor takes an item with the default value of None and
		sets self.root to None if item is None else sets it to Node of item.
		'''
		if item:
			self.root = Node(item)
		else:
			self.root = None

	def __add__(self,item):
		'''
		This magic method inserts a new item into self.
		'''
		if self:
			if self.root:
				self.root + item
			else:
				self.root = Node(item)

	def __contains__(self,item):
		'''
		This magic method takes an item and returns True if item is in self
		else returns False.
		'''
		if self:
			if self.root:
				if item in self.root:
					return True
		return False

	def sort(self):
		'''
		This method returns a list of data in self in ordered fashion.
		'''
		lst = []
		if self:
			if self.root:
				self.root.sort(lst)
		return lst

	def __eq__(self,other):
		'''
		This magic method takes a BST object and returns True if item is in self and other have equal number of nodes.
		'''
		if not self.root and not other.root:
			return True
		if self.root and other.root:
			if self.root == other.root:
				return True
		return False

	@classmethod
	def from_file(cls,fname,type1 = None):
		'''
		This classmethod takes a filename and a type argument which defaults to None.
		It initializes a BST tree and reads the file,stripping it and adds it to the Tree in the type
		as is required in the type argument. If type argument is None, it adds to the tree as it is.
		'''
		tree = cls()
		with open(fname,'r') as file:
			text = file.readlines()
			for line in text:
				line = line.strip()
				if type1 is None:
					tree + line
				else:
					tree + type1(line)
		return tree



	
def selection_sort(lst):
	'''
	This function applies the selection algorithm to a list of 
	unordered objects and returns an ordered list.
	'''
	for i in range((len(lst))):
		key = i
		for j in range(i + 1,len(lst)):
			if lst[key] > lst[j]:
				key = j
		lst[i],lst[key] = lst[key],lst[i]
	return lst