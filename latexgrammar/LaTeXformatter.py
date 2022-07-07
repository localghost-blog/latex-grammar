import re
import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from .LaTeXLexer import LaTeXLexer
from .LaTeXParser import LaTeXParser
from .LaTeXParserVisitor import LaTeXParserVisitor

class Formatter(LaTeXParserVisitor):
	def visitComment(self, ctx: LaTeXParser.CommentContext):
		return ctx.getText().split('\n')[0] + '\n'
	def visitVerbatim(self, ctx: LaTeXParser.VerbatimContext):
		result = []
		display = ctx.children[0].symbol.text[7:-1] in ['verbatim', 'verbatim*']
		result.append(ctx.children[0].symbol.text)
		if display and ctx.children[1].symbol.text != '\n':
			result.append('\n')
		last_CR = 0
		for i, child in enumerate(ctx.children[1:-1]):
			if isinstance(child, TerminalNodeImpl):
				text = child.symbol.text
				if text == '\n':
					last_CR = i + 1
				result.append(text)
		is_lastline_blank = True
		for i in range(last_CR, len(ctx.children) - 1):
			if isinstance(ctx.children[i], TerminalNodeImpl):
				text = ctx.children[i].symbol.text
				if not text.isspace():
					is_lastline_blank = False
					break
		if display:
			if is_lastline_blank:
				result = result[:last_CR]
			result.append('\n')
		result.append(ctx.children[-1].symbol.text)
		return ''.join(result)
	def visitMath(self, ctx: LaTeXParser.MathContext):
		result = []
		make_indent = lambda s, char, level: '\n'.join([char * level + line for line in s.split('\n')])
		bg : TerminalNodeImpl = ctx.children[0]
		text = bg.symbol.text
		inline = text in ['$', '\\(', '\\begin{math}']
		tagged = text in ['\\begin{equation}']
		if inline:
			result.append('$')
		else:
			if tagged:
				result.append('\\begin{equation}')
			else:
				result.append('\\[')
		for child in ctx.children[1:-1]:
			if isinstance(child, LaTeXParser.MathcontentContext):
				content = self.visit(child)
				linebreak = len(content) > 80 or content.count('\n') > 0
				if linebreak:
					result.append('\n' + make_indent(content, '\t', 1) + '\n')
				else:
					result.append(content)
		if inline:
			result.append('$')
		else:
			if tagged:
				result.append('\\end{equation}')
			else:
				result.append('\\]')
		return ''.join(result)
	def visitMacro(self, ctx: LaTeXParser.MacroContext):
		result = []
		for child in ctx.children:
			if isinstance(child, LaTeXParser.ArgumentContext):
				result.append(self.visit(child))
			if isinstance(child, TerminalNodeImpl):
				type = child.symbol.type
				text = child.symbol.text
				if type == LaTeXLexer.MACRO:
					i = 2
					while i < len(text):
						if not text[i].isspace():
							i += 1
						else:
							break
					result.append(text[:i])
				else:
					result.append(text)
		return ''.join(result)
	def visitArgument(self, ctx: LaTeXParser.ArgumentContext):
		is_single_macro = lambda c: isinstance(c, LaTeXParser.MacroContext) and len(c.children) == 1 and c.children[0].symbol.text != '\\ '
		result = []
		macro_name = ctx.parentCtx.children[0].symbol.text[1:]
		verbatim = macro_name in ['label', 'ref', 'cite', 'url', 'href', 'input', 'include']
		for index, child in enumerate(ctx.children):
			if index > 0:
				lastChild = ctx.children[index - 1]
			if isinstance(child, ParserRuleContext):
				result.append(self.visit(child))
			if isinstance(child, TerminalNodeImpl):
				type = child.symbol.type
				text = child.symbol.text
				if verbatim:
					result.append(text)
				else:
					if type == LaTeXLexer.SPACE:
						if index > 0 and isinstance(lastChild, TerminalNodeImpl):
							if lastChild.symbol.type == LaTeXLexer.PUNC:
								if lastChild.symbol.text in ['=', '|', '&', '.', '?', '!', ',', ':', ';', '\'', ')']:
									continue
						result.append(' ')
					elif type == LaTeXLexer.PUNC:
						if index > 0 and isinstance(lastChild, TerminalNodeImpl) and lastChild.symbol.type == LaTeXLexer.SPACE:
							result.pop()
						if index > 1 and text in ['=', '|', '&', '`', '(']:
							result.append(' ')
						result.append(text)
						if index < ctx.getChildCount() - 2 and text in ['=', '|', '&', '.', '?', '!', ',', ':', ';', '\'', ')']:
							result.append(' ')
					else:
						if index > 0 and index < ctx.getChildCount() - 1 and is_single_macro(lastChild):
							result.append(' ')
						result.append(text)
		return ''.join(result)
	def visitEnv(self, ctx: LaTeXParser.EnvContext):
		result = []
		env_name = ctx.children[0].symbol.text[7:-1]
		make_indent = lambda s, char, level: '\n'.join([char * level + line for line in s.split('\n')])
		for child in ctx.children:
			if isinstance(child, LaTeXParser.ArgumentContext):
				result.append(self.visit(child))
			if isinstance(child, LaTeXParser.ContentContext):
				content : str = self.visit(child)
				result.append('\n')
				if env_name in ['document']:
					result.append(content)
				else:
					lines = content.split('\n')
					in_verbatim = False
					for i, line in enumerate(lines):
						if line.strip().startswith('\\end{verbatim'):
							in_verbatim = False
						if not in_verbatim:
							lines[i] = '\t' + line
						if line.strip().startswith('\\begin{verbatim'):
							in_verbatim = True
					result.append('\n'.join(lines))
				result.append('\n')
			if isinstance(child, TerminalNodeImpl):
				text = child.symbol.text
				result.append(text)
		return ''.join(result)
	def visitMathenv(self, ctx: LaTeXParser.MathenvContext):
		result = []
		make_indent = lambda s, char, level: '\n'.join([char * level + line for line in s.split('\n')])
		for index, child in enumerate(ctx.children):
			if isinstance(child, LaTeXParser.ArgumentContext):
				result.append(self.visit(child))
			if isinstance(child, LaTeXParser.MathcontentContext):
				result.append('\n')
				content = self.visit(child)
				result.append(make_indent(content, '\t', 1))
			if isinstance(child, TerminalNodeImpl):
				if index == ctx.getChildCount() - 1:
					result.append('\n')
				text = child.symbol.text
				result.append(text)
		return ''.join(result)
	def visitMathmacro(self, ctx: LaTeXParser.MathmacroContext):
		result = []
		for child in ctx.children:
			if isinstance(child, LaTeXParser.MathcontentContext):
				result.append(self.visit(child))
			if isinstance(child, TerminalNodeImpl):
				text = child.symbol.text
				result.append(text)
		return ''.join(result)
	def visitMathscript(self, ctx: LaTeXParser.MathscriptContext):
		result = []
		for child in ctx.children:
			if isinstance(child, LaTeXParser.MathmacroContext):
				result.append(self.visit(child))
			if isinstance(child, LaTeXParser.MathcontentContext):
				result.append(self.visit(child))
			if isinstance(child, TerminalNodeImpl):
				text = child.symbol.text
				result.append(text)
		return ''.join(result)
	def visitMathcontent(self, ctx: LaTeXParser.MathcontentContext):
		is_single_macro = lambda c: (isinstance(c, LaTeXParser.MacroContext) or isinstance(c, LaTeXParser.MathmacroContext)) and len(c.children) == 1 and c.children[0].symbol.text != '\\ '
		result = []
		for index, child in enumerate(ctx.children):
			if index > 0:
				lastChild = ctx.children[index - 1]
			if isinstance(child, LaTeXParser.CommentContext):
				result.append(self.visit(child))
			if isinstance(child, LaTeXParser.MacroContext):
				if index > 0:
					result.append(' ')
				result.append(self.visit(child))
			if isinstance(child, LaTeXParser.MathmacroContext):
				if index > 0:
					result.append(' ')
				result.append(self.visit(child))
			if isinstance(child, LaTeXParser.MathscriptContext):
				result.append(self.visit(child))
			if isinstance(child, LaTeXParser.MathenvContext):
				result.append(self.visit(child))
			if isinstance(child, LaTeXParser.MathcontentContext):
				result.append(self.visit(child))
			if isinstance(child, TerminalNodeImpl):
				text = child.symbol.text
				type = child.symbol.type
				if index > 0 and is_single_macro(lastChild):
					if lastChild.children[0].symbol.text == '\\\\':
						result.append('\n')
					elif type in [LaTeXParser.MATH_VARIABLE, LaTeXParser.MATH_LEFT]:
						result.append(' ')
				if type in [LaTeXParser.MATH_BINARY_OPERATOR, LaTeXParser.MATH_AMPERSAND]:
					if index > 0:
						result.append(' ')
					result.append(text)
					if index > 0 or text in ['|']:
						result.append(' ')
				elif type in [LaTeXParser.MATH_SUBEXPR_BEGIN, LaTeXParser.MATH_SUBEXPR_END]:
					result.append(text)
					if text in [')', ']']:
						result.append(' ')
				elif type == LaTeXParser.PUNC:
					result.append(text)
					if text in [',']:
						result.append(' ')
				else:
					result.append(text)
		for index, value in enumerate(result):
			if value == ' ' and (index == 0 or index == len(result) - 1 or result[index - 1] == ' ' or result[index - 1] == ' '):
				result[index] = ''
		return ''.join(result)
	def visitContent(self, ctx: LaTeXParser.ContentContext):
		is_single_macro = lambda c: isinstance(c, LaTeXParser.MacroContext) and len(c.children) == 1 and c.children[0].symbol.text != '\\ '
		is_root = False
		for child in ctx.children:
			if isinstance(child, LaTeXParser.EnvContext):
				if child.getChild(0).symbol.text == '\\begin{document}':
					is_root = True
					break
		all_macro_env = True
		for child in ctx.children:
			if isinstance(child, TerminalNodeImpl) and child.symbol.type not in [LaTeXParser.NEWLINE, LaTeXParser.SPACE]:
				all_macro_env = False
				break
		result = []
		current_len = 0
		for index, child in enumerate(ctx.children):
			if index > 0:
				lastChild = ctx.children[index - 1]			
			if isinstance(child, ParserRuleContext):
				result.append((child.__class__.__name__, self.visit(child)))
			if isinstance(child, TerminalNodeImpl):
				type = child.symbol.type
				text = child.symbol.text
				if index > 0:
					lastChild = ctx.children[index - 1]
				if type in [LaTeXParser.NEWLINE, LaTeXParser.SPACE]:
					if index > 0 and index < len(ctx.children) - 1 and len(result) > 0 and not result[-1][1].isspace():
						if type == LaTeXParser.NEWLINE:
							result.append((type, '\n\n'))
						if type == LaTeXParser.SPACE:
							if all_macro_env:
								result.append((type, '\n'))
							else:
								if isinstance(lastChild, LaTeXParser.MacroContext) and len(lastChild.children) == 1 and len(lastChild.children[0].symbol.text) > 2:
									result.append((type, '\n'))
								else:
									result.append((type, ' '))
				else:
					if index > 0 and is_single_macro(lastChild) and type in [LaTeXParser.STR]:
						result.append((LaTeXParser.SPACE, ' '))
					result.append((type, text))
		
		text_result = []
		prev_or_next_str = r'(?:\\(label|(sub)?paragraph|newpage|(print)?bibliography|printindex|(front|main|back)matter|include|input|maketitle|tableofcontents|appendix|\\))'
		line_break_prev = lambda x: (x[0] == 'MacroContext' and re.match(prev_or_next_str + r'|(\\item)', x[1]) is not None) or (x[0] == 'EnvContext') or (x[0] == 'MathContext' and not x[1].startswith('$')) or (x[0] == 'VerbatimContext' and not x[1].startswith('\\verb'))
		line_break_next = lambda x: (x[0] == 'MacroContext' and re.match(prev_or_next_str, x[1]) is not None) or (x[0] == 'EnvContext') or (x[0] == 'MathContext' and not x[1].startswith('$')) or (x[0] == 'VerbatimContext' and not x[1].startswith('\\verb'))
		space_level = lambda x: [' ', '\n', '\n\n'].index(x)
		for i, value in enumerate(result):
			type = value[0]
			text : str = value[1]
			if line_break_prev((type, text)):
				if len(text_result) > 0 and text_result[-1] == ' ':
					text_result.pop()
				if len(text_result) > 0 and not text_result[-1].endswith('\n'):
					text_result.append('\n')
			if text.isspace():
				level = space_level(text)
				if len(text_result) > 0:
					if text_result[-1].isspace():
						if space_level(text_result[-1]) < space_level(text):
							text_result[-1] = text
					else:
						text_result.append(text)
			else:
				text_result.append(text)
			if i < len(result) - 1 and line_break_next((type, text)):
				text_result.append('\n')
		max_length = {'.': 20, '?': 40, '!': 40, ';': 50, ',': 70}
		for i, text in enumerate(text_result):
			if text.endswith('\n'):
				current_len = 0
			else:
				current_len += len(text)

			if text == ' ':
				if current_len > max_length.get(text_result[i - 1], 70):
					text_result[i] = '\n'
					current_len = 0
		return ''.join([text for text in text_result])
	

def format(text):
	input_stream = InputStream(text)

	lexer = LaTeXLexer(input_stream)
	stream = CommonTokenStream(lexer)

	parser = LaTeXParser(stream)
	tree = parser.content()

	visitor = Formatter()
	result = visitor.visit(tree)
	return result

if __name__ == '__main__':
	lines = []
	for line in sys.stdin:
		lines.append(line)
	text = ''.join(lines)
	print(format(text))