indentChar = " "


def charCount(string, char):
    if len(char) != 1:
        raise ValueError("\"{}\" isn't one character long".format(char))

    ret = 0

    for c in string:
        if c == char:
            ret += 1

    return ret

class DecorateIndenter(object):
    """It indents DECORATE and ACS! Sweet jesus."""

    def __init__(self, indentWidth=4, colonUnindent=2):
        self.indentWidth = indentWidth
        self.colonUnindent = colonUnindent

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ", ".join([self.indentWidth, self.colonUnindent])
                              )
    
    def processFile(self, file):
        return self.processText(file.read())

    def processText(self, text):
        indentLevel = 0
        nextIndentLevel = 0
        
        ret = []
        
        for line in text.splitlines():
            indentLevel = nextIndentLevel

            newLine, indentLevel, nextIndentLevel = self.processLine(line, indentLevel)
            
            ret.append(newLine)

        return "\n".join(ret)

    def processLine(self, line, indentLevel):
        line = line.lstrip()

        openBraceCount  = charCount(line, "{")
        closeBraceCount = charCount(line, "}")

        indentDiff = (openBraceCount - closeBraceCount)

        if indentDiff < 0:
            indentLevel = max(indentLevel + indentDiff, 0)
            nextIndentLevel = indentLevel
        else:
            nextIndentLevel = indentLevel + indentDiff

        retLine = (indentChar * (indentLevel * self.indentWidth)) + line

        noCommentLine = line.rsplit("//", 1)[0].rstrip()

        if noCommentLine.endswith(":"):
            whitespaceCut = min(indentLevel * self.indentWidth, self.colonUnindent)
            retLine = retLine[whitespaceCut:]

        return retLine, indentLevel, nextIndentLevel
