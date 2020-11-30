import re
from re import L


basicTokens = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2
}

def split_keep(s,d):
    split = s.split(d)
    return [substr + d for substr in split[:-1]] + [split[-1]]

class Parser:
    def __init__(self, optimize: bool = True, sort: bool = True, tokens: dict[str, int] = basicTokens):
        """
            A basic infix arithmatic parsing class
            
            - Optimize [bool]
                Specifies whether to "optimize" the code. This mainly resolves constant integers.
                For example:
                    3 * 2 would be resolved to 6
                If this is not specified, it defaults to True
            
            - Sort [bool]
                You almost never want to set this to False. This makes sure that 
                values areclosest to their first reference. If you wanted to 
                use this to convert arithmatic to assembly, you would need to do this anyways
        """
        self.optimize = optimize
        self.sort = sort

        # Parentheses always need to be considered tokens
        self.tokens = tokens | {"(":0,")":0}
    
    def tokenize_expr(self, expr: str) -> str:
        """
            Tokenizes the expression

            - expr [str]
                The expression to tokenize
        """

        # Output Variable
        # For now, this is equivilent to expr
        out = expr

        for token in self.tokens.keys():
            # Lets add a backslash between every character
            # Of the token
            token = [f"\{tok}" for tok in token]
            token = ''.join(token)
            
            # Split it by the token
            splt =  re.split(f"({token})", out)

            # And join those splits by a space
            out = ' '.join(splt)
        
        # Now lets get individual tokens list
        # By splitting by space
        out = out.split()

        # And lets return, filtering out any empty
        # list items
        return list(filter(lambda value: value.strip(),out))

    def is_token(self, tok: str) -> bool:
        return tok in self.tokens.keys()

    def get_token_priority(self, tok: str) -> int:
        if self.is_token(tok):
            return self.tokens[tok]
        else:
            return 0

    def infix_to_postfix(self, expr: str) -> str:
        """
            Converts infix algebra to postfix algebra.

            - expr [str]
                The input expression
        """

        # The stack that we will be performing operations on
        stack: list[str] = []

        # The output
        output: str = ""

        # We always need surrounding parentheses
        expr = f"({expr})"

        # The tokenized expression
        expr = self.tokenize_expr(expr)


        
        # For every token in expression
        for token in expr:
            # Check what token it is
            if token == "(":
                # If it is a (, then append to stack
                stack.append("(")
            elif token == ")":
                # If it is a ), then iterate over stack
                while stack[-1] != '(':
                    # Popping the last item from stack, to output
                    # Include a trailing space
                    # Until the last item in the stack is a (
                    output += f"{stack.pop()} "
                # Pop the last ( from the stack
                stack.pop()
            elif re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", token):
                # If it matches a name/variable
                # Append to output with a trailing space
                output += f"{token} "
            elif re.match(r"\d+",token):
                # If it is a number
                # Then append with a trailing space
                output += f"{token} "
            else:
                if self.is_token(token):
                    # If it is a token
                    # Pop it from the stack while
                    # It's priority is smaller than
                    # the last priority of the stack
                    # Put it into output with a trailing space
                    while self.get_token_priority(token) <= self.get_token_priority(stack[-1]):
                        output += f"{stack.pop()} "
                    # And append token to stack
                    stack.append(token)
        # Return output
        return output
    
    def infix_to_prefix(self, expr: str) -> str:
        """
            Converts infix algebra to prefix algebra.

            - expr [str]
                The input expression
        """
        
        # Reverse expr
        expr = reversed(expr)

        # Convert expr to list
        expr = list(expr)

        # Reverse all parantheses
        for i, e in enumerate(expr):
            if e == "(":
                expr[i] = ")"
            elif e == ")":
                expr[i] = "("
        
        # Convert expr back to string
        expr = ''.join(expr)

        # Convert expr to postfix
        expr = self.infix_to_postfix(expr)

        # Reverse expr again
        expr = reversed(expr)

        # Convert expr to string again
        expr = ''.join(expr)

        # Return expr
        return expr
