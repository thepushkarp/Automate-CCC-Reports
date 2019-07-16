'''Scrapes the data from contest URL and saves in the variables of the class Contest.'''

from os import path
import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class Contest:
    '''Class for storing  contest variables after scaping.'''

    def __init__(self):
        '''Constructor for initialising contest variables.'''

        self.url = None # Contest URL
        self.contest_type = None # Solo/Team Contest
        self.rankurl = None # Contest rankings URL
        self.contest_name = None # Contest Name
        self.problem_count = 0 # Number of probelms
        self.problem_codes = [] # List of Problem Codes
        self.submissions = [] # List of number of sccess submissions of problems
        self.accuracies = [] # List of accuracies of problems
        self.least_acc = None # Least accurate problem/s
        self.most_acc = None # Most accurate problem/s
        self.least_sub = None # Least successfully submitted solution/s
        self.most_sub = None # Most successfully submitted problems
        self.duration = None # Contest duration
        self.start_time = None # Contest start time
        self.end_time = None # Contest end time
        self.contest_style = None # Contest style - ACM, IOI, Long
        self.names = [] # Names of top 5 in leaderboard
        self.usernames = [] # Usernames of top 5 in leaderboard
        self.institutes = [] # Institutes of top 5 in leaderboard
        self.scores = [] # Scores of top 5 in leaderboard


    def download_pages(self, contest_url, rankpage_url):
        '''Function to open and download webpage.'''

        print('\nDownloading contest pages...')

        chrome_options = Options()
        chrome_options.add_argument('--log-level=3') # Does not displays logs
        chrome_options.add_argument('--headless') # Runs Chrome in headless mode
        chrome_options.add_argument('--no-sandbox') # Bypass OS security model
        chrome_options.add_argument('--disable-gpu') # Applicable to Windows only
        chrome_options.add_argument('--disable-extensions')
        driver_path = 'chromedriver.exe'
        if not path.exists(driver_path):
            print('Please add the path to Chrome Driver in line no. 50 of scrape.py')
            sys.exit()
        driver = webdriver.Chrome(driver_path, options=chrome_options)

        # Open contest page
        driver.get(contest_url)
        url_soup = BeautifulSoup(driver.page_source, 'lxml')

        # Open rankings page
        driver.get(rankpage_url)
        rankurl_soup = BeautifulSoup(driver.page_source, 'lxml')

        # Close browser
        driver.quit()

        return (url_soup, rankurl_soup)


    def scrape(self, url, contest_type):
        '''Function to scrape data and save them in contest variables.'''

        self.url = url
        self.contest_type = contest_type

        # Contest ranings URL
        spliturl = url.split('/')
        spliturl.insert(3, 'rankings')
        self.rankurl = '/'.join(spliturl)

        url_soup, rankurl_soup = self.download_pages(self.url, self.rankurl)

        print('\nScraping contest pages...')

        # Contest name
        self.contest_name = url_soup.find('title').getText().rstrip(' CodeChef ').rstrip(' |')

        # Contest problem containers in <tr> tag
        problems = url_soup.select('.plr15 tbody tr')[:]

        # Number of problems
        self.problem_count = len(problems)

        # Problem Codes, Submissions and Accuracies
        for problem in problems:
            problem_code = problem.find('td', class_=None).getText().strip('\n')
            self.problem_codes.append(problem_code)
            submission = int(problem.select('td.num div div')[0].getText())
            self.submissions.append(submission)
            accuracy = float(problem.select('td.num div a')[0].getText())
            self.accuracies.append(accuracy)

        # Minimum and maximum accuracies and submissions
        self.least_acc = ', '.join([self.problem_codes[i] for i, x in enumerate(self.accuracies) \
            if x == min(self.accuracies)])
        self.most_acc = ', '.join([self.problem_codes[i] for i, x in enumerate(self.accuracies) \
            if x == max(self.accuracies)])
        self.least_sub = ', '.join([self.problem_codes[i] for i, x in enumerate(self.submissions) \
            if x == min(self.submissions)])
        self.most_sub = ', '.join([self.problem_codes[i] for i, x in enumerate(self.submissions) \
            if x == max(self.submissions)])

        # Timings
        self.duration = url_soup.find('strong', string='Duration: ').next_element.next_element\
            .strip(' \" ')
        self.start_time = url_soup.find('strong', string='Start time: ').next_element.next_element\
            .strip(' \" ')
        self.end_time = url_soup.find('strong', string='End time: ').next_element.next_element\
            .strip(' \" ')

        # Contest style
        self.contest_style = rankurl_soup.select('.rank-style-head a')[0].getText()\
            .rstrip(' Ranklist ')

        # Ranking containers in <tr> tag
        ranks = rankurl_soup.select('.table-component tbody tr')[0:5]

        # Rankings with name, username, institute and score
        for user in ranks:
            name = user.find('div', class_='user-name')['title']
            self.names.append(name)
            if contest_type == 1:
                username = user.find('span', class_=None).getText()
            elif contest_type == 2:
                username = user.select('.user-name a')[0].getText()
            self.usernames.append(username)
            institute = user.find('div', class_='institute').getText()
            self.institutes.append(institute)
            score = user.select('.num')[1].find('div').getText()
            score = int(re.sub(r'\s*[-]\s*\(\d+\)\s*', '', score).strip(' \n '))
            self.scores.append(score)
