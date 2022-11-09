import urllib.request
import shutil
# import os

def get_teams():
	with open('cbbscorebot/team_list.txt','r') as imp_file:
		lines=imp_file.readlines()
	flairs={}
	rank_names={}
	for line in lines:
		(team,flair,rank_name)=line.replace('\n','').split(',')
		flairs[team]=flair
		rank_names[rank_name]=team
	return flairs,rank_names

def get_rcbb_poll():
	(flairs,rank_names)=get_teams()
	url='http://cbbpoll.com/'
	with urllib.request.urlopen(url) as response, open ('cbbscorebot/ranking.html', 'wb') as out_file:
		shutil.copyfileobj(response, out_file)
	with open('cbbscorebot/ranking.html','r') as imp_file:
		lines=imp_file.readlines()
	ranking,headerranking,first_place_votes=[],[],[]
	i=1
	while i<125:
		first_place_votes.append('('+str(i)+')')
		i=i+1

	for line in lines:
		if "<td><span class='team-name'>" in line:
			# Rank
			team_rank=lines[lines.index(line)-1].replace('<td>','').replace('</td>','')
			# Votes
			team_vote=lines[lines.index(line)+1].replace('<td>','').replace('</td>','')
			# Team, FPV
			line=line.replace('&#39;',"'").replace('&#38;','&')
			begin=line.find('></span>')
			end=line.find('</span></td>')
			team=line[begin+9:end]
			for vote in first_place_votes:
				if vote in team:
					team=team.replace(vote,'')
					team_fpv=vote
					break
			else:
				team_fpv=''
			
			ranking.append("#"+str(int(team_rank))+"|"+flairs[rank_names[team.replace('&amp;','&')]]+"|"+team.replace('&amp;','&')+" "+team_fpv+"|"+str(int(team_vote)))
			
			headerranking.append(flairs[rank_names[team.replace('&amp;','&')]])
			
	# os.remove('cbbscorebot/ranking.html')
	with open('cbbscorebot/ranking.txt','w') as f:
		for team in ranking:
			f.write(team+'\n')
		
	with open('cbbscorebot/headerranking.txt','w') as f:
		for team in headerranking:
			if team == headerranking[-1]:
				f.write(team)
			else:
				f.write(team+' ')

try:
	get_rcbb_poll()
except:
	print("Failed to Pull cbb poll")
	quit()
quit()
