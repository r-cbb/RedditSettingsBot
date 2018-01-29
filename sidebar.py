from urllib.request import urlopen, Request
from fake_useragent import UserAgent
import json
import time
import html
import re
import strings
import reddit_login

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
		# botposttime = {}
		
		for submission in submissions:
			link = submission.shortlink
			title = submission.title
			time_created = submission.created_utc
			
			url[title]=link
			# botposttime[url]=time_created
		return url # ,botposttime
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
				
def updateschedule(r):

	MODE_ACTIVE = 0
	MODE_INACTIVE = 1
	GAME_STATUS_PRE = 0
	GAME_STATUS_IN = 1
	GAME_STATUS_POST = 2
	
	try:
		req = Request("http://www.espn.com/mens-college-basketball/scoreboard/_/group/50/?t=" + str(time.time()))
		req.headers["User-Agent"] = UserAgent(verify_ssl=False).chrome
	except:
		print("Failed to Pull ESPN json file")
		raise

	# Load data
	scoreData = urlopen(req).read().decode("utf-8")
	scoreData = scoreData[scoreData.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):]
	scoreData = json.loads(scoreData[:scoreData.find('};')+1])

	games = dict()
	
	allgamestr = ''
	top25gamestr = ''
	hasgamethreadstr = ''
	restgamestr = ''
	
	(teams,rank_names)=get_teams()
	url=get_gamethreads(r)
	teamranking = getheaderrankingslist()
	
	for event in scoreData['events']:
		team1in25 = False
		team2in25 = False
		hasgamethread = False
		
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
		elif game['status'] == GAME_STATUS_IN and game['time'] != "Halftime" and game['time'] != "Delayed" and game['time'] != "End of 2nd":
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
			team1in25 = True
			
		if team2 in teams.keys():
			team2flair = teams[team2]
		else:
			team2flair = "Non D1"
			# team2flair = team2
		
		if team2flair in teamranking.keys():
			team2flair = "^#"+str(teamranking[team2flair])+' '+team2flair
			team2in25 = True
		
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
			
			# print("HomeKey:" + homekey[0:len(team1)]+". Home:" + team1+". "+homekey[len(team1)-1:])
			# print()
			# print(homekey[len(team2)-1:])
			
			# time.sleep(0.1)
			
			# if team2 == awaykey[:-1] and team1 == homekey[0:len(team1)] and homekey[len(team1)-1:].startswith('('):
			if team2 == awaykey[:-1] and team1 == homekey[0:len(team1)] and len(homekey[len(team1):]) <= 14:
				# print("AwayKey:"+awaykey[:-1]+". Away:"+team2+".")
				# print("HomeKey:" + homekey[0:len(team1)]+". Home:" + team1+". Rest of Key: "+homekey[len(team1):])
				gamestring += "[" + str(score1) + "-" + str(score2) + "](" + url[key] + ")"
				hasgamethread = True
				break
		else:
			gamestring += str(score1) + "-" + str(score2)
		
		if team1in25 == True or team2in25 == True:
			top25gamestr += gamestring + '\n'
		elif hasgamethread == True:
			hasgamethreadstr += gamestring + '\n'
			restgamestr += gamestring + '\n'
		else:
			restgamestr += gamestring + '\n'
		
	if top25gamestr != '':
		allgamestr = " ---- | **Ranked** | **Games** | ---- | ----  \n" + top25gamestr + "---- | **All** | **Games** | ---- | ---- \n" + restgamestr
	else:
		allgamestr = restgamestr
	
	if len(allgamestr)-len([m.start() for m in re.finditer('\n',allgamestr)]) > 6250:
		allgamestr = " ---- | **Ranked** | **Games** | ---- | ----  \n" + top25gamestr + "---- | **Has** | **Game** | **Thread** | ---- \n" + hasgamethreadstr
		if len(allgamestr)-len([m.start() for m in re.finditer('\n',allgamestr)]) > 6250:
			allgamestr = " ---- | **Ranked** | **Games** | ---- | ----  \n" + top25gamestr
		
	return allgamestr

def updatesidebar():
	r = scriptlogin()
	
	# sidebarstring = strings.PreTop25 + getrankings() + strings.BetweenTop25andSchedule + updateschedule(r) + getheaderrankings() + strings.PostTop25Header
	sidebarstring = strings.PreTop25 + getrankings() + strings.BetweenTop25andSchedule + updateschedule(r) + "#### 200,000 Subscribers! \n" + strings.PostTop25Header
	
	settings=r.subreddit('cbbprivateflairtest').mod.settings()
	
	if sidebarstring != settings["description"]:
		print('Does Not Equal, Resetting')
		r.subreddit('cbbprivateflairtest').mod.update(description=sidebarstring)
	else:
		print('Doing Nothing, As they are the same')
	
try:
	updatesidebar()
except:
	print('Failed to Update Sidebar')
	quit()
quit()
