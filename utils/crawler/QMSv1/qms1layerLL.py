from lxml import etree
from QMSv1.getUrlInfo import get_urlInfo


# parse  first layer after the entrance of QMS(https://nokia.sharepoint.com/sites/NokiaQMS/SitePages/Home.aspx)     such as:   https://nokia.sharepoint.com/sites/NokiaQMS/SitePages/Policies%20and%20Strategy.aspx?slrid=7182589e-505c-5000-81be-649898865441
def qms1_parse(url):
    try:
        html = get_urlInfo(url)
        sel = etree.HTML(html)
    except ValueError:
        print(ValueError)
        print("Cookie potentially error")
        return None
    qms1_linkList = []
    f_NC_body_ahref = sel.xpath("//td[@id='script']/table[@summary='NOKIA content list ']/tr/td[@class='ms-vb2']/a/@href")
    f_t_ahref = sel.xpath("//tbody/tr[@class='ms-rteTableEvenRow-default']/td[@class='ms-rteTableEvenCol-default']/a/@href")

    #  -------------------------------------------------------------------------------------------------------------------------------------------

    s_NC_body_ahref = sel.xpath("//td[@id='script']/table[@summary='NSW content list ']/tr/td[@class='ms-vb2']/a/@href")

    s_FC_body_ahref = sel.xpath("//td[@id='script']/table[@summary='FN content list ']/tr/td[@class='ms-vb2']/a/@href")

    s_IC_body_ahref = sel.xpath("//td[@id='script']/table[@summary='ION content list ']/tr/td[@class='ms-vb2']/a/@href")

    s_MC_body_ahref = sel.xpath("//td[@id='script']/table[@summary='ION content list ']/tr/td[@class='ms-vb2']/a/@href")

    #  -------------------------------------------------------------------------------------------------------------------------------------------

    t_GC_body_ahref = sel.xpath("//td[@id='script']/table[@summary='GS content list ']/tr/td[@class='ms-vb2']/a/@href")

    t_CC_body_ahref = sel.xpath("//td[@id='script']/table[@summary='CO content list ']/tr/td[@class='ms-vb2']/a/@href")

    t_GOC_body_ahref = sel.xpath("//td[@id='script']/table[@summary='GOPS content list ']/tr/td[@class='ms-vb2']/a/@href")

    t_C0C_body_ahref = sel.xpath("//td[@id='script']/table[@summary='CF content list ']/tr/td[@class='ms-vb2']/a/@href")

    #  -------------------------------------------------------------------------------------------------------------------------------------------

    qms1_linkList.extend(f_NC_body_ahref)
    qms1_linkList.extend(f_t_ahref)
    qms1_linkList.extend(s_NC_body_ahref)
    qms1_linkList.extend(s_FC_body_ahref)
    qms1_linkList.extend(s_IC_body_ahref)
    qms1_linkList.extend(s_MC_body_ahref)
    qms1_linkList.extend(t_GC_body_ahref)
    qms1_linkList.extend(t_CC_body_ahref)
    qms1_linkList.extend(t_GOC_body_ahref)
    qms1_linkList.extend(t_C0C_body_ahref)

    return qms1_linkList

