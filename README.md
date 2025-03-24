# Made by Dhruv Sharma
Run scanner first, then run parser.

Using following tokens:
	String: "<STR, {self.value}>"
	Numbers (Both integer and decimal): "<INT, {self.value}>"
	LBRACE: "<{>"
	RBRACE: "<}>"
	LBRACKET: "<[>"
	RBRACKET: "<]>"
	COMMA: "<,>"
	COLON: "<:>"
	TRUE: "<true>"
	FALSE: "<false>"
	NULL: "<NULL>"
	EOF: "<EOF>"

The code also error detect semantic errors. The code prints out the errors and the AST into test_input_X_errors.txt and test_AST_output_X.txt respectively where
X matches test_input_X.txt
