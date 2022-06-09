# Generated from LaTeXParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LaTeXParser import LaTeXParser
else:
    from LaTeXParser import LaTeXParser

# This class defines a complete generic visitor for a parse tree produced by LaTeXParser.

class LaTeXParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LaTeXParser#comment.
    def visitComment(self, ctx:LaTeXParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#escape.
    def visitEscape(self, ctx:LaTeXParser.EscapeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#verbatim.
    def visitVerbatim(self, ctx:LaTeXParser.VerbatimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#math.
    def visitMath(self, ctx:LaTeXParser.MathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#textmacro.
    def visitTextmacro(self, ctx:LaTeXParser.TextmacroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#macro.
    def visitMacro(self, ctx:LaTeXParser.MacroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#argument.
    def visitArgument(self, ctx:LaTeXParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#env.
    def visitEnv(self, ctx:LaTeXParser.EnvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#mathenv.
    def visitMathenv(self, ctx:LaTeXParser.MathenvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#mathmacro.
    def visitMathmacro(self, ctx:LaTeXParser.MathmacroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#mathscript.
    def visitMathscript(self, ctx:LaTeXParser.MathscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#mathcontent.
    def visitMathcontent(self, ctx:LaTeXParser.MathcontentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LaTeXParser#content.
    def visitContent(self, ctx:LaTeXParser.ContentContext):
        return self.visitChildren(ctx)



del LaTeXParser