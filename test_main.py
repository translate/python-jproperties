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

def test_colon_separator():
	_test_deserialize(
		("a:b", [("a", "b")]),
		("a: b", [("a", "b")]),
		("a : b", [("a", "b")]),
		("a :b", [("a", "b")]),
	)


def test_space_separator():
	_test_deserialize(
		("a b", [("a", "b")]),
		("a  b", [("a", "b")]),
		("a        b", [("a", "b")]),
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
