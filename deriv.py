import math
import random
import sys

class Node:
	def __init__(self):
		self._deriv = None
		pass
	def __add__(self, other):
		return NodeAdd(self, other)
	def __radd__(self, other):
		return NodeAdd(other, self)
	def __sub__(self, other):
		return NodeSub(self, other)
	def __rsub__(self, other):
		return NodeSub(other, self)
	def __mul__(self, other):
		return NodeMul(self, other)
	def __rmul__(self, other):
		return NodeMul(other, self)
	def __truediv__(self, other):
		return NodeDiv(self, other)
	def __rtruediv__(self, other):
		return NodeDiv(other, self)
	def __pow__(self, other):
		return NodePow(self, other)
	def __rpow__(self, other):
		return NodePow(other, self)
	def __neg__(self):
		return NodeNeg(self)
	def get_deriv(self):
		if self._deriv is None:
			self._deriv = self._compute_deriv()
		return self._deriv

class NodeNumber(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = float(a)
		pass
	def __str__(self):
		if self._a == e:
			return "e"
		if self._a == pi:
			return "pi"
		return str(self._a)
	def __float__(self):
		return self._a
	def _compute_deriv(self):
		return NodeNumber(0)
	def simplify(self):
		return self

class NodeX(Node):
	def __init__(self):
		Node.__init__(self)
		pass
	def __str__(self):
		return "x"
	def _compute_deriv(self):
		return NodeNumber(1)
	def simplify(self):
		return self

class NodeAdd(Node):
	def __init__(self, a, b):
		Node.__init__(self)
		self._a = a
		self._b = b
		pass
	def __str__(self):
		return "(%s)+(%s)" % (str(self._a), str(self._b))
	def _compute_deriv(self):
		return self._a.get_deriv() + self._b.get_deriv()
	def simplify(self):
		a = self._a.simplify()
		b = self._b.simplify()
		if type(a) == NodeNumber and type(b) == NodeNumber:
			return NodeNumber(float(a) + float(b))
		if type(a) == NodeNumber and float(a) == 0.0:
			return b
		if type(b) == NodeNumber and float(b) == 0.0:
			return a
		return a + b

class NodeSub(Node):
	def __init__(self, a, b):
		Node.__init__(self)
		self._a = a
		self._b = b
		pass
	def __str__(self):
		return "(%s)-(%s)" % (str(self._a), str(self._b))
	def _compute_deriv(self):
		return self._a.get_deriv() - self._b.get_deriv()
	def simplify(self):
		a = self._a.simplify()
		b = self._b.simplify()
		if type(a) == NodeNumber and type(b) == NodeNumber:
			return NodeNumber(float(a) - float(b))
		if type(a) == NodeNumber and float(a) == 0.0:
			return -b
		if type(b) == NodeNumber and float(b) == 0.0:
			return a
		return a - b

class NodeMul(Node):
	def __init__(self, a, b):
		Node.__init__(self)
		self._a = a
		self._b = b
		pass
	def __str__(self):
		return "(%s)*(%s)" % (str(self._a), str(self._b))
	def _compute_deriv(self):
		return self._a.get_deriv()*self._b + self._a*self._b.get_deriv()
	def simplify(self):
		a = self._a.simplify()
		b = self._b.simplify()
		if type(b) == NodeNumber:
			a, b = b, a
		if type(a) == NodeNumber and type(b) == NodeNumber:
			return NodeNumber(float(a) * float(b))
		if type(a) == NodeNumber and float(a) == 0.0:
			return NodeNumber(0)
		if type(a) == NodeNumber and float(a) == 1.0:
			return b
		if type(a) == NodeNumber and float(a) == -1.0:
			return -b
		return a * b

class NodeDiv(Node):
	def __init__(self, a, b):
		Node.__init__(self)
		self._a = a
		self._b = b
		pass
	def __str__(self):
		return "(%s)/(%s)" % (str(self._a), str(self._b))
	def _compute_deriv(self):
		return (self._a.get_deriv()*self._b - self._a*self._b.get_deriv()) / (self._b ** NodeNumber(2))
	def simplify(self):
		a = self._a.simplify()
		b = self._b.simplify()
		if type(a) == NodeNumber and type(b) == NodeNumber:
			return NodeNumber(float(a) / float(b))
		if type(a) == NodeNumber and float(a) == 0.0:
			return NodeNumber(0)
		if type(b) == NodeNumber and float(b) == 1.0:
			return a
		if type(b) == NodeNumber and float(b) == -1.0:
			return -a
		return a / b

class NodeNeg(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "-(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return -self._a.get_deriv()
	def simplify(self):
		a = self._a.simplify()
		if type(a) == NodeNumber:
			return NodeNumber(-float(a))
		if type(a) == NodeNeg:
			return a._a
		return -a

class NodePow(Node):
	def __init__(self, a, b):
		Node.__init__(self)
		self._a = a
		self._b = b
		pass
	def __str__(self):
		return "(%s)**(%s)" % (str(self._a), str(self._b))
	def _compute_deriv(self):
		if type(self._b) == NodeNumber:
			return self._b * (self._a ** NodeNumber(float(self._b) - 1)) * self._a.get_deriv()
		p = NodeLn(self._a) * self._b
		return (self._a ** self._b) * p.get_deriv()
	def simplify(self):
		a = self._a.simplify()
		b = self._b.simplify()
		if type(a) == NodeNumber and type(b) == NodeNumber:
			return NodeNumber(float(a) ** float(b))
		if type(b) == NodeNumber and float(b) == 0.0:
			return NodeNumber(1.0)
		if type(b) == NodeNumber and float(b) == 1.0:
			return a
		if type(a) == NodeNumber and float(a) == 0.0:
			return a
		if type(a) == NodeNumber and float(a) == 1.0:
			return a
		return a ** b

class NodeLn(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "ln(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return self._a.get_deriv() / self._a
	def simplify(self):
		a = self._a.simplify()
		if type(a) == NodeNumber and float(a) == e:
			return NodeNumber(1)
		if type(a) == NodeNumber and float(a) == 1.0:
			return NodeNumber(0)
		return ln(a)

class NodeSin(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "sin(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return NodeCos(self._a) * self._a.get_deriv()
	def simplify(self):
		a = self._a.simplify()
		return sin(a)

class NodeCos(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "cos(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return -NodeSin(self._a) * self._a.get_deriv()
	def simplify(self):
		a = self._a.simplify()
		return cos(a)

class NodeTg(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "tg(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return self._a.get_deriv() / (NodeCos(self._a) ** NodeNumber(2))
	def simplify(self):
		a = self._a.simplify()
		return tg(a)

class NodeCtg(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "ctg(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return -self._a.get_deriv() / (NodeSin(self._a) ** NodeNumber(2))
	def simplify(self):
		a = self._a.simplify()
		return ctg(a)

class NodeArcsin(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "arcsin(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return self._a.get_deriv() / ((NodeNumber(1) - self._a ** NodeNumber(2)) ** NodeNumber(0.5))
	def simplify(self):
		a = self._a.simplify()
		return arcsin(a)

class NodeArccos(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "arccos(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return -self._a.get_deriv() / ((NodeNumber(1) - self._a ** NodeNumber(2)) ** NodeNumber(0.5))
	def simplify(self):
		a = self._a.simplify()
		return arccos(a)

class NodeArctg(Node):
	def __init__(self, a):
		Node.__init__(self)
		self._a = a
		pass
	def __str__(self):
		return "arctg(%s)" % (str(self._a), )
	def _compute_deriv(self):
		return self._a.get_deriv() / (NodeNumber(1) + self._a ** NodeNumber(2))
	def simplify(self):
		a = self._a.simplify()
		return arctg(a)

def ln(a):
	if type(a) in (float, int):
		return math.log(a)
	return NodeLn(a)
def sin(a):
	if type(a) in (float, int):
		return math.sin(a)
	return NodeSin(a)
def cos(a):
	if type(a) in (float, int):
		return math.cos(a)
	return NodeCos(a)
def tg(a):
	if type(a) in (float, int):
		return math.tan(a)
	return NodeTg(a)
def ctg(a):
	if type(a) in (float, int):
		return math.cos(a) / math.sin(a)
	return NodeCtg(a)
def arcsin(a):
	if type(a) in (float, int):
		return math.asin(a)
	return NodeArcsin(a)
def arccos(a):
	if type(a) in (float, int):
		return math.acos(a)
	return NodeArccos(a)
def arctg(a):
	if type(a) in (float, int):
		return math.atan(a)
	return NodeArctg(a)
e = math.e
pi = math.pi
x = NodeX()

def nodify_numbers(t):
	if type(t) in (float, int):
		return NodeNumber(t)
	if type(t) == NodeNumber:
		return t
	if "_a" in t.__dict__:
		t._a = nodify_numbers(t._a)
	if "_b" in t.__dict__:
		t._b = nodify_numbers(t._b)
	return t

def build_tree(s):
	t = eval(s)
	return nodify_numbers(t)

def evaluate(t, x):
	return eval(str(t))

fin = open("deriv.in", "r")
fout = open("deriv.out", "w")

for s in fin.readlines():
	s = s.strip()
	if s == "":
		continue
	expr = build_tree(s)
	deriv = expr.get_deriv()
	deriv = deriv.simplify()
	print(deriv, file=fout)

fin.close()
fout.close()
