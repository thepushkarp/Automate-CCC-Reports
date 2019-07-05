import os
import sys
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Contets page
url = input("Enter the contest link:\n")

# Check for errors
try:
	requests.get(url).raise_for_status()
except requests.exceptions.RequestException as excep:
	print(f'\nThere was a problem:\n{excep}')
	sys.exit()

# Rankings page
spliturl = url.split('/')
spliturl.insert(3, 'rankings')
rankurl = '/'.join(spliturl)

# Solo or Team Contest
contestType = 0
while contestType not in range (1,3):
	contestType = int(input("\nEnter the contest type (1 or 2):\n1. Solo Contest\n2. Team Contest\n"))

# Open browser
chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--headless') # Runs Chrome in headless mode.
chrome_options.add_argument('--no-sandbox') # Bypass OS security model
chrome_options.add_argument('--disable-gpu') # Applicable to windows os only
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--disable-extensions')
driver = webdriver.Chrome(options = chrome_options)

# Open contest page
driver.get(url)
urlSoup = BeautifulSoup(driver.page_source, 'lxml')

# Open rankings page
driver.get(rankurl)
rankurlSoup = BeautifulSoup(driver.page_source, 'lxml')

# Close browser
driver.quit()

# Contest name
contestName = urlSoup.find('title').getText().rstrip(' CodeChef ').rstrip(' |')

# Contest problem containers in <tr> tag
problems = urlSoup.select('.plr15 tbody tr')[:]

# Total number of problems
numberOfProblems = len(problems)

# Problem Codes, Submissions and Accuracies
problemCodes = []
submissions = []
accuracies = []
for problem in problems:
	problemCode = problem.find('td', class_ = None).getText().strip('\n')
	problemCodes.append(problemCode)
	submission = int(problem.select('td.num div div')[0].getText())
	submissions.append(submission)
	accuracy = float(problem.select('td.num div a')[0].getText())
	accuracies.append(accuracy)

# Minimum and maximum accuracies and submissions
minAccu = [(problemCodes[i], accuracies[i]) for i, x in enumerate(accuracies) if x == min(accuracies)]
maxAccu = [(problemCodes[i], accuracies[i]) for i, x in enumerate(accuracies) if x == max(accuracies)]
minSub = [(problemCodes[i], submissions[i]) for i, x in enumerate(submissions) if x == min(submissions)]
maxSub = [(problemCodes[i], submissions[i]) for i, x in enumerate(submissions) if x == max(submissions)]

# Timings
duration = urlSoup.find('strong', string = 'Duration: ').next_element.next_element.strip(' \" ')
startTime = urlSoup.find('strong', string = 'Start time: ').next_element.next_element.strip(' \" ')
endTime = urlSoup.find('strong', string = 'End time: ').next_element.next_element.strip(' \" ')

# Contest style
contestStyle = rankurlSoup.select('.rank-style-head a')[0].getText()

# Ranking containers in <tr> tag
ranks = rankurlSoup.select('.table-component tbody tr')[0:5]

# Rankings with name, username, institute and score
names = []
usernames = []
institutes = []
scores = []
for user in ranks:
	name = user.find('div', class_ = 'user-name')['title']
	names.append(name)
	if contestType == 1:
		username = user.find('span', class_ = None).getText()
	elif contestType ==2:
		username = user.select('.user-name a')[0].getText()
	usernames.append(username)
	institute = user.find('div', class_ = 'institute').getText()
	institutes.append(institute)
	score = user.select('.num')[1].find('div').getText()
	score  = int(re.sub(r'\s*[-]\s*\(\d+\)\s*', '', score).strip(' \n '))
	scores.append(score)
