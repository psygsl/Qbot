#
#   Sharepoint crawling module
#
from __future__ import unicode_literals
import os
from datetime import datetime
import requests
import urllib
import urllib3
import sys
import browser_cookie3
#
#----------------------------------------------------------------------------------------------------------
def nb_GETs():
    global List_GETs
    return len(List_GETs)
#
#----------------------------------------------------------------------------------------------------------
def nb_Folders():
    global List_Folders
    return len(List_Folders)
#

def get_data(next_link):
    return {
        'func': 'll.login',
        'CurrentClientTime': datetime.today().strftime('D/%Y/%m/%d:%H:%M:%S'),
        'NextURL': next_link,
        'Username': 'rc033272',   # USER_NAME
        'Password': 'Rapid.123'   # PASSWORD     
    }

def make_GET_sharenet(link, file=None, login=None):
    global Req_Session
    my_Headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                "Accept-Encoding": 'application/json;odata=verbose'}     # "gzip, deflate, br"

#    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

#    req = requests.session()
#    print("req : ", req)

    if login == True :
        resp = Req_Session.get(link, data=None, verify=False, headers=my_Headers, proxies={'HTTP':'http://10.144.1.10:8080','HTTPS':'http://10.144.1.10:8080'})
        print ("HTTP RESPONSE is : ", resp.status_code)
        if resp.status_code != 200 :
            print ("HTTP RESPONSE is not 200")
            return False

        #     GET 2
        resp = Req_Session.get('https://sharenet-ims.int.net.nokia.com/livelink/livelink', data=None, verify=False, headers=my_Headers, stream=True, proxies={'HTTP':'http://10.144.1.10:8080','HTTPS':'http://10.144.1.10:8080'})
        print ("HTTP RESPONSE is : ", resp.status_code)
        if resp.status_code != 200 :
            print ("HTTP RESPONSE is not 200")
            return False
        print("After GET 2")
        
        #     GET 3
        resp = Req_Session.get('https://sharenet-ims.int.net.nokia.com/livelink/livelink?func=LL.getlogin&NextURL=%2Flivelink%2Flivelink%3FRedirect%3D1', data=None, verify=False, headers=my_Headers, stream=True, proxies={'HTTP':'http://10.144.1.10:8080','HTTPS':'http://10.144.1.10:8080'})
        print ("HTTP RESPONSE is : ", resp.status_code)
        if resp.status_code != 200 :
            print ("HTTP RESPONSE is not 200")
            return False
        print("After GET 3")

        #     POST 1 for login
        data = get_data('/livelink/livelink/Redirect=1')    #   provide user and passwd
        resp = Req_Session.post('https://sharenet-ims.int.net.nokia.com/livelink/livelink', data=data, verify=False, stream=True, headers=my_Headers, proxies={'HTTP':'http://10.144.1.10:8080','HTTPS':'http://10.144.1.10:8080'})
        print ("posted login info   HTTP RESPONSE is : ", resp.status_code)
        if resp.status_code != 200 :
            print ("HTTP RESPONSE is not 200")
            return False
        print("After POST 1")
        return True

    #             get source code or file
    resp = Req_Session.get(link, data=None, verify=False, stream=True, headers=my_Headers, proxies={'HTTP':'http://10.144.1.10:8080','HTTPS':'http://10.144.1.10:8080'})
    print ("GET : ", link, "HTTP RESPONSE is : ", resp.status_code)
    if resp.status_code != 200 :
        print ("HTTP RESPONSE is not 200")
        return False
 
    filename = ''
    if file == None :
        filename = filename + File_Temp    #   U a folder I presume
        file_size = 4000                   #   not too good, OK, but no mean to know the size of the source code of a folder ... 
    else :
        # file Url structure = 'https://sharenet-ims.int.net.nokia.com/livelink/livelink/425832820/Create_Process_Introduction_MN.pptx?func=doc.Fetch&nodeid=425832820'
        filong = link.split('/')[-1]
        filename = filename + filong.split('?')[0]     #   U a file I presume      same name in current folder on local hard disk
        try :
            file_size = int(resp.headers['content-length'])
        except :
            print('Not normal : was meant to be a file and no content-length in header')
            return False

    print ("filename is : ", filename)
    
    file_size_dl = 0
    block_size = 8192    #  4096

    handle = open(filename, 'wb')
    for block in resp.iter_content(block_size):      #   can use the read() method also
        if not block:
            break
        handle.write(block)
        file_size_dl += len(block)
        print('{:.2f}%'.format(100*file_size_dl/file_size),end='\r', flush=True)     #   printing on same line   OK, progress bar would be better ... 

    handle.close()
    if file_size_dl > 0.5 * file_size :    # looks strange ... OK and in fact it is wrong : because for short text files used for tests, EOL chars are not part of it ... 
        return True
    else :
        return False
#----------------------------------------------------------------------------------------------------------
#             download files or folder source code, depending on file parameter
#             if folder, a temporary file is created that will be parsed at next round
#----------------------------------------------------------------------------------------------------------
def make_GET_sharepoint(url, file=None):
    global File_Temp
    my_Headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                'Accept':'application/json;odata=verbose'}         #      "Accept-Encoding": "gzip, deflate, br",

    #    these authentication cookies get expired after 5 days     these ones are 2018/04/02
    #cookies_dict = {'rtFa':'ne+el0FPWzMGxWrvTagSQ1TEpf7/XGRvnBqVmXPzb7UmNUQ0NzE3NTEtOTY3NS00MjhELTkxN0ItNzBGNDRGOTYzMEIwc1iA0ARmj8Vl7agBd220WH8aSg4IPSZEdLYHly5nmH/3m5hvx0UBop8aS9iNNdDUwdW4jbUs+eiHDxEw27lcjbN6SCTfKhlSzz9lNJywmpdB2rNGbmBzweK7024w2d5tW5AcqVQk3uKbx5ajGVXXv0l6dQlWw4Gsb5A5pOz/NHPaH2cGEHUZP9LiUD50o8GX29GMTlEIYVg/EKVGmdFgZi7EjHCj/2/m5PVoKJ+grqyuUtBXOq0k3gE4sqNpMun6TABWARWTT0JtQiVRF7LgTlwNzD0zyOpfF6z53RQnzbvkkUAWA0WV2fqF6q7raU9MEWFdBAgsD1CqlL1QmzmmbkUAAAA=',
    #           'FedAuth':'77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjMsMGguZnxtZW1iZXJzaGlwfDEwMDMzZmZmOTU5ODQyMTRAbGl2ZS5jb20sMCMuZnxtZW1iZXJzaGlwfGNocmlzdGlhbi5yYW1waW5Abm9raWEuY29tLDEzMTY3MzA4MjczMDAwMDAwMCwxMzE2NTQ4OTA1NTAwMDAwMDAsMTMxNjc3NDAyNzYyOTM5MzcyLDAuMC4wLjAsMiw1ZDQ3MTc1MS05Njc1LTQyOGQtOTE3Yi03MGY0NGY5NjMwYjAsLFYyITEwMDMzRkZGOTU5ODQyMTQhMTMxNjczMDgyNzMsMWYyMzVhOWUtNjAxYy01MDAwLTgxYmUtNmVlMWYyMjQxNzEyLDFmMjM1YTllLTYwMWMtNTAwMC04MWJlLTZlZTFmMjI0MTcxMiwsMCxGbi9GUmlLcWxIenhLRlZjNXpyZ0d6bkVON01Lclc5WHB5amNGRFJUOEpJYjJQdDNhS2wxMkxmMlVtSDA3UEw4MnAwTS9UT0hvZnpZRStxSTlUUFhpeStTR1pMQ3FsTW5pcTlTUU9lWjdqa0tWWUlONzlRUnlTMkwzNmtSUCswdktwNkpOa2pkS3hNTHZINCtVYjFRS2NXdG1wWkJBVC9LRnI2dUZySHJXZjFHektjVTdHaUlwdytFc0JqRFJjc3FSRU82YmlqVXpJSFJ6OVNJbS9yTFhnWmdFZWJaQTRFbS9HeEpWWXVOckdYYStoSmM4RVhvaHZpalBXZXc2NVVVaFExUmIrdXdSSFBwbWZoR1M5L3l2akFaR1UvR3g3Rm5qaHFFVXlrNHRnUStjTmk1c1NnMUY0MlBBVndmeUgxNnRtNGxEbkVJRDdYMkhoNmZDd0gwVmc9PTwvU1A+',
    #           'ai_session':'loleU|1522843974137.4|1522849155863.4',
    #           'ai_user':'8BIbU|2018-03-05T18:35:42.011Z'}
    cookies_sql3lite = browser_cookie3.load()
    cookies_dict = {}
    for ck in cookies_sql3lite :
        if ck.name == 'FedAuth' or ck.name == 'ai_session' or ck.name == 'ai_user' or ck.name == 'rtFa' :
            #print (ck.name, ' : ', ck.value)
            cookies_dict[ck.name] = ck.value

    proxies={'HTTP':'http://10.144.1.10:8080','HTTPS':'http://10.144.1.10:8080'}
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

    print("make_GET_sharepoint of : ", url)

    req = requests.session()
    print("GET to : ", url)
    resp = req.get(url, data=None, verify=False, stream=True, headers=my_Headers, cookies=cookies_dict, proxies=proxies)
    print ("HTTP RESPONSE is : ", resp.status_code)
    if resp.status_code != 200 :
        print ("HTTP RESPONSE is not 200")
        print ("Error HTTP")
        req.close()
        return False

    filename = ''
    if file == None :
        filename = filename + File_Temp    #   U a folder I presume
        file_size = 4000                   #   not too good, OK, but no mean to know the size of the source code of a folder ... 
    else :
        filename = filename + url.split('/')[-1]         #   U a file I presume      same name in current folder on local hard disk
        #    to be improved : it must never crash ...
        try :
            file_size = int(resp.headers['content-length'])
        except :
            print('Not normal : was meant to be a file and no content-length in header')
            return False
    
    file_size_dl = 0
    block_size = 8192    #  4096
    
    #   now, either a temp file is created and will be read at next round, either a relevant file is downloaded
    handle = open(filename, 'wb')
    for block in resp.iter_content(block_size):        #   can use the read() method also
        if not block:
            break
        handle.write(block)
        file_size_dl += len(block)
        print('{:.2f}%'.format(100*file_size_dl/file_size),end='\r', flush=True)     #   printing on same line   OK, progress bar would be better ...
    print("\n")
    handle.close()
    req.close()
    if file_size_dl > 0.5 * file_size :    # looks strange ... OK and in fact it is wrong : because for short text files used for tests, EOL chars are not part of it ... 
        return True
    else :
        return False
#
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
def make_GET(url, file=None):
    if "sharepoint" in url :
        if make_GET_sharepoint(url, file) == False :
            return False
    if "sharenet" in url :
        if make_GET_sharenet(url, file) == False :
            return False
    return True
#--------------------------------------------------------------------------------------------
#    here we test if downloading the file is interesting
#    e.g. with          if ".docx" in filename
#--------------------------------------------------------------------------------------------
def  download_file_if_relevant(filename):
    if ".xls" in filename or ".xlsx" in filename or ".ppt" in filename or ".pptx" in filename or ".doc" in filename or ".docx" in filename or ".pdf" in filename :
        print("file to be downloaded", filename)         #   it does not download all files : can be changed
        return make_GET(filename, file=True)
    else :
        return True

#--------------------------------------------------------------------------------------------
#   looks in folders list to find the next most relevant folder
#--------------------------------------------------------------------------------------------
def last_list_fold_with_no_get():
    global List_Folders
    lg = len (List_Folders)
    if lg == 0:
        print("list of folders is empty")
        return ''

    #  print("in function last_list_fold_with_no_get : ", "\nList_Folders", List_Folders, "\nList_GETs", List_GETs)    #   for debug
    
    for i in range(lg) :
        if List_Folders[-1-i] not in List_GETs :
            print("in function last_list_fold_with_no_get : This is the next folder to be crawled : ", List_Folders[-1-i])
            return List_Folders[-1-i]

    print("in function last_list_fold_with_no_get : NOT FOUND another folder to be crawled. Crawling should end")
    return ''
#--------------------------------------------------------------------------------------------
#        here the html source code is parsed, looking for the fileleafref keyword that is followed with folder or file name
#        enrich lists
#        download files if relevant
#        determin next url
#--------------------------------------------------------------------------------------------
def work_lists_and_dwld_files_sharepoint():
    global Url_Crawled
    global List_Files
    global List_Folders
    global File_Temp

    print('in function work_lists_and_dwld_files_sharepoint : List_Files = ', List_Files)
    print('in function work_lists_and_dwld_files_sharepoint : List_Folders = ', List_Folders)

    url_proposed = ''
    with open(File_Temp, 'r') as f:      #  text mode
        for s in f:             #    equivalent of :  s = f.readline()
            if "FileLeafRef" in s:
                if s.index("FileLeafRef") > 1 :
                    continue      #  it must be to define the keyword FileLeafRef in source code file
                print (s)
                if len(s) < 17 :
                    print("\n\nPROBLEM IN SOURCE CODE FILE : THE LINE IS NOT LONG ENOUGH\n\n")
                    continue
                if ".aspx" in s : #   links are excluded from the crawling
                    continue
                st = s[16:-3]    #   after FileLeafRef which pattern is 16 long
                print (st)
                url_fi_or_fo = Url_Crawled + '/' + st
                if (len(st) > 4 and (st[-5]== '.' or st[-4] == '.')):      #   assuming that a file is .xls, or .xlsx, or .ppt ...
                    print("found file FileLeafRef : ", url_fi_or_fo)
                    List_Files.append(url_fi_or_fo)           #    it is a file
                    download_file_if_relevant(url_fi_or_fo)
                else :
                    print("found folder : ", url_fi_or_fo)
                    List_Folders.append(url_fi_or_fo)     #    it is a folder
                    if url_proposed == '' :     #    CRITICAL POINT in algorithm : the fist folder found is to be crawled
                        url_proposed = url_proposed + url_fi_or_fo
                        print("url_proposed = ", url_proposed)

            if "Field=\"LinkFilename\"" in s:                 # pattern is : Field="LinkFilename"
                long_url_fi1 = s.split("Field=\"LinkFilename\"")[1]    #   string after Field="LinkFilename"
                long_url_fi2 = long_url_fi1.split("href=\"")[1]        #   string after href="
                url_fi_or_fo = long_url_fi2.split("\"")[0]             #   string before "
                if (len(url_fi_or_fo) > 4 and (url_fi_or_fo[-5]== '.' or url_fi_or_fo[-4] == '.')):      #   assuming that a file is .xls, or .xlsx, or .ppt ... 
                    print("found file LinkFilename : ", url_fi_or_fo,"\n")
                    List_Files.append(url_fi_or_fo)           #    it is a file
                    download_file_if_relevant(url_fi_or_fo)

    f.close()
    if url_proposed == '' :      #    no url proposed    come back to other nodes of the tree
        print("in function work_lists_and_dwld_files_sharepoint : no url_proposed    trying to find one")
        Url_Crawled = ''
        Url_Crawled = Url_Crawled + last_list_fold_with_no_get()
        print("in function work_lists_and_dwld_files_sharepoint : next url to be crawled is : ", Url_Crawled)
    else:      #     a next url to be crawled is proposed
        print("in function work_lists_and_dwld_files_sharepoint, the url_proposed is : ", url_proposed)
        Url_Crawled = ''    #  likely not useful this line ... 
        Url_Crawled = Url_Crawled + url_proposed
        print("in function work_lists_and_dwld_files_sharepoint : next url to be crawled - proposed - is : ", Url_Crawled)
    return True

#--------------------------------------------------------------------------------------------
#        here the html source code is parsed, looking for the fileleafref keyword that is followed with folder or file name
#        enrich lists
#        download files if relevant
#        determin next url
#--------------------------------------------------------------------------------------------
def work_lists_and_dwld_files_sharenet():
    global Url_Crawled
    global List_Files
    global List_Folders
    global File_Temp

    print('in function work_lists_and_dwld_files_sharenet : List_Files = ', List_Files)
    print('in function work_lists_and_dwld_files_sharenet : List_Folders = ', List_Folders)

    url_proposed = ''

    with open(File_Temp, 'r') as f:
        for s in f:             #    equivalent of :  s = f.readline()
            if "DataStringToVariables" in s:
                print ('DataStringToVariables found')
                break
    f.close()

    # finding folders     pattern is "typeName":"Document"
    list_fold_raw = s.split("typeName\":\"Folder\",\"name\":\"")
    for i in range(1, len(list_fold_raw)) :      #  start at 1 so just after pattern
        foldname = list_fold_raw[i].split("\",\"link")[0]      #   adresses string before this second pattern
        list_obj = list_fold_raw[i].split("objId=")    #  also need objId
        long_objId = list_obj[1]      #  adresses string after last pattern
        objId = long_objId.split("&obj")[0]     #  finally objId is before this 3rd pattern
        print ("Folder ", i, ": ", foldname, ' ', "     objId for folder = ", objId)
        # folder Url structure = 'https://sharenet-ims.int.net.nokia.com/livelink/livelink?func=ll&objId=425832824&objAction=browse&viewType=1'
        url_fo = 'https://sharenet-ims.int.net.nokia.com/livelink/livelink?func=ll&objId='+objId+'&objAction=browse&viewType=1'
        List_Folders.append(url_fo)
        if url_proposed == '' :     #    CRITICAL POINT in algorithm : the fist folder found is to be crawled
            url_proposed = url_proposed + url_fo
            print("url_proposed = ", url_proposed)

    # finding files       pattern is "typeName":"Document"
    list_fi_raw = s.split("typeName\":\"Document\",\"name\":\"")
    for i in range(1, len(list_fi_raw)) :      #  start at 1 so just after pattern
        list_fil = list_fi_raw[i].split("?func=doc.Fetch&nodeid=")       #  cut string in 2
        fi = urllib.parse.unquote(list_fil[0].split("/")[-1])           #   1st part of string contains file name after last /
        objId = list_fil[1].split("&")[0]         #   2nd part of string contains objId before &
        print ("file or link ", i, ": ", fi, "     objId for file or link = ", objId)
        # file Url structure = 'https://sharenet-ims.int.net.nokia.com/livelink/livelink/425832820/Create_Process_Introduction_MN.pptx?func=doc.Fetch&nodeid=425832820'
        url_fi = 'https://sharenet-ims.int.net.nokia.com/livelink/livelink/'+objId+'/'+fi+'?func=doc.Fetch&nodeid='+objId
        List_Files.append(url_fi)           #    it is a file
        download_file_if_relevant(url_fi)

    if url_proposed == '' :      #    no url proposed    come back to other nodes of the tree
        print("in function work_lists_and_dwld_files_sharenet : no url_proposed    trying to find one")
        Url_Crawled = ''
        Url_Crawled = Url_Crawled + last_list_fold_with_no_get()
        print("in function work_lists_and_dwld_files_sharenet : next url to be crawled is : ", Url_Crawled)
    else:      #     a next url to be crawled is proposed
        print("in function work_lists_and_dwld_files_sharenet, the url_proposed is : ", url_proposed)
        Url_Crawled = ''    #  likely not useful this line ... 
        Url_Crawled = Url_Crawled + url_proposed
        print("in function work_lists_and_dwld_files_sharenet : next url to be crawled - proposed - is : ", Url_Crawled)
    return True
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
def work_lists_and_dwld_files():
    global Url_Crawled
    if "sharepoint" in Url_Crawled :
        if work_lists_and_dwld_files_sharepoint() == False :
            return False
    if "sharenet" in Url_Crawled :
        if work_lists_and_dwld_files_sharenet() == False :
            return False
    return True
#------------------------------------------------------------------------------------------
#   triggers the GET url
#------------------------------------------------------------------------------------------
def crawl_folder(Url):
    global List_GETs
    if Url == '' :
        List_GETs.append("Url empty")     #  main criteria in the number of gets vs number of folders so we add one
        print ("Error : url empty is not to be added")
        return False
    if Url[:4] != "http" :
        List_GETs.append("Url not beginning with http")        #  main criteria in the number of gets vs number of folders so we add one
        print ("Url does not begin with http. Cannot crawl", Url, "Url received = ", Url[:4])
        return False
    if len(Url) > 300 :
        List_GETs.append("Url appears too long    more than 300 characters")        #  main criteria in the number of gets vs number of folders
        print("URL more than 300 characters : deemed as an error")
        return False

    List_GETs.append(Url)     #  whatever result of make_GETs : OK
    print ("in function crawl_folder List_GETs is : ", List_GETs)
    if make_GET(Url) != False:
        work_lists_and_dwld_files()
        return True
    return False
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
def test_network (url):
    if "sharepoint" in url :
        if make_GET_sharepoint('https://nokia.sharepoint.com') == False :    # polite people say hello before crawling
            print("Impossible to reach https://nokia.sharepoint.com")
            return False
    if "sharenet" in url :
        if make_GET_sharenet('https://sharenet-ims.int.net.nokia.com', login=True) == False :    # polite people say hello before crawling
            print("Impossible to reach https://sharenet-ims.int.net.nokia.com")
            return False
    return True

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
def crawl_URL():
    #   init global variables before crawling
    global List_GETs
    global List_Folders
    global List_Files
    global Url_Crawled
    global Req_Session

    Req_Session = requests.session()
    print("req : ", Req_Session)
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
    List_GETs = []
    List_Folders = []
    List_Files = []

    if test_network (Url_Crawled) == False :
        Req_Session.close()
        return False

    while nb_GETs() <= nb_Folders() :     #   same number of gets to make as number of folders to explore
        if crawl_folder(Url_Crawled) == False :
            print("function crawl_folder returned False")
            break
        if nb_GETs() > 500 :
            print("Number of GETs is more than 200 : we stop here")
            break
    Req_Session.close()
    return True
#    end crawl_URL()

#------------------------------------------------------------------------------------------
#    main program
#------------------------------------------------------------------------------------------
List_GETs = []
List_Folders = []
List_Files = []
File_Temp = 'temp_file.txt'
Req_Session = requests.session()

with open("config.txt", 'r') as f:      #  text mode
    for s in f:             #    equivalent of :  s = f.readline()
        print(s)
        if s[0] == '#':      #    comment line
            continue
        url_to_crawl = s.split('#')[0]   #   no blank
        #print ("URL : ", url_to_crawl)
        if "http" not in url_to_crawl:
            print("not a URL, does not contain http")
            continue
        Url_Crawled = ''
        Url_Crawled = url_to_crawl
        crawl_URL()     #    we do not test the returned value, we will try to crawl what we can
f.close()

#    end main program
#------------------------------------------------------------------------------------------
