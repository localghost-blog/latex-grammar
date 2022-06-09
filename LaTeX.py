import sys
from antlr4 import *
from src.LaTeXLexer import LaTeXLexer
from src.LaTeXParser import LaTeXParser
from src.LaTeXParserVisitor import LaTeXParserVisitor

class Visitor(LaTeXParserVisitor):
	def visitMath(self, ctx: LaTeXParser.MathContext):
		print('math: ', ctx.getText())
		return super().visitMath(ctx)
	def visitArgument(self, ctx: LaTeXParser.ArgumentContext):
		print('argument: ', ctx.getText())
		return super().visitArgument(ctx)
	def visitTextmacro(self, ctx: LaTeXParser.TextmacroContext):
		print('textmacro: ', ctx.getText())
		return super().visitTextmacro(ctx)
	def visitMacro(self, ctx: LaTeXParser.MacroContext):
		print('macro: ', ctx.getText())
		return super().visitMacro(ctx)
	

def output(text):
	input_stream = InputStream(text)

	lexer = LaTeXLexer(input_stream)
	stream = CommonTokenStream(lexer)

	parser = LaTeXParser(stream)
	tree = parser.content()

	visitor = Visitor()
	visitor.visit(tree)

if __name__ == '__main__':
	with open('sample.tex', 'r') as f:
		text = f.read()
		output(text)