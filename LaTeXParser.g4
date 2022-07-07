parser grammar LaTeXParser;

options { tokenVocab = LaTeXLexer; }

comment		: COMMENT;
verbatim	: VERB_BEGIN VERB_CHAR* VERB_END;
math		: MATH_BEGIN mathcontent? MATH_END;
macro		: MACRO (SPACE? argument)*;
argument	: ARG_BEGIN (comment | macro | math | SPACE | HYPHEN | STR | NUMBER | PUNC)* ARG_END;
env			: ENV_BEGIN argument* content? ENV_END;
mathenv		: MATH_ENV_BEGIN argument* mathcontent? MATH_ENV_END;
mathmacro	: MATH_MACRO (MATH_ARG_BEGIN mathcontent? MATH_ARG_END)*;
mathscript	: MATH_SCRIPT (mathmacro | MATH_VARIABLE | (MATH_ARG_BEGIN mathcontent MATH_ARG_END));
mathcontent	: (comment | macro | mathmacro | mathscript | mathenv | MATH_VARIABLE | MATH_BINARY_OPERATOR | MATH_UNARY_OPERATOR | PUNC | MATH_AMPERSAND | (MATH_SUBEXPR_BEGIN mathcontent? MATH_SUBEXPR_END) | (MATH_LEFT mathcontent? MATH_RIGHT))+;
content		: (comment | verbatim | math | macro | env | NEWLINE | SPACE | HYPHEN | STR | NUMBER | PUNC)+;