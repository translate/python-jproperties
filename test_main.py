#!/usr/bin/env python
import sys
from io import StringIO
from jproperties import Properties


def _test_deserialize(*data):
	for s, items in data:
		props = Properties()
		props.load(StringIO(s))
		assert list(props.items()) == items


def test_eq_separator():
	_test_deserialize(
		("a=b", [("a", "b")]),
		("a= b", [("a", "b")]),
		("a = b", [("a", "b")]),
		("a =b", [("a", "b")]),
	)


def test_escaped_whitespace():
	_test_deserialize(
		(r"a = \f", [("a", "\f")]),
		(r"a = \n", [("a", "\n")]),
		(r"a = \r", [("a", "\r")]),
		(r"a = \t", [("a", "\t")]),
	)


def test_empty_value():
	_test_deserialize(
		("a = ", [("a", "")]),
		("a : ", [("a", "")]),
	)


def test_colon_separator():
	_test_deserialize(
		("a:b", [("a", "b")]),
		("a: b", [("a", "b")]),
		("a : b", [("a", "b")]),
		("a :b", [("a", "b")]),
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

def test_space_in_key():
	_test_deserialize(
		("key\ with\ spaces = b", [("key with spaces", "b")]),
		("key\ with\ spaces b", [("key with spaces", "b")]),
		("key\ with\ spaces : b", [("key with spaces", "b")]),
		("key\ with\ spaces\ : b", [("key with spaces ", "b")]),
	)


def main():
	for name, f in globals().items():
		if name.startswith("test_") and callable(f):
			f()


if __name__ == "__main__":
	main()
