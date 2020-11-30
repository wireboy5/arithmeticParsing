import arithmatic_parsing

parser = arithmatic_parsing.Parser()
a = parser.infix_to_prefix("(testVar+2*3)-(testVar2+3*3)")
print(a)