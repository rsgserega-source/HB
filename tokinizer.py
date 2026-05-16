from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str
    line: int

class Tokenizer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.tokens = []

    def peek(self):
        if self.pos >= len(self.code):
            return ""
        return self.code[self.pos]

    def advance(self):
        ch = self.peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
        return ch

    def add(self, type_, value=""):
        self.tokens.append(Token(type_, value, self.line))

    def tokenize(self):
        while self.pos < len(self.code):
            ch = self.peek()

            if ch in " \t\r":
                self.advance()
                continue

            if ch == "\n":
                self.advance()
                continue

            if ch == "@":
                self.advance()
                word = ""
                while self.peek().isalpha():
                    word += self.advance()
                self.add("ATUSE", word)
                continue

            if ch == "#":
                self.advance()
                word = ""
                while self.peek().isalpha():
                    word += self.advance()
                self.add("HASHWORD", word)
                continue

            if ch.isdigit():
                num = ""
                while self.peek().isdigit():
                    num += self.advance()
                self.add("NUMBER", num)
                continue

            if ch.isalpha():
                word = ""
                while self.peek().isalnum() or self.peek() == "_":
                    word += self.advance()
                if word == "print":
                    self.add("PRINT", word)
                else:
                    self.add("IDENT", word)
                continue

            if ch == '"':
                self.advance()
                text = ""
                while self.peek() != '"' and self.peek() != "":
                    text += self.advance()
                self.advance()
                self.add("STRING", text)
                continue

            if ch == "{":
                self.advance()
                self.add("LBRACE", "{")
                continue

            if ch == "}":
                self.advance()
                self.add("RBRACE", "}")
                continue

            if ch == "=":
                self.advance()
                self.add("EQUAL", "=")
                continue

            if ch == "+":
                self.advance()
                self.add("PLUS", "+")
                continue

            if ch == "-":
                self.advance()
                self.add("MINUS", "-")
                continue

            if ch == "*":
                self.advance()
                self.add("MUL", "*")
                continue

            if ch == "/":
                self.advance()
                self.add("DIV", "/")
                continue

            self.advance()

        self.add("EOF", "")
        return self.tokens
