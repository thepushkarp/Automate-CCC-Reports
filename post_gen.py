'''Generates the post from the scraped data and saves as a .txt file'''

from os import path
import sys
import re
import requests
from scrape import Contest


# Contest page
URL = input('Enter the contest link:\n')

# Check for errors
try:
    requests.get(URL).raise_for_status()
except requests.exceptions.RequestException as excep:
    print(f'\nThere was a problem:\n{excep}')
    sys.exit()

# Type of contest - Solo/Team
CONTEST_TYPE = int(input('\nEnter the contest type (1 or 2):\n1. Solo Contest \n2. Team Contest\n'))
if CONTEST_TYPE not in range(1, 3):
    print('Input must be either \'1\' or \'2\'')
    sys.exit()

# Contest Object
CONTEST = Contest()
CONTEST.scrape(URL, CONTEST_TYPE)

print('Generating the post...')


# Template of post
TEMPLATE = f'''Greetings from the IIITV CodeChef Campus Chapter!

We are proud to announce the success of our {CONTEST.contest_style} contest, {CONTEST.contest_name}, \
which was held for {CONTEST.duration} from {CONTEST.start_time} to {CONTEST.end_time}.

The contest had a total of {CONTEST.problem_count} problems.
The problem breakdown after the contest is as follows:
• Most Accuracy - {CONTEST.most_acc} ({max(CONTEST.accuracies)}% Accuracy)
• Least Accuracy - {CONTEST.least_acc} ({min(CONTEST.accuracies)}% Accuracy)
• Most Submissions - {CONTEST.most_sub} ({max(CONTEST.submissions)} Submissions)
• Least Submissions - {CONTEST.least_sub} ({min(CONTEST.submissions)} Submissions)

The problems are available for practice at: {CONTEST.url}

We hope that we were able to trigger your brainstorming skills and bring up your enthusiasm, \
motivating you to continue with Competitive Programming. We aim to give our 100% in organising \
every contest and achieve a next level every other time. Thank you for your participation and \
support.

We would like to congratulate the winner, 🏆 {CONTEST.names[0]} ({CONTEST.usernames[0]}), who \
scored {CONTEST.scores[0]}  points and is on the top of the leaderboard. 🎉😉

The top 5 in the leaderboard are :\n
1) {CONTEST.names[0]} ({CONTEST.usernames[0]}), {CONTEST.institutes[0]} - {CONTEST.scores[0]} \
points
2) {CONTEST.names[1]} ({CONTEST.usernames[1]}), {CONTEST.institutes[1]} - {CONTEST.scores[1]} \
points
3) {CONTEST.names[2]} ({CONTEST.usernames[2]}), {CONTEST.institutes[2]} - {CONTEST.scores[2]} \
points
4) {CONTEST.names[3]} ({CONTEST.usernames[3]}), {CONTEST.institutes[3]} - {CONTEST.scores[3]} \
points
5) {CONTEST.names[4]} ({CONTEST.usernames[4]}), {CONTEST.institutes[4]} - {CONTEST.scores[4]} \
points

We extend a hearty Congratulations to all the participants!

The 250 CodeChef Laddus 🎁 have been given to the top 3 in the leaderboard. 😋

We would like to thank CodeChef 😁 for giving us the platform to host this competition.

Stay tuned, for the solution and editorials of the problems.

We also encourage you to leave your reviews of the contest in the comments! 😁
'''


# Saving the post as .txt
FILENAME = re.sub(' ', '_', CONTEST.contest_name) + '.txt'
POST_FILE = open(path.join('posts', f'{FILENAME}'), mode='w', encoding='utf-8')
POST_FILE.write(TEMPLATE)
POST_FILE.close()

print(f'Post saved as {FILENAME}')
