#import urllib.request
from urllib.request import urlopen, Request
import shutil
import json

#Get Team List of current active teams.  cbbpoll.net, espn, r/collegebasketball, and kenpom (Unused)
def get_teams():
    with open('cbbscorebot/team_list.txt','r') as imp_file:
        lines=imp_file.readlines()
    flairs={}
    rank_names={}
    for line in lines:
        (team,flair,rank_name,kenpom)=line.replace('\n','').split(',')
        flairs[team]=flair
        rank_names[rank_name]=team
    return flairs,rank_names

#Request Webpage
def webrequest():
    try:
        req = Request("https://www.cbbpoll.net/")
        req.headers["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'
    except:
        print("Failed to Pull cbbpoll json file")
        raise

    return req
    
#Pull the json
def loaddata(req):
    line = urlopen(req).read().decode('utf-8')
    start_str = 'type="application/json">'
    start_index = line.find(start_str)
    data = json.loads(line[start_index + len(start_str): line.find('</script>', start_index)])
    top25rank = data['props']['pageProps']['userpoll']

    return top25rank              
                
# Main Program Call                
def get_rcbb_poll():
    (flairs,rank_names)=get_teams()

    ranking,headerranking,first_place_votes=[],[],[]

    top25rank = loaddata(webrequest())

    for i in range(25):
        team = top25rank[i]['shortName']
        team_rank = top25rank[i]['rank']
        team_vote = top25rank[i]['points']
        if top25rank[i]['firstPlaceVotes'] == 0:
            team_fpv = ''
        else:
            team_fpv = "("+str(top25rank[i]['firstPlaceVotes'])+")"
                
        ranking.append("#"+str(int(team_rank))+"|"+flairs[rank_names[team.replace('&amp;','&')]]+"|"+team.replace('&amp;','&')+" "+team_fpv+"|"+str(int(team_vote)))
        headerranking.append(flairs[rank_names[team.replace('&amp;','&')]])
            
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

