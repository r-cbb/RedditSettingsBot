import cbbpolldata

# Main Program Call                
def get_rcbb_poll():
    (flairs,rank_names)=cbbpolldata.get_teams()

    ranking,headerranking=[],[]

    top25rank, currentweek = cbbpolldata.loaddata(cbbpolldata.webrequest())

    for i in range(25):
        team = top25rank[i]['shortName']
        team_rank = top25rank[i]['rank']
        team_vote = top25rank[i]['points']
        if top25rank[i]['firstPlaceVotes'] == 0:
            team_fpv = ''
        else:
            team_fpv = "("+str(top25rank[i]['firstPlaceVotes'])+")"
        
        teamstring = team.replace('&amp;','&')
        
        ranking.append("#"+str(int(team_rank))+"|"+flairs[rank_names[teamstring]]+"|"+team.replace('&amp;','&')+" "+team_fpv+"|"+str(int(team_vote)))
        headerranking.append(flairs[rank_names[teamstring]])
            
    with open('data/ranking.txt','w') as f:
        for team in ranking:
            f.write(team+'\n')
        
    with open('data/headerranking.txt','w') as f:
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

