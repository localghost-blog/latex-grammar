lexer grammar LaTeXLexer;

options {language = Python3;}

tokens {STR, SPACE, MACRO, COMMENT, ENV}



@members {
def next_char(self) -> int:
	for pos in range(self._input._index, self._input._size):
		if not chr(self._input.data[pos]).isspace():
			return self._input.data[pos]
	return -1

def last_char(self) -> int:
	return self._input.LA(-1)
}

NEWLINE			: BLANK* EOL (BLANK* EOL)+ BLANK*;
SPACE			: BLANK+ | (BLANK* EOL BLANK*) {self._input.LA(1) not in [10, 13]}?;
COMMENT			: '%' .*? (EOF | (EOL BLANK*));
ESCAPE			: '\\' ('#' | '$' | '%' | '&' | '_' | '{' | '}') -> type(MACRO);
SPACEMACRO		: '\\' ('!' | ',' | ':' | ';' | ' ') -> type(MACRO);
NEWLINEMACRO	: '\\\\' -> type(MACRO);
HYPHEN			: '-'+;
STR				: (CHAR | '/')+ ('/' | '_' | HYPHEN | DIGIT | CHAR)*;
NUMBER			: DIGIT+ ('.' DIGIT+)?;
PUNC			: '.' | '?' | '!' | ',' | ':' | ';' | '~' | '`' | '\'' | '"' | '(' | ')' | '*' | '=' | '|' | '&';
VERB_BEGIN: '\\verb' '*'? ~('a'..'z' | 'A'..'Z' | ' ' | '\t' | '\f' | '\r' | '\n' | '*') {
	self.stack.append(self._input._index + self._input.strdata[self._input._index:].find(self.text[-1]))
	self.pushMode(LaTeXLexer.modeNames.index('VERBATIM'))
};
DISPLAYVERB_BEGIN: '\\begin{verbatim' '*'? '}' {
	self.stack.append(self._input._index + self._input.strdata[self._input._index:].find('\\end{' + self.text[7:-1] + '}'))
	self.pushMode(LaTeXLexer.modeNames.index('VERBATIM'))
} -> type(VERB_BEGIN);
MATH_BEGIN		: ('$$' | '\\[' | '\\begin{displaymath}' | '\\begin{equation*}') {
	self.stack.append('displaymath')
} -> pushMode(MATH);
INLINEMATH_BEGIN: ('$' | '\\(' | '\\begin{math}') {
	self.stack.append('inlinemath')
} -> pushMode(MATH), type(MATH_BEGIN);
EQUATION_BEGIN	: '\\begin{equation}' {
	self.stack.append('equation')
} -> pushMode(MATH), type(MATH_BEGIN);
ENV_BEGIN		: '\\begin{' ALPHA+ '*'? '}' {
	self.stack.append(self.text[7:-1])
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};
ENV_END			: '\\end{' ALPHA+ '*'? '}' {
	env = self.stack.pop()
	assert self.text[5: -1] == env, 'Environment mismatch: {} != {}'.format(self.text[5: -1], env)
};
URLMACRO		: '\\' ('url' | 'href') SPACE? '{' ~('}')* '}' -> type(MACRO);
MACRO			: '\\' ALPHA+ '*'? SPACE? {
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};

mode VERBATIM;

VERB_CHAR		: . { self._input.index <= self.stack[-1] }?;
VERB_END		: '\\end{verbatim}' {
	self.stack.pop()	
} -> popMode;
VERB_STAR_END	: '\\end{verbatim*}' {
	self.stack.pop()	
} -> popMode, type(VERB_END);
INLINEVERB_END	: . {
	self.stack.pop()	
} -> popMode, type(VERB_END);

mode MATCHARG;

ARG_PRESPACE: SPACE -> skip;
ARG_BEGIN: ('{' | '[') { 
	self.stack.append(self.text)	
} -> pushMode(ARG);

mode ARG;

ARG_END			: ('}' | ']') {ord(self.text) == ord(self.stack[-1]) + 2}? {
	self.stack.pop()
	self.popMode()
	self.popMode()
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};
ARG_SPACE		: SPACE {self._input.LA(1) not in [10, 13]}? -> type(SPACE);
ARG_COMMENT		: COMMENT -> type(COMMENT);
ARG_ESCAPE		: ESCAPE -> type(MACRO);
ARG_SPACEMACRO	: SPACEMACRO -> type(MACRO);
ARG_NEWLINEMACRO: NEWLINEMACRO -> skip;
ARG_HYPHEN		: HYPHEN -> type(HYPHEN);
ARG_STR			: STR -> type(STR);
ARG_NUMBER		: NUMBER -> type(NUMBER);
ARG_PUNC		: PUNC -> type(PUNC);
ARG_MATH_BEGIN	: MATH_BEGIN {
	self.stack.append('displaymath')
} -> pushMode(MATH), type(MATH_BEGIN);
ARG_INLINEMATH_BEGIN: INLINEMATH_BEGIN {
	self.stack.append('inlinemath')
} -> pushMode(MATH), type(MATH_BEGIN);
ARG_MACRO		: MACRO {
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
} -> type(MACRO);

mode MATH;

MATH_END				: ('$$' | '\\]' | '\\end{displaymath}' | '\\end{equation*}') {
	env = self.stack.pop()
	assert env == 'displaymath', 'Environment mismatch: {} != {}'.format('displaymath', env)
} -> popMode;
INLINEMATH_END			: ('$' | '\\)' | '\\end{math}') {
	env = self.stack.pop()
	assert env == 'inlinemath', 'Environment mismatch: {} != {}'.format('inlinemath', env)
} -> popMode, type(MATH_END);
EQUATION_END			: '\\end{equation}' {
	env = self.stack.pop()
	assert env == 'equation', 'Environment mismatch: {} != {}'.format('equation', env)
} -> popMode, type(MATH_END);
MATH_NEWLINE			: NEWLINE -> skip;
MATH_SPACE				: SPACE -> skip;
MATH_COMMENT			: COMMENT -> type(COMMENT);
MATH_ESCAPE				: ESCAPE -> type(MACRO);
MATH_SPACEMACRO			: SPACEMACRO -> type(MACRO);
MATH_NEWLINEMACRO		: NEWLINEMACRO -> type(MACRO);
MATH_INLINEVERB_BEGIN	: VERB_BEGIN -> type(VERB_BEGIN);
MATH_ENV_BEGIN			: '\\begin{' ALPHA+ '*'? '}' {
	self.stack.append(self.text[7:-1])
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
};
MATH_ENV_END			: '\\end{' ALPHA+ '*'? '}' {
	env = self.stack.pop()
	assert self.text[5: -1] == env, 'Environment mismatch: {} != {}'.format(self.text[5: -1], env)
};
MATH_TEXTMACRO			: '\\' (('\\text' (| 'bf' | 'it' | 'sc')) | 'label' | 'mbox') {not chr(self._input.LA(1)).isalpha()}? SPACE? {
	if self.next_char() in [91, 123]:
		self.pushMode(LaTeXLexer.modeNames.index('MATCHARG'))
} -> type(MACRO);
MATH_LEFT				: '\\left' ('(' | '[' | '\\{' | '|' | '\\|' | '.');
MATH_RIGHT				: '\\right' (')' | ']' | '\\}' | '|' | '\\|' | '.');
MATH_MACRO				: '\\' ALPHA+ '*'?;
MATH_VARIABLE			: ALPHA | DIGIT;
MATH_SCRIPT				: '_' | '^';
MATH_BINARY_OPERATOR	: '+' | '-' | '*' | '/' | '=' | '>' | '<' | '|';
MATH_UNARY_OPERATOR		: '!';
MATH_ARG_BEGIN			: '{';
MATH_ARG_END			: '}';
MATH_SUBEXPR_BEGIN		: '(' | '[' | '\\{';
MATH_SUBEXPR_END		: ')' | ']' | '\\}';
MATH_AMPERSAND			: '&';
MATH_PUNC				: (PUNC | '\\|') -> type(PUNC);
// MATH_NUMBER				: NUMBER -> type(NUMBER);

fragment EOL	: '\r' ? '\n';
fragment BLANK	: ' ' | '\t' | '\f';
fragment ALPHA	: 'a'..'z' | 'A'..'Z';
fragment CHAR	: 'a'..'z' | 'A'..'Z' | '\u0100' .. '\u017E';
fragment DIGIT	: '0'..'9';
fragment ANY	: '\u0000' .. '\uFFFE';