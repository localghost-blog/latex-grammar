lexer grammar LaTeXLexer;

options {language = Python3;}

@members
{
def next_char(self) -> int:
	for pos in range(self._input._index, self._input._size):
		if not chr(self._input.data[pos]).isspace():
			return self._input.data[pos]
	return -1
}

COMMENT				: '%' .*? (EOF | NEWLINE);
ESCAPE				: '\\' ('&' | '%' | '$' | '#' | '_' | '{' | '}' | '~' | '^');
SPECIALMACRO		: '\\' ('!' | ' ' | ',' | ':' | ';' | '\\');
NEWLINE				: '\n' | '\r' | '\r\n' | '\f';
SPACE				: (' ' | '\t' | '~')+;
VERB				: '\\verb|' .*? '|';
DISPLAYVERB			: '\\begin{verbatim}' .*? '\\end{verbatim}' -> type(VERB);
MATH_BEGIN			: ('$$' | '\\[' | '\\begin{displaymath}' | '\\begin{equation*}') 
{
	self.stack.append('displaymath')
} -> pushMode(MATH);
INLINEMATH_BEGIN	: ('$' | '\\(' | '\\begin{math}') 
{
	self.stack.append('inlinemath')
} -> pushMode(MATH), type(MATH_BEGIN);
EQUATION_BEGIN	: '\\begin{equation}'
{
	self.stack.append('equation')
} -> pushMode(MATH), type(MATH_BEGIN);
ENV_BEGIN			: '\\begin{' WORD '}'
{
	self.stack.append(self.text[7:-1])
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};
ENV_END				: '\\end{' WORD '}'
{
	env = self.stack.pop()
	assert self.text[5: -1] == env, 'Environment mismatch: {} != {}'.format(self.text[5: -1], env)
};
TEXTMACRO			: ('\\text' ('a'..'z' | 'A'..'Z')*)
{
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};
MACRO				: '\\' ('a'..'z' | 'A'..'Z')+ '*'?
{
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};
WORD				: ('a'..'z' | 'A'..'Z')+ ('a'..'z' | 'A'..'Z' | '0'..'9' | '-' | '/' | '_')*;
NUMBER				: ('0'..'9')+;
TEXTSTOP			: '.' | ',' | '!' | '?' | ':' | ';' | ')' | ']' | '\'';
TEXTCONTINUE		: '(' | '[' | '`';
TEXTSPLIT			: '&' | '|';
HYPHEN				: '-';
EQUAL				: '=';
PUNCTUATION			: '*';

mode MATCHARG;

ARG_PRESPACE: SPACE -> type(SPACE);
ARG_BEGIN: ('{' | '[')
{ 
	self.stack.append(self.text)	
} -> pushMode(ARG);

mode ARG;

ARG_END			: ('}' | ']') 
{ord(self.text) == ord(self.stack[-1]) + 2}?
{
	self.stack.pop()
	self.popMode()
	self.popMode()
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};
ARG_MACRO		: MACRO
{
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
} -> type(MACRO);
ARG_COMMENT		: COMMENT -> type(COMMENT);
ARG_ESCAPE		: ESCAPE -> type(ESCAPE);
ARG_SPECIALMACRO: SPECIALMACRO -> type(SPECIALMACRO);
ARG_NEWLINE		: NEWLINE -> type(NEWLINE);
ARG_SPACE		: SPACE -> type(SPACE);
ARG_VERB		: VERB -> type(VERB);
ARG_TEXTMACRO	: TEXTMACRO 
{
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
} -> type(TEXTMACRO);
ARG_INLINEMATH_BEGIN: ('$' | '\\(')
{
	self.stack.append('inlinemath')
} -> type(MATH_BEGIN), pushMode(MATH);
ARG_WORD			: WORD -> type(WORD);
ARG_NUMBER		: NUMBER -> type(NUMBER);
ARG_TEXTSTOP	: TEXTSTOP -> type(TEXTSTOP);
ARG_TEXTCONTINUE: TEXTCONTINUE -> type(TEXTCONTINUE);
ARG_TEXTSPLIT	: TEXTSPLIT -> type(TEXTSPLIT);
ARG_HYPHEN		: HYPHEN -> type(HYPHEN);
ARG_EQUAL		: EQUAL -> type(EQUAL);
ARG_PUNCTUATION	: PUNCTUATION -> type(PUNCTUATION);

mode MATH;

MATH_END				: ('$$' | '\\]' | '\\end{displaymath}' | '\\end{equation*}') 
{
	env = self.stack.pop()
	assert env == 'displaymath', 'Environment mismatch: {} != {}'.format('displaymath', env)
} -> popMode;
INLINEMATH_END			: ('$' | '\\)' | '\\end{math}')
{
	env = self.stack.pop()
	assert env == 'inlinemath', 'Environment mismatch: {} != {}'.format('inlinemath', env)
} -> popMode, type(MATH_END);
EQUATION_END			: '\\end{equation}'
{
	env = self.stack.pop()
	assert env == 'equation', 'Environment mismatch: {} != {}'.format('equation', env)
} -> popMode, type(MATH_END);
MATH_COMMENT			: COMMENT -> type(COMMENT);
MATH_ESCAPE				: '\\' ('&' | '%' | '$' | '#' | '_' | '~' | '^') -> type(ESCAPE);
MATH_SPECIALMACRO		: '\\' ('!' | ' ' | ',' | ':' | ';' | '\\' | '|') -> type(SPECIALMACRO);
MATH_NEWLINE			: NEWLINE -> type(NEWLINE);
MATH_SPACE				: SPACE -> type(SPACE);
MATH_ENV_BEGIN			: '\\begin{' WORD '}'
{
	self.stack.append(self.text[7:-1])
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};
MATH_ENV_END			: '\\end{' WORD '}'
{
	env = self.stack.pop()
	assert self.text[5: -1] == env, 'Environment mismatch: {} != {}'.format(self.text[5: -1], env)
};
MATH_TEXTMACRO			: TEXTMACRO
{
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
} -> type(TEXTMACRO);
MATH_LEFT				: '\\left' ('(' | '[' | '\\{' | '|' | '.');
MATH_RIGHT				: '\\right' (')' | ']' | '\\}' | '|' | '.');
MATH_MACRO				: '\\' ('a'..'z' | 'A'..'Z')+;
MATH_VARIABLE			: ('a'..'z' | 'A'..'Z');
MATH_SCRIPT				: '_' | '^';
MATH_BINARY_OPERATOR	: '+' | '-' | '*' | '/' | '=' | ':' | '>' | '<' | '|';
MATH_UNARY_OPERATOR		: '!';
MATHSTOP				: ('.' | ',') -> type(TEXTSTOP);
MATH_ARG_BEGIN			: '{';
MATH_ARG_END			: '}';
MATH_SUBEXPR_BEGIN		: '(' | '[' | '\\{';
MATH_SUBEXPR_END		: ')' | ']' | '\\}';
MATH_AMPERSAND			: '&';
MATH_NUMBER				: NUMBER -> type(NUMBER);