# arithmeticParsing

Arithmetic parsing is a simple python library designed for parsing arithmetic expressions.\
It is designed to be easy to use and to maintain, and does not focus on optimization as much as it does ease of use.\

This library is designed to use minimal dependancies, and the only non-standard-library module this uses is [treelib](https://github.com/caesar0301/treelib)

## Installation
To install, it is as easy as using pip on this git repository \
I recommend using python -m pip instead of just pip, as this confirms that you are installing on the right python version
```bash
python3.9 -m pip install git+https://github.com/wireboy5/arithmeticParsing
```
You can also install by cloning and then running setup.py
```bash
git clone https://github.com/wireboy5/arithmeticParsing
cd arithmeticParsing
python3.9 setup.py install
```
## Basic usage

arithmetic-parsing was designed to be as easy as possible to use\
A basic example:
```python
import arithmetic_parsing

parseString = "(testVar1 + 2 * 6) + (testVar2 + 2 * 6)"

parser = arithmetic_parsing.Parser()
parsed = parser.parse(parseString)

print(parsed)
```
This will output this:
``` bash
base
└── +
    ├── +
    │   ├── *
    │   │   ├── 2
    │   │   └── 6
    │   └── testVar1
    └── +
        ├── *
        │   ├── 2
        │   └── 6
        └── testVar2
```

Also, because this uses treelib, you can get a json result:
```python
print(parsed.as_json())
```
```json
{
    "base": {
        "children": [
            {
                "+": {
                    "children": [
                        {
                            "+": {
                                "children": [
                                    {
                                        "*": {
                                            "children": [
                                                "2",
                                                "6"
                                            ]
                                        }
                                    },
                                    "testVar1"
                                ]
                            }
                        },
                        {
                            "+": {
                                "children": [
                                    {
                                        "*": {
                                            "children": [
                                                "2",
                                                "6"
                                            ]
                                        }
                                    },
                                    "testVar2"
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }
}
```


