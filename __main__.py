import arithmatic_parsing

parser = arithmatic_parsing.Parser()
a = parser.parse("(testVar+2*3)-(testVar2+3*3)")
print(a.as_json())