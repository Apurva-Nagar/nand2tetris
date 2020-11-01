'''
-------------------------------------------------------------------------------------------------
Class - CompilationEngine (API)
-------------------------------------------------------------------------------------------------
Constructor(INPUT FILE, OUTPUT FILE):
	RETURN:
		NONE
	1) Creates a new CompilationEngine with the given input and output.
	2) The next routine called must be compileClass().

compileClass():
	RETURN:
		NONE
	1) Compiles a complete class.

compileClassVarDec():
	RETURN:
		NONE
	1) Compiles a static variable declaration or a field variable declaration.

compileSubroutineDec():
	RETURN:
		NONE
	1) Compiles a complete method, function, or constructor.

compileParameterList():
	RETURN:
		NONE
	1) Compiles a (possibly empty) parameter list.
	2) Does not handle the enclosing "()".

compileSubroutineBody():
	RETURN:
		NONE
	1) Compiles a subroutine's body.

compileVarDec():
	RETURN:
		NONE
	1) Compiles a var declaration.

compileStatements():
	RETURN:
		NONE
	1) Compiles a sequence of statements.
	2) Does not handle the enclosing "{}". 

compileLet():
	RETURN:
		NONE
	1) Compiles a let statement.

compileIf():
	RETURN:
		NONE
	1) Compiles an if statement, possibly with a trailing else clause.

compileWhile():
	RETURN:
		NONE
	1) Compiles a while statement.

compileDo():
	RETURN:
		NONE
	1) Compiles a do statement.

compileReturn():
	RETURN:
		NONE
	1) Compiles a return statement.

compileExpression():
	RETURN:
		NONE
	1) Compiles an expression.

compileTerm():
	RETURN:
		NONE
	1) Compiles a term.
	2) If the current token is an identifier, the routine must distinguish between a variable, an array entry or
	   or a subroutine call.
	3) A single look-ahead token which may be one of '[', '(', '.', suffices to distinguish between the above
	   possibilities.
	4) Any other token is not part of this term and should not be advanced over.

compileExpressionList():
	RETURN:
		NONE
	1) Compiles a (possibly empty) comma seperated list of expressions.
'''
import os, sys

class CompilationEngine:
	CLASS_VAR_DEC_TOKENS = ["static", "field"]
	SUBROUTINE_DEC_TOKENS = ["function", "method", "constructor"]

	def __init__(self, tokenizer, dest):
		self.tokenizer = tokenizer
		self.output_file = open(dest, 'w')

	def compileClass(self):
		self.output_file.write("<{}>\n".format('class'))
		self.tokenizer.advance()
		self.__eat(self.tokenizer.currentToken, 'class')
		self.compileCurrentToken()
		self.__eat(self.tokenizer.currentToken, '{')

		'''
		#Any Number of these
		while self.tokenizer.hasMoreTokens(): 
			if self.tokenizer.currentToken in self.CLASS_VAR_DEC_TOKENS:
				self.compileClassVarDec()
			if self.tokenizer.currentToken in self.SUBROUTINE_DEC_TOKENS:
				self.compileSubroutineDec()

		self.__eat(self.token.currentToken, '}')
		'''

		self.output_file.write("</{}>".format('class'))


	def compileClassVarDec(self):
		self.output_file.write("<{}>\n".format('classVarDec'))
		self.compileCurrentToken()

	def compileSubroutineDec(self):
		pass

	def compileParameterList(self):
		pass

	def compileSubroutineBody(self):
		pass

	def compileVarDec(self):
		pass

	def compileStatements(self):
		pass

	def compileLet(self):
		pass

	def compileWhile(self):
		pass

	def compileDo(self):
		pass

	def compileReturn(self):
		pass

	def compileExpression(self):
		pass

	def compileTerm(self):
		pass

	def compileExpressionTerm(self):
		pass

	def __eat(self, token, match_string):
		if(token != match_string):
			print('Error!')
			sys.exit()
		else:
			t_type = self.tokenizer.tokenType()
			self.output_file.write("<{}> {} </{}>\n".format(t_type, token, t_type))
			self.tokenizer.advance()

	def compileCurrentToken(self):
		t_type = self.tokenizer.tokenType()
		self.output_file.write("<{}> {} </{}>\n".format(t_type, self.tokenizer.currentToken, t_type))
		self.tokenizer.advance()

	def multiComparisonCheck(self, comparison_list, token):
		if token in comparison_list:
			t_type = self.tokenizer.tokenType()
			self.output_file.write("<{}> {} </{}>\n".format(t_type, token, t_type))
			self.tokenizer.advance()

	def closeFile(self):
		self.output_file.close()
