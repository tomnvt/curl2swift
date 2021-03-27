from pygments import highlight
from pygments.lexers import SwiftLexer
from pygments.formatters import TerminalFormatter


def pprint_color(obj):
    print(highlight(obj, SwiftLexer(), TerminalFormatter()))
