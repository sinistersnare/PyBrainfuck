"""
brainfuck interpreter written in python
@author: Davis-Sinistersnare

"""

####################################################
"""
TODO:
-have REPL remember its history
-give REPL a '_' feature, like the Python REPL
-CLASSIFY

"""
####################################################


import sys
import argparse


def evaluate(code):
    """
    the evaluate method parses through the code 
    and executes it byte by byte
    """
    code = delcomments(code)
    bmap = makemap(code)
    
    cells,pos,codepos = [0],0,0
    while codepos < len(code):
        token = code[codepos]
        
        if token == '+':
            cells[pos] += 1
        elif token == '-':
            cells[pos] -= 1
        elif token == '>':
            pos+=1
            if pos >= len(cells):
                cells.append(0)

        elif token == '<':
            pos = 0 if pos <=0 else pos - 1
        elif token == '.':
            #print cells[pos]
            sys.stdout.write(chr(cells[pos]))
        elif token == ',':
            try:
                cells[pos] = ord(raw_input()[0])
            except IndexError:
                cells[pos] = 0
        elif token == '[' and cells[pos] == 0:
            codepos = bmap[codepos]     
            codepos = bmap[codepos]
            
        elif token == ']' and cells[pos] != 0:
            codepos = bmap[codepos]
        else:
            pass #anything else doesnt matter
        
        codepos += 1
    print
    
def delcomments(code):
    """
    this removes all characters not in the token directory.
    """
    return filter(lambda x: x in ['+','-','<','>',',','.','[',']'], code)
    
def makemap(code):
    """
    This makes a map of the left and right braces, usd for loops
    """
    bmap = {}
    lbmap=[]
    for pos, val in enumerate(code):
        if val == '[':
            lbmap.append(pos)
        if val == ']':
            popd = lbmap.pop()
            bmap[popd] = pos
            bmap[pos] = popd
    return bmap

            
def main():
    """
    starts the execution of code
    """
    
    repl()
    print
    
def repl(prompt="bf>"):
    while True:
        evaluate(raw_input(prompt))
        print


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f","--file",help="Specifies a file for use.")
    group.add_argument("-r","--repl",help="uses a repl. argument will be prompt empty uses default")
    
    args = parser.parse_args()

    if args.file:
        evaluate(open(args.file).read())
    elif args.repl:
        repl(args.file)
    else:
        repl()
    