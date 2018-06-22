import requests
from QMSv1.sharepointCookies import cookies

def get_urlInfo(url):
    my_Headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        'Accept': 'application/json;odata=verbose'}  # "Accept-Encoding": "gzip, deflate, br",


    proxies = {'HTTP': 'http://10.144.1.10:8080', 'HTTPS': 'http://10.144.1.10:8080'}
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
    req = requests.session()
    try:
        print("Visiting pdf url ",url)
        resp = req.get(url, data=None, stream=True, headers=my_Headers, cookies=cookies, proxies=proxies)
        print("HTTP RESPONSE is : ", resp.status_code)
        if resp.status_code != 200:
            print("Can't access this site")
            return False
        html = resp.content
        resp.close()
        return html
    except:
        print(url+' looks like inaccessible...')
        print(url + " is inaccessible")
        return False


def downlPDF(url, filename):
    def downl(url, filename):
        html_byte = get_urlInfo(url)
        if html_byte:
            with open("PDFs/"+filename.replace('/', '_') + ".pdf", "wb") as f:  # in case there are forbidden symbol in filename such as '/'
                f.write(html_byte)
                print('Downloading from ',url)
                return True
    isture = downl(url, filename)
    if isture:
        print('Successfully download ' + filename + '.pdf')