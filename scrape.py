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
        pass

    @staticmethod
    def download_pages(contest_url, rankpage_url):
        '''
        Function to open and download webpage.

        Parameters:
        contest_url (string): Contest landing page URL
        rankpage_url (string): Contest ranking page URL

        Returns:
        url_soup (class 'bs4.BeautifulSoup'): BeautifulSoup object of Contest landing page URL
        rankurl_soup (class 'bs4.BeautifulSoup'): BeautifulSoup object of Contest ranking page URL
        '''

        driver_path = 'Add path to Chrome Driver here'
        if not path.exists(driver_path):
            print('\nPlease add the path to Chrome Driver in line no. 31 of scrape.py')
            sys.exit()

        print('\nDownloading contest pages...')

        chrome_options = Options()
        chrome_options.add_argument('--log-level=3') # Does not displays logs
        chrome_options.add_argument('--headless') # Runs Chrome in headless mode
        chrome_options.add_argument('--no-sandbox') # Bypass OS security model
        chrome_options.add_argument('--disable-gpu') # Applicable to Windows only
        chrome_options.add_argument('--disable-extensions')

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

    @classmethod
    def scrape(cls, url, contest_type):
        '''
        Function to scrape data and save them in contest variables.

        Parameters:
        url (string): Contest landing page URL
        contest_type (int): Type of contest (1 for Solo and 2 for Team)
        '''

        cls.url = url
        cls.contest_type = contest_type

        # Contest ranings URL
        spliturl = url.split('/')
        spliturl.insert(3, 'rankings')
        cls.rankurl = '/'.join(spliturl)

        url_soup, rankurl_soup = cls.download_pages(cls.url, cls.rankurl)

        print('Scraping contest pages...')

        # Contest name
        cls.contest_name = url_soup.find('title').getText().rstrip(' CodeChef ').rstrip(' |')

        # Contest problem containers in <tr> tag
        problems = url_soup.select('.plr15 tbody tr')[:]

        # Number of problems
        cls.problem_count = len(problems)

        # Problem Codes, Submissions and Accuracies
        cls.problem_codes = [] # List of Problem Codes
        cls.submissions = [] # List of number of sccess submissions of problems
        cls.accuracies = [] # List of accuracies of problems

        for problem in problems:
            problem_code = problem.find('td', class_=None).getText().strip('\n')
            cls.problem_codes.append(problem_code)
            submission = int(problem.select('td.num div div')[0].getText())
            cls.submissions.append(submission)
            accuracy = float(problem.select('td.num div a')[0].getText())
            cls.accuracies.append(accuracy)

        # Minimum and maximum accuracies and submissions
        cls.least_acc = ', '.join([cls.problem_codes[i] for i, x in enumerate(cls.accuracies) \
            if x == min(cls.accuracies)])
        cls.most_acc = ', '.join([cls.problem_codes[i] for i, x in enumerate(cls.accuracies) \
            if x == max(cls.accuracies)])
        cls.least_sub = ', '.join([cls.problem_codes[i] for i, x in enumerate(cls.submissions) \
            if x == min(cls.submissions)])
        cls.most_sub = ', '.join([cls.problem_codes[i] for i, x in enumerate(cls.submissions) \
            if x == max(cls.submissions)])

        # Timings
        cls.duration = url_soup.find('strong', string='Duration: ').next_element.next_element\
            .strip(' \" ')
        cls.start_time = url_soup.find('strong', string='Start time: ').next_element.next_element\
            .strip(' \" ')
        cls.end_time = url_soup.find('strong', string='End time: ').next_element.next_element\
            .strip(' \" ')

        # Contest style
        cls.contest_style = rankurl_soup.select('.rank-style-head a')[0].getText()\
            .rstrip(' Ranklist ')

        # Ranking containers in <tr> tag
        ranks = rankurl_soup.select('.table-component tbody tr')[0:5]

        # Rankings with name, username, institute and score
        cls.names = [] # Names of top 5 in leaderboard
        cls.usernames = [] # Usernames of top 5 in leaderboard
        cls.institutes = [] # Institutes of top 5 in leaderboard
        cls.scores = [] # Scores of top 5 in leaderboard

        for user in ranks:
            name = user.find('div', class_='user-name')['title']
            cls.names.append(name)
            if contest_type == 1:
                username = user.find('span', class_=None).getText()
            elif contest_type == 2:
                username = user.select('.user-name a')[0].getText()
            cls.usernames.append(username)
            institute = user.find('div', class_='institute').getText()
            cls.institutes.append(institute)
            score = user.select('.num')[1].find('div').getText()
            score = int(re.sub(r'\s*[-]\s*\(\d+\)\s*', '', score).strip(' \n '))
            cls.scores.append(score)
