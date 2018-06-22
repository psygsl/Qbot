from lxml import etree
from QMSv1.qmsUrls import qmsUrls
from QMSv1.getUrlInfo import get_urlInfo
import re
from QMSv1.qms1layerLL import qms1_parse
from QMSv1.qmsDownlPDF import downlPDF
import time
from QMSv1.FolderURLs import folderUrls

from pymongo import MongoClient
import QMSv1.mongoSetting as ms



# import browser_cookie3
# from NonFileUrlLinkProcess import get_deltaPlaceHolderMain
# from tld import get_tld


def stripMidSpace(strObj):
    stripurl = ''
    for str in re.split('\s', strObj):
        stripurl += str + '%20'
    return stripurl.rstrip('%20')


def get_deltaPlaceHolderMain(html):
    try:
        sel = etree.HTML(html)
    except ValueError:
        print(ValueError)
        return False
    # pageTitle = sel.xpath("//head/title/text()")[0]

    if sel.xpath(
            "//div[@id='DeltaPlaceHolderMain']/div[@id='wizdomPageLayout']//div[@class='row']//div[@class='col-md-12']/div[@class='row'][2]/div[@class='col-md-9']"):
        deltaPlaceHolderMain_Element = sel.xpath(
            "//div[@id='DeltaPlaceHolderMain']/div[@id='wizdomPageLayout']//div[@class='row']//div[@class='col-md-12']/div[@class='row'][2]/div[@class='col-md-9']")
        ahref = sel.xpath(
            "//div[@id='DeltaPlaceHolderMain']/div[@id='wizdomPageLayout']//div[@class='row']//div[@class='col-md-12']/div[@class='row'][2]/div[@class='col-md-9']//a/@href")
    elif sel.xpath(
            "//div[@id='DeltaPlaceHolderMain']/div[@id='wizdomPageLayout']//div[@class='row']/div[@class='col-md-9']"):
        deltaPlaceHolderMain_Element = sel.xpath(
            "//div[@id='DeltaPlaceHolderMain']/div[@id='wizdomPageLayout']//div[@class='row']/div[@class='col-md-9']")
        ahref = sel.xpath(
            "//div[@id='DeltaPlaceHolderMain']/div[@id='wizdomPageLayout']//div[@class='row']/div[@class='col-md-9']//a/@href")
    elif sel.xpath("//div[@id='DeltaPlaceHolderMain']/div[@id='ctl00_PlaceHolderMain_WikiField']"):
        deltaPlaceHolderMain_Element = sel.xpath(
            "//div[@id='DeltaPlaceHolderMain']/div[@id='ctl00_PlaceHolderMain_WikiField']")
        ahref = sel.xpath("//div[@id='DeltaPlaceHolderMain']/div[@id='ctl00_PlaceHolderMain_WikiField']//a/@href")
    else:
        deltaPlaceHolderMain_Element = sel.xpath("//div[@id='DeltaPlaceHolderMain']")
        ahref = sel.xpath("//div[@id='DeltaPlaceHolderMain']//a/@href")
    try:
        deltaPlaceHolderMain = deltaPlaceHolderMain_Element[0].xpath('string(.)').strip()
    except IndexError:
        deltaPlaceHolderMain = ''
    return ahref, deltaPlaceHolderMain



wpqvar = ['WPQ' + str(seq_var) + 'ListData' for seq_var in range(1, 11)]


def write_WPQListDataUrl_intocsv(html, link, wpqvar=wpqvar):
    csv_string = ''
    for wpq in wpqvar:
        if wpq in html:
            csv_string += link + '\n'
    with open('QMSv1/WPQListDataUrl.csv', 'a') as f:
        f.write(csv_string)



allLinksInQMSList = []
# content = []
errorLink = []
def get_ahref(aLayerLink):
    global allLinksInQMSList
    global content
    global errorLink
    ahref = []
    aLayerLink = get_trueLinkList([aLayerLink])[0]
    if aLayerLink.endswith('.pdf'):
        try:
            downlPDF(aLayerLink, aLayerLink.split('/')[-1].split('.')[0].replace('%20', ''))
        except TypeError:
            pass
    elif aLayerLink.__contains__('.mp4') or aLayerLink.__contains__('.jpg') or aLayerLink.__contains__('.pptx') or aLayerLink.__contains__(
            '.zip') or aLayerLink.__contains__('.xlsx') or aLayerLink.__contains__('.txt') or aLayerLink.__contains__(
            '.ppt') or aLayerLink.__contains__('.xls') or aLayerLink.__contains__('.doc') or aLayerLink.__contains__(
            '.docx') or aLayerLink.__contains__('.wmv') or aLayerLink.__contains__('.PPTX'):
        write_intocsv([aLayerLink],'QMSv1/mediaUrls.txt', encoding='utf-8')
        return False
    else:
        html = get_urlInfo(aLayerLink)
        if html:
            try:
                save_anc_db(aLayerLink, get_deltaPlaceHolderMain(html)[1])
            except:
                errorLink.append(aLayerLink)
                save_anc_db(aLayerLink, 'Error as Empty')
                pass
            write_WPQListDataUrl_intocsv(html, aLayerLink)
            print("Crawling:", aLayerLink)
            ahref = get_deltaPlaceHolderMain(html)[0]
            if not set(get_trueLinkList(ahref)).issubset(set(allLinksInQMSList)):
                standardizing_append = list(set(get_trueLinkList(ahref))-set(allLinksInQMSList)-set(folderUrls))
                allLinksInQMSList.extend(standardizing_append)
                print("Newly added link into allLinksInQMSList:", standardizing_append)
                print('Writing Newly-added link into txt file....')
                write_intocsv(standardizing_append, 'allLinksInQMSList.txt', encoding='utf-8')
                # print('Writing new-content into txt file....')
                # write_intocsv(content, 'allcontent.txt', encoding='utf-8')
            else:
                return None
    return ahref

UnicodeEncodeErrorList = []
def write_intocsv(*args, **kwargs):
    global UnicodeEncodeErrorList
    csv_string = ''
    for _ in args[0]:
        if '\u200b' in _:
            _ = _.replace('\u200b','\\u200b')
            csv_string += _ +'\n'
        else:
            csv_string += _ + '\n'
    try:
        with open(args[1], 'a', **kwargs) as f:
            f.write(csv_string)
            return True
    except UnicodeEncodeError:
        UnicodeEncodeErrorList.append(args[0])
        print("UnicodeEncodeError Happened!")
        pass


# in qms1Urls , some qms1Urls are just a href,not a complete url,this function committed to get entire url address, saved in a list
def get_trueLinkList(q1urls):
    truelinks = []
    try:
        for url in q1urls:
            dominUrl = 'https://nokia.sharepoint.com'
            if url.startswith("javascript") or url.startswith("mailto"):
                continue
            elif url.startswith('/'):
                truelinks.append(stripMidSpace(dominUrl + url))
            else:
                if url.startswith(dominUrl):
                    truelinks.append(stripMidSpace(url))
        return truelinks
    except TypeError:
        return None
# save data into db
def save_anc_db(aahref,acontent):
    anc_dic = {}
    client = MongoClient(ms.ipAddr, ms.port)
    db = client[ms.dbname]
    db.authenticate(ms.account, ms.pwd)
    collection = db[ms.collectionName]
    anc_dic[aahref] = acontent
    collection.insert(anc_dic, check_keys=False)





