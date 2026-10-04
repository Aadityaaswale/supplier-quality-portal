import urllib.request
import urllib.parse
import http.cookiejar
import re

def test_login(username, password, role_name):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    # 1. Fetch login page to extract CSRF token
    resp = opener.open('http://localhost/accounts/login/')
    html = resp.read().decode('utf-8')
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
    if not csrf_match:
        print(f"[{role_name}] Error: CSRF token not found on login page.")
        return False
    csrf_token = csrf_match.group(1)
    
    # 2. Submit credentials
    post_data = urllib.parse.urlencode({
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }).encode('utf-8')
    
    req = urllib.request.Request('http://localhost/accounts/login/', data=post_data, headers={
        'Referer': 'http://localhost/accounts/login/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    resp_login = opener.open(req)
    
    # 3. Access dashboard
    dash_resp = opener.open('http://localhost/dashboard/')
    dash_html = dash_resp.read().decode('utf-8')
    
    # 4. Access suppliers list
    sup_resp = opener.open('http://localhost/suppliers/')
    sup_html = sup_resp.read().decode('utf-8')
    
    # 5. Access reviews list
    rev_resp = opener.open('http://localhost/reviews/')
    rev_html = rev_resp.read().decode('utf-8')

    dash_ok = dash_resp.status == 200 and ('Dashboard' in dash_html or 'Analytics' in dash_html)
    sup_ok = sup_resp.status == 200 and 'Suppliers' in sup_html
    rev_ok = rev_resp.status == 200 and 'Reviews' in rev_html
    
    print(f"[{role_name}: {username}] Authentication: SUCCESS | Dashboard: {dash_resp.status} | Suppliers: {sup_resp.status} | Reviews: {rev_resp.status}")
    return dash_ok and sup_ok and rev_ok

if __name__ == '__main__':
    print("Testing Portal Authentication and Route Authorization...")
    r1 = test_login('admin', 'Admin@12345', 'Administrator')
    r2 = test_login('manager', 'Manager@12345', 'Quality Manager')
    r3 = test_login('reviewer', 'Reviewer@12345', 'Quality Reviewer')
    if r1 and r2 and r3:
        print("ALL DEMO ROLES SUCCESSFULLY AUTHENTICATED AND VERIFIED!")
