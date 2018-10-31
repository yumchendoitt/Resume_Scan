import re


class KeywordExtractor:

    content = []
    keywords = []
    exact_match = set()
    partial_match = set()
    num_keyword = 0

    def __init__(self, title):
        with open('keyword/' + title + '.txt', 'r') as f:
            self.keywords = f.read().replace('.', '\.').split(',')
            self.num_keyword = len(self.keywords)

    def search(self, keyword, words):
        for word in words:
            if re.search(r'^%s$' % keyword, word, re.I):
                self.exact_match.add(word)
                if word in self.partial_match:
                    self.partial_match.remove(word)
            elif re.search(r'%s' % keyword, word, re.I):
                if word not in self.exact_match:
                    self.partial_match.add(word.strip('(),'))

    def new_resume(self):
        self.exact_match = set()
        self.partial_match = set()
        self.content = []
        return self

    def extract(self, content):
        self.content = re.split(' ', content.replace(',', ''))
        for keyword in self.keywords:
            self.search(keyword, self.content)

    def get_skills(self):
        return self.exact_match, self.partial_match, self.num_keyword
