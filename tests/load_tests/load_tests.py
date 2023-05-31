import datetime
from sys import argv
import requests
import os
import re
from jinja2 import Environment, FileSystemLoader
env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates"))
)

# check commandline arguments
if(len(argv) < 4):
    print("[E] Missing required commandline arguments")
    print("Command should be launched with url, superuser name and superuser password as arguments")
    print("ex: python ./ 'http://127.0.0.1:8888' root password")
    exit(1)


if(not argv[1].startswith("http://") and not argv[1].startswith("https://")): #? add http manually?
    print("[E] URL argument should start with a HTTP(S) protocol")
    exit(1)

base_url = argv[1] # omitting /admin is required
su_name= argv[2]
su_pass= argv[3]

results = []

def main():
    start = datetime.datetime.now()
    s = requests.session() # create session to store cookies
    pre_login = send_request(s,f"{base_url}/admin/") # get admin login page, so we can grab CSRF token
    csrfReg = re.findall(r"<input .+?csrfmiddlewaretoken\" value=\"(.+?)\"",pre_login.text)
    if(len(csrfReg) == 0):
        print("Couldn't find a CSRF token, exitting...")
        exit(1)
    login = s.post(f"{base_url}/admin/login/?next=/admin/",{"csrfmiddlewaretoken":csrfReg[0],"username":su_name,"password":su_pass,"next":"/admin/"}) # ? Try logging in; will the cookie survive 'till the end?
    results.append({"availability":{"failed":login.status_code > 399,"code":login.status_code}, "speed":{"response_time":login.elapsed.total_seconds()}, "url":base_url+"/login"})
    if(login.status_code>399):
        print(f"[I] Request to login failed with code {login.status_code}")
        exit(1) # exit, because we can't do anything without logging in first
    send_request(s,f"{base_url}/admin/ninetofiver/")

    # save results to file
    print ("[I] Rendering results...")
    template = env.get_template("result_template.html")
    end = datetime.datetime.now()
    total_time = end - start
    with open("test_results.html","w",encoding="utf-8") as result:
        results.sort(key=lambda e:e["speed"]["response_time"])
        print(results)
        result.writelines(template.render({"results":results,"date":datetime.datetime.now(),"total":total_time.total_seconds()})) # render HTML result with results sorted by response time by default
        print("[I] Run successfully completed, exiting...")

def send_request(s:requests.Session,url:str) -> requests.Response:
    print(f"[I] Sending request to {url}")
    r = s.get(f"{url}") 
    results.append({"availability":{"failed":r.status_code > 399,"code":r.status_code}, "speed":{"response_time":r.elapsed.total_seconds()},"url":url})
    if(r.status_code > 399):
        print(f"[I] Request to {url} failed with code {r.status_code}")
        return r
    print(f"[I] Request to {url} successful")
    
    # move to other URLs found
    links = re.findall(r'<th.+?><a href="(.+?)">',r.text,flags=re.MULTILINE)
    for l in links:
        send_request(s,f"{base_url}{l}")

    return r

main()

