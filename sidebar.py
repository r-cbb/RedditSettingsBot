from urllib.request import urlopen, Request
import json
import time
from fake_useragent import UserAgent
import html
import reddit_login
import urllib.request
import shutil
import os
import re
import strings
import time

def scriptlogin():
	r = reddit_login.login()
	return r
	
def get_teams():
	with open('settingsbot/team_list.txt','r') as imp_file:
		lines=imp_file.readlines()
	flairs={}
	rank_names={}
	for line in lines:
		(team,flair,rank_name)=line.replace('\n','').split(',')
		flairs[team]=flair
		rank_names[rank_name]=team
	return flairs,rank_names
	
def get_gamethreads(r):
	submissions = r.redditor('cbbbot').submissions.new()
	
	url = {}
	# botposttime = {}
	
	for submission in submissions:
		link = submission.permalink
		title = submission.title
		time_created = submission.created_utc
		
		url[title]=link
		# botposttime[url]=time_created
	return url # ,botposttime
	

def getrankings():
	with open('settingsbot/ranking.txt','r') as imp_file:
		lines=imp_file.readlines()
	sidebarrankings='\n'
	for line in lines:
		sidebarrankings += line
	return sidebarrankings
		
def getheaderrankings():
	with open('settingsbot/headerranking.txt','r') as imp_file:
		lines=imp_file.readlines()
	headerranking='#### '
	for line in lines:
		headerranking += line
	return headerranking
	
def getheaderrankingslist():
	with open('settingsbot/headerranking.txt','r') as imp_file:
		lines=imp_file.readlines()
	flairs = lines[0].split(' ')
	ranking = []
	i = 1
	while i<26:
		ranking.append(str(i))
		i=i+1
	n = 0
	rankings={}
	for flair in flairs:
		rankings[flair]=str(ranking[n])
		n=n+1
	return rankings
				
def updateschedule(r):

	MODE_ACTIVE = 0
	MODE_INACTIVE = 1
	GAME_STATUS_PRE = 0
	GAME_STATUS_IN = 1
	GAME_STATUS_POST = 2
	
	req = Request("http://www.espn.com/mens-college-basketball/scoreboard/_/group/50/?t=" + str(time.time()))
	req.headers["User-Agent"] = UserAgent(verify_ssl=False).chrome

	# Load data
	scoreData = urlopen(req).read().decode("utf-8")
	scoreData = scoreData[scoreData.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):]
	scoreData = json.loads(scoreData[:scoreData.find('};')+1])

	games = dict()
	
	allgamestr = ''
	
	(teams,rank_names)=get_teams()
	url=get_gamethreads(r)
	teamranking = getheaderrankingslist()
	
	for event in scoreData['events']:
		game = dict()

		game["date"] = event['date']
		status = event['status']['type']['state']
		if status == "pre":
			game['status'] = GAME_STATUS_PRE
		elif status == "in":
			game['status'] = GAME_STATUS_IN
		else:
			game['status'] = GAME_STATUS_POST
			
		team1 = html.unescape(event['competitions'][0]['competitors'][0]['team']['location'])
		tid1 = event['competitions'][0]['competitors'][0]['id']
		score1 = int(event['competitions'][0]['competitors'][0]['score'])
		team1abv = event['competitions'][0]['competitors'][0]['team']['abbreviation']
		team2 = html.unescape(event['competitions'][0]['competitors'][1]['team']['location'])
		tid2 = event['competitions'][0]['competitors'][1]['id']
		score2 = int(event['competitions'][0]['competitors'][1]['score'])
		team2abv = event['competitions'][0]['competitors'][1]['team']['abbreviation']

		# Hawaii workaround
		if team1 == "Hawai'i":
			team1 = "Hawaii"
		if team2 == "Hawai'i":
			team2 = "Hawaii"

		homestatus = event['competitions'][0]['competitors'][0]['homeAway']

		if homestatus == 'home':
			game['hometeam'], game['homeid'], game['homeabv'], game['homescore'], game['awayteam'], game['awayid'], game['awayabv'], game['awayscore'] =\
				team1, tid1, team1abv, score1, team2, tid2, team2abv, score2
		else:
			game['hometeam'], game['homeid'], game['homeabv'], game['homescore'], game['awayteam'], game['awayid'], game['awayabv'], game['awayscore'] = \
				team2, tid2, team2abv, score2, team1, tid1, team1abv, score1

		game['time'] = event['status']['type']['shortDetail']
		
		if game['status'] == GAME_STATUS_PRE:
			searchedstring = re.search(' - (.*) EST',game['time'])
			gametime = searchedstring.group(1)
		elif game['status'] == GAME_STATUS_IN and game['time'] != "Halftime" and game['time'] != "Delayed":
			gametime = game['time'].replace(" - "," (") + ")"
		else:
			gametime = game['time']
		
		if team1 in teams.keys():
			team1flair = teams[team1]
		else:
			team1flair = "Non D1"
			# team1flair = team1
				
		if team1flair in teamranking.keys():
			team1flair = "^#"+str(teamranking[team1flair])+' '+team1flair
			
		if team2 in teams.keys():
			team2flair = teams[team2]
		else:
			team2flair = "Non D1"
			# team2flair = team2
		
		if team2flair in teamranking.keys():
			team2flair = "^#"+str(teamranking[team2flair])+' '+team2flair
		
		gamestring = gametime + " | " + team1flair + " | " + team2flair + " | "

		try:
			game['network'] = event['competitions'][0]['broadcasts'][0]['names'][0]
			
			if game['network'] in strings.tv_flairs.keys():
				networkstring=strings.tv_flairs[game['network']]
			else:
				networkstring=game['network']
			
			gamestring += networkstring + " | "
			
			# gamestring += game['network'] + " | "
			
		except:
			gamestring += " | "

		for key in url.keys():
			(awaykey,homekey)=str(key).replace('[Game Thread] ','').split('@')
			
			if team1 == homekey and team2==homekey[0:len(team2)] and homekey[len(team2)+1:].startswith(' ('):
				gamestring += "[" + str(score1) + "-" + str(score2) + "](" + url[key] + ")"
				break
		else:
			gamestring += str(score1) + "-" + str(score2)
		
		allgamestr += gamestring + '\n'
		
	return allgamestr

def updatesidebar():
	r = scriptlogin()
	
	sidebarstring = strings.PreTop25 + getrankings() + strings.BetweenTop25andSchedule + updateschedule(r) + getheaderrankings() + strings.PostTop25Header
	
	settings=r.subreddit('cbbprivateflairtest').mod.settings()
	
	if sidebarstring != settings["description"]:
		print('Does Not Equal, Resetting')
		r.subreddit('cbbprivateflairtest').mod.update(description=sidebarstring)
	else:
		print('Doing Nothing, As they are the same')
	
while True:
	updatesidebar()
	print('Sleeping for 180 seconds')
	time.sleep(60)
	print('Sleeping for 120 seconds')
	time.sleep(60)
	print('Sleeping for 60 seconds')
	time.sleep(60)
	
