from urllib.request import urlopen
import json
import reddit_login
import cbbpolldata

SUBREDDIT = 'collegebasketball'
 
# Main Program Call                
def parse_rcbb_poll():
    (flairs,rank_names)=cbbpolldata.get_teams()

    ranking,receivingvotes=[],[]

    top25rank,currentweek = cbbpolldata.loaddata(cbbpolldata.webrequest())

    for i in range(len(top25rank)):
        team = top25rank[i]['shortName']
        team_rank = top25rank[i]['rank']
        team_vote = top25rank[i]['points']
        if top25rank[i]['firstPlaceVotes'] == 0:
            team_fpv = ''
        else:
            team_fpv = "("+str(top25rank[i]['firstPlaceVotes'])+")"
        
        teamstring = team.replace('&amp;','&')
        
        if team_rank <= 25:
            ranking.append("#"+str(int(team_rank))+"|"+flairs[rank_names[teamstring]]+"|"+team.replace('&amp;','&')+" "+team_fpv+"|"+str(int(team_vote)))
        else:
            receivingvotes.append(flairs[rank_names[teamstring]]+" "+team.replace('&amp;','&')+" "+team_fpv+" "+str(int(team_vote)))
    
    top25string = ''
    receivingvotesstring = ''
    
    for top25 in ranking:
        top25string = top25string + top25 + "\n"
    
    for recvote in receivingvotes:
        receivingvotesstring = receivingvotesstring +recvote
        
        if recvote != receivingvotes[-1]:
            receivingvotesstring = receivingvotesstring + ", "
        
    return top25string, receivingvotesstring, currentweek

def parse_rcbb_poll_test():
    flairs_temp,rank_names_temp,cbbnames=cbbpolldata.get_teams_test()
    (flairs,rank_names)=flairs_temp,rank_names_temp

    ranking,receivingvotes=[],[]

    print(flairs)
    print(rank_names)

    for i in cbbnames:        
        i = i.replace('&amp;','&')
        
        print(i)
        print(flairs[rank_names[i]])
        
    exit()

        
def createPostText():

    top25string, receivingvotesstring, currentweek = parse_rcbb_poll()

    StartText = """Rank||Team (First Place Votes)|Score
:--:|:--:|:---|:---\n"""
    EndText = """Individual ballot information can be found at [https://www.cbbpoll.net/](https://www.cbbpoll.net/) by clicking on individual usernames from the homepage. 
    
Please feel free to discuss the poll results along with individual ballots, but **please be respectful of others' opinions, remain civil**, and remember that these are not professionals, just fans like you."""

    PostTitle = 'UserPoll: Week ' + currentweek
    PostString = StartText + top25string + "\n\n Receiving Votes:" + receivingvotesstring + "\n\n" + EndText
    
    return PostTitle, PostString

def PostPoll():
    posttitle,posttext = createPostText()
    
    r = reddit_login.scriptlogin(2)
    
    submission = r.subreddit(SUBREDDIT).submit(title=posttitle,selftext=posttext)

    