from string import split

class Tokenizer(object):
    """Abstract tokenizer class"""
    def tokenize(self, string):
        raise NotImplementedError( "Should have implemented a tokenize(self, string) method" )

class PuncTokenizer(Tokenizer):
    """Splits string using punctuation as the delimiting character"""
    def __init__(self):
        pass
    def tokenize(self, string):
        self.tokens = list()
        cur = ''
        for n in string:
            if ((ord(n) >= 33) and (ord(n) <= 47)) or ((ord(n) >= 58) and (ord(n) <= 64)):
                if cur != '':
                    self.tokens.append(cur)
                cur = ''
            else:
                cur += n
        if cur != '':
            self.tokens.append(cur)
        return self.tokens
    
class NumTokenizer(Tokenizer):
    """Splits string using digits as the delimiting character"""
    def __init__(self):
        pass
    def tokenize(self, string):
        self.tokens = list()
        cur = ''
        for n in string:
            if (ord(n) >= 48) and (ord(n) <= 57):
                if cur != '':
                    self.tokens.append(cur)
                cur = ''
            else:
                cur += n
        if cur != '':
            self.tokens.append(cur)
            return self.tokens
