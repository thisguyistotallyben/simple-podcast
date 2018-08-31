from modules import podbean

with open('config/podbean.txt', 'r') as f:
    lines = f.readlines()
    if len(lines) != 2:
        raise IOError()
    else:
        pbid = lines[0].strip()
        pbsecret = lines[1].strip()
        pb = podbean.Podbean(pbid, pbsecret)

'''
# login
pb.auth()

title = 'This is a title'
content = "This is a description of content" # PROBLEM WITH HTML TAGS
# akey = pb.upload_file('testaudio.mp3')

pb.publish_episode(title=title, content=content)
'''

pb.convert()
