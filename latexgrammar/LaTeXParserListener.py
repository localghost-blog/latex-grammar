# Generated from LaTeXParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LaTeXParser import LaTeXParser
else:
    from LaTeXParser import LaTeXParser

# This class defines a complete listener for a parse tree produced by LaTeXParser.
class LaTeXParserListener(ParseTreeListener):

    # Enter a parse tree produced by LaTeXParser#comment.
    def enterComment(self, ctx:LaTeXParser.CommentContext):
        pass

    # Exit a parse tree produced by LaTeXParser#comment.
    def exitComment(self, ctx:LaTeXParser.CommentContext):
        pass


    # Enter a parse tree produced by LaTeXParser#verbatim.
    def enterVerbatim(self, ctx:LaTeXParser.VerbatimContext):
        pass

    # Exit a parse tree produced by LaTeXParser#verbatim.
    def exitVerbatim(self, ctx:LaTeXParser.VerbatimContext):
        pass


    # Enter a parse tree produced by LaTeXParser#math.
    def enterMath(self, ctx:LaTeXParser.MathContext):
        pass

    # Exit a parse tree produced by LaTeXParser#math.
    def exitMath(self, ctx:LaTeXParser.MathContext):
        pass


    # Enter a parse tree produced by LaTeXParser#macro.
    def enterMacro(self, ctx:LaTeXParser.MacroContext):
        pass

    # Exit a parse tree produced by LaTeXParser#macro.
    def exitMacro(self, ctx:LaTeXParser.MacroContext):
        pass


    # Enter a parse tree produced by LaTeXParser#argument.
    def enterArgument(self, ctx:LaTeXParser.ArgumentContext):
        pass

    # Exit a parse tree produced by LaTeXParser#argument.
    def exitArgument(self, ctx:LaTeXParser.ArgumentContext):
        pass


    # Enter a parse tree produced by LaTeXParser#env.
    def enterEnv(self, ctx:LaTeXParser.EnvContext):
        pass

    # Exit a parse tree produced by LaTeXParser#env.
    def exitEnv(self, ctx:LaTeXParser.EnvContext):
        pass


    # Enter a parse tree produced by LaTeXParser#mathenv.
    def enterMathenv(self, ctx:LaTeXParser.MathenvContext):
        pass

    # Exit a parse tree produced by LaTeXParser#mathenv.
    def exitMathenv(self, ctx:LaTeXParser.MathenvContext):
        pass


    # Enter a parse tree produced by LaTeXParser#mathmacro.
    def enterMathmacro(self, ctx:LaTeXParser.MathmacroContext):
        pass

    # Exit a parse tree produced by LaTeXParser#mathmacro.
    def exitMathmacro(self, ctx:LaTeXParser.MathmacroContext):
        pass


    # Enter a parse tree produced by LaTeXParser#mathscript.
    def enterMathscript(self, ctx:LaTeXParser.MathscriptContext):
        pass

    # Exit a parse tree produced by LaTeXParser#mathscript.
    def exitMathscript(self, ctx:LaTeXParser.MathscriptContext):
        pass


    # Enter a parse tree produced by LaTeXParser#mathcontent.
    def enterMathcontent(self, ctx:LaTeXParser.MathcontentContext):
        pass

    # Exit a parse tree produced by LaTeXParser#mathcontent.
    def exitMathcontent(self, ctx:LaTeXParser.MathcontentContext):
        pass


    # Enter a parse tree produced by LaTeXParser#content.
    def enterContent(self, ctx:LaTeXParser.ContentContext):
        pass

    # Exit a parse tree produced by LaTeXParser#content.
    def exitContent(self, ctx:LaTeXParser.ContentContext):
        pass


