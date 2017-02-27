"""
python-jproperties
Java .properties file parsing and handling
"""
from collections import OrderedDict
from collections.abc import MutableMapping


__version__ = "0.1"
__author__ = "Jerome Leclanche"
__email__ = "jerome@leclan.ch"


class EmptyNode:
	def __repr__(self):
		return "<EmptyNode>"


class Comment:
	def __init__(self, value, sigil="#"):
		self.value = value
		self.sigil = sigil

	def __str__(self):
		return "\n".join("%s %s" % (self.sigil, line) for line in self.value.split("\n"))

	def __repr__(self):
		return "<Comment: %r>" % (str(self))


class Property:
	DEFAULT_SEPARATOR = " = "

	def __init__(self, key, value, separator=DEFAULT_SEPARATOR):
		self.key = key
		self.value = value
		self.separator = separator

	def __repr__(self):
		return "<Property %r %s %r>" % (self.key, self.separator, self.value)


class Properties(MutableMapping):
	def __init__(self, defaults=None):
		if defaults is not None:
			self._props = defaults.copy()
		else:
			self._props = OrderedDict()
		self.nodes = []

	def __str__(self):
		ret = []
		for node in self.nodes:
			if isinstance(node, Comment):
				ret.append(str(node))
			elif isinstance(node, EmptyNode):
				ret.append("")
			else:
				ret.append(self.escape_key(node.key) + node.separator + self.escape(node.value))
		return "\n".join(ret)

	def __getitem__(self, key):
		return self._props.get(key, "")
	getProperty = __getitem__

	def __setitem__(self, key, value):
		self._props[key] = value
		for node in self.nodes:
			if isinstance(node, Property) and node.key == key:
				self.nodes[self.nodes.index(node)] = Property(key, value)
				break
		else:
			self.nodes.append(Property(key, value))
	setProperty = __setitem__

	def __delitem__(self, key):
		for node in self.nodes:
			if isinstance(node, Property) and node.key == key:
				del self.nodes[self.nodes.index(node)]
		del self._props[key]
	delProperty = __delitem__

	def __iter__(self):
		for key in self._props.keys():
			yield key

	def __len__(self):
		return len(self._props.keys())

	def __contains__(self, key):
		return key in self._props

	@staticmethod
	def escape(value):
		return value.encode("unicode_escape").decode("utf-8")

	@staticmethod
	def escape_key(value):
		return value.encode("unicode_escape") \
			.decode("utf-8") \
			.replace(":", r"\:") \
			.replace("=", r"\=") \
			.replace(" ", r"\ ")

	@staticmethod
	def unescape(value):
		ret = []
		backslash = False
		for c in value:
			if backslash:
				if c == "u":
					# fall through to native unicode_escape
					ret.append(r"\u")
				elif c == "t":
					ret.append("\t")
				elif c == "r":
					ret.append("\r")
				elif c == "n":
					ret.append("\n")
				elif c == "f":
					ret.append("\f")
				else:
					ret.append(c)
				backslash = False
			elif c == "\\":
				backslash = True
			else:
				ret.append(c)

		ret = "".join(ret).encode("utf-8").decode("unicode_escape")
		return ret

	@staticmethod
	def _get_lines(stream):
		def _strip_line(line):
			last = ""
			while line.endswith(("\n", "\r", " ")):
				if line[-1] == "\\":
					line += last
					break
				last = line[-1]
				line = line[:-1]

			return line.lstrip()

		buf = []
		cont = False
		for line in stream.readlines():
			if line.endswith("\\\n") and not line.endswith("\\\\\n"):
				buf.append(line[:-2].lstrip())
				cont = True
				continue
			elif cont:
				buf.append(line.strip())
				cont = False
			else:
				buf.append(line)

			yield _strip_line("".join(buf))
			buf = []

	@staticmethod
	def _separate(line):
		def getkey(s):
			ret = []
			escaping = False
			for c in s:
				if not escaping:
					if c in " \t:=":
						break
					elif c == "\\":
						escaping = True
				else:
					escaping = False

				ret.append(c)
			return "".join(ret)

		def getseparator(s):
			ret = []
			for c in s:
				if c not in " \t:=":
					return "".join(ret)
				ret.append(c)
			return "".join(ret)

		def getvalue(s):
			ret = []
			escaping = False
			for c in s:
				if not escaping:
					if c == "\\":
						escaping = True
				else:
					escaping = False

				ret.append(c)
			return "".join(ret)

		key = getkey(line)
		idx = len(key)
		sep = getseparator(line[idx:])
		idx += len(sep)
		value = getvalue(line[idx:])
		return key, sep, value

	def load(self, stream):
		comment = []
		for line in self._get_lines(stream):
			# Skip null lines
			if not line:
				self.nodes.append(EmptyNode())
				continue

			if line.startswith(("#", "!")):
				# NOTE: Multiline comments with different sigils will be normalized on the
				# last specified sigil
				sigil = line[0]
				comment.append(line[1:].strip())
				continue
			elif comment:
				self.nodes.append(Comment("\n".join(comment), sigil))
				comment = []

			key, separator, value = self._separate(line)
			key = self.unescape(key)
			value = self.unescape(value)
			self._props[key] = value
			node = Property(key, value, separator)
			self.nodes.append(node)

	def propertyNames(self):
		# Java compat
		return self._props.keys()
