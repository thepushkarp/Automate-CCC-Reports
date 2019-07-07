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
chromeOptions = Options()
chromeOptions.add_argument('--log-level=3') # Does not displays logs
chromeOptions.add_argument('--headless') # Runs Chrome in headless mode.
chromeOptions.add_argument('--no-sandbox') # Bypass OS security model
chromeOptions.add_argument('--disable-gpu') # Applicable to Windows only
chromeOptions.add_argument('--disable-extensions')
path = 'add path to Chrome Driver here'
if not os.path.exists(path):
	print('Please add the path to Chrome Driver in line no. 36 postGen.py')
	sys.exit()
driver = webdriver.Chrome(path, options = chromeOptions)

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
leastAcc = ', '.join([problemCodes[i] for i, x in enumerate(accuracies) if x == min(accuracies)])
mostAcc = ', '.join([problemCodes[i] for i, x in enumerate(accuracies) if x == max(accuracies)])
leastSub = ', '.join([problemCodes[i] for i, x in enumerate(submissions) if x == min(submissions)])
mostSub = ', '.join([problemCodes[i] for i, x in enumerate(submissions) if x == max(submissions)])

# Timings
duration = urlSoup.find('strong', string = 'Duration: ').next_element.next_element.strip(' \" ')
startTime = urlSoup.find('strong', string = 'Start time: ').next_element.next_element.strip(' \" ')
endTime = urlSoup.find('strong', string = 'End time: ').next_element.next_element.strip(' \" ')

# Contest style
contestStyle = rankurlSoup.select('.rank-style-head a')[0].getText().rstrip(' Ranklist ')

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

# Template of post
template = f'Greetings from the CodeChef Campus Chapter!\n\n' + \
f'We are proud to announce the success of our {contestStyle} contest, {contestName}, which was held ' + \
f'for {duration} from {startTime} to {endTime}.\n\n' + \
f'The contest had a total of {numberOfProblems} problems.' + \
f'The problem breakdown after the contest is as follows:\n' + \
f'• Most Accuracy - {mostAcc} ({max(accuracies)}% Accuracy)\n' + \
f'• Least Accuracy - {leastAcc} ({min(accuracies)}% Accuracy)\n' + \
f'• Most Submissions - {mostSub} ({max(submissions)} Submissions)\n' + \
f'• Least Submissions - {leastSub} ({min(submissions)} Submissions)\n\n' + \
f'The problems are available for practice at: {url}\n\n' + \
f'We hope that we were able to trigger your brainstorming skills and bring up your enthusiasm ,' + \
f'motivating you to continue with Competitive Programming. We aim to give our 100% in organising ' + \
f'every contest and achieve a next level every other time. Thank you for your participation and support.\n\n' + \
f'We would like to congratulate the winner, 🏆 {names[0]} ({usernames[0]}), who scored {scores[0]} ' + \
f'points and is on the top of the leaderboard.🎉😉.\n\n' + \
f'The top 5 in the leaderboard are :\n' + \
f'1) {names[0]} ({usernames[0]}), {institutes[0]} - {scores[0]} points\n' + \
f'2) {names[1]} ({usernames[1]}), {institutes[1]} - {scores[1]} points\n' + \
f'3) {names[2]} ({usernames[2]}), {institutes[2]} - {scores[2]} points\n' + \
f'4) {names[3]} ({usernames[3]}), {institutes[3]} - {scores[3]} points\n' + \
f'5) {names[4]} ({usernames[4]}), {institutes[4]} - {scores[4]} points\n\n' + \
f'We extend a hearty Congratulations to all the participants!\n\n' + \
f'The 250 CodeChef Laddus 🎁 have been given to the top 3 in the leaderboard😋.\n\n' + \
f'We would like to thank CodeChef😁 for giving us the platform to host this competition.\n\n' + \
f'Stay tuned, for the solution and editorials of the problems.\n\n' + \
f'We also encourage you to leave your reviews of the contest in the comments!😁'

# Saving post as .txt
fileName = re.sub(' ', '-', contestName)
postFile = open(os.path.join('posts', f'{fileName}.txt'), mode = 'w', encoding = 'utf-8')
postFile.write(template)
postFile.close()
print(f'\nPost saved as {fileName}.txt')
