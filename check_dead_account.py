from modules import *
from golike import check_instagram_account_id, GOLIKE_HEADERS
GOLIKE_HEADERS['Authorization'] = open("auth.txt").read()
GOLIKE_HEADERS['t'] = open("t.txt").read()

check = check_instagram_account_id()
for account_id in check:
    uid = account_id[0]
    username = account_id[1]

    response = scraper.get(f"https://www.instagram.com/{username}/#")
    if len(response.text.split("- See Instagram photos and videos from")) > 1:
        print(success_color(f"[*] Username: {username}, hoạt động."))
    else:
        print(error_color(f"[!] Username: {username}, đã dead."))
    time.sleep(1)