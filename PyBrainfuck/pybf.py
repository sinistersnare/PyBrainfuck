#!/usr/bin/env python

"""
brainfuck interpreter written in python
@author: Davis-Sinistersnare
@version 1.1
"""

####################################################
"""
TODO:
-pretty sure this is 100% broken, but am pushing it to mark a moment of progress!
-Catching an error when you increment a cell, then attempt to throw with unmatched braces...
-The above is really pissing me off, but ill push anyways.
-I HAVE NO IDEA!
-IDEA! i could add unit tests! what a good idea! good job sinistersnare!
-Its too late...time for bed! 
"""
####################################################


#import this,antigravity
import sys
import argparse


class BFE:
   """
   brainfuck extended!
   """

   def __init__(self,code='',repl=True):
      """ initializes all of the fields for use in the class """
      self.mapping = {'+':self._add, '-':self._sub, '<':self._inc, '>':self._dec, ',':self._input, '.':self._out, '[':self._lbrace, ']':self._rbrace, '/':self._cellval}
      self.operators = ['+','-','<','>',',','.','[',']','/']
      self.code = ""
      self.cells = [0]
      self.pos = 0
      self.codepos = 0
      self.prompt = "bf> "
      self.endof = ''
      self.bmap = {}
   def makemap(self):
      """ builds a map for the loop to run through """
      
      bmap = {}
      lbmap = []
      
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
               
      return bmap
    #end _makemap()
   
   def updatecode(self,newcode):
      self.code = filter(lambda x: x in self.operators,newcode)
   
   
   def _add(self):
      """adds one to the current cell"""
      
      cells = self.cells
      pos = self.pos
      
      if not cells[pos] >= 255: cells[pos] += 1
      
   
   def _sub(self):
      """subtracts one from the current cell"""
      
      cells = self.cells
      pos = self.pos
      
      if not cells[pos] <= 0: cells[pos] -= 1

   
   def _inc(self):
      """Increments the pointer position. Will add a 0 to the end of the list if it is maximized"""
      
      pos = self.pos
   
      pos += 1
      if pos >= len(cells): cells.append(0)
   
   def _dec(self):
      """Decrements the pointer position. will retain at 0 if already there"""
      
      pos = self.pos
      
      if not pos != 0: pos -= 1
   
   def _out(self):
      """outputs the ASCII value of the value at the position"""
      
      cells = self.cells
      pos = self.pos
      
      sys.stdout.write(chr(cells[pos]))
               
   def _input(self):
      """Reads from stdin, then writes the int value from ASCII into the grid"""
      
      cells = self.cells
      pos = self.pos
      try:
         rinput = raw_input()[0]
         ordinput = ord(rinput)
         if 0 < ordinput < 31: cells[pos] = 0 #0-31 are all null-like characters in ASCII
         else: cells[pos] = ordinput #if its not null-like, than put it into the cells
      except IndexError:
         cells[pos] = 0
 
   def _lbrace(self):
      """If the value of the current cell is 0, then go to the mapped right brace, otherwise, do nothing (go throught the loop) """
      cells = self.cells
      pos = self.pos
      bmap = self.bmap
      codepos = self.codepos
         
      if not cells[pos]: #is 0
         try:
            codepos = bmap[codepos]
         except KeyError:
            sys.stderr.write("BracketingError! \"[\" python KeyError")
                          
   def _rbrace(self):
      """If the value of the current cells is NOT zero, then it goes back to the mapped left brace to re-loop """
      cells = self.cells
      pos = self.pos
      bmap = self.bmap
      codepos = self.codepos
      
      if cells[pos]: #not 0
         try:
            codepos = bmap[codepos]
         except KeyError:
            #happens when there is a cell thats not 0
            sys.stderr.write("BracketingError! \"]\" python KeyError")            

   def _cellval(self):
      """My own little operator! This just prints the int value of the current cell """
      cells = self.cells
      pos = self.pos
      
      sys.stdout.write(str(cells[pos]))
   

   def execute(self,repl=True,to_use=''):
      """
      runs throught the code and executes it
      """
      
      if not to_use:
         code = self.code
      else:
         code = to_use
      code = self.updatecode(code)
      codepos = self.codepos
      cells = self.cells
      pos = self.pos
      bmap = self.makemap()
      funcs = self.mapping
      print code
      while codepos < len(code):
         token = code[codepos]
         
         if token not in funcs: print "TOKEN IS NOT IN FUNCS. WAT" #just in case
         funcs[token]()
         
         codepos += 1
         
      print
      return
         
   
   def repl(self):
      """
      the standard REPL for my bf interpreter, missing many key features (see TODO section)
      """
      while True:
         updatecode(raw_input(self.prompt))
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
      bfe.updatecode(code)
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
