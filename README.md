# arithmeticParsing

Arithmetic parsing is a simple python library designed for parsing arithmetic expressions.\
It is designed to be easy to use and to maintain, and does not focus on optimization as much as it does ease of use.

This library is designed to use minimal dependancies, and the only non-standard-library module this uses is [treelib](https://github.com/caesar0301/treelib)

## Installation
To install, it is as easy as using pip on this git repository \
I recommend using python -m pip instead of just pip, as this confirms that you are installing on the right python version
```bash
python3.9 -m pip install arithmetic-parsing
```
You can also install by cloning and then running setup.py
```bash
git clone https://github.com/wireboy5/arithmeticParsing
cd arithmeticParsing
python3.9 setup.py install
```
## Usage

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

Another output form is the list output
```python
print(parsed.as_list())
```

```python
[
    ['dyn', 'base_0', '+', 'testVar2', '12'], 
    ['dyn', 'base_1', '+', 'testVar1', '12'], 
    ['dyn', 'base_2', '+', 'base_1', 'base_0']
]
```

Lets take a look at the first item:
```python
['dyn', 'base_0', '+', 'testVar2', '12']
```
And lets break it down
- Dyn
    - This specifies that it is a dynamic value, and not a constant
- base_0
    - This is the variable name, If you were to convert this into something like python.
- \+
    - This is the operator
- testVar2
    - This is the first operand
- 12
    - This is the second operand

Notice how it has 12 instead of 2 * 6?\
That is because it is optimizing the result.\
We can disable this optimization by setting optimize to false:
```python
parser = arithmetic_parsing.Parser(
    optimized = False
)
```

Also notice that the parsed list has the values in a different order than you would expect? \
The parser automatically sorts them to be as close as possible to their first reference, from the top down.\
This to can be disabled:
```python
parser = arithmetic_parsing.Parser(
    sort = False
)
```

We can use this to convert the value to assembly:
```python
from arithmetic_parsing.examples import assembly

asm = assembly.listToAssembly(parsed.as_list(),parseString)

asm = "\n".join(asm)

print(asm)
```
This will output NASM code:
```nasm
mov rbx, [testVar2]
add rbx, 12
mov rbx, [testVar1]
add rbx, 12
mov rax, rbx
add rax, rbx'
```
NOTE: Do not use this function for converting to assembly in an actual program. \
This function is for demonstration purposes and has not been tested thouroughly


