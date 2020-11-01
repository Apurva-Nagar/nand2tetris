'''
-------------------------------------------------------------------------------------------------
Class - JackTokenizer (API)
-------------------------------------------------------------------------------------------------
Constructor(INPUT FILE):
	RETURN:
		NONE
	1) Opens the input .jack file and gets ready to tokenize it.

hasMoreTokens():
	RETURN:
		boolean
	1) Check if there are more tokens in the input.

advance():
	RETURN:
		NONE
	1) Gets the next token from input and makes it the current input.
	2) Call only if hasMoreTokens is True.
	3) Initially there is no current token.

tokenType():
	RETURN:
		KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
	1) Returns the type of the current token as a constant.

keyword():
	RETURN:
		CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN, CHAR, VOID, VAR, 
		STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS
	1) Returns the keyword which is in the current token as a constant.
	2) Should be called only if tokenType() is KEYWORD.

symbol():
	RETURN:
		char
	1) Returns the character which is in the current token.
	2) Should be called only if tokenType() is SYMBOL.

identifier():
	RETURN:
		string
	1) Returns the identifier which is in the current token.
	2) Should be called only if tokenType() is IDENTIFIER.

intVal():
	RETURN:
		int
	1) Returns the integer value of the current token.
	2) Should be called only if tokenType() is INT_CONST.

stringVal():
	RETURN:
		string
	1) Returns the string value of the current token without double quotes.
	2) Should be called only if tokenType() is STRING_CONST.
'''

class JackTokenizer:
	KEYWORDS = ['class', 'constructor', 'function', 'method', 'field', \
        		'static', 'var', 'int', 'char', 'boolean', 'void', 'true', \
        		'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', \
        		'return']

	SYMBOLS = ['(', ')', '[', ']', '{', '}', ',', ';', '=', '.', '+', '-', '*', \
		 	   '/', '&', '|', '~', '<', '>', '&lt;', '&gt;', '&quot;', '&amp;']

	WHITESPACES = [' ', '', '\n', '\t']

	COMMENTS = ['/', '*']

	XML_SYMBOL = {
		'<': '&lt;',
        '>': '&gt;',
        '\"': '&quot;',
        '&': '&amp;'
    }

	def __init__(self, source):
		self.file = open(source, "r")
		self.file.seek(0, 2)
		self.EOF = self.file.tell()
		self.file.seek(0, 0)
		self.nextToken = True
		self.currentToken = ''


	def hasMoreTokens(self):
		if self.file.tell() == self.EOF:
			self.nextToken = False
		return self.nextToken


	def advance(self):
		token = ''
		current_char = self.file.read(1)
		self.hasMoreTokens()

		while (current_char in self.WHITESPACES or current_char in self.COMMENTS) and self.hasMoreTokens():
			if current_char in self.WHITESPACES:
				current_char = self.file.read(1)
			if current_char in self.COMMENTS:
				last_pos = self.file.tell()
				char_LL2 = self.file.read(2)
				if self.isComment(current_char, char_LL2):
					self.file.readline()
					current_char = self.file.read(1)
				else:
					self.file.seek(last_pos)
					break

		while self.hasMoreTokens() and not (current_char==' ' or current_char=='\n'):
			if current_char in self.SYMBOLS:
				if token == '':
					token += current_char
					self.hasMoreTokens()
					break
				else:
					self.file.seek(last_pos)
					self.hasMoreTokens()
					break
			elif current_char == '\"':
				current_char = self.file.read(1)
				token += current_char
				while not current_char == '\"':
					current_char = self.file.read(1)
					token += current_char
					self.hasMoreTokens()
				break

			token += current_char
			last_pos = self.file.tell()
			current_char = self.file.read(1)
			self.hasMoreTokens()			

		if token.strip() in self.XML_SYMBOL:
			self.currentToken = self.XML_SYMBOL[token.strip()]
		else:	
			self.currentToken = token.strip()
	

	def isComment(self, current_char, char_LL2):
		single_line = char_LL2[0] == self.COMMENTS[0]
		multi_line = current_char == self.COMMENTS[0] and char_LL2 == '**'
		continued_comment = current_char == self.COMMENTS[1] and char_LL2[0] == ' ' and not (char_LL2[1].isdigit() or char_LL2[1] == '(')
		return single_line or multi_line or continued_comment


	def tokenType(self):
		if self.currentToken in self.KEYWORDS:
			return "keyword"
		elif self.currentToken in self.SYMBOLS:
			return "symbol"
		elif '"' in self.currentToken:
			return "stringConstant"
		elif self.currentToken.isdigit():
			return "integerConstant"
		else:
			return "identifier"


	def keyword(self):
		return self.currentToken

	def symbol(self):
		return self.currentToken

	def identifier(self):
		return self.currentToken

	def intVal(self):
		return int(self.currentToken)

	def stringVal(self):
		return self.currentToken.replace('"', '')


'''
def main():
	input_file = ''
	output_file = input_file.split('.')[0] + 'Tokens.xml' 
	tokenizer = JackTokenizer(input_file)
	output = open(output_file, 'w')
	output.write("<tokens>\n")
	while tokenizer.hasMoreTokens():
		tokenizer.advance()
		t_type = tokenizer.tokenType()
		token = tokenizer.currentToken
		if t_type == "stringConstant":
			token = tokenizer.stringVal()
		if not tokenizer.currentToken == '':
			output.write("<{}> {} </{}>\n".format(t_type, token, t_type))
	output.write("</tokens>")

if __name__ == "__main__":
	main()
'''