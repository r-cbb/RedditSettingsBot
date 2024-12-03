import reddit_login

admin_users = ["cinciforthewin","SleveMcDichael4"]

def get_users():
    try:
        with open ('data/user_list.txt','r') as imp_file:
            lines=imp_file.readlines()
        
        username = []
        
        for line in lines:
            username.append(line.replace('\n',''))
        
        return(username)
    except:
        print("Failed to pull username")
        raise

def SendMessage(PollVoters,Reddit):

    for user in admin_users:
        try:
            r.redditor(user).message(subject="Starting /r/Collegebasketball Poll Notifications",message="Starting /r/Collegebasketball User Poll Notifications")
        except:
            print("Failed to message admin user: "+user)
        
    UserError = []

    for Voter in PollVoters:
        try:
            r.redditor(Voter).message(subject="CollegeBasketball UserPoll is now Open!",message="Hello " + Voter + ",\n\n The weekly top 25 poll is now live at https://www.cbbpoll.net/.  The poll is due by Monday at 10:00am EST.  \n\n Thanks, /r/collegebasketball Team \n\n *** \n\n *You are receiving this message because you are participating in the /r/collegebasketball userpoll.*")
            print("User Messaged Succesfully")
        except:
            UserError.append(Voter)
            print("Failed to message user: "+Voter)
            continue
            
    adminmessage = "Ending /r/Collegebasketball User Poll Notifications. \n\n These users could not receive the message for various reasons: \n\n"
    
    for user in UserError:
        adminmessage = adminmessage + user + "\n\n"
            
    for user in admin_users:
        try:
            r.redditor(user).message(subject="Ending /r/Collegebasketball Poll Notifications",message=adminmessage)
        except:
            print("Failed to message admin user: "+user)


try:
    print("Logging into Reddit")
    r=reddit_login.scriptlogin(2)
    print("Succesfully Logged into Reddit as user:")
    print(r.user.me())
except:
    print("Could not login to reddit")
    raise
    
SendMessage(get_users(),r)
exit()
        