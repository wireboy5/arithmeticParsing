from itertools import cycle
import arithmetic_parsing
import string
registers = [
        ("rax", 64),
        ("rbx", 64),
        ("rcx", 64),
        ("rdx", 64),
        ("rsi", 64),
        ("rdi", 64),
        ("rbp", 64),
        ("rsp", 64),
        ("eax", 32),
        ("ebx", 32),
        ("ecx", 32),
        ("edx", 32),
        ("esi", 32),
        ("edi", 32),
        ("ebp", 32),
        ("esp", 32),
        ("ax",  16),
        ("bx",  16),
        ("cx",  16),
        ("dx",  16),
        ("si",  16),
        ("di",  16),
        ("bp",  16),
        ("sp",  16),
        ("ah",   8),
        ("bh",   8),
        ("ch",   8),
        ("al",   8),
        ("bl",   8),
        ("cl",   8),
        ("dl",   8),
        ("sl",   8),
        ("dl",   8),
        ("bpl",  8),
        ("spl",  8)
]
registers.extend([(f"r{i}", 64) for i in range(8,16)])
registers.extend([(f"r{i}d", 32) for i in range(8,16)])
registers.extend([(f"r{i}w", 16) for i in range(8,16)])
registers.extend([(f"r{i}b", 8) for i in range(8,16)])
reg, regsize = zip(*registers)

def resolve_value(value: str) -> str:
    if value.isnumeric():
        return f"{value}"
    elif value in reg:
        return f"{value}"
    elif value.startswith("0x") and all(c in string.hexdigits for c in value.split("0x")[1]):
        return f"{value}"
    else:
        return f"[{value}]"

def listToAssembly(tree_list: list[list], origExpr: str, namespace: str = "base", reg1: str = "rax", reg2: str = "rbx"):
    # Replace variables with registers

    # Create a cycle
    regCyc = cycle([
        reg2,
        reg1
    ])
    
    # Initiate a dictionary to hold out replacements
    regDict: dict = {}

    # For every expression
    for r,expr in zip(regCyc, tree_list):
        # Set the regDict entry to its 
        # respective register
        regDict[expr[1]] = r

    # For every expression
    for i,expr in enumerate(tree_list):
        # For every part of that expression
        for j, x in enumerate(expr):
            # If it si a variable
            if x in regDict.keys():
                # Replace with it's register
                expr[j] = regDict[x]


    # If the last statement is reg2, set it to reg1
    try:
        if tree_list[-1][1] == reg2:
            tree_list[-1][1] = reg1
    except IndexError:
        pass

    # Make sure that the values are properly aligned
    # (So that it works for assembly add)
    for expr in tree_list:
        # Is a the same as variable
        aIsVar = expr[3] == expr[1]

        # Is b the same as variable
        bIsVar = expr[4] == expr[1]

        # Are both?
        bthIsVar = aIsVar and bIsVar

        # If a or both are, skip this one
        if bthIsVar or aIsVar or not bIsVar:
            continue
        
        # If not, and if bIsVar, and this is multiply/add
        if bIsVar and expr[2] in ["+","*"]:
            # Swap a and b
            expr[3], expr[4] = expr[4], expr[3]
    

    # Create output variable
    out = []

    # Create a comment
    comment = f"for {namespace} : {origExpr}"

    # Set expr variable
    expr = tree_list

    # If it is just a single const value
    if len(expr) == 1 and expr[0][0] == "const": 
        # Then just mov into the first register
        out += [
            f"mov {reg1}, {resolve_value(expr[0][2])} ; {comment}"
        ]
    
    # Iterate over expressions
    for ex in expr:
        reg = ex[1] # Get register
        op = ex[2]  # Get operator
        a = ex[3]   # Get A
        b = ex[4]   # Get B
        # If a is not the register
        if a != reg:
            # Mov a into register
            out += [
                f"mov {reg}, {resolve_value(a)}"
            ]
        # If we are adding a negative, switch to a subtraction
        if op == "+" and b.startswith("-"):
            b = b.lstrip("-")
            op = "-"
        # Resolve the operator
        if op == "+":   # Add
            out += [
                f"add {reg}, {resolve_value(b)}"
            ]
        elif op == "*": # Multiply
            out += [
                f"imul {reg}, {resolve_value(b)}"
            ]
        elif op == "-": # Subtract
            out += [
                f"sub {reg}, {resolve_value(b)}"
            ]
        elif op == "/": # Divide
            out += [
                f"idiv {reg}, {resolve_value(b)}"
            ]
    # Return out
    return out


def main():
    # Equation
    equation = "(a+2*3)+7-(a+2*8)"

    # Parse
    parser = arithmetic_parsing.Parser()
    parsed = parser.parse(equation, namespace="asm")

    # Convert to assembly
    asm = listToAssembly(parsed.as_list(),equation,"asm")

    # Join
    asm = "\n".join(asm)

    # Print
    print(asm)

if __name__ == "__main__":
    main()