import math
from pathlib import Path

from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
from PyQt5.Qt import *
from PyQt5.QtGui import QColor, QFont

from PyQt5.QtWidgets import QShortcut
from pygments import lexers, styles
from pygments.lexer import Error, Text, _TokenType


EXTRA_STYLES = {
    "monokai": {
        "background": "#272822",
        "caret": "#F8F8F0",
        "foreground": "#F8F8F2",
        "invisibles": "#F8F8F259",
        "lineHighlight": "#3E3D32",
        "selection": "#49483E",
        "findHighlight": "#FFE792",
        "findHighlightForeground": "#000000",
        "selectionBorder": "#222218",
        "activeGuide": "#9D550FB0",
        "misspelling": "#F92672",
        "bracketsForeground": "#F8F8F2A5",
        "bracketsOptions": "underline",
        "bracketContentsForeground": "#F8F8F2A5",
        "bracketContentsOptions": "underline",
        "tagsOptions": "stippled_underline",
    }
}


class ViewLexer(QsciLexerCustom):
    def __init__(self, lexer_name, style_name):
        super().__init__()

        # Lexer + Style
        self.pyg_style = styles.get_style_by_name(style_name)
        self.pyg_lexer = lexers.get_lexer_by_name(lexer_name, stripnl=False)
        self.cache = {0: ("root",)}
        self.extra_style = EXTRA_STYLES[style_name]

        self.font = QFont("", 14, weight=QFont.Medium)

        self.token_styles = {}
        index = 0
        for k, v in self.pyg_style:
            self.token_styles[k] = index
            if v.get("color", None):
                self.setColor(QColor(f"#{v['color']}"), index)
            if v.get("bgcolor", None):
                self.setPaper(QColor(f"#{v['bgcolor']}"), index)
            self.setFont(self.font, index)
            index += 1

    def defaultPaper(self, style):
        return QColor(self.extra_style["background"])

    def language(self):
        return self.pyg_lexer.name

    def get_tokens_unprocessed(self, text, stack=("root",)):
        lexer = self.pyg_lexer
        pos = 0
        tokendefs = lexer._tokens
        statestack = list(stack)
        statetokens = tokendefs[statestack[-1]]
        while 1:
            for rexmatch, action, new_state in statetokens:
                m = rexmatch(text, pos)
                if m:
                    if action is not None:
                        if type(action) is _TokenType:
                            yield pos, action, m.group()
                        else:
                            for item in action(lexer, m):
                                yield item
                    pos = m.end()
                    if new_state is not None:
                        if isinstance(new_state, tuple):
                            for state in new_state:
                                if state == "#pop":
                                    statestack.pop()
                                elif state == "#push":
                                    statestack.append(statestack[-1])
                                else:
                                    statestack.append(state)
                        elif isinstance(new_state, int):
                            del statestack[new_state:]
                        elif new_state == "#push":
                            statestack.append(statestack[-1])
                        else:
                            assert False, "wrong state def: %r" % new_state
                        statetokens = tokendefs[statestack[-1]]
                    break
            else:
                try:
                    if text[pos] == "\n":
                        statestack = ["root"]
                        statetokens = tokendefs["root"]
                        yield pos, Text, "\n"
                        pos += 1
                        continue
                    yield pos, Error, text[pos]
                    pos += 1
                except IndexError:
                    break

    def highlight_slow(self, start, end):
        view = self.editor()
        code = view.text()[start:]
        tokensource = self.get_tokens_unprocessed(code)

        self.startStyling(start)
        for _, ttype, value in tokensource:
            self.setStyling(len(value), self.token_styles[ttype])

    def styleText(self, start, end):
        view = self.editor()
        self.highlight_slow(start, end)
        len_text = len(view.text())

    def description(self, style_nr):
        return str(style_nr)


class SwiftHighlighter(QsciScintilla):
    def __init__(self, lexer_name="swift", style_name="monokai"):
        super().__init__()
        view = self

        self.setEolMode(QsciScintilla.EolUnix)
        self.lexer = ViewLexer(lexer_name, style_name)
        self.setLexer(self.lexer)

        # # -------- Multiselection --------
        self.SendScintilla(view.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(view.SCI_SETMULTIPASTE, 1)
        self.SendScintilla(view.SCI_SETADDITIONALSELECTIONTYPING, True)

        # -------- Extra settings --------
        self.set_extra_settings(EXTRA_STYLES[style_name])

    def get_line_separator(self):
        m = self.eolMode()
        if m == QsciScintilla.EolWindows:
            eol = "\r\n"
        elif m == QsciScintilla.EolUnix:
            eol = "\n"
        elif m == QsciScintilla.EolMac:
            eol = "\r"
        else:
            eol = ""
        return eol

    def set_extra_settings(self, dct):
        self.setIndentationGuidesBackgroundColor(QColor(0, 0, 255, 0))
        self.setIndentationGuidesForegroundColor(QColor(0, 255, 0, 0))

        if "caret" in dct:
            self.setCaretForegroundColor(QColor(dct["caret"]))

        if "line_highlight" in dct:
            self.setCaretLineBackgroundColor(QColor(dct["line_highlight"]))

        if "brackets_background" in dct:
            self.setMatchedBraceBackgroundColor(QColor(dct["brackets_background"]))

        if "brackets_foreground" in dct:
            self.setMatchedBraceForegroundColor(QColor(dct["brackets_foreground"]))

        if "selection" in dct:
            self.setSelectionBackgroundColor(QColor(dct["selection"]))

        if "background" in dct:
            c = QColor(dct["background"])
            self.resetFoldMarginColors()
            self.setFoldMarginColors(c, c)
