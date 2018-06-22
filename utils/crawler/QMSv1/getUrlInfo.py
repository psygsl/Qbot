import requests
import urllib3
from QMSv1.sharepointCookies import cookies


def get_urlInfo(url):
    # dict_cook = {}
    # cookies = browser_cookie3.chrome(domain_name="nokia.sharepoint.com")
    # for ck in cookies:
    #     if ck.name == 'FedAuth' or ck.name == 'ai_session' or ck.name == 'ai_user':
    #         dict_cook[ck.name] = ck.value
    my_Headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        'Accept': 'application/json;odata=verbose'}  # "Accept-Encoding": "gzip, deflate, br",



    proxies = {'HTTP': 'http://10.144.1.10:8080', 'HTTPS': 'http://10.144.1.10:8080'}
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
    req = requests.session()
    try:
        print("Visiting ",url)
        resp = req.get(url, data=None,  stream=True, headers=my_Headers, cookies=cookies, proxies=proxies, timeout=10)
        print("HTTP RESPONSE is : ", resp.status_code)
        if resp.status_code != 200:
            print("Can't access this site" )
            return False
        html = resp.content.decode("utf-8")
        resp.close()
        return html
    except:
        print(url + ' looks like inaccessible....')
        print(url + " is inaccessible")
        return None
