#!/usr/bin/env python3

import argparse
import sys
import os

from src import decorateindenter

def error(reason):
    print("ERROR: {}".format(reason), file=sys.stderr)


def main(args):
    streamMode = (args.file is sys.stdin)

    if streamMode:
        indBuffer = []
        indString = ""

        try:
            while 1:
                indBuffer.append(input())
        
        except KeyboardInterrupt:
            print()
            return 1

        except EOFError:
            if indBuffer:
                indString = "\n".join(indBuffer)
            else:
                return 0

        toIndent = indString

    else:
        try:
            toIndent = open(args.file).read()

        except IOError:
            error("\"{}\" does not exist".format(args.file) )
            return 1

    indenter = decorateindenter.DecorateIndenter(indentWidth=args.space,
                                                 colonUnindent=args.colon,
                                                 changeLines=args.blank)

    indented = indenter.processText(toIndent)

    if args.dryrun or streamMode:
        print(indented)

    else:
        indentedFile = open(args.file, "w")
        indentedFile.write(indented)
        indentedFile.close()

    return 0


if __name__ == "__main__":

    argp = argparse.ArgumentParser("decindent")

    argp.add_argument("file", default=sys.stdin,  nargs="?", help="the file to indent (defaults to stdin)")
    argp.add_argument("-b", "--blank",  action="store_false", default=1, help="don't add or remove blank lines")
    argp.add_argument("-c", "--colon",  default=2, help="how far to unindent on a colon")
    argp.add_argument("-d", "--dryrun", action="store_true", default=0, help="don't change anything")
    argp.add_argument("-s", "--space",  default=4, help="the amount of spaces to indent to")

    args = argp.parse_args()
    
    exit = main(args)
    
    if exit and isinstance(exit, int):
        sys.exit(exit)
