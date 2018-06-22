from MongoConn import MongoConn
import requests
import json
import time
import browser_cookie3


def search_people():    # the key is what you want to search , * means all datas
    if __name__ == "__main__":
        my_conn = MongoConn()
    proxies = {'http': 'http://10.144.1.10:8080', 'https': 'http://10.144.1.10:8080'}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "upgrade-insecure-requests": "1",
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "cache-control":"max-age=0"
    }
    cookies = {}
    cookies1 = browser_cookie3.chrome(domain_name="delve.office.com")
    for ck in cookies1:
        if ck.name == 'X-Delve-AuthEur' or ck.name == 'X-Delve-DigestCookieEur':
            cookies[ck.name] = ck.value

    cookies2 = browser_cookie3.chrome(domain_name="office.com")
    for ck in cookies2:
        if ck.name == 'AADAuth' or ck.name == 'AADAuthCode' or 'AADSID' or 'AADState' or 'AADState' or 'AMCV_EA76ADE95776D2EC7F000101%40AdobeOrg' or 'LPVID' or 'MSFPC' or '__qca' or '_mkto_trk' or 'optimizelyEndUserId' or 'seerid':
            cookies[ck.name] = ck.value
    # cookies = {'X-Delve-AuthEur':'pQG9-JaUMkaXrL7NcPl7qQ0ULsX_AcarU0o9leFaprMcnveOuKyrZmAOIT4-tfOnOUaK5vhVysCE9R1M1bwv5Vi8IU2diL0x21xXozylvNRlMmW-0iacyLHyOBIvWrwBUj1RXJ3wV9Z5tmOK8M0jVx8oIdh0XHJ0ewcp_brojoDGXT1fsxGoDARgzICrh5rj76XTOO69wtzTSEZjQ5HUaMiupf6FZnl2NCutTeFVgXzDG5Npb0rNA1GosbvMN62khI55Jm7pakhKN5c6nqk_Ja54piv-EffTsZkLTsRk3n2yCNNd-1n_JfgNIbpBPj9zu3Qxn7wp5h0zNTd61rarDysdV74L87GfVE8H4_b3Fp_a1iZutjy3uha5vPLkTF-jg8Rh0zqxJkW62yAaf-iO8rSOfdXvx7nBCn0Kkj7n5M2A7hHmxHS8y7lcsHl-jk9e_4bNSt8ifBvUnFjmaGGlyJzNq5waychMRY7xlvr1zvKptZciERw6GD3MHDUMydRNn2hfZ9Gv4DvIW4Dfd0R90dpfpTcQ0ggePUCqygjkWGKZVf03DoW1LAshshMs9t-8IayKnP4A9if8n9eF4atKiE1Olbh4Pgb9WP7IZ1HAwqiDMPEL4tkI_2kDwj5eDJjlW-NAcWcaRHw5_0rL1Ho_mYBOWCHYMnsHYJrqIW2b23b_Tyjsto0E5TpEdF8gydVByjdUpVtLZZOkMwZT_5NRAxMkAk1yiGJPHILMnrz4hfDRwbaNj9-6uGhQm6_FtUk68Dj7whcGzSBd99F9bFQyQKrbwguA3v7t4rAVEJLy_315XGbmj8_uxWk4to3QxANJMUma60jtYWtsSLDnKoSIvTm29fa5LY_dfnD_NUIZaPhd4R9R5TTmBaYtB0c2_nkr-lfvukffbFunTbnUKVtlg0-nuvM4QxxUeQ4-0CmRxVNRLgS7BFTt2J6PZY1qhSIbT5qYPK32ZftHhJH1Y14ZP8TzaCbekXyIbiIPa3vXAvkrpgkoE8Pm1R6_uwnb_N7EGdsN7ZHs6kld2dB9DiftV886XZHv12gb7nwOkcOFg_wOYjVUrxeO5OYrfTm3dR3-Su4Te-MYK3-iQZBzCXl8lESHjOXGIJy5TnQlNTpyoqoIoNXN7iMpSjedO6r3oGm0Xl5uQD6Jx1kCvtqnK5VLGr93hOsnTXLp4GynCzz3zrgXX357uLNL5RPQZ4FG-ZfaEpGIb8qJ301b8x8Ap6EhpVujFtvQEtVLnrk9PALLh3ErjUNtb9ipTOnLH9KeMZhnpG1Tx3YTtoyzHrLOIkiu9b5y_m5v9k7M-drCKJ17cFQz6R23aV7mFaynP3j7Ir2unDpjNpGH1UF419YIgU9LzLvRaNJ7ZH63UeOkDca1iYHj5bEXcl77OYImOEZbuRGf9fpyNp-66EPCL5C9dbTv3ET-kPRzMPqfXR2Bysz54vFvOHyLpdyk4bZ3jeMJ-bXveN_C423O3WYGFrNeEguJwxsYp-BSbRV3Wx1aGuU0z52387VlL_-v9H_Ycd1NI0K1pZVNr3jcMRt9bkHfNs3So6tbGJXZQx4HHYSgGPCdv7yDaSDs3LwTBciG8ryS_FPMH-GmhMdU7uN2GVcI4xnVozVsmWVEvB7LC69Ee_tT-GIbkOFBz2RLJMFdUjtbua4pRfcwxOLfeMBvTt2pq5Lf_XjV38dJw8_V9zZ7taqG7JQeQSYjzMpo3b4gMlByQUW4ctWNXidt54esNsOvTPXfa5VvIJjXLj8Z6gTfxVt-kYwpFQ_6EHuVdSDyiXkobwE5571IaKu9oN3CT0rog_HtpP-KWqyXWJo34njqvHYzE8GDVNKKqDTpCiGCrk8zrXM9WAvnGc0S0eGP_5ogshpMGq8stM-UhjJZGGJ3TUHuCFttWaQom1rxMu0r0gVOfz1gGgKy6msl8DbA7zzvF_1wE5xMfZ1C5_uPzhTXLO4sEt_SMJGryHxwtOcKtq8S8qbpJ7TFLNKgrqVDAr9S0IWIDnnK58C2BClK8tJBYniinCJAgX4SWgkif08cczHcrAf2RCvbu4ah8PBRFI0N9smiTBShWVtXVEDSYpB-DYpbIqB3eRoNdTi9DldEg1Lmgoyt8dptTHBxmWahdbZBsMZo8G59uSiOCsZvI9jjTpkBIjk3ogr6Tjx0c1bZyi_hxDE66aDIWaM674y9uTzXHvGNh36pQuh7lN-Q5FoOOlQcYEPHJxXe761Tc70vCJXDRg6RKqOLAu178wjMp-fxDoljlhtcYIUCYE-vcMuM2jf71GYZF4DRzEfjm9wxqfIRQk41',
    #            'X-Delve-DigestCookieEur':'z3DP4We7EFNkbLuzonxC42bL-Iz0dqqyQ371v47oCn9pHL2LlfG3XvlDxdamaF5adSssG4KIPhGe67tovAqVgXtGxgNiLUGIuP39ib1-5Zs1',
    #            'optimizelyEndUserId':'oeu1521178579887r0.16230397634938765',
    #            'AADAuth':'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkZTaW11RnJGTm9DMHNKWEdtdjEzbk5aY2VEYyIsImtpZCI6IkZTaW11RnJGTm9DMHNKWEdtdjEzbk5aY2VEYyJ9.eyJhdWQiOiI0YjIzMzY4OC0wMzFjLTQwNGItOWE4MC1hNGYzZjIzNTFmOTAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81ZDQ3MTc1MS05Njc1LTQyOGQtOTE3Yi03MGY0NGY5NjMwYjAvIiwiaWF0IjoxNTIyODE5ODk3LCJuYmYiOjE1MjI4MTk4OTcsImV4cCI6MTUyMjkwNjU5NiwiYWlvIjoiQVRRQXkvOEdBQUFBSE9kSUZOZDUzM296YkM0U0Q5MEZIandNZ3Q0WUpBNzFkd0J5TlcwdW9BbmZXbkRNcE9lODRRUXBDbEhidFdLeCIsImFtciI6WyJ3aWEiLCJtZmEiXSwiY19oYXNoIjoienA3RGk4VjJuZmg0VkUxeGlkNzRaZyIsImZhbWlseV9uYW1lIjoiU2hhbyIsImdpdmVuX25hbWUiOiJZaWtlIiwiaW5fY29ycCI6InRydWUiLCJpcGFkZHIiOiIxMzEuMjI4LjY3LjIyIiwibmFtZSI6IlNoYW8sIFlpa2UgKEVYVC1OU0IgLSBDTi9IYW5nemhvdSkiLCJub25jZSI6IjFiMWE1NjkzLTdlMWEtNGUzNS04NjIxLTUyZDA0ZDUxNmM2My42MzY1ODQxNjk5Mzc3OTE2NTciLCJvaWQiOiJhZDA4MjE4OS05NjFhLTRkZWEtODZlOC0xMjIyODllNTk2YmYiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMTU5MzI1MTI3MS0yNjQwMzA0MTI3LTE4MjU2NDEyMTUtMjc1MjU3NCIsInB1aWQiOiIxMDAzMDAwMEE5M0MwODEzIiwic3ViIjoiaUtwcUJpa0ItdVJUVjRGbkxjamVOV0kwdTc2UjZyRllENkdDMFNFSkFQYyIsInRpZCI6IjVkNDcxNzUxLTk2NzUtNDI4ZC05MTdiLTcwZjQ0Zjk2MzBiMCIsInVuaXF1ZV9uYW1lIjoieWlrZS5zaGFvLmV4dEBub2tpYS1zYmVsbC5jb20iLCJ1cG4iOiJ5aWtlLnNoYW8uZXh0QG5va2lhLXNiZWxsLmNvbSIsInV0aSI6IlZqRGw0blNjOGtldmdiZE5SdlV2QUEiLCJ2ZXIiOiIxLjAifQ.xOXA6Aw2m90ZuMJUvBOe41hPLo4a7h6X3g6CKqSseLogxzEWoTrl5qxBS-pjYjgtbXaqjGSBKtCD79DvBg7DQPOkIvOiKqFIIzPq1DA0SMzE3a1VYwZt99mg2n94MfYeh4FelwzpiAbvc7VMe56LnY5am31TfwZxHicyfHGbomMJQIM4qMi2GQ_hfj9HBVRzoPKLRaAYoKvvjf4JOmalaDblDpTLw6xqzSc7SNLs7Hv-LOLoPEBNDzp4jXu5sIBlGxLvOQcdf3SPyITtOGWjwaD1To-YA1uS8NK2MuxBMxscyfI_rUueIDBNkGyfke6tEGz0TKH2uDreCMW1BBiJtg',
    #            'AADAuthCode':'AQABAAIAAABHh4kmS_aKT5XrjzxRAtHzSRWVMpfEwaJhitHhaM5MxR4M2mNu5PJYrgtvsOwY6f4sIsCaGWTZth_lWxptWF1QxcDdaK1OPK6tyiPs95WjKk1WnwCuH-rszBPZiBVowifwb0Whhh_5c2ZJtx191lEs-sASfiCZG02OFQ99HTP_SD4NnHvv2T9PcAplSfgdLJjJzRpAppe6dEHEpSviSDdmaDNL5fL0QVlatuhzUo7GViHObWJ5AyOohteMBemUDAHkwLmhor6QznX6ZvdD4TIY3OvbpQfdICDzLAut_jFgsFz2JViYT4qc-GdqRukiakNMUVFwwEpqvuZm8dAmIp6O36am4XLburXkRQSY5bu6JBwrXtoW_FubKPpQIC7ePmjtpywGJTFXCE-Mf3Js7z36Hm8phG84WSDJdX-r8jlkwrhMo-NO0mnCmnHlq8ua6bLISzbge7Cd1NhoTTWr2YIyUnA-PwQEYN6Ccc7f43zMlnuBoZPoS_UmoDqnsmE_6IcedOkva3TbxE6gnLuDLSofTUB_RlXF1ZJkjhnQDWnYi7icYkcbrD7gn7KI8K5iil1oLvcg5GjozM5uZwxuAaaGrm9189uA8eve9QeZ2K10l8QHqFtC3NbTzQ4Ryv-NW5rWCZ0nxNCsKNlpXGvnKclgK9Czvn54K0K8ZmhP_nMulgSMRGM8rY6mxf_9Hpag4hyQHrl2fHaMtzkj5_R8Gp_XAbo03bV3dtcnYqnzadBB_EbwxxC5jJzEF2bkZknp9ROBwlhN4Az1umyB2fWloiGZIAA',
    #            'AADSID':'9c158207-8c74-47f0-85f9-7bbcf6343adf'}
    start = 0;
    url = 'https://eur.delve.office.com/mt/v3/search/people?queryText=*'
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
    req = requests.session()
    resp = req.get(url, verify=False, stream=True, headers=headers, cookies=cookies, proxies=proxies,timeout=None)

    while resp.status_code == 401:              #   there is a problem that status_code shows 401 error sometime,but status_code will show 200 after some minutes.
        resp.close()
        print("HTTP RESPONSE is : ", resp.status_code)
        resp = req.get(url, verify=False, stream=True, headers=headers, cookies=cookies, proxies=proxies,timeout=None) #  i can not solve this issue great. so i let the crawl run agagin if it shows 401
    html = resp.content.decode("utf-8")
    resp.close()
    data = json.loads(html)
    total_count = data['TotalCount']    #we should get total_count first
    print(total_count)
    top = 500

    my_conn.db['delve_download'].remove({})

    while total_count>start:
        lst = []
        if(top>total_count-start):
            top = total_count-start
        url = 'https://eur.delve.office.com/mt/v3/search/people?queryText=*&top='+str(top)+'&skip='+str(start)    #start means where you
        print(url)
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
        req = requests.session()
        try:
            resp = req.get(url, verify=False, stream=True, headers=headers, cookies=cookies, proxies=proxies,timeout=None)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        while resp.status_code==401 or resp.status_code==500:
            resp.close()
            print("HTTP RESPONSE is : ", resp.status_code)
            try:
                time.sleep(20)
                resp = req.get(url, verify=False, stream=True, headers=headers, cookies=cookies, proxies=proxies,timeout=None)
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
        if resp.status_code == 200:
            print("HTTP RESPONSE is : ", resp.status_code)
            html = resp.content.decode("utf-8")
            resp.close()
            data = json.loads(html)
            results = data['Results']
            for result in results:
                dic = {}
                dic['Id'] = result["Id"]
                dic['FullName'] = result["FullName"]
                if "Email" not in result.keys():
                    dic['Email'] = ''
                else:
                    dic['Email'] = result["Email"]
                if "WorkPhone" not in result.keys():
                    dic['WorkPhone'] = ''
                else:
                    dic['WorkPhone'] = result["WorkPhone"]
                if "JobTitle" not in result.keys():
                    dic['JobTitle'] = ''
                else:
                    dic['JobTitle'] = result["JobTitle"]
                if "Department" not in result.keys():
                    dic['Department'] = ''
                else:
                    dic['Department'] = result["Department"]
                if "Memberships" not in result.keys():
                    dic['Memberships'] = ''
                else:
                    dic['Memberships'] = result["Memberships"]
                if "Schools" not in result.keys():
                    dic['Schools'] = ''
                else:
                    dic['Schools'] = result["Schools"]
                if "Skills" not in result.keys():
                    dic['Skills'] = ''
                else:
                    dic['Skills'] = result["Skills"]
                if "AboutMe" not in result.keys():
                    dic['AboutMe'] = ''
                else:
                    dic['AboutMe'] = result["AboutMe"]
                lst.append(dic)

            start += top
            print(total_count)
            print(start)
            if(len(lst)>0):
                my_conn.db['delve_download'].insert(lst)        #   insert the datas to the database


