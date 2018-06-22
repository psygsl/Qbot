#
#   Sharepoint crawling module
#
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
#----------------------------------------------------------------------------------------------------------
#             download files or folder source code, depending on file parameter
#             if folder, a temporary file is created that will be parsed at next round
#----------------------------------------------------------------------------------------------------------
def make_GET(url, file=None):
    global File_Temp
    my_Headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                'Accept':'application/json;odata=verbose'}         #      "Accept-Encoding": "gzip, deflate, br",

    #    these authentication cookies get expired after 5 days     these ones are 2018/03/17
    cookies = {'rtFa':'4vnUqyv129B/hJm4hmdG+tYiOvHdcrpziiA1yAdcLFgmNUQ0NzE3NTEtOTY3NS00MjhELTkxN0ItNzBGNDRGOTYzMEIwkneC0j39XHfSH6+lNQCoKx9aHokbsCy7OJpNG73ON7csj1+rmm/huDG9hq9yQpyXGP+03MLBThagQSBkHoAAlUqZTzGFFXe+9IbmjN8zjywNrIfTJsywCDAEiJ+uMpyfhItlWkurzOadMpwezH+BQO4N+wzR2ohCZEg9xxqieImfcDvWQ0WpvT1G1Tdm9HfrD2AOtC4E5ckXV1p9BFL0yteO+fulS1NT4EtGZbPnLAciyzWN/jNvKdXHRtVqtzrLDqlyQ1B9ngqa3SL8BgirYjGRtD3pcXpuypNnZYXoZH7ULu8rxAYJ78SiivyBHDrOgTWNSUQ2A8XaBrZ3/1JWQUUAAAA=','FedAuth':'77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjMsMGguZnxtZW1iZXJzaGlwfDEwMDMzZmZmOTU5ODQyMTRAbGl2ZS5jb20sMCMuZnxtZW1iZXJzaGlwfGNocmlzdGlhbi5yYW1waW5Abm9raWEuY29tLDEzMTY1Nzc4MjIwMDAwMDAwMCwxMzE2NTQ4OTA1NTAwMDAwMDAsMTMxNjYyMTAyMjI1MDcyMDMyLDAuMC4wLjAsMiw1ZDQ3MTc1MS05Njc1LTQyOGQtOTE3Yi03MGY0NGY5NjMwYjAsLFYyITEwMDMzRkZGOTU5ODQyMTQhMTMxNjU3NzgyMjAsZjI2ZjU0OWUtZTBkMC01MDAwLTUyMGQtNTIwNjNhMWFiOWYzLGYyNmY1NDllLWUwZDAtNTAwMC01MjBkLTUyMDYzYTFhYjlmMywsMCxkWWNON2dheFZEVEh4OEQ5MVlFMWFudDh4c051NnhBRjYvNlk2MnFJdERxUUJGck5ZUHpKdEE3OHJPZ3N5aFhudmJ6cTI0OStycXE1YVZCVDhTUExubGQvMTJHZU9iNzdlWHFOUE1neldlcmE5emU5dzlOMzB4UnZ6c0owQWNKTmpuQ1NhMHZOVk5sNnJuZW9oK3p5UWhDcU9ueldCZktjVmhtUGlsMjQxdXY1eTVxY1IxeWJndjVuMEtINGxERWhBdHVhd1hPU2grN3E1WE9jTFFKdk1pZXlVU0tDbFJKRDUzMGJRcDFQWUZuUXRRUEp2YjFIc205STdXL3FxVElIY3AwMXRWaFFKWTZma0lvcVB1bStHa2dObklnNWhHS2pzUkRPa21hZlpDcEZQYVAza3NpRnBPb200dDZlcWkxQVM4WnZab2RveSsvOUxmMUlFL09BUlE9PTwvU1A+','ai_session':'gxu3e|1521304642133.8|1521304642133.8','ai_user':'8BIbU|2018-03-05T18:35:42.011Z'}

    # cookies = browser_cookie3.load()     does not work so far   likely because the format is sqlite, it must be turned into dictionnary
    #print('cookiejar = ', cookies)

    proxies={'HTTP':'http://10.144.1.10:8080','HTTPS':'http://10.144.1.10:8080'}
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

    print("make_GET of : ", url)

    req = requests.session()
    print("GET to : ", url)
    resp = req.get(url, data=None, verify=False, stream=True, headers=my_Headers, cookies=cookies, proxies=proxies)
    print ("HTTP RESPONSE is : ", resp.status_code)
    if resp.status_code != 200 :
        print ("HTTP RESPONSE is not 200")
        print ("Error HTTP")
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
        #    to be improved : it must never crash ... 
    
    #f_Info = resp.info()     #   TO BE STUDIED   perhaps with keyword "try" ... 
    file_size_dl = 0
    block_size = 4096

    #   now, either a temp file is created and will be read at next round, either a relevant file is downloaded
    handle = open(filename, 'wb')
    for block in resp.iter_content(block_size):
        if not block:
            break
        handle.write(block)
        file_size_dl += len(block)
        print('{:.2f}%'.format(100*file_size_dl/file_size),end='\r', flush=True)     #   printing on same line   OK, progress bar would be better ...
    print("\n")
    handle.close()
    if file_size_dl > 0.5 * file_size :    # looks strange ... OK and in fact it is wrong : because for short text files used for tests, EOL chars are not part of it ... 
        return True
    else :
        return False
#
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
def work_lists_and_dwld_files():
    global Url_Crawled
    global List_Files
    global List_Folders
    global File_Temp

    print('in function work_lists_and_dwld_files : List_Files = ', List_Files)
    print('in function work_lists_and_dwld_files : List_Folders = ', List_Folders)

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
                    print("found file : ", url_fi_or_fo)
                    List_Files.append(url_fi_or_fo)           #    it is a file
                    download_file_if_relevant(url_fi_or_fo)
                else :
                    print("found folder : ", url_fi_or_fo)
                    List_Folders.append(url_fi_or_fo)     #    it is a folder
                    if url_proposed == '' :     #    CRITICAL POINT in algorithm : the fist folder found is to be crawled
                        url_proposed = url_proposed + url_fi_or_fo
                        print("url_proposed = ", url_proposed)
    f.close()
    if url_proposed == '' :      #    no url proposed    come back to other nodes of the tree
        print("in function work_lists_and_dwld_files : no url_proposed    trying to find one")
        Url_Crawled = ''
        Url_Crawled = Url_Crawled + last_list_fold_with_no_get()
        print("in function work_lists_and_dwld_files : next url to be crawled is : ", Url_Crawled)
    else:      #     
        print("in function work_lists_and_dwld_files, the url_proposed is : ", url_proposed)
        Url_Crawled = ''    #  likely not useful this line ... 
        Url_Crawled = Url_Crawled + url_proposed
        print("in function work_lists_and_dwld_files : next url to be crawled - proposed - is : ", Url_Crawled)
#------------------------------------------------------------------------------------------
#   triggers the GET url
#------------------------------------------------------------------------------------------
def crawl_folder(Url):
    global List_GETs
    if Url == '' :
        List_GETs.append("Url empty")     #  main criteria in the number of gets vs number of folders
        print ("Error : and url empty is not to be added")
        return False
    if Url[:4] != "http" :
        List_GETs.append("Url not beginning with hrrp")        #  main criteria in the number of gets vs number of folders
        print ("Url does not begin with http. Cannot crawl", Url, "Url received = ", Url[:4])
        return False
    if len(Url) > 200 :
        List_GETs.append("Url appears too long    more than 200 characters")        #  main criteria in the number of gets vs number of folders
        print("URL more than 200 characters : deemed as an error")
        return False

    List_GETs.append(Url)     #  whatever result of make_GETs : OK
    print ("in function : crawl_folder List_GETs", List_GETs)
    if make_GET(Url) != False:
        work_lists_and_dwld_files()
        return True
    return False
#------------------------------------------------------------------------------------------
#    main program
#
# global variables (beginning uppercase)
#Url_Start = 'https://nokia.sharepoint.com/sites/kpioffice/CQO KPI Steering Board'
#Url_Start = 'https://nokia.sharepoint.com/sites/CreateProcessPortal'
#------------------------------------------------------------------------------------------

#Url_Start = 'https://nokia.sharepoint.com/sites/MBBQPO/MN Q Scorecard 2017/2018 Scorecard Planning'
#Url_Start = 'https://nokia.sharepoint.com/sites/CreateProcessPortal/sitepages'
#Url_Start = 'https://nokia.sharepoint.com/sites/MBBQPO/MN Q Scorecard 2017/2018 Scorecard Planning'
#Url_Start = 'https://nokia.sharepoint.com/sites/CreateProcessPortal'

#Url_Start = 'https://nokia.sharepoint.com/sites/kpioffice/'
#https://nokia.sharepoint.com/sites/kpioffice/Quality%20Documents/Forms/AllItems.aspx?RootFolder=%2Fsites%2Fkpioffice%2FQuality%20Documents%2FQuality%20KPI%20Definitions%2F2017%20KPI%20Defintions&FolderCTID=0x0120007FFF67E22034264D9FC5F602FFDEBB07&View=%7BA8DF229C-22F0-41C0-854D-29583DF7CE09%7D
Url_Start = 'https://nokia.sharepoint.com/sites/kpioffice/Quality Documents/Quality KPI Definitions/2017 KPI Defintions'

Url_Crawled = ''
List_GETs = []
List_Folders = []
List_Files = []
File_Temp = 'temp_file.txt'

Url_Crawled = Url_Crawled + Url_Start

if make_GET('https://nokia.sharepoint.com') == False :    # polite people say hello before crawling
    print("Impossible to reach https://nokia.sharepoint.com")
    sys.exit()

while nb_GETs() <= nb_Folders() :     #   same number of gets to make as number of folders to explore
    if crawl_folder(Url_Crawled) == False :
        print("function crawl_folder returned False")
        break
    if nb_GETs() > 200 :
        print("Number of GETs is more than 200 : we stop here")
        break

print('End of crawling : PRESS ENTER KEY TO END PROGRAM')       #    for execution is command prompt during development
input()                                                         #    for execution is command prompt during development
#    end
#------------------------------------------------------------------------------------------
#              following are examples for debug phase
#    'https://nokia.sharepoint.com/sites/kpioffice'                                  get Reporting
#    'https://nokia.sharepoint.com/sites/kpioffice/Reporting'                        get 2017
#    'https://nokia.sharepoint.com/sites/kpioffice/Reporting/2017'                   get P05
#    'https://nokia.sharepoint.com/sites/kpioffice/Reporting/2017/P05'               get files Excel,, ppt, pdf ...   recursively
#file_to_dl = "https://sites/kpioffice/Quality Documents/Quality KPI Definitions/2017 KPI Defintions/Outage Restore.pptx"
#file_to_dl = "https://nokia.sharepoint.com/sites/microwave_compl_eng/Shared%20Documents/file to be read.txt"
#file_to_dl = 'https://nokia.sharepoint.com/sites/nokiacreate/SitePages/Home%20R2.0.aspx'      not to be downloaded
#file_to_dl = 'https://nokia.sharepoint.com/sites/microwave_compl_eng/SiteAssets/SitePages/Reports%20for%20CE%20marking/9500%20MPR%20-%20Wavence/DoC/3DB19459AAAAEUZZA_01.pdf'        #  OK downloaded
#file_to_dl = 'https://nokia.sharepoint.com/sites/kpioffice/_layouts/15/DocIdRedir.aspx?ID=SP-PTI5P5LIQQQ4-1167207291-124'
#file_to_dl = 'https://nokia.sharepoint.com/sites/kpioffice/Reporting/2018/P01/Tier1_GOPS_Quality_Scorecard_2018_P01.pdf'     #  OK downloaded
#file_to_dl = 'https://nokia.sharepoint.com/sites/kpioffice/Reporting/2017/P05/ION%20BG%20Tier%201%20Quality%20Scorecard%202017_P05_19062017.xlsx'    #  OK downloaded
#file_to_dl = 'https://nokia.sharepoint.com/sites/kpioffice/Reporting/2017/P05/ION BG Tier 1 Quality Scorecard 2017_P05_19062017.xlsx'    #  OK downloaded
#file_to_dl = 'https://nokia.sharepoint.com/sites/kpioffice/SitePages/Home.aspx'
