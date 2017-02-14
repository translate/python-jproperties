python-jproperties
==================
[![Build Status](https://travis-ci.org/translate/python-jproperties.svg)](https://travis-ci.org/translate/python-jproperties)

A python library for parsing and handling Java .properties files.


Installation
------------

To build, run the following command:

```
 $ python setup.py build
```

To install, preferably into a virtual environment:

```
 $ python setup.py install
```

Usage
-----

A Properties object is, on the outside, a simple key-value store.

Initialize it as such:

```python
from jproperties import Properties

p = Properties()

# Or with default values:
p2 = Properties({"foo": "bar"})
print(p2["foo"])
```

The usual dictionary interfaces are available:

```python
p2["key"] = "value"
for key in p2.keys():
	print(key, p2[key])
```

Note that keys and values are all expected to be and be treated as strings.

To serialize the object into the .properties format, turn it into a string:

```python
with open("out.properties", "w") as f:
	f.write(str(p2))
```

To read an existing properties file, use `Properties.load()` on an already-
instanced Properties object.. That method expects a file-like object that
supports the `readlines()` method.

```python
with open("out.properties", "r") as f:
	p2.load(f)
```

Note that comments and blank lines are loaded into the Properties object's
nodes when using load(), and will be serialized in str().

If comments and blank lines are unimportant and you want to get rid of them,
you can create a new Properties object from an existing one's keys:

```python
p3 = Properties(p2.keys())
```


### License

This project is licensed under the MIT license. The full license text is
available in the LICENSE file.
