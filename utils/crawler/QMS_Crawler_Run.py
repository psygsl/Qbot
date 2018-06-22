from QMSv1.QMSv1 import *

if __name__ == '__main__':
    start = time.time()
    ol = 0
    for eachList in qmsUrls:
        qms1Urls = qms1_parse(eachList)  # get urls in first layer of qms such as 'https://nokia.sharepoint.com/sites/ReadyforGrowthTransformation' which is  """in""" qmsUrls's content   HTTP RESPONSE is :  200
        trueLinks = get_trueLinkList(qms1Urls)  # first layer of qms's truelinks, list        such as  https://nokia.sharepoint.com/sites/ReadyforGrowthTransformation
        # allLinksInQMSList.extend([ispdf if not ispdf.endswith('.pdf') else downlPDF(ispdf, ispdf.split('/')[-1].split('.')[0].replace('%20', '')) for ispdf in trueLinks ])  # now allLinksInQMSList stores all hrefs of first layer
        # allLinksInQMSList = list(filter(None,allLinksInQMSList))
        ol = allLinksInQMSList.__len__()
        allLinksInQMSList.extend(trueLinks)
        write_intocsv(allLinksInQMSList, 'QMSv1/allLinksInQMSList.txt', encoding='utf-8')
        # now you are in     https://nokia.sharepoint.com/sites/ReadyforGrowthTransformation

        # First step:just get all url,no consider of content
        for each in allLinksInQMSList:
            if allLinksInQMSList.index(each) < ol:
                continue
            else:
                print("allLinksInQMSList length: ", allLinksInQMSList.__len__())
                # print("content length: ", content.__len__())
                get_ahref(each)
    end = time.time()
    print("Total time consuming : %f s" % (end - start))
    print(errorLink)
    print(UnicodeEncodeErrorList)