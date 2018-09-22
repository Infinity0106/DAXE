all:
	python -m lark.tools.standalone littleDuck.lark > littleDuck_parser.py
	cat add_error.txt >> littleDuck_parser.py