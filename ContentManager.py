from PyPDF2 import PdfFileReader
import re
import os
import spacy
import operator
import docx2txt


class ContentExtractor:

    pdf = None
    nlp = spacy.load('en_core_web_sm')
    doc = None
    word_doc = None

    curPage = 0
    totalPage = 0
    index = 120
    new_resume = False
    TERMS = ['LINKEDIN', 'HTTP', 'HTTPS', 'AVE', 'ST', 'NY', 'NJ', 'CT', 'PA']
    
    cur_startPage = 0
    cur_content = ''
    cur_email = ''
    cur_address = ''
    cur_phone = ''
    cur_name = ''
    cur_website = ''
    prev_startPage = 0
    prev_content = ''
    prev_email = ''
    prev_address = ''
    prev_phone = ''
    prev_name = ''
    prev_website = ''

    def __init__(self, filename):
        if filename.endswith('.docx'):
            self.word_doc = docx2txt.process(os.getcwd() + filename).strip(' ').replace('\n', ' ')
            self.totalPage = 1
        elif filename.endswith('.pdf'):
            f = open(os.getcwd() + filename, 'rb')
            self.pdf = PdfFileReader(f)
            self.totalPage = self.pdf.numPages

    def get_info(self):
        return self.cur_name, self.cur_email, self.cur_phone, self.cur_address, self.cur_website, self.cur_startPage

    def get_prev_info(self):
        return self.prev_name, self.prev_email, self.prev_phone, self.prev_address, self.prev_website, self.prev_startPage

    def get_content(self):
        return self.cur_content

    def has_next_page(self):
        return self.curPage < self.totalPage

    def next_page(self):

        page_num = self.curPage
        self.curPage += 1

        if self.pdf:
            page = self.pdf.getPage(page_num)
            page_content = page.extractText()
            content = page_content.encode('utf-8')
            content = unicode(str(' '.join(re.findall(r'[\w@.()$-/]+', str(content)))))
        elif self.word_doc:
            content = self.word_doc

        self.prev_content = self.cur_content
        self.prev_website = self.cur_website
        self.prev_phone = self.cur_phone
        self.prev_email = self.cur_email
        self.prev_address = self.cur_address
        self.prev_startPage = self.cur_startPage
        self.prev_name = self.cur_name

        self.cur_content = content

        return self

    def new(self):
        if self.prev_content == self.cur_content:
            self.cur_content = ''
        if self.prev_website == self.cur_website:
            self.cur_website = ''
        if self.prev_phone == self.cur_phone:
            self.cur_phone = ''
        if self.prev_email == self.cur_email:
            self.cur_email = ''
        if self.prev_address == self.cur_address:
            self.cur_address = ''
        if self.prev_startPage == self.cur_startPage:
            self.cur_startPage = ''
        if self.prev_name == self.cur_name:
            self.cur_name = ''

    def go_to_page(self, page):
        self.curPage = page

    def is_same_email(self):
        return self.cur_email == self.prev_email or self.cur_email.split('@')[0] == self.prev_email.split('@')[0]

    def is_same_phone_address(self):
        if self.prev_address == self.cur_address and self.prev_phone == self.cur_phone:
            return True
        elif self.prev_phone == self.cur_phone:
            count = 0.0
            for word in self.cur_address.split(' '):
                if word in self.prev_address:
                    count += 1
            return count / len(self.cur_address.split(' ')) > 0.7
        return False

    def is_new_resume(self):
        # print self.get_info()
        # print self.get_prev_info()
        if self.is_same_email():
            return False
        elif self.is_same_phone_address():
            self.cur_email = self.prev_email
            return False
        return True

    def cur_page_website(self):
        website = re.search(r'www\.linkedin\.com[\w/]*', self.cur_content)
        if website:
            new_website = 'https://' + website.group(0).strip().replace(' ', '')
            if new_website != self.cur_website:
                self.cur_website = new_website
                return self.cur_content.find(self.cur_website) + len(self.cur_website)
        return self.cur_content.find(self.cur_website) + len(self.cur_website)

    def cur_page_email(self):
        email = re.search(r'[\w\.]+@[a-zA-Z_]+?(\.[a-zA-Z]{2,3}){1,2}', self.cur_content)
        if email:
            new_email = email.group(0).upper()
            if new_email != self.cur_email:
                self.cur_email = new_email
                return self.cur_content.find(self.cur_email) + len(self.cur_email)
        return self.cur_content.find(self.cur_email) + len(self.cur_email)

    def cur_page_phone(self):
        phone = re.search(r'\(?[2-9]\d{2}\)?[\.\-\s]{0,3}\d{3}[\.\-\s]{0,3}\d{4}', self.cur_content)
        if phone:
            new_phone = phone.group(0)
            phone_num = ''
            for c in new_phone:
                if c.isdigit():
                    phone_num += c
            if phone_num != self.cur_phone:
                self.cur_phone = phone_num.upper()
                return self.cur_content.find(self.cur_phone) + len(self.cur_phone)
        return self.cur_content.find(self.cur_phone) + len(self.cur_phone)

    def cur_page_address(self):
        in_between = '(,|\.)?'
        street_number = '(\d{1,3}[\s-]\d{1,2})|(\d{1,5}))\w?'
        street_type = 'lane|ave|drive|avenue|street|st|blvd|rd|road|Terrace|ct|court|route'
        direction = '((east|west|north|south|w|e|s|n)\s)?'
        street_names = '\s%s(((\w+)\s(%s))|((%s)\s\w{1,4}))' % (direction, street_type, street_type)
        apartment = '(%s\s(apt|apartment)\s\w{1,3})?' % in_between
        city = '%s(\s[a-zA-Z]+){1,2}' % in_between
        state = '%s((\s[a-zA-Z]+){1,2}|\d{2})' % in_between
        zip_code = '%s(\s\d{5})?' % in_between
        regex = '(%s%s%s%s%s%s' % (street_number, street_names, apartment, city, state, zip_code)
        address = re.search(regex, self.cur_content, re.I)
        if address:
            new_address = address.group(0).upper()
            if new_address != self.cur_address:
                self.cur_address = address.group(0).upper()
                return self.cur_content.find(self.cur_address) + len(self.cur_address)
        return self.cur_content.find(self.cur_address) + len(self.cur_address)

    def cur_page_name(self, new_resume=False):
        if new_resume:
            self.cur_startPage = self.curPage
            name = self.parse_name()
            if not name or not name.__contains__(' '):
                self.trim_content()
                name = self.parse_name()
            if not name or not name.__contains__(' '):
                name = self.cur_email.split('@')[0]
                name = name.replace('_', '.').replace('.', ' ')
            self.cur_name = name
        self.new_resume = new_resume

    def parse_name(self):
        persons = {}
        for ent in self.doc.ents:
            if ent.label_ == 'PERSON':
                persons[str(ent)] = 0

        if len(persons) > 0:
            for person in persons:
                full_name = person.split(' ')
                for name in full_name:
                    if self.cur_email.__contains__(name.upper()):
                        persons[person] += 5
                for word in person.split(' '):
                    if self.name_is_vocab(word):
                        persons[person] -= 2
                    if self.cur_address.__contains__(word.upper()):
                        persons[person] -= 10
            name = max(persons.iteritems(), key=operator.itemgetter(1))[0]

            if persons[name] < 0:
                return None
            if len(name.split(' ')) > 3:
                name = ' '.join(name.split(' ')[0:2])
            return name
        else:
            return None

    def name_is_vocab(self, words):
        for word in words.split(' '):
            if word.lower() in self.nlp.vocab and not self.cur_email.__contains__(word.upper()):
                return True
        return False

    def trim_content(self):
        trim_content = []
        words = self.cur_content[0:self.index].split(' ')
        for word in words:
            word = word.strip('., ')
            if (word.isalpha() and word.lower() not in self.nlp.vocab and not self.cur_address.__contains__(word.upper())
                and word.upper() not in self.TERMS) or (self.cur_email.__contains__(word.upper()) and len(word) > 3 and
                                                        self.cur_email != word.upper()):
                trim_content.append(word[0].upper() + word[1:].lower())
        # print 'trim content: ' + ' '.join(trim_content)
        self.doc = self.nlp(unicode(' '.join(trim_content)))

    def reset(self):
        self.cur_email = ''
        self.cur_address = ''
        self.cur_phone = ''
        self.cur_name = ''
        self.cur_website = ''

    def process(self):
        a_index = self.cur_page_address()
        p_index = self.cur_page_phone()
        e_index = self.cur_page_email()
        w_index = self.cur_page_website()

        self.index = self.cur_content.find(' ', 100)
        self.index = max([a_index, p_index, e_index, w_index, self.index])

        self.doc = self.nlp(self.cur_content[0:self.index])
        self.cur_page_name(self.is_new_resume())
