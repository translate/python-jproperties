"""
python-jproperties
Java .properties file parsing and handling
"""
import pkg_resources
from .properties import Comment, EmptyNode, Properties, Property


__all__ = ["Comment", "EmptyNode", "Properties", "Property"]
__version__ = pkg_resources.require("jproperties")[0].version
