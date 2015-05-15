from collections import OrderedDict


class EmptyNode:
	def __repr__(self):
		return "<EmptyNode>"


class Comment(str):
	pass


class Property:
	def __init__(self, key, value, separator=" = "):
		self.key = key
		self.value = value
		self.separator = separator

	def __repr__(self):
		return "<Property %r %s %r>" % (self.key, self.separator, self.value)


class Properties(object):
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
				ret.append("\n".join("# " + line for line in node.strip().split("\n")))
			elif isinstance(node, EmptyNode):
				ret.append("")
			else:
				ret.append(self.escape(node.key) + node.separator + self.escape(node.value))
		return "\n".join(ret)

	def __getitem__(self, name):
		return self._props.get(key, "")
	getProperty = __getitem__

	def __setitem__(self, key, value):
		self._props[key] = value
		self.nodes.append(Property(key, value))
	setProperty = __setitem__

	@staticmethod
	def escape(value):
		return value.replace(":", r"\:").replace("=", "\=")

	@staticmethod
	def unescape(value):
		return value.replace(r"\:", ":").replace(r"\=", "=")

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

		key = []
		value = []
		buf = []
		cont = False
		for line in stream.readlines():
			if line.endswith("\\\n") and not line.endswith("\\\\\n"):
				buf.append(line[:-2])
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
					if c in " :=":
						return "".join(ret)
					elif c == "\\":
						escaping = True
				else:
					escaping = False

				ret.append(c)
			raise SyntaxError(repr(s))

		def getseparator(s):
			ret = []
			for c in s:
				if c not in " :=":
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

	def items(self):
		return self._props.items()

	def load(self, stream):
		comment = ""
		for line in self._get_lines(stream):
			# Skip null lines
			if not line:
				self.nodes.append(EmptyNode())
				continue

			if line.startswith(("#", "!")):
				comment += line[1:].strip() + "\n"
				continue
			elif comment:
				self.nodes.append(Comment(comment))
				comment = ""

			key, separator, value = self._separate(line)
			key = self.unescape(key)
			value = self.unescape(value)
			self._props[key] = value
			node = Property(key, value, separator)
			self.nodes.append(node)

	def propertyNames(self):
		# Java compat
		return self._props.keys()
