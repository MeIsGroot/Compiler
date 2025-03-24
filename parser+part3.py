# Since I implemented using Tokens and scanner first and then converted to reading a file,
# I found it easier to just put the token class in the Parser which was earlier in the scanner.
# This still works by reading tokens from a file, format for which is given in README.

class TokenType:
	SEMICOLON = 'SEMICOLON'  # ';'
	LBRACE = 'LBRACE'  # '{'
	RBRACE = 'RBRACE'  # '}'
	LBRACKET = 'LBRACKET'  # '['
	RBRACKET = 'RBRACKET'  # ']'
	NULL = 'NULL'  # 'null'
	FALSE = 'FALSE'  # 'false'
	TRUE = 'TRUE'  # 'true'
	COMMA = 'COMMA'  # ','
	COLON = 'COLON'  # ':'
	STRING = 'STRING'  # Tree leaves or node names
	NUMBER = 'NUMBER'  # Edge lengths or numeric values
	EOF = 'EOF'  # End of input


class Token:
	def __init__(self, type_, value=None):
		self.type = type_
		self.value = value
	
	def __repr__(self):
		if self.type == TokenType.STRING:
			return f"<STR, {self.value}>"
		elif self.type == TokenType.NUMBER:
			return f"<NUM, {self.value}>"
		elif self.type == TokenType.LBRACE:
			return "<{>"
		elif self.type == TokenType.RBRACE:
			return "<}>"
		elif self.type == TokenType.LBRACKET:
			return "<[>"
		elif self.type == TokenType.RBRACKET:
			return "<]>"
		elif self.type == TokenType.COMMA:
			return "<,>"
		elif self.type == TokenType.COLON:
			return "<:>"
		elif self.type == TokenType.TRUE:
			return "<true>"
		elif self.type == TokenType.FALSE:
			return "<false>"
		elif self.type == TokenType.NULL:
			return "<NULL>"
		elif self.type == TokenType.EOF:
			return "<EOF>"
		else:
			return f"<{self.type}>"


class Node:
	# Same implementation as example code
	def __init__(self, label=None, is_leaf=False):
		self.label = label
		self.children = []
		self.is_leaf = is_leaf
	
	def add_child(self, child):
		self.children.append(child)
	
	def print_tree(self, depth=0, outputfile=""):
		indent = " " * depth * 3
		
		if self.is_leaf:
			print(f"{indent}{self.label}")
			print(f"{indent}{self.label}", file=outputfile)
		else:
			print(f"{indent}{self.label}", file=outputfile)
			print(f"{indent}{self.label if self.label else '(none)'}")
			for child in self.children:
				child.print_tree(depth + 1, outputfile)

class SemanticError:
	def __init__(self, file):
		# The output file
		self.file = file
	
	def log(self, message):
		# Print to file and to console
		print(message)
		print(message, file=self.file)
	
	# Types of errors by level
	def TypeCError(self, message):
		self.log("Level C Semantic Error: " + message)
	
	def TypeBError(self, message):
		self.log("Level B Semantic Error: " + message)
	
	def TypeAError(self, message):
		self.log("Level A Semantic Error: " + message)
	
class ParserError:
	def __init__(self, token=None, error_type="", error="", file_name=""):
		
		self.token = token
		self.error = error
		self.file_name = file_name
		
		if error_type == "D":
			self.print_error_dict()
		elif error_type == "L":
			self.print_error_list()
		elif error_type == "P":
			self.print_error_pair()
		elif error_type == "V":
			self.print_error_value()
		elif error_type == "F":
			self.print_error_file()
		elif error_type == "S":
			self.print_error_string()
		elif error_type == "N":
			self.print_error_number()
	
	def print_error_dict(self):
		print(f"Error trying to parse {self.token} in dictionary: {self.error}")
	
	def print_error_list(self):
		print(f"Error trying to parse {self.token} in list: {self.error}")
	
	def print_error_pair(self):
		print(f"Error trying to parse {self.token} in pair: {self.error}")
	
	def print_error_value(self):
		print(f"Error trying to parse {self.token} as value: {self.error}")
	
	def print_error_string(self):
		print(f"Error trying to parse {self.token} as string: {self.error}")
		
	def print_error_number(self):
		print(f"Error trying to parse {self.token} as number: {self.error}")
		
	def print_error_boolean(self):
		print(f"Error trying to parse {self.token} as boolean: {self.error}")
	
	def print_error_file(self):
		print(f"file: {self.file_name} might be empty")

# Reverse tokenization (Does what the __repr__ in TokenType does but in reverse
def tokenize(line):
	line = line.strip()
	if line == "<{>":
		# Remove the angular brackets
		return [Token(TokenType.LBRACE)]
	elif line == "<}>":
		return [Token(TokenType.RBRACE)]
	elif line == "<[>":
		return [Token(TokenType.LBRACKET)]
	elif line == "<]>":
		return [Token(TokenType.RBRACKET)]
	elif line == "<,>":
		return [Token(TokenType.COMMA)]
	elif line == "<:>":
		return [Token(TokenType.COLON)]
	elif line == "<true>":
		return [Token(TokenType.TRUE)]
	elif line == "<false>":
		return [Token(TokenType.FALSE)]
	elif line == "<NULL>":
		return [Token(TokenType.NULL)]
	elif line == "<EOF>":
		return [Token(TokenType.EOF)]
	elif "STR, " in line:
		line = line[6:-1]
		return [Token(TokenType.STRING, line)]
	elif "NUM, " in line:
		line = line[6:-1]
		return [Token(TokenType.NUMBER, line)]
	elif line == "\n" or line == "\t" or line.isspace() or line == "<\'>" or line == "<\">":
		# Skip if space or quotation
		return " "
	else:
		# This is assumed to not happen during testing since input should have correct tokens
		# so just raise error and stop parsing if unknown token detected for now
		raise Exception("Unknown type of Token: " + line)


class Parser:
	def __init__(self, file_name=""):
		# Setting up error file
		self.semanticError = SemanticError(open(file_name[0:-4] + "_errors.txt", "w"))
		self.current_token = None
		self.file_name = file_name
		self.file = open(file_name, "r")
		self.index = 0
		# The tokens from token file
		self.tokenStream = self.init_tokens()
	
	def init_tokens(self):
		tokens = []
		for line in self.file:
			if line is not None and line != '\n':
				tokens.extend(tokenize(line))
		return tokens
	
	def get_next_token(self):
		if self.index >= len(self.tokenStream):
			return Token(TokenType.EOF, "<EOF>")
		self.current_token = self.tokenStream[self.index]
		self.index += 1
	
	def eat(self, token_type):
		# Consumes a token if it matches the expected type.
		if self.current_token.type == token_type:
			self.get_next_token()
		# Edge case where token isn't same as what is expected, should not happen after error detection
		else:
			raise Exception(f"Expected token {token_type}, got {self.current_token.type}")
	
	def parse(self):
		# Starts the parsing process by fetching the first token and calling the first grammar rule.
		self.get_next_token()
		return self.value()
	
	def value(self):
		# Start a node with label set to value since this is the root of parse tree
		node = Node(label="value")
		# Check for what the token type is and perform operations accordingly
		if self.current_token is None:
			return node
		# If token is not none, then it can only be one of the following if syntax is correct
		elif self.current_token is not None:
			if self.current_token.type == TokenType.NUMBER:
				node.add_child(self.number())
			elif self.current_token.type == TokenType.STRING:
				node.add_child(self.string())
			elif self.current_token.type == TokenType.LBRACE:
				return self.dict()
			elif self.current_token.type == TokenType.LBRACKET:
				return self.list()
			elif self.current_token.type == TokenType.TRUE:
				node.add_child(self.true())
			elif self.current_token.type == TokenType.FALSE:
				node.add_child(self.false())
			elif self.current_token.type == TokenType.NULL:
				node.add_child(self.null())
			elif self.current_token.type == TokenType.EOF:
				return node
			else:
				ParserError(self.current_token, "V", f"Unexpected Token at position {self.index}: {self.current_token}. Datatype should start with opening brackets or should be a terminal")
		else:
			ParserError(self.current_token,"F", "Unexpected error", self.file_name)
		return node
	
	def dict(self):
		# Parsing dict: "{" pair (", " pair)* "}"
		node = Node(label="dict")
		
		# First LBRACE is read
		node.add_child(Node(label="{"))
		self.eat(TokenType.LBRACE)
		
		# Then you read a pair
		pair = self.pair()
		node.add_child(pair)
		
		if self.current_token.type != TokenType.COMMA and self.current_token.type != TokenType.RBRACE:
			ParserError(self.current_token, "D", f"Missing <,> at {self.index} in Token Stream or unexpected token: {self.current_token}")
		
		# Continue reading pairs until no more input(Last comma is read)
		while self.current_token.type == TokenType.COMMA:
			node.add_child(Node(label=","))
			if self.current_token.type == TokenType.COMMA:
				self.eat(TokenType.COMMA)
			else:
				# Error should never happen because of while loop conditions but just in case
				ParserError(self.current_token, "D", f"<,> Missing at position {self.index} in Token Stream or unexpected token: {self.current_token}")
			pair = self.pair()
			node.add_child(pair)
		
		# Finish with RBRACE and error correction
		if self.current_token.type == TokenType.RBRACE:
			self.eat(TokenType.RBRACE)
		else:
			ParserError(self.current_token, "D", "Missing <}> " + f"at position {self.index} in Token Stream or unexpected token: {self.current_token}")
		node.add_child(Node(label="}"))
		return node
	
	def list(self):
		# Parsing list: "[" value (", " value)* "]"
		node = Node(label="list")
		all_values = []
		
		# Start with LBRACKET
		node.add_child(Node(label="["))
		self.eat(TokenType.LBRACKET)
		
		# Add first value into list
		value = self.value()
		all_values.append(value)
		node.add_child(value)
		
		if self.current_token.type != TokenType.COMMA and self.current_token.type != TokenType.RBRACKET:
			ParserError(self.current_token, "L", f"Missing <,> at position {self.index} in Token Stream or unexpected token: {self.current_token}")
		
		# Similar to Dictionary, read until commas finish and add all values read
		while self.current_token.type == TokenType.COMMA:
			node.add_child(Node(label=","))
			if self.current_token.type == TokenType.COMMA:
				self.eat(TokenType.COMMA)
			else:
				# Error should never happen because of while loop conditions but just in case
				ParserError(self.current_token, "L", f"<,> Missing at position {self.index} in Token Stream or unexpected token: {self.current_token}")
			value = self.value()
			all_values.append(value)
			node.add_child(value)
		
		# Finish with RBRACKET and error correction
		if self.current_token.type == TokenType.RBRACKET:
			self.eat(TokenType.RBRACKET)
		else:
			ParserError(self.current_token, "L", "<]> " + f"Missing at position {self.index} in Token Stream or unexpected token: {self.current_token}")
		node.add_child(Node(label="]"))
		return node
	
	def pair(self):
		# Parsing pair: STRING " : " value
		node = Node(label="pair")
		
		# Get first string
		key = self.string("p")
		node.add_child(key)
		node.add_child(Node(label=":"))
		
		if self.current_token.type == TokenType.COLON:
			self.eat(TokenType.COLON)
		else:
			ParserError(self.current_token, "P", f"<:> missing at {self.index} in Token Stream or unexpected token: {self.current_token}")
		
		# Get second value
		value = self.value()
		node.add_child(value)
		
		return node
	
	# Parsing Terminals (leaves of the tree)
	def string(self, r=""):
		# Parsing a STRING while checking for errors
		self.checkReservedKeys(self.current_token.value, "A")
		if r == "p":
			# We are checking for pairs so do specific things
			value = self.current_token.value
			self.checkValidPair(value)
			self.checkReservedKeys(value)
			node = Node(label="STRING: " + str(value), is_leaf=True)
			# If current token is not a string, log error
			if self.current_token.type == TokenType.STRING:
				self.eat(TokenType.STRING)
			else:
				self.semanticError.TypeBError(f"Type 4 at {self.current_token}: Reserved Words as Dictionary Key")
				self.eat(self.current_token.type)
			return node
		else:
			value = self.current_token.value
			#Should never happen but in case this method is called for a type other than String
			if self.current_token.type == TokenType.STRING:
				node = Node(label="STRING: " + value, is_leaf=True)
				self.eat(TokenType.STRING)
				return node
			else:
				ParserError(self.current_token, "S", f"Unexpected Token at {self.index}: {self.current_token}")
				self.eat(self.current_token.type)
				return Node("Invalid String: " + str(value), is_leaf=True)
	
	def number(self):
		# Parsing Numbers(Both Integer and Float)
		value = self.current_token.value
		if "." in value:
			# Check for Float format
			self.checkValidDecimal()
			# Should never happen but in case this method is called for a type other than String
			if self.current_token.type == TokenType.NUMBER:
				node = Node(label="NUMBER: " + str(value), is_leaf=True)
				self.eat(TokenType.NUMBER)
				return node
			else:
				ParserError(self.current_token, "N", f"Unexpected Token at {self.index}: {self.current_token}")
				self.eat(self.current_token.type)
				return Node(label="INVALID NUMBER: " + str(value), is_leaf=True)
		else:
			# Check for Int format
			self.checkValidInteger()
			# Should never happen but in case this method is called for a type other than String
			if self.current_token.type == TokenType.NUMBER:
				node = Node(label="NUMBER: " + str(value), is_leaf=True)
				self.eat(TokenType.NUMBER)
				return node
			else:
				ParserError(self.current_token, "N", f"Unexpected Token at {self.index}: {self.current_token}")
				self.eat(self.current_token.type)
				return Node(label="INVALID NUMBER: " + str(value), is_leaf=True)
		
	
	def true(self):
		# Parsing true boolean
		if self.current_token.type == TokenType.TRUE:
			self.eat(TokenType.TRUE)
			return Node(label="BOOLEAN: TRUE", is_leaf=True)
		else:
			ParserError(self.current_token, "B", f"Expected <true>, got: {self.current_token}")
			value = self.current_token.value
			self.eat(self.current_token.type)
			return Node(label="Invalid Boolean: " + str(value), is_leaf=True)
			
	
	def false(self):
		# Parsing false boolean
		if self.current_token.type == TokenType.FALSE:
			self.eat(TokenType.FALSE)
			return Node(label="BOOLEAN: FALSE", is_leaf=True)
		else:
			ParserError(self.current_token, "B", f"Expected <false>, got: {self.current_token}")
			value = self.current_token.value
			self.eat(self.current_token.type)
			return Node(label="Invalid Boolean: " + str(value), is_leaf=True)
	
	def null(self):
		# Parsing null "boolean"
		if self.current_token.type == TokenType.NULL:
			self.eat(TokenType.NULL)
			return Node(label="BOOLEAN: NULL", is_leaf=True)
		else:
			ParserError(self.current_token, "B", f"Expected <null>, got: {self.current_token}")
			value = self.current_token.value
			self.eat(self.current_token.type)
			return Node(label="Invalid Boolean: " + str(value), is_leaf=True)
	
	#All the methods to check for validity or throw errors for Part 3
	def checkValidDecimal(self):
		Num = self.current_token.value.split(".")
		if len(Num[1]) <= 0 or len(Num[0]) <= 0:
			self.semanticError.TypeCError(f"Type 1 at {self.current_token}: Invalid Decimal Numbers")
			return False
		else:
			return True

	def checkValidPair(self, Key):
		if Key is None or Key.strip() == "" or Key == "\"\"":
			self.semanticError.TypeCError(f"Type 2 at {self.current_token}: Empty Key")
			return False
		else:
			return True

	def checkValidInteger(self):
		if self.current_token.value[0] in ["0", "+"]:
			self.semanticError.TypeBError(f"Type 3 at {self.current_token}: Invalid Numbers")

	def checkReservedKeys(self, Key, Type="B"):
		if Type == "B":
			if Key in ["\"false\"", "\"true\"", "\"null\"", "false", "true", "NULL"]:
				self.semanticError.TypeBError(f"Type 4 at {self.current_token}: Reserved Words as Dictionary Key")
				return False
		else:
			if Key in ["\"false\"", "\"true\"", "\"null\"", "false", "true", "NULL"]:
				self.semanticError.TypeAError(f"Type 7 at {self.current_token}: Reserved Words as Strings")
				return False
		return True

	def checkConsistentType(self, valueNodes):
		type = valueNodes.pop(0).children.pop(0).label
		while valueNodes:
			node = valueNodes.pop(0).children.pop(0)
			value = node.label[0:3]
			if type[0:3] != value:
				# Basically just check first three letters of label, which should contain (NUMBERS), (STRING) or another value. If they don't match then problem
				self.semanticError.TypeAError(f"Type 6 at <{node.label}> (Expected Type: {type[:3]}): Inconsistent Types for List Elements")
				return False
		return True

# Main
if __name__ == "__main__":
	for i in range(1, 4):
		file_name = "test_input_parser_" + str(i) + ".txt"
		print("Parsing file: " + file_name)
		theParser = Parser(file_name)
		theJSONOutput = theParser.parse()
		outputFile = open(file_name[0:4] + "_AST_output_" + str(i) + ".txt", "w")
		theJSONOutput.print_tree(outputfile=outputFile)
		print("------ File " + file_name + " Parsed!------\n")