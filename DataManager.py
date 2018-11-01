import datetime
import xlsxwriter


class DataHandler:

    cursor = None
    conn = None
    title = ''
    WORKBOOK = None
    EXCEL = None
    row = 0
    col = 0

    def __init__(self, title):

        # store in excel
        self.WORKBOOK = xlsxwriter.Workbook('Outputs/' + title + '.xlsx')
        self.EXCEL = self.WORKBOOK.add_worksheet()
        header = ['name', 'filename', 'page', 'rating', 'exact_match', 'partial_match', 'email',
                  'phone', 'address', 'website', 'title', 'create_date']

        for attr in header:
            self.EXCEL.write(self.row, self.col, attr)
            self.col += 1
        self.row += 1
        self.col = 0

        self.title = title

    def close(self):
        self.WORKBOOK.close()

    def store(self, filename, info, skills, mode='excel'):
        if mode == 'excel':
            self.store_excel(filename, info, skills)
        else:
            self.store_database(filename, info, skills)

    def store_excel(self, filename, info, skills):
        name, email, phone, address, website, page = info
        exact_match, partial_match, num_keyword = skills

        raw_score = len(exact_match) * 4 + len(partial_match) * 1
        total_score = num_keyword * 5
        rating = round(float(raw_score) / float(total_score) * 100, 2)
        create_date = datetime.datetime.today().strftime('%d-%b-%y')

        new_row = [name, filename, str(page), str(rating), ' '.join(exact_match), ' '.join(partial_match), email,
                   phone, address, website, self.title, create_date]

        for attr in new_row:
            self.EXCEL.write(self.row, self.col, attr)
            self.col += 1
        self.row += 1
        self.col = 0

    def store_database(self, filename, info, skills):
        pass
