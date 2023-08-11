from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from datetime import date
import pandas as pd
import re
import sys

class customHtml():
    def __init__(self, file_path):
        self.file_path = file_path
        self.html_data = None
        self.bs_data = None
        self.rank_tb = None
        self.ranking = None
        self.update = None

        with open(self.file_path, encoding='utf-8') as f:
            self.html_data = f.read()

        self.bs_data = bs(self.html_data, 'html.parser')
        self.rank_tb = self.bs_data.find('table', attrs={'class':'zvh5L2Gz'})

        kw_head = '<p>\s\(更新日時：'
        kw_date = '[1-9][0-9]{3}/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])'
        kw_foot = '\s([0-9]|[0-2][0-9]):[0-5][0-9]\)</p>'
        keyword = kw_head + kw_date + kw_foot

        result = []
        
        for _, e in enumerate(self.bs_data.find_all('p')):
            if re.fullmatch(keyword, str(e)) is not None:
                result.append(re.search(kw_date, str(e)).group())

        if len(result) == 1:
            date_type = dt.strptime(result[0], '%Y/%m/%d')
            self.update = date(date_type.year, date_type.month, date_type.day)
        else:
            print('Do not match update date search')
            sys.exit(10)
    
    def getRank(self):

        body = self.rank_tb.tbody
        body_text = [s for s in body.find_all('tr')]
        
        col = []
        for _, s in enumerate(body_text):
            col.append(
                [
                    self.update, 
                    s.find_all('li')[0].text, 
                    float(s.find_all('span', attrs={'class':'_3rXWJKZF'})[0].text.replace(',', '')), 
                    float(s.find_all('span', attrs={'class':'_3rXWJKZF'})[1].text.replace(',', '')), 
                    float(s.find_all('span', attrs={'class':'_3rXWJKZF'})[2].text), 
                    int(s.find_all('span', attrs={'class':'_3rXWJKZF'})[3].text.replace(',', ''))
                ]
            )

        self.ranking = pd.DataFrame(data=col)

        return self.ranking

    def existTBL(self):
        elems = self.bs_data.select('#item > div > p')

        if len(elems) == 0:
            return True
        elif len(elems) == 1:
            return False
        else:
            print('two or more elements found.')
            sys.exit(11)
