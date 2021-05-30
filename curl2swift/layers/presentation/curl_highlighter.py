from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format(color, style=""):
    """Return a QTextCharFormat with the given attributes."""
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if "bold" in style:
        _format.setFontWeight(QFont.Bold)
    if "italic" in style:
        _format.setFontItalic(True)

    return _format


STYLES = {
    "keyword": format("yellow"),
    "operator": format("orange"),
    "string": format("magenta"),
}


class CurlHighlighter(QSyntaxHighlighter):

    keywords = [
        "curl",
        "command",
        "url",
        "d",
        "data",
        "b",
        "data-binary",
        "data-raw",
        "data-urlencode",
        "X",
        "H",
        "header",
    ]

    methods = ["GET", "POST", "PATCH", "UPDATE", "DELTE"]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        self.tri_single = (QRegExp("'''"), 1, STYLES["string"])
        self.tri_double = (QRegExp('"""'), 2, STYLES["string"])

        rules = []

        # Keyword, operator, and brace rules
        rules += [
            (r"\b%s\b" % w, 0, STYLES["keyword"]) for w in CurlHighlighter.keywords
        ]
        rules += [(r"%s" % o, 0, STYLES["operator"]) for o in CurlHighlighter.methods]

        # All other rules
        rules += [
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES["string"]),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES["string"]),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
