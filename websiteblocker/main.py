from datetime import datetime
from plyer import notification
from bs4 import BeautifulSoup
import requests

html_text = requests.get("https://porngeek.com/").text
sites_to_blocks = ['www.facebook.com/','facebook.com/']
sites_to_block =[]
host_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect = '127.0.0.1'
soup = BeautifulSoup(html_text, "lxml")
sites = soup.find_all("li", class_="item-list__row")

for site in sites:
    site = site.find("a")
    site = site["href"]
    site = site.replace('https://','')
    site = site.replace('http://','')
    sites_to_block.append(site)
print(sites_to_block)
def blocksite():
    for i in range(1):
        with open(host_path,'r+') as hostfile:
            host_content = hostfile.read()
            for site in sites_to_block:
                if site not in host_content:
                    hostfile.write(redirect + " " + site + "\n")
    print("Block Site")
    notification.notify(
    title= "Blocked Sites", message = """
 All porn sites have been blocked
    """)
def unblocksite():
    print("Unblock Sites")
    with open(host_path, 'r+') as hostfile:
        lines = hostfile.readlines()
        hostfile.seek(0)
        for line in lines:
            if not any(site in line for site in sites_to_blocks):
                hostfile.write(line)
        hostfile.truncate()
    notification.notify(
    title="Unblocked Sites", message="""
       All porn sites have been unblocked
       """)
blocksite()
