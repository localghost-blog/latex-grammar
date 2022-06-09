parser grammar LaTeXParser;

options { tokenVocab = LaTeXLexer; }

comment		: COMMENT;
escape		: ESCAPE;
verbatim	: VERB;
math		: MATH_BEGIN mathcontent? MATH_END;
textmacro	: TEXTMACRO (SPACE? argument)*;
macro		: SPECIALMACRO | (MACRO (SPACE? argument)*);
argument	: (ARG_BEGIN (macro | textmacro | math | comment | WORD | NUMBER | HYPHEN | TEXTSTOP | TEXTCONTINUE | TEXTSPLIT | PUNCTUATION | EQUAL | SPACE)* ARG_END);
env			: ENV_BEGIN argument* content? ENV_END;
mathenv		: MATH_ENV_BEGIN argument* mathcontent? MATH_ENV_END;
mathmacro	: SPECIALMACRO | (MATH_MACRO (SPACE? MATH_ARG_BEGIN mathcontent MATH_ARG_END)*);
mathscript	: MATH_SCRIPT (MATH_VARIABLE | NUMBER | mathmacro | (MATH_ARG_BEGIN mathcontent MATH_ARG_END));
mathcontent	: (MATH_VARIABLE | NUMBER | mathscript | mathenv | mathmacro | textmacro | comment | escape | MATH_BINARY_OPERATOR | MATH_UNARY_OPERATOR | TEXTSTOP | MATH_AMPERSAND | SPACE | NEWLINE | (MATH_SUBEXPR_BEGIN mathcontent? MATH_SUBEXPR_END) | (MATH_LEFT mathcontent? MATH_RIGHT))+;
content		: (macro | textmacro | env | math | comment | escape | verbatim | WORD | NUMBER | HYPHEN | TEXTSTOP | TEXTCONTINUE | TEXTSPLIT | PUNCTUATION | EQUAL | SPACE | NEWLINE)+;