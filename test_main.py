#!/usr/bin/env python
import sys
from collections import OrderedDict
from io import StringIO
from jproperties import Properties


def _test_deserialize(*data):
	for s, items in data:
		props = Properties()
		props.load(StringIO(s))
		assert list(props.items()) == items


def _test_serialize(*data):
	for items, s in data:
		d = OrderedDict(items)
		props = Properties(d)
		assert list(props.items()) == items


def test_eq_separator():
	_test_deserialize(
		("a=b", [("a", "b")]),
		("a= b", [("a", "b")]),
		("a = b", [("a", "b")]),
		("a =b", [("a", "b")]),
	)
	_test_serialize(
		([("a", "b")], "a = b"),
	)


def test_escaped_whitespace():
	_test_deserialize(
		(r"a = \f", [("a", "\f")]),
		(r"a = \n", [("a", "\n")]),
		(r"a = \r", [("a", "\r")]),
		(r"a = \t", [("a", "\t")]),
	)
	_test_serialize(
		([("a", "\f")], r"a = \f"),
		([("a", "\n")], r"a = \n"),
		([("a", "\r")], r"a = \r"),
		([("a", "\t")], r"a = \t"),
	)


def test_empty_value():
	_test_deserialize(
		("a = ", [("a", "")]),
		("a : ", [("a", "")]),
	)
	_test_serialize(
		([("a", "")], "a = "),
	)


def test_colon_separator():
	_test_deserialize(
		("a:b", [("a", "b")]),
		("a: b", [("a", "b")]),
		("a : b", [("a", "b")]),
		("a :b", [("a", "b")]),
	)


def test_dropped_escapes():
	_test_deserialize(
		(r"a : http://example.org/?foo=bar", [("a", "http://example.org/?foo=bar")]),
		(r"a = http\://example.org/?foo\=bar", [("a", "http://example.org/?foo=bar")]),
		(r"\b = \z", [("b", "z")]),
		(r"a = \'single quotes'", [("a", "'single quotes'")]),
		(r'a = \"double quotes"', [("a", '"double quotes"')]),
	)


fruits = r"""
fruits                           apple, banana, pear, \
                                 cantaloupe, watermelon, \
                                 kiwi, mango
""".strip()
fruits_values = "apple, banana, pear, cantaloupe, watermelon, kiwi, mango"
def test_java_examples():
	_test_deserialize(
		("Truth = Beauty", [("Truth", "Beauty")]),
		(" Truth:Beauty", [("Truth", "Beauty")]),
		("Truth                    :Beauty", [("Truth", "Beauty")]),
		(fruits, [("fruits", fruits_values)]),
		("cheeses", [("cheeses", "")]),
	)


def test_space_separator():
	_test_deserialize(
		("a b", [("a", "b")]),
		("a  b", [("a", "b")]),
		("a        b", [("a", "b")]),
		("a\tb", [("a", "b")]),  # Tab is also a valid separator
	)


def test_separator_in_key():
	_test_deserialize(
		(r"key\:with\:colons : b", [("key:with:colons", "b")]),
		(r"key\=with\=equals = b", [("key=with=equals", "b")]),
		(r"key\twith\ttabs b", [("key\twith\ttabs", "b")]),
	)
	_test_serialize(
		([("key:with:colons", "b")], r"key\:with\:colons = b"),
		([("key=with=equals", "b")], r"key\=with\=equals = b"),
		([("key with spaces", "b")], r"key\ with\ spaces = b"),
		([("key\twith\ttabs", "b")], r"key\twith\ttabs = b"),
	)


def test_space_in_key():
	_test_deserialize(
		("key\ with\ spaces = b", [("key with spaces", "b")]),
		("key\ with\ spaces b", [("key with spaces", "b")]),
		("key\ with\ spaces : b", [("key with spaces", "b")]),
		("key\ with\ spaces\ : b", [("key with spaces ", "b")]),
	)


def test_property_node_update():
	s = "key = value"
	props = Properties()
	props.load(StringIO(s))
	props["key"] = "another_value"
	assert str(props) == "key = another_value"


def test_iterable_properties():
	items = [
		("a", "b"),
		("c", "d"),
		("e", "f")
	]
	d = OrderedDict(items)
	props = Properties(d)
	assert [key for key in props] == list(d.keys())


def test_len():
	items = [
		("a", "b"),
		("c", "d"),
		("e", "f")
	]
	d = OrderedDict(items)
	props = Properties(d)
	assert len(props) == 3


def test_empty_len():
	props = Properties()
	assert len(props) == 0

	d = OrderedDict()
	props = Properties(d)
	assert len(props) == 0


def test_equals():
	items = [
		("a", "b"),
		("c", "d"),
		("e", "f")
	]
	d = OrderedDict(items)
	props = Properties(d)
	assert props == Properties(d)


def test_not_equals():
	assert Properties(OrderedDict([
		("a", "b"),
		("c", "d"),
		("e", "f")
	])) != Properties(OrderedDict([
		("c", "d"),
		("e", "f")
	]))


def test_update():
	"""test MutableMapping derived method"""
	items = [
		("a", "b"),
		("c", "d"),
		("e", "f")
	]
	d = OrderedDict(items)
	props = Properties(d)
	props.update({
		"g": "h",
		"c": "i"
	})
	assert props == Properties(OrderedDict([
		("a", "b"),
		("c", "i"),
		("e", "f"),
		("g", "h")
	]))


def test_delete():
	items = [
		("a", "b"),
		("c", "d"),
		("e", "f")
	]
	d = OrderedDict(items)
	props = Properties(d)
	del props["a"]

	assert "a" not in props
	assert props == Properties(OrderedDict([
		("c", "d"),
		("e", "f")
	]))


def main():
	for name, f in globals().items():
		if name.startswith("test_") and callable(f):
			f()


if __name__ == "__main__":
	main()
