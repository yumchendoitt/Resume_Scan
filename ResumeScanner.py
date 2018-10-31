from ContentManager import ContentExtractor
import os
from Util import progress
from KeywordManager import KeywordExtractor
from DataManager import DataHandler
import sys

try:
    TITLE = sys.argv[1]
except IndexError:
    print 'Please provide a keyword file'
    sys.exit()

RESUME_FOLDER = 'resumes'
extractor = KeywordExtractor(TITLE)
data_handler = DataHandler(TITLE)

for filename in os.listdir(RESUME_FOLDER):
    output = open('Outputs/' + filename.replace(filename[filename.find('.'):], '.txt'), 'w+')
    resumes = ContentExtractor('/%s/%s' % (RESUME_FOLDER, filename))
    # Debugging
    # resumes.go_to_page(0)
    while resumes.has_next_page():
        resumes.next_page().process()

        if resumes.is_new_resume() and resumes.curPage != 1:
            data_handler.store(filename, resumes.get_prev_info(), extractor.get_skills())
            output.write('%s %d: %s\n' % (filename, resumes.prev_startPage, resumes.prev_name))
            extractor.new_resume()

        extractor.extract(resumes.cur_content)

        progress(filename, resumes.curPage, resumes.totalPage)
        # Debugging
        # output.write(filename + ' Page ' + str(resumes.curPage) + ': ' + str(resumes.get_info()) + '\n')

    data_handler.store(filename, resumes.get_info(), extractor.get_skills())
    output.write('%s %d: %s\n' % (filename, resumes.cur_startPage, resumes.cur_name))
    output.close()

