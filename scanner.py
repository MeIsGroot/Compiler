# Token types
class TokenType:
	STRING = 'STRING'  # String datatype
	NUMBER = 'NUMBER'  # numeric datatype
	EOF = 'EOF'  # End of file(End of input)
	NULL = 'NULL'  # 'null'
	FALSE = 'false'  # 'false'
	TRUE = 'true'  # 'true'
	
	# Other types of tokens
	LBRACE = 'LBRACE'  # '{'
	RBRACE = 'RBRACE'  # '}'
	LBRACKET = 'LBRACKET'  # '['
	RBRACKET = 'RBRACKET'  # ']'
	COMMA = 'COMMA'  # ','
	COLON = 'COLON'  # ':'
	SEMICOLON = 'SEMICOLON'  # ';'


# Defining tokens
class Token:
	
	def __init__(self, type_, value=None):
		self.type = type_
		self.value = value
	
	def __repr__(self):
		# Recognize string, number, booleans and all other characters relevant in JSON
		if self.type == TokenType.STRING:
			return f"<STR, {self.value}>"
		elif self.type == TokenType.NUMBER:
			return f"<NUM, {self.value}>"
		elif self.type == TokenType.NULL:
			return "<NULL>"
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
		elif self.type == TokenType.SEMICOLON:
			return "<;>"
		else:
			return f"<{self.type}>"


# Lexer error
class LexerError:
	def __init__(self, position, character, exception_type=""):
		self.character = character
		self.position = position
		if exception_type == "C":
			self.print_character_related_error()
		elif exception_type == "E":
			self.print_string_related_error()
		elif exception_type == "B":
			self.print_boolean_related_error()
	
	def print_character_related_error(self):
		print(f"Invalid character '{self.character}' at position {self.position}")
		
	def print_string_related_error(self):
		print(f"Invalid string at position {self.position}, character {self.character}")
	
	def print_boolean_related_error(self):
		print(f"Invalid boolean (true/false/null) at position {self.position}, character: {self.character}")


class DFA:
	def __init__(self, input_text):
		# Input string
		self.input_text = input_text
		# Current position
		self.position = 0
		self.current_char = self.input_text[self.position] if self.input_text else None
		# Symbol table
		self.symbol_table = {}
		
	# Tokenize the input
	def tokenize(self):
			tokens = []
			while True:
				token = self.get_next_token()
				if token is not None and token.type == TokenType.EOF:
					break
				tokens.append(token)
			return tokens
	
	# Get next token from input
	def get_next_token(self):
		while self.current_char is not None:
			
			if self.current_char.isspace() or self.current_char == "\n" or self.current_char == "\t":
				self.skip_whitespace()
				continue
			# All other tokens
			if self.current_char == '{':
				self.advance()
				return Token(TokenType.LBRACE)
			if self.current_char == '}':
				self.advance()
				return Token(TokenType.RBRACE)
			if self.current_char == '[':
				self.advance()
				return Token(TokenType.LBRACKET)
			if self.current_char == ']':
				self.advance()
				return Token(TokenType.RBRACKET)
			if self.current_char == ',':
				self.advance()
				return Token(TokenType.COMMA)
			if self.current_char == ':':
				self.advance()
				return Token(TokenType.COLON)
			if self.current_char == ';':
				self.advance()
				return Token(TokenType.SEMICOLON)
			
			# Strings
			if self.current_char == "\"":
				return self.recognize_string()
			if self.current_char == 't':
				return self.recognize_boolean()
			if self.current_char == 'f':
				return self.recognize_boolean()
			if self.current_char == 'n':
				return self.recognize_boolean()
			# Numbers
			if self.current_char.isdigit() or self.current_char in ['-', '+']:
				return self.recognize_number()
			# Unrecognized characters
			LexerError(self.position, self.current_char, "C")
			self.advance()
		# Eof
		return Token(TokenType.EOF)
	
	# Input Buffering
	def advance(self):
		self.position += 1
		if self.position >= len(self.input_text):
			# End of input
			self.current_char = None
		else:
			self.current_char = self.input_text[self.position]
	
	# Skip whitespace
	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace() or self.current_char == '\n' or self.current_char == '\t':
			self.advance()
	
	# Recognize string
	def recognize_string(self):
		result = ''
		self.advance()
		while self.current_char is not None and self.current_char != '"':
			result += self.current_char
			self.advance()
		if self.current_char == '"':
			self.advance()
		else:
			LexerError(self.position, self.current_char, "S")
			return ""
		
		return Token(TokenType.STRING, result)
	
	# Recognize numbers
	def recognize_number(self):
		result = ''
		while self.current_char is not None and (
				self.current_char.isdigit() or self.current_char in ['.', 'e', 'E', '-', '+']):
			result += self.current_char
			self.advance()
		return Token(TokenType.NUMBER, result)

	def recognize_boolean(self):
		result = ''
		position = self.position
		while self.current_char is not None and self.current_char.isalpha():
			result += self.current_char
			self.advance()
		
		if result == 'true':
			return Token(TokenType.TRUE)
		elif result == 'false':
			return Token(TokenType.FALSE)
		elif result == 'null':
			return Token(TokenType.NULL)
		else:
			LexerError(position, self.current_char, "B")
			

# Testing the Lexer with input
if __name__ == "__main__":
	for i in range(1, 4):
		file_name = "test_input_" + str(i) + ".txt"
		print("Testing file " + file_name)
		file = open(file_name, "r")
		input_string = ""
		for line in file:
			input_string += line
		lexer = DFA(input_string)
		Output_file = open("test_input_parser_" + str(i) + ".txt", "w")
		tokens = lexer.tokenize()
		for token in tokens:
			if token is not None:
				print(token, file=Output_file)
				print(token)
		print("------End of file: " + file_name + "------")
		print()
		Output_file.close()
