from .LaTeXformatter import format
import sys 
if __name__ == '__main__':
	lines = []
	for line in sys.stdin:
		lines.append(line)
	text = ''.join(lines)
	print(format(text))
