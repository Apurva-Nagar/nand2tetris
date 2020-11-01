from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
import os, sys


def main():
	input_path = sys.argv[1]
	if os.path.isfile(input_path):
		tokenizer = JackTokenizer(input_path)
		compilation_engine_output = input_path.split('.')[0] + "CompilationEngine.xml"
		compilation_engine = CompilationEngine(tokenizer, compilation_engine_output)
		compilation_engine.compileClass()
		compilation_engine.closeFile()
	else:
		files = [file for file in os.listdir(input_path) if file.endswith(".jack")]

		for f in files:
			tokenizer = JackTokenizer(input_path + "/" + f)
			compilation_engine_output = input_path + "/" + f.split('.')[0] + "CompilationEngine.xml"
			compilation_engine = CompilationEngine(tokenizer, compilation_engine_output)
			compilation_engine.compileClass()
			compilation_engine.closeFile()

'''
def main():
	input_path = sys.argv[1]
	if os.path.isfile(input_path):
		tokenizer = JackTokenizer(input_path)
		tokenizer_output_file = input_path.split('.')[0] + "Tokens.xml"
		output = open(tokenizer_output_file, 'w')
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
		output.close()
	else:
		files = [file for file in os.listdir(input_path) if file.endswith(".jack")]
		
		for f in files:
			tokenizer = JackTokenizer(input_path + "/" + f)
			tokenizer_output_file = input_path + "/" + f.split('.')[0] + "Tokens.xml"
			output = open(tokenizer_output_file, 'w')
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
			output.close()
'''

if __name__ == "__main__":
	main()
