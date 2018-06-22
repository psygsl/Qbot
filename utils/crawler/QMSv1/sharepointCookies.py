

import browser_cookie3
cookies = {}

cookies1 = browser_cookie3.chrome(domain_name="nokia.sharepoint.com")
for ck in cookies1:
    if ck.name == 'FedAuth' or ck.name == 'ai_session' or ck.name == 'ai_user' :
        cookies[ck.name] = ck.value


cookies2 = browser_cookie3.chrome(domain_name="sharepoint.com")
for ck in cookies2 :
    if ck.name == 'rtFa' :
        cookies[ck.name] = ck.value








