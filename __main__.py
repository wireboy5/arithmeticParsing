import arithmetic_parsing
import argparse


"""
    Basic program to test arithmetic_parsing
"""



parser = argparse.ArgumentParser(description='Parse an equation')
parser.add_argument('equation', help='the input equation')
parser.add_argument('-o','--output', type = str, default = "tree",
    help='The output format. json, list, or tree',
    choices = ["json","list","tree"]
)

parser.add_argument('--nosort', action="store_true",
    default = False,
    help = "Disables sorting the output (Only if list)"
)

parser.add_argument('--nooptimize', action="store_true",
    default = False,
    help = "Disables optimizing the output (Only if list)"
)
parser.add_argument('-ns','--namespace', type = str, default = "base",
    help='The namespace of the variables in list format'
)


args = parser.parse_args()


# Create parser with default values
parser = arithmetic_parsing.Parser(
    optimize= not args.nooptimize,
    sort = not args.nosort
)

parsed = parser.parse(args.equation, args.namespace)

if args.output == "tree":
    print(parsed)
elif args.output == "json":
    print(parsed.as_json())
elif args.output == "list":
    print(parsed.as_list())



