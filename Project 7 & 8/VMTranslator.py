'''
Proposed Project Design: 

Parser:
1) Constructor - Opens the input file 

2) hasMoreCommands - Are there more commands?

3) advance - reads the next command from input and makes it the current command. Called only if hasMoreCommands is True. Initially there is no current command.

4) commandType - Returns a constant representing the type of the current command.
C_ARITHMETIC is retured for all the arithmetic commands.

5) arg1 - Returns first argument of the current command. 

6) arg2 - Returns second argument of the command

NEW:
1) Handle parsing of VM commands:
	goto
	if-goto
	label
	call
	function
	return

---------------------

CodeWriter:
1) Constructor - Opens the outputfile

2) writeArithmetic  - Writes the assembly code to implement arithmetic command

3) writePushPop - Writes the assembly code to implement Push/Pop command

4) Close - Closes the output file

NEW:
1) setFileName - Informs the CW that the translation of a new VM file has started. Called by main.
2) writeInit - Writes the assembly instruction that effect the bootstrap code that initializes the VM. 
				This code must be placed at the beginning of the generated *.asm file.
3) writeLabel - Assembly for label command
4) writeGoto - Assembly for goto command
5) writeIf - Assembly for if-goto command
6) writeFunction - Assembly for function command
7) writeCall - Assembly for call command
8) write Return - Assembly for return command
----------------------

Main:
Gets input file. Goes through the file all the while calling Parser and CodeWriter

NEW:
1) Input: File or directory
2) Ouput: filename.asm or directoryname.asm
'''


import os, sys

class Parser:
	def __init__(self, source):
		self.file = open(source, "r")
		self.command = []
		self.file.seek(0, 2)
		self.EOF = self.file.tell()
		self.file.seek(0, 0)
		self.nextLine = True

		self.command_type = {
			"push"		:	"C_PUSH",
			"pop"		:	"C_POP",
			"add"		: 	"C_ARITHMETIC",
			"sub"		: 	"C_ARITHMETIC",
			"neg"		: 	"C_ARITHMETIC",
			"eq"		: 	"C_ARITHMETIC",
			"gt"		: 	"C_ARITHMETIC",
			"lt"		: 	"C_ARITHMETIC",
			"and"		: 	"C_ARITHMETIC",
			"or"		: 	"C_ARITHMETIC",
			"not"		: 	"C_ARITHMETIC",
			"label"		: 	"C_LABEL",
			"goto"		: 	"C_GOTO",
			"if-goto"	: 	"C_IF",
			"function"	: 	"C_FUNCTION",
			"call"		: 	"C_CALL",
			"return"	: 	"C_RETURN",
		}

	def hasMoreCommands(self):
		return self.nextLine

	def advance(self):
		current_line = ''
		current_line = self.file.readline()
		if self.file.tell() == self.EOF:
			self.nextLine = False

		if current_line.strip()[0:2] == "//" or current_line.strip()[:] == '':
			self.command = []
		else:
			self.command = current_line.strip().split()

	def commandType(self):
		return self.command_type.get(self.command[0])

	def arg1(self):
		return self.command[1]

	def arg2(self):
		return self.command[2]


class CodeWriter:
	def __init__(self, dest):
		self.file = open(dest, "w")
		self.label_counter = 0
		self.current_file = None
		self.static_label = self.current_file


	def setFileName(self, file_name):
		self.current_file = file_name[:-3]
		self.file.write("//NEW FILE: " + self.current_file + "\n")
		self.static_label = self.current_file


	def writeInit(self):
		self.file.write("//INIT\n")
		assembly = ""
		assembly += "@256\n"
		assembly += "D=A\n"
		assembly += "@SP\n"
		assembly += "M=D\n"
		self.file.write(assembly)
		self.writeCall("Sys.init", 0)


	def writeLabel(self, label):
		self.file.write("//LABEL\n")
		assembly = ""
		assembly += "(" + self.current_file + "$" + label + ")\n"
		self.file.write(assembly + "\n")


	def writeGoto(self, label):
		self.file.write("//GOTO\n")
		assembly = ""
		assembly += "@" + self.current_file + "$" + label + "\n"
		assembly += "0;JMP\n"
		self.file.write(assembly + "\n")


	def writeIf(self, label):
		self.file.write("//IF-GOTO\n")
		assembly = ""
		assembly += "@SP\n"
		assembly += "A=M-1\n"
		assembly += "D=M\n"
		assembly += "@SP\n"
		assembly += "M=M-1\n"
		assembly += "@" + self.current_file + "$" + label + "\n"
		assembly += "D;JNE\n"
		self.file.write(assembly + "\n")


	def writeFunction(self, function_name, numVars):
		self.file.write("//FUNCTION: " + function_name + "\n")
		assembly = ""
		assembly += "(" + function_name + ")\n"

		for i in range(int(numVars)):
			assembly += "D=0\n"
			assembly += "@SP\n"
			assembly += "A=M\n"
			assembly += "M=D\n"
			assembly += "@SP\n"
			assembly += "M=M+1\n"

		self.file.write(assembly + "\n")


	def writeCall(self, function_name, numArgs):
		self.file.write("//CALL: " + function_name + "\n")
		return_address = function_name + "RETURN" + str(self.label_counter)
		self.label_counter += 1
		
		#PUSH RETURN ADDRESS
		assembly = ""
		assembly += "@" + return_address + "\n"
		assembly += "D=A\n"
		assembly += "@SP\n"
		assembly += "A=M\n"
		assembly += "M=D\n"
		assembly += "@SP\n"
		assembly += "M=M+1\n"

		#PUSH LCL, ARG, THIS, THAT
		for seg in ['@LCL\n', '@ARG\n', '@THIS\n', '@THAT\n']:
			assembly += seg
			assembly += "D=M\n"
			assembly += "@SP\n"
			assembly += "A=M\n"
			assembly += "M=D\n"
			assembly += "@SP\n"
			assembly += "M=M+1\n"

		#LCL = SP
		assembly += "@SP\n"
		assembly += "D=M\n"
		assembly += "@LCL\n"
		assembly += "M=D\n"

		#ARG = SP-n-5
		assembly += "@SP\n"
		assembly += "D=M\n"
		assembly += "@" + str(int(numArgs)+5) + "\n"
		assembly += "D=D-A\n"
		assembly += "@ARG\n"
		assembly += "M=D\n"

		#goto function
		assembly += "@" + function_name + "\n"
		assembly += "0;JMP\n"

		#return label
		assembly += "(" + return_address + ")\n"

		self.file.write(assembly + "\n")


	def writeReturn(self):
		self.file.write("//RETURN\n")
		assembly = ""

		#FRAME = LCL
		FRAME = "R13"
		assembly += "@LCL\n"
		assembly += "D=M\n"
		assembly += "@" + FRAME + "\n"
		assembly += "M=D\n"	

		#return_address = *(FRAME-5)
		RETURN = "R14"
		assembly += "@" + FRAME + "\n"
		assembly += "D=M\n"
		assembly += "@5\n"
		assembly += "D=D-A\n"
		assembly += "A=D\n"
		assembly += "D=M\n"
		assembly += "@" + RETURN + "\n"
		assembly += "M=D\n"

		#*ARG = POP()
		assembly += "@SP\n"
		assembly += "A=M-1\n"
		assembly += "D=M\n"
		assembly += "@SP\n"
		assembly += "M=M-1\n"
		assembly += "@ARG\n"
		assembly += "A=M\n"
		assembly += "M=D\n"

		#SP = ARG+1
		assembly += "@ARG\n"
		assembly += "D=M\n"
		assembly += "@SP\n"
		assembly += "M=D+1\n"

		index = 1
		for seg in ['@THAT\n', '@THIS\n', '@ARG\n', '@LCL\n']:
			assembly += "@" + FRAME + "\n"
			assembly += "D=M\n"
			assembly += "@" + str(index) + "\n"
			assembly += "D=D-A\n"
			assembly += "A=D\n"
			assembly += "D=M\n"
			assembly += seg
			assembly += "M=D\n"
			index += 1

		#GOTO RETURN
		assembly += "@" + RETURN + "\n"
		assembly += "A=M\n"
		assembly += "0;JMP\n"

		self.file.write(assembly + "\n")


	def writeArithmetic(self, command):
		assembly = ""
		self.file.write("//" + command + "\n")
		if command == "add":
			assembly += "@SP\n"		# SP
			assembly += "A=M-1\n"
			assembly += "D=M\n"		# D=First Number
			assembly += "A=A-1\n"	# M=Second Number
			assembly += "D=D+M\n" 	# Add the two numbers
			assembly += "M=D\n"		# Place sum in correct place
			assembly += "D=A+1\n"	# D=incremented pointer address
			assembly += "@SP\n"		
			assembly += "M=D\n" 	# Update SP value

		elif command == "sub":
			assembly += "@SP\n"	
			assembly += "A=M-1\n"
			assembly += "D=M\n"	
			assembly += "A=A-1\n"
			assembly += "D=M-D\n" 	
			assembly += "M=D\n"		
			assembly += "D=A+1\n"
			assembly += "@SP\n"		
			assembly += "M=D\n" 

		elif command == "eq":
			label_num = str(self.label_counter)
			self.label_counter += 1
			assembly += "@SP\n"		#SP
			assembly += "A=M-1\n"
			assembly += "D=M\n"
			assembly += "A=A-1\n"
			assembly += "D=D-M\n"
			assembly += "M=-1\n"	#Initially seet to true
			assembly += "@END" + label_num + "\n"
			assembly += "D;JEQ\n"	#If A-B=0 then jump to end
			assembly += "@SP\n"
			assembly += "A=M-1\n"
			assembly += "A=A-1\n"
			assembly += "M=0\n"		#Otherwise change to false
			assembly += "(END" + label_num + ")\n"
			assembly += "@SP\n"
			assembly += "M=M-1\n" 	#Reduce Pointer

		elif command == "lt":
			label_num = str(self.label_counter)
			self.label_counter += 1
			assembly += "@SP\n"		#SP
			assembly += "A=M-1\n"
			assembly += "D=M\n"
			assembly += "A=A-1\n"
			assembly += "D=M-D\n"
			assembly += "M=-1\n"	#Initially seet to true
			assembly += "@END" + label_num + "\n"
			assembly += "D;JLT\n"	#If A-B<0 then jump to end
			assembly += "@SP\n"
			assembly += "A=M-1\n"
			assembly += "A=A-1\n"
			assembly += "M=0\n"		#Otherwise change to false
			assembly += "(END" + label_num + ")\n"
			assembly += "@SP\n"
			assembly += "M=M-1\n" 	#Reduce Pointer

		elif command == "gt":
			label_num = str(self.label_counter)
			self.label_counter += 1
			assembly += "@SP\n"		#SP
			assembly += "A=M-1\n"
			assembly += "D=M\n"
			assembly += "A=A-1\n"
			assembly += "D=M-D\n"
			assembly += "M=-1\n"	#Initially seet to true
			assembly += "@END" + label_num + "\n"
			assembly += "D;JGT\n"	#If A-B<0 then jump to end
			assembly += "@SP\n"
			assembly += "A=M-1\n"
			assembly += "A=A-1\n"
			assembly += "M=0\n"		#Otherwise change to false
			assembly += "(END" + label_num + ")\n"
			assembly += "@SP\n"
			assembly += "M=M-1\n" 	#Reduce Pointer

		elif command == "neg":
			assembly += "@SP\n"
			assembly += "A=M-1\n"
			assembly += "M=-M\n"

		elif command == "and":
			assembly += "@SP\n"		
			assembly += "A=M-1\n"
			assembly += "D=M\n"
			assembly += "A=A-1\n"
			assembly += "M=M&D\n"
			assembly += "D=A+1\n"
			assembly += "@SP\n"
			assembly += "M=D\n"

		elif command == "or":
			assembly += "@SP\n"		
			assembly += "A=M-1\n"
			assembly += "D=M\n"
			assembly += "A=A-1\n"
			assembly += "M=M|D\n"
			assembly += "D=A+1\n"
			assembly += "@SP\n"
			assembly += "M=D\n"

		else:
			assembly += "@SP\n"
			assembly += "A=M-1\n"
			assembly += "M=!M\n"

		self.file.write(assembly + "\n")


	def writePushPop(self, command, segment, value):
		assembly = ""
		self.file.write("//" + command + " " + segment + " " + value + "\n")
		if command == "push":
			if segment == "constant":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@SP\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "M=M+1\n"

			elif segment == "local":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@LCL\n"
				assembly += "A=D+M\n"
				assembly += "D=M\n"
				assembly += "@SP\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "D=A+1\n"
				assembly += "@SP\n"
				assembly += "M=D\n"

			elif segment == "this":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@THIS\n"
				assembly += "A=D+M\n"
				assembly += "D=M\n"
				assembly += "@SP\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "D=A+1\n"
				assembly += "@SP\n"
				assembly += "M=D\n"

			elif segment == "that":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@THAT\n"
				assembly += "A=D+M\n"
				assembly += "D=M\n"
				assembly += "@SP\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "D=A+1\n"
				assembly += "@SP\n"
				assembly += "M=D\n"

			elif segment == "argument":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@ARG\n"
				assembly += "A=D+M\n"
				assembly += "D=M\n"
				assembly += "@SP\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "D=A+1\n"
				assembly += "@SP\n"
				assembly += "M=D\n"

			elif segment == "temp":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@5\n"
				assembly += "A=D+A\n"
				assembly += "D=M\n"
				assembly += "@SP\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "D=A+1\n"
				assembly += "@SP\n"
				assembly += "M=D\n"

			elif segment == "static":
				assembly += "@" + self.static_label + "." + value + "\n"
				assembly += "D=M\n"
				assembly += "@SP\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "M=M+1\n"

			elif segment == "pointer":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@3\n"
				assembly += "A=D+A\n"
				assembly += "D=M\n"
				assembly += "@SP\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "D=A+1\n"
				assembly += "@SP\n"
				assembly += "M=D\n"

		elif command == "pop":
			if segment == "local":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@LCL\n"
				assembly += "A=M\n"
				assembly += "D=D+A\n"
				assembly += "@R13\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=M\n"
				assembly += "M=0\n"
				assembly += "@R13\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=A\n"
				assembly += "@SP\n"
				assembly += "M=D\n"
				assembly += "@R13\n"
				assembly += "M=0\n"

			elif segment == "this":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@THIS\n"
				assembly += "A=M\n"
				assembly += "D=D+A\n"
				assembly += "@R13\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=M\n"
				assembly += "M=0\n"
				assembly += "@R13\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=A\n"
				assembly += "@SP\n"
				assembly += "M=D\n"
				assembly += "@R13\n"
				assembly += "M=0\n"

			elif segment == "that":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@THAT\n"
				assembly += "A=M\n"
				assembly += "D=D+A\n"
				assembly += "@R13\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=M\n"
				assembly += "M=0\n"
				assembly += "@R13\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=A\n"
				assembly += "@SP\n"
				assembly += "M=D\n"
				assembly += "@R13\n"
				assembly += "M=0\n"

			elif segment == "argument":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@ARG\n"
				assembly += "A=M\n"
				assembly += "D=D+A\n"
				assembly += "@R13\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=M\n"
				assembly += "M=0\n"
				assembly += "@R13\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=A\n"
				assembly += "@SP\n"
				assembly += "M=D\n"
				assembly += "@R13\n"
				assembly += "M=0\n"

			elif segment == "temp":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@5\n"
				assembly += "D=D+A\n"
				assembly += "@R13\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=M\n"
				assembly += "M=0\n"
				assembly += "@R13\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=A\n"
				assembly += "@SP\n"
				assembly += "M=D\n"
				assembly += "@R13\n"
				assembly += "M=0\n"

			elif segment == "static":
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=M\n"
				assembly += "@" + self.static_label + "." + value + "\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=A\n"
				assembly += "@SP\n"
				assembly += "M=D\n"

			elif segment == "pointer":
				assembly += "@" + value + "\n"
				assembly += "D=A\n"
				assembly += "@3\n"
				assembly += "D=D+A\n"
				assembly += "@R13\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=M\n"
				assembly += "M=0\n"
				assembly += "@R13\n"
				assembly += "A=M\n"
				assembly += "M=D\n"
				assembly += "@SP\n"
				assembly += "A=M-1\n"
				assembly += "D=A\n"
				assembly += "@SP\n"
				assembly += "M=D\n"
				assembly += "@R13\n"
				assembly += "M=0\n"

		self.file.write(assembly + "\n")

	def closeFile(self):
		self.file.close()


def main():
	input_path = sys.argv[1]
	if os.path.isfile(input_path):
		parser = Parser(input_path)
		output_file = input_path.replace(".vm", ".asm")
		translator = CodeWriter(output_file)
		name = output_file.split("/")[-1]
		translator.setFileName(name[:-1])
		#translator.writeInit()

		while parser.hasMoreCommands():
			parser.advance()
			if(len(parser.command)>0):
				command_type = parser.commandType()
				if command_type == "C_POP" or command_type == "C_PUSH":
					translator.writePushPop(parser.command[0], parser.arg1(), parser.arg2())
				elif command_type == "C_ARITHMETIC":
					translator.writeArithmetic(parser.command[0])
				elif command_type == "C_LABEL":
					translator.writeLabel(parser.arg1()) 
				elif command_type == "C_GOTO":
					translator.writeGoto(parser.arg1())
				elif command_type == "C_IF":
					translator.writeIf(parser.arg1())
				elif command_type == "C_FUNCTION":
					translator.writeFunction(parser.arg1(), parser.arg2())
				elif command_type == "C_CALL":
					translator.writeCall(parser.arg1(), parser.arg2())
				elif command_type == "C_RETURN":
					translator.writeReturn()
		translator.closeFile()

	else:
		files = [file for file in os.listdir(input_path) if file.endswith(".vm")]
		output_file = input_path + "/" + input_path.split("/")[-1] + ".asm"
		translator = CodeWriter(output_file)
		translator.writeInit()

		for f in files:
			parser = Parser(input_path + "/" + f)
			translator.setFileName(f)
			while parser.hasMoreCommands():
				parser.advance()
				if(len(parser.command)>0):
					command_type = parser.commandType()
					if command_type == "C_POP" or command_type == "C_PUSH":
						translator.writePushPop(parser.command[0], parser.arg1(), parser.arg2())
					elif command_type == "C_ARITHMETIC":
						translator.writeArithmetic(parser.command[0])
					elif command_type == "C_LABEL":
						translator.writeLabel(parser.arg1()) 
					elif command_type == "C_GOTO":
						translator.writeGoto(parser.arg1())
					elif command_type == "C_IF":
						translator.writeIf(parser.arg1())
					elif command_type == "C_FUNCTION":
						translator.writeFunction(parser.arg1(), parser.arg2())
					elif command_type == "C_CALL":
						translator.writeCall(parser.arg1(), parser.arg2())
					elif command_type == "C_RETURN":
						translator.writeReturn()

		translator.closeFile()


if __name__ == "__main__":
	main()







