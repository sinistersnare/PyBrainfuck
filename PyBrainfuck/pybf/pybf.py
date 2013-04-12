#!/usr/bin/env python

"""
brainfuck interpreter written in python
@author: Davis-Sinistersnare
@version 1.1
"""

####################################################
"""
TODO:
-Catching an error when you increment a cell, then attempt to throw with unmatched braces...
-The above is really pissing me off, but ill push anyways.
-I HAVE NO IDEA!
-IDEA! i could add unit tests! what a good idea! good job sinistersnare!
-Its too late...time for bed!
"""
####################################################



import sys
import argparse


class BFE:
   """
   brainfuck extended!
   """

   def __init__(self,code='',repl=True):
      """ initializes all of the fields for use in the class """
      
      self.operators = ['+','-','<','>',',','.','[',']','/']
      self.code = filter(lambda x: x in self.operators, code)
      self.cells = [0]
      self.pos = 0
      self.codepos = 0
      self.prompt = "bf> "

   def makemap(self):
      """ builds a map for the loop to run through """
      bmap = {}
      lbmap = []
      
      #THIS DOESNT WORK
      
      
      for pos, val in enumerate(self.code):
         if val == '[':
            lbmap.append(pos)
            
         if val == ']':
            try:
            
               popd = lbmap.pop()
               bmap[popd] = pos
               bmap[pos] = popd
            except IndexError as e:
               #this works because the exception happens here, not at run time like the left bracket...
               #not sure if this should be frowned upon, but im doing it anyways!
               sys.stderr.write("BracketingError! \"]\" python IndexError")
               print e.value
      return bmap
    #end _makemap()
    
   def execute(self,repl=True,to_use=''):
      """
      runs through the code and executes it
      """
      #doing this so i dont have to write out `self` each time
      #woohoo i understand scopes :D
      
      if not to_use:
         code = self.code
      else:
         code = to_use
         
      codepos = self.codepos
      cells = self.cells
      pos = self.pos
      bmap = self.makemap()
      prevcode = ""
      
      while codepos < len(code):
         token = code[codepos]
     
         if token == '+':
            cells[pos] += 1
               
         elif token == '-':
            cells[pos] -= 1
               
         elif token == '>':
            pos += 1
            if pos >= len(cells):
               cells.append(0)

         elif token == '<':
            pos = 0 if pos <= 0 else pos - 1
                
         elif token == '.':
            sys.stdout.write(chr(cells[pos]))
                
         elif token == ',':
            try:
               cells[pos] = ord(raw_input()[0])
            except IndexError:
               cells[pos] = 0
                    
         elif token == '[' and cells[pos] == 0:
            try:
               codepos = bmap[codepos]
            except KeyError:
               sys.stderr.write("BracketingError! \"[\" python KeyError")
               
            
         elif token == ']' and cells[pos] != 0:
            try:
               codepos = bmap[codepos]
            except KeyError:
               #pretty certain this will never happen!
               sys.stderr.write("BracketingError! \"]\" python KeyError")
               
               
         elif token == '/':
            sys.stdout.write(str(cells[pos]))            
            
         else:
            pass  # anything else doesnt matter
            
         codepos += 1
      print
      return

   def repl(self):
      """
      the standard REPL for my bf interpreter, missing many key features (see TODO section)
      """
      while True:
         self.code = raw_input(self.prompt)
         self.execute()
   #end repl()
                
#end class BFE

def main(code="",repl=True,cmd=""):
   """
   starts the execution of code
   """
    
   bfe = BFE()
   if repl:
      if cmd:
         bfe.prompt = cmd
      bfe.repl()
   elif code:
      bfe.code=code
      bfe.execute(repl=False)
        
        
   print
    
    
    
if __name__ == '__main__': 
   parser = argparse.ArgumentParser()
   group = parser.add_mutually_exclusive_group()
   group.add_argument("-f","--file",help="Specifies a file for use.")
   group.add_argument("-r","--repl",help="uses a repl. argument will be prompt empty uses default")
    
   args = parser.parse_args()
    
   if args.file:
      main(code=open(args.file).read(),repl=False)
   elif args.repl:
      main(prompt=args.repl)
   else:
      main()
