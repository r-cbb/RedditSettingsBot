from urllib.request import urlopen, Request
import json

#Get Team List of current active teams.  cbbpoll.net, espn, r/collegebasketball, and kenpom (Unused)
def get_teams():
    with open('data/team_list.txt','r') as imp_file:
        lines=imp_file.readlines()
    flairs={}
    rank_names={}
    for line in lines:
        (team,flair,rank_name,kenpom)=line.replace('\n','').split(',')
        flairs[team]=flair
        rank_names[rank_name]=team
    return flairs,rank_names

def get_teams_test():
    with open('data/team_list.txt','r') as imp_file:
        lines=imp_file.readlines()
    flairs={}
    rank_names={}
    rank_names_temp=[]
    for line in lines:
        (team,flair,rank_name,kenpom)=line.replace('\n','').split(',')
        flairs[team]=flair
        rank_names[rank_name]=team
        rank_names_temp.append(rank_name)
    print(rank_name)
    return flairs,rank_names,rank_names_temp

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
    
    #Top 25 Search
    start_str = 'type="application/json">'
    start_index = line.find(start_str)
    data = json.loads(line[start_index + len(start_str): line.find('</script>', start_index)])
    top25rank = data['props']['pageProps']['userpoll']
    
    #Week Search
    start_str = 'Week <!-- -->'
    end_str = '<!-- --> Poll'
    start_index = line.find(start_str)
    
    currentweek = line[start_index + len(start_str):line.find(end_str)]

    return top25rank, currentweek
    