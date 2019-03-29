import requests
import subprocess
import sys, argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
list_url = 'crawl_dvc.txt'
listsite = []
def resend(url, retry=0):
    try:
        r = requests.get(url,timeout=10, verify=False)
        return r
    except:
        if retry==0:
            resend(url,1)
        else:
            return False
    return 0

def check_liferay(url):
    req = requests.get(url + "/api/jsonws", timeout=10, verify=False)
    if "get-user-by-id" in req.text:
        print url + ' Site use Liferay'
        listsite.append(url)               

def check_sharepoint(url):
    proc = subprocess.Popen(['wad','-u',url],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    out = proc.stdout.read()
    if "Microsoft SharePoint" in out:
        print url + 'Site use Microsoft SharePoint'
        listsite.append(url)               

def check_dotnetnuke(url):
    proc = subprocess.Popen(['wad','-u',url],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    out = proc.stdout.read()
    if "DNN" in out:
        print url + 'Site use DotnetNuke'
        listsite.append(url)               
    
def check_php(url):
    proc = subprocess.Popen(['wad','-u',url],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    out = proc.stdout.read()
    if "PHP" in out:
        print url + 'Site use Framework PHP'
        listsite.append(url)               
    
def check_java(url):
    proc = subprocess.Popen(['wad','-u',url],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    out = proc.stdout.read()
    if "Java" in out:
        print url + 'Site use Framework Java'
        listsite.append(url)               

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check cms")
    parser.add_argument("-c", "--check", help="Check cms.", required=True)
    args = parser.parse_args()
    with open(list_url) as f:
        urls = f.read().splitlines()
        for url in urls:
            print "Checking: " + url
            r = resend(url)
            if r != False:
                if "liferay" in args.check:
                    check_liferay(url)
                elif "sharepoint" in args.check:
                    check_sharepoint(url)
                elif "dnn" in args.check:
                    check_dotnetnuke(url)
                elif "php" in args.check:
                    check_php(url)
                elif "java" in args.check:
                    check_java(url)
    print '\n'.join(listsite)
