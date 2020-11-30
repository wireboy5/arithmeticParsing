from treelib import Tree, Node
from collections import deque
from . import mathFuncs
import treelib
import math
import re

from treelib import tree


basicTokens = {
    "+": [1, mathFuncs.add],
    "-": [1, mathFuncs.sub],
    "*": [2, mathFuncs.mul],
    "/": [2, mathFuncs.div]
}

def split_keep(s,d):
    split = s.split(d)
    return [substr + d for substr in split[:-1]] + [split[-1]]


class ParseResult:
    tree_list: list[list]
    infix: str
    prefix: str
    postfix: str
    tree: Tree

    def __str__(self):
        return self.tree.__str__()
    
    def as_json(self):
        return self.tree.to_json()

    def as_list(self):
        return self.tree_list



class Parser:
    def __init__(self, optimize: bool = True, sort: bool = True, tokens: dict[str, int] = basicTokens):
        """
            A basic infix arithmetic parsing class
            
            - Optimize [bool]
                Specifies whether to "optimize" the code. This mainly resolves constant integers.
                For example:
                    3 * 2 would be resolved to 6
                If this is not specified, it defaults to True
            
            - Sort [bool]
                You almost never want to set this to False. This makes sure that 
                values areclosest to their first reference. If you wanted to 
                use this to convert arithmetic to assembly, you would need to do this anyways
        """
        self.optimize = optimize
        self.sort = sort

        # Parentheses always need to be considered tokens
        self.tokens = tokens | {"(":[0, None],")":[0, None]}
    
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
            return self.tokens[tok][0]
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

    def _add_prefix_to_node(self, prefix_deque: deque, tree: Tree, node: Node, index: int) -> tuple[Tree, int]:
        """
            Adds the prefix algebra to a treelib node.
            This should not be accessed externally
        """

        # Get the current token by popping the left of the prefix_deque
        token = prefix_deque.popleft()


        # If the token is an operator
        if self.is_token(token):
            # Create a new node
            new_node = tree.create_node(
                f"{token}", # Name the same as token
                index, # ID that of index
                parent = node # And parent this node
            )
            # Increment index
            index += 1

            # Calculate child A
            tree,index = self._add_prefix_to_node(prefix_deque, tree, new_node, index)

            # Calculate child B
            tree,index = self._add_prefix_to_node(prefix_deque, tree, new_node, index)

            # Return the tree and the index
            return tree, index
        else:
            # If the token is not an operator

            # Just create a new node
            new_node = tree.create_node(
                f"{token}", # Name the same as token
                index, # ID that of index
                parent = node # And parent this node
            )

            # Increment index
            index += 1
            
            # Return index and tree
            return tree, index

    def prefix_to_tree(self, expr: str, delimeter: str = None, node_name: str = "base") -> Tree:
        """
            Converts prefix math to a treelib tree.

            - expr [str]
                The input expression
                This MUST be delimeted by some form
                of delimeter

            - delimeter [str] = None
                This is the character that the infix algebra is delimeted
                by. None means whitespace
            
            - name [str] = "base"
                The name of the root node of the tree
        """
        # Create a tree
        tree = Tree()

        # Convert the expression to a deque
        expr_deque = deque(expr.split(delimeter))

        # Create a base node
        base_node = tree.create_node(node_name,0)

        # Start the add loop
        tree, count = self._add_prefix_to_node(expr_deque, tree, base_node, 1)

        # Return tree
        return tree
    
    def infix_to_tree(self, expr: str, delimeter: str = None, node_name: str = "base") -> Tree:
        """
            Converts post math to a treelib tree.

            - expr [str]
                The input expression
                This MUST be delimeted by some form
                of delimeter

            - delimeter [str] = None
                This is the character that the infix algebra is delimeted
                by. None means whitespace
            
            - name [str] = "base"
                The name of the root node of the tree
        """

        # Convert expr to prefix
        prefix = self.infix_to_prefix(expr)

        # Return prefix_to_tree of this expr
        return self.prefix_to_tree(prefix, delimeter, node_name)
    
    def _tree_to_list(self, tree: Tree, node: Node, output: list[list[list]], namespace: str = "namespace"):
        """
            Converts a tree to a list.
            This is for internal use. A Better frontend version
            will be created later
        """
        # Make sure that the node is from this tree
        node = tree[node.identifier]

        # Get the node's tag
        tag: str = str(node.tag)

        # If this is the root node
        if len(tree.children(node.identifier)) == 1:
            # Calculate A
            a = tree.children(node.identifier)[0]
            return self._tree_to_list(tree, a, output, namespace)
        
        if node.is_leaf(): # If this node is a leaf
            # Create the variable
            vname: str = f"{namespace}_{len(output[1])+1}"

            # Add the variable to the list of variables
            output[1].append([vname])

            # And assign the variable as a const
            output[0].append(["const", vname, tag])
        else: # If this node is not a leaf
            # Calculate children
            children = tree.children(node.identifier)

            # Get a
            a = children[0]

            # Get b
            b = children[1]

            # Recurse on a
            output = self._tree_to_list(tree, a, output, namespace)

            # Assign the variable that A created to varA
            varA = output[1][-1][0]

            # Recurse on b
            output = self._tree_to_list(tree, b, output, namespace)

            # Assign the variable that B created to varB
            varB = output[1][-1][0]

            # Generate the result variable name
            vname: str = f"{namespace}_{len(output[1])+1}"


            # Set vname to the operation between A and B
            output[0].append(["dyn", vname, tag, varA, varB])

            # And now append vname to the list of variables
            output[1].append([vname])
        
        # Return output
        return output
    
    def optimize_tree_list(self, tree_list: list[list[list]], namespace: str = "base") -> list[list[list]]:
        """
            Optimizes a tree_list.

            - tree_list [list[list[list]]]
                The input list
            
            - namespace [str]:
                The input namespace
        """

        # First lets take all constant values and insert them into a dictionary
        # For later reference
        const_values: dict = {}

        # For every expression
        for expr in tree_list[0]:
            # If it is a const:
            if expr[0] == "const":
                # Add it to const vals
                const_values[expr[1]] = expr[2]
        
        # Now filter constants from expressions
        tree_list[0] = filter(lambda value: value if value[0] == "dyn" else None, tree_list[0])

        # And convert tree list back to a list
        tree_list[0] = list(tree_list[0])

        # Now resolve and replace constant values
        for expr in tree_list[0]:
            for i, x in enumerate(expr):
                if x in const_values.keys():
                    expr[i] = const_values[x]
        
        # Now we check for variables consisting only of constants
        # We replace them with their result
        # And we keep bubbling until none need to be replaced

        # Create a constant list of variables
        variables_list = [expr[0] for expr in tree_list[1]]

        keep_going = True
        while keep_going:
            # Assume we are not going to keep going
            keep_going = False

            # Create a dictionary for the consts found
            replace_consts: dict = {}

            # For every expression
            for expr in tree_list[0]:
                # Check if a is a constant int
                aConst = expr[3] not in variables_list and str(expr[3]).isnumeric()

                # Check if b is a constant int
                bConst = expr[4] not in variables_list and str(expr[4]).isnumeric()

                # Check if both are constant ints
                bthConst = aConst and bConst

                # If both are constant integers
                if bthConst:
                    # Perform the expression on them

                    # Get the expression
                    x = expr[2]

                    # Default value to 0
                    val = 0

                    # Check if this is an operator
                    if self.is_token(x):
                        # If it is, calculate
                        val = self.tokens[x][1](
                            int(expr[3]), # A
                            int(expr[4]) # B
                        )
                    else:
                        # If not, just skip
                        continue
                    
                    # And add to replace_consts
                    replace_consts[expr[1]] = str(val)

            # Now strip all const declarations
            # For every expression in tree_list
            for i,expr in enumerate(tree_list[0]):
                # If it is a constant
                if expr[1] in replace_consts.keys():
                    # Delete
                    del tree_list[0][i]
            
            # Now replace all constant references
            # For every expression
            for expr in tree_list[0]:
                # For every part of the expression
                for i, x in enumerate(expr):
                    # If this part is a const and is not a declaration
                    if x in replace_consts.keys() and i != 1:
                        # Make sure that we keep going
                        keep_going = True
                        # And replace it
                        expr[i] = replace_consts[x]
        

        # Now all unneeded variables have been removed
        # or replaced

        # Renumber all of the elements
        # Lets create a dictionary of references to renumber
        renumDict: dict = {}
        for i,expr in enumerate(tree_list[0]):
            renumDict[expr[1]] = f"{namespace}_{i}"

        # Now lets replace these renumbers
        for expr in tree_list[0]:
            for i,x in enumerate(expr):
                if x in renumDict.keys():
                    expr[i] = renumDict[x]

        # Return treelist
        return tree_list

    def sort_tree_list(self, tree_list: list[list[list]], namespace: str = "base") -> list[list[list]]:
        # Make sure that the values are properly sorted
        # Make sure that they are as close to their first reference
        # as possible

        # Iterate over the tree_list
        for _ in tree_list[0]:
            # And iterate over it again
            for i, expr in enumerate(tree_list[0]):
                # Find first reference
                # By default it is i
                firstReference = i
                # Iterate over the treelist again
                for j, ex in enumerate(tree_list[0]):
                    # If it is in this expression, but is not this expression
                    if expr[1] in ex and expr[1] != ex[1]:
                        # It is the first reference
                        # So set
                        firstReference = j
                        # And break
                        break
                # Now we want to move this next to the first reference
                # So pop it
                popped = tree_list[0].pop(i)
                # And insert
                tree_list[0].insert(firstReference, popped)
        
        # Renumber all of the elements
        # Lets create a dictionary of references to renumber
        renumDict: dict = {}
        for i,expr in enumerate(tree_list[0]):
            renumDict[expr[1]] = f"{namespace}_{i}"

        # Now lets replace these renumbers
        for expr in tree_list[0]:
            for i,x in enumerate(expr):
                if x in renumDict.keys():
                    expr[i] = renumDict[x]


        # Return tree_list
        return tree_list
    
    def parse(self, expr: str, namespace: str = "base") -> ParseResult:
        """
            Parse the expr to a result

            - expr [str]
                Input expression

            - namespace [str]
                The namespace to use for creating variables
        """

        # Convert infix to tree
        tree = self.infix_to_tree(expr)

        # Convert tree to list
        tree_list = self._tree_to_list(tree, tree[0], [[],[]], namespace)

        if self.optimize:
            # If we should optimize, do that now
            tree_list = self.optimize_tree_list(tree_list, namespace)
        
        if self.sort:
            # If we should sort it, do that now as well
            tree_list = self.sort_tree_list(tree_list, namespace)
        
        # Lets generate the result
        results = ParseResult()

        # Set the tree list
        results.tree_list = tree_list[0]

        # Set the infix value
        results.infix = expr
        
        # Generate and set the prefix value
        results.prefix = self.infix_to_prefix(expr)

        # Generate and set the postfix value
        results.postfix = self.infix_to_postfix(expr)

        # Set the tree value
        results.tree = tree
        # Return results
        return results