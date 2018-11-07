from urllib.request import urlopen, Request
from fake_useragent import UserAgent
import json
import time
import html
import re
import reddit_login

MODE_ACTIVE = 0
MODE_INACTIVE = 1
GAME_STATUS_PRE = 0
GAME_STATUS_IN = 1
GAME_STATUS_POST = 2
	

def scriptlogin():
	try:
		r = reddit_login.login()
		return r
	except:
		print("Failed to Login")
		raise
	
def get_teams():
	try:
		with open('cbbscorebot/team_list.txt','r') as imp_file:
			lines=imp_file.readlines()
		flairs={}
		rank_names={}
		for line in lines:
			(team,flair,rank_name)=line.replace('\n','').split(',')
			flairs[team]=flair
			rank_names[rank_name]=team
		return flairs,rank_names
	except:
		print("Failed to finish get_teams")
		raise
	
def get_gamethreads(r):
	try:
		submissions = r.redditor('cbbbot').submissions.new()
		
		url = {}
		
		for submission in submissions:
			link = submission.shortlink
			title = submission.title
			time_created = submission.created_utc
			
			url[title]=link
			
		return url
	except:
		print("Failed to Grab cbbbot Submissions")
		raise

def getrankings():
	try:
		with open('cbbscorebot/ranking.txt','r') as imp_file:
			lines=imp_file.readlines()
		sidebarrankings='\n'
		for line in lines:
			sidebarrankings += line
		return sidebarrankings
	except:
		print("Failed to Pull Sidebar Team Rankings")
		raise
		
def getheaderrankings():
	try:
		with open('cbbscorebot/headerranking.txt','r') as imp_file:
			lines=imp_file.readlines()
		headerranking='#### '
		for line in lines:
			headerranking += line
		return headerranking
	except:
		print("Failed to Pull Header Team Rankings")
		raise
	
def getheaderrankingslist():
	try:
		with open('cbbscorebot/headerranking.txt','r') as imp_file:
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
	except:
		print("Failed to Create a list of ranked flairs")
		raise
		
def createconfigfile(r):
	try:
		wikipage = r.subreddit('collegebasketball').wiki['config_scorebot']
	
		with open('scorebot_config.py','w',newline='') as out_file:
			for line in wikipage.content_md:
				out_file.write(line)
	except:
		print("Failed to read wiki")
		raise
		
def setteamflair(team, teams, teamranking, teamflag):
	teamflair = ''
	if team in teams.keys():
		teamflair = teams[team]
	else:
		teamflair = "Non D1"
		#nond1list(team)
	
	if teamflair in teamranking.keys():
		teamflair = "^#"+str(teamranking[teamflair])+' '+teamflair
		teamflag = True
		
	return teamflair, teamflag

def nond1list(team):
	with open('cbbscorebot/nond1_list.txt','a',newline='') as out_file:
		out_file.write(team + '\n')

def pulljson():
	try:
		req = Request("http://www.espn.com/mens-college-basketball/scoreboard/_/group/50/?t=" + str(time.time()))
		#req.headers["User-Agent"] = UserAgent(verify_ssl=False).chrome
		req.headers["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'
	except:
		print("Failed to Pull ESPN json file")
		raise
	
	return req

def loaddata(req):
	# Load data
	scoreData = urlopen(req).read().decode("utf-8")
	scoreData = scoreData[scoreData.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):]
	scoreData = json.loads(scoreData[:scoreData.find('};')+1])
	
	return scoreData

def parsevent(event):
	game = dict()
	
	#GameDate
	game["date"] = event['date']
	
	#Before, During, or After Game
	status = event['status']['type']['state']
	if status == "pre":
		game['status'] = GAME_STATUS_PRE
	elif status == "in":
		game['status'] = GAME_STATUS_IN
	else:
		game['status'] = GAME_STATUS_POST
	
	#Teams, Shorthand, and Scores
	team1 = html.unescape(event['competitions'][0]['competitors'][0]['team']['location'])
	tid1 = event['competitions'][0]['competitors'][0]['id']
	score1 = int(event['competitions'][0]['competitors'][0]['score'])
	try:
		team1abv = event['competitions'][0]['competitors'][0]['team']['abbreviation']
	except:
		team1abv = "na"
	team2 = html.unescape(event['competitions'][0]['competitors'][1]['team']['location'])
	tid2 = event['competitions'][0]['competitors'][1]['id']
	score2 = int(event['competitions'][0]['competitors'][1]['score'])
	try:
		team2abv = event['competitions'][0]['competitors'][1]['team']['abbreviation']
	except:
		team2abv = "na"
	
	print(team1,tid1,score1,team1abv,team2,tid2,score2,team2abv)

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
	
	try:
		game['network'] = event['competitions'][0]['broadcasts'][0]['names'][0]
	except:
		game['network'] = 'unavailable'
		
	return game

def setgametime(game):
	if game['status'] == GAME_STATUS_PRE:
		if game['time'] == "TBD":
			gametime = "TBD"
		else:
			searchedstring = re.search(' - (.*) EST',game['time'])
			if searchedstring is None:
				searchedstring = re.search(' - (.*) EDT',game['time'])
			gametime = searchedstring.group(1)
	elif game['status'] == GAME_STATUS_IN and game['time'] != "Halftime" and game['time'] != "Delayed" and game['time'] != "End of 2nd":
		gametime = game['time'].replace(" - "," (") + ")"
	else:
		gametime = game['time']
		
	return gametime

def setnetwork(game,gamestring):
	import scorebot_config
	try:	
		if game['network'] == 'unavailable':
			gamestring += " | "
		else:
			if game['network'] in scorebot_config.tv_flairs.keys():
				networkstring=scorebot_config.tv_flairs[game['network']]
			else:
				networkstring=game['network']
		
			gamestring += networkstring + " | "
		
	except Exception as e:
		print(e)
		gamestring += " | "
		
	return gamestring

def addgamethread(url,game,gamestring,hasgamethread):
	for key in url.keys():
		(awaykey,homekey)=str(key).replace('[Game Thread] ','').split('@')
		
		if awaykey.startswith('#'):
			# print('Entered Away If Statement')
			i = 1
			while i < 26:
				# print('#'+str(i))
				if awaykey.startswith('#'+str(i)+' '):
					if i < 10:
						awaykey=awaykey[3:]
					else:
						awaykey=awaykey[4:]
					break
				i = i + 1
			
		if homekey[1:].startswith('#'):
			# print('Entered Home If Statement')
			i = 1
			while i < 26:
				# print('#'+str(i))
				if homekey[1:].startswith('#'+str(i)+' '):
					if i < 10:
						homekey=homekey[4:]
					else:
						homekey=homekey[5:]
					break
				i = i + 1
		else:
			homekey=homekey[1:]
		
		# print("AwayKey:"+awaykey[:-1]+". Away:"+team2+".")
		# print()
		
		# print("HomeKey:" + homekey[0:len(game['hometeam'])]+". Home:" + game['hometeam']+". "+homekey[len(game['hometeam'])-1:])
		# print()
		# print(homekey[len(team2)-1:])
					
		# 14 is the maximum value of the game time in title.
		if game['awayteam'] == awaykey[:-1] and game['hometeam'] == homekey[0:len(game['hometeam'])] and len(homekey[len(game['hometeam']):]) <= 14: 
			# print("AwayKey:"+awaykey[:-1]+". Away:"+game['awayteam']+".")
			# print("HomeKey:" + homekey[0:len(game['hometeam'])]+". Home:" + game['hometeam']+". Rest of Key: "+homekey[len(game['hometeam']):])
			gamestring += "[" + str(game['homescore']) + "-" + str(game['awayscore']) + "](" + url[key] + ")"
			hasgamethread = True
			break
	else:
		gamestring += str(game['homescore']) + "-" + str(game['awayscore'])
		
	return gamestring, hasgamethread
	
def updateschedule(r):
	import scorebot_config

	#Scrape and Load Data from ESPN
	req = pulljson()
	scoreData = loaddata(req)
	
	#Initilize Strings
	allgamestr = ''
	top25gamestr = ''
	hasgamethreadstr = ''
	restgamestr = ''
	
	#Load Teams, Rankings, Gamethreads
	(teams,rank_names)=get_teams()
	url=get_gamethreads(r)
	teamranking = getheaderrankingslist()
	
	for event in scoreData['events']:
		hometeamin25 = False
		awayteamin25 = False
		hasgamethread = False
		
		game = parsevent(event)
		
		gametime = setgametime(game)
		
		# If the team has a flair or is ranked, set the variables as such.		
		hometeamflair, hometeamin25 = setteamflair(game['hometeam'], teams, teamranking, hometeamin25)
		awayteamflair, awayteamin25 = setteamflair(game['awayteam'], teams, teamranking, awayteamin25)
		
		# Start of the schedule line for each game.
		gamestring = gametime + " | " + hometeamflair + " | " + awayteamflair + " | "

		# Adds the network if it is being played on one.  Empty cell otherwise.
		gamestring = setnetwork(game,gamestring)
		
		# Scraping the game threads for the most recent ones.
		gamestring, hasgamethread = addgamethread(url,game,gamestring,hasgamethread)
		
		if hometeamin25 == True or awayteamin25 == True:
			top25gamestr += gamestring + '\n'
		elif hasgamethread == True:
			hasgamethreadstr += gamestring + '\n'
			restgamestr += gamestring + '\n'
		else:
			restgamestr += gamestring + '\n'
	
	# If there is a ranked game, use this.
	if top25gamestr != '':
		allgamestr = " ---- | **Ranked** | **Games** | ---- | ----  \n" + top25gamestr + "---- | **All** | **Games** | ---- | ---- \n" + restgamestr
	elif top25gamestr != '' and restgamestr == '':
		allgamestr = " ---- | **Ranked** | **Games** | ---- | ----  \n" + top25gamestr
	else:
		allgamestr = restgamestr
	
	if len(allgamestr)-len([m.start() for m in re.finditer('\n',allgamestr)]) > scorebot_config.maxlength:
		allgamestr = " ---- | **Ranked** | **Games** | ---- | ----  \n" + top25gamestr + "---- | **Has** | **Game** | **Thread** | ---- \n" + hasgamethreadstr
		if len(allgamestr)-len([m.start() for m in re.finditer('\n',allgamestr)]) > scorebot_config.maxlength:
			allgamestr = " ---- | **Ranked** | **Games** | ---- | ----  \n" + top25gamestr
		
	return allgamestr

#Off Season Time to Season Counter
def timetoseason(top25barflag):
	from datetime import datetime
	seasonstartdate = datetime(2018,11,6,12,30) #This should be manually changed every year.
	numofdays = abs(seasonstartdate - datetime.now()).days
	if top25barflag == 1:
		returnstring = "#### " + str(numofdays) + " Days Until Tipoff"
	else:
		numofhours = round(abs(seasonstartdate - datetime.now()).seconds/3600)
		returnstring = "#### " + str(numofdays) + " Days, " + str(numofhours) + " Hours Until Tipoff"
	return returnstring

def updatesidebar():
	r = scriptlogin()
	createconfigfile(r)
	import scorebot_config
	
	if scorebot_config.top25barflag == 0:
		sidebarstring = scorebot_config.PreTop25 + getrankings() + scorebot_config.BetweenTop25andSchedule + updateschedule(r) + getheaderrankings() + scorebot_config.PostTop25Header
	elif scorebot_config.top25barflag == 1 or scorebot_config.top25barflag == 2:
		sidebarstring = scorebot_config.PreTop25 + getrankings() + scorebot_config.BetweenTop25andSchedule + updateschedule(r) +  timetoseason(scorebot_config.top25barflag) + scorebot_config.PostTop25Header
	else:
		sidebarstring = scorebot_config.PreTop25 + getrankings() + scorebot_config.BetweenTop25andSchedule + updateschedule(r) +  scorebot_config.top25customstring + scorebot_config.PostTop25Header
	
	settings=r.subreddit('collegebasketball').mod.settings()
	
	if sidebarstring != settings["description"]:
		print('Does Not Equal, Resetting')
		r.subreddit('collegebasketball').mod.update(description=sidebarstring)
	else:
		print('Doing Nothing, As they are the same')
	
try:
	updatesidebar()
	quit()
except Exception as e:
	print(e)
	print('Failed to Update Sidebar')
	quit()
