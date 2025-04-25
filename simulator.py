from modules import *

def smooth_scroll(driver, hist_i=0, i=0, limit=500, speed=50):
    while i < limit:
        i += speed
        driver.execute_script(f"window.scrollTo({hist_i}, {i});")
        hist_i = i
    return hist_i, i

def hard_scroll(driver):
    driver.execute_script(f"window.scrollTo(0, 100);")

def rdn_do():
    list_decision = [False for _ in range(5)] + [True for _ in range(4)]
    return random.choice(list_decision)

def post_scroll(driver: webdriver.Chrome, time_scroll):
    for i in range(4):
        try:
            home_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@class='x9f619 x3nfvp2 xr9ek0c xjpr12u xo237n4 x6pnmvc x7nr27j x12dmmrz xz9dl7a xn6708d xsag5q8 x1ye3gou x80pfx3 x159b3zp x1dn74xm xif99yt x172qv1o x10djquj x1lhsz42 xzauu7c xdoji71 x1dejxi8 x9k3k5o xs3sg5q x11hdxyr x12ldp4w x1wj20lx x1lq5wgf xgqcy7u x30kzoy x9jhf4c']")
                )
            )[0]
            home_btn.click()
            break
        except:
            time.sleep(1)
            print(error_color(f"[!] chưa tìm thấy nút home, thử refresh lại trang {i}/4"))
            driver.refresh()
            continue
    else:
        return 0

    hist_i, i, limit, speed = 0, 0, 500, 50
    for _ in range(time_scroll):
        hist_i, i = smooth_scroll(driver, hist_i, i, limit, speed)
        limit += 500
        time.sleep(1)
        print(system_color(f"[>] scroll lần {_+1}/{time_scroll}"))

        while True:
            if not rdn_do():
                print("[>] chờ 1s...")
                time.sleep(1)
            else:
                break

def explore_scroll(driver: webdriver.Chrome, time_scroll):
    for i in range(4):
        try:
            explore_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@class='x9f619 x3nfvp2 xr9ek0c xjpr12u xo237n4 x6pnmvc x7nr27j x12dmmrz xz9dl7a xn6708d xsag5q8 x1ye3gou x80pfx3 x159b3zp x1dn74xm xif99yt x172qv1o x10djquj x1lhsz42 xzauu7c xdoji71 x1dejxi8 x9k3k5o xs3sg5q x11hdxyr x12ldp4w x1wj20lx x1lq5wgf xgqcy7u x30kzoy x9jhf4c']")
                )
            )[2]
            explore_btn.click()
            break
        except:
            time.sleep(1)
            print(error_color(f"[!] chưa tìm thấy nút home, thử refresh lại trang {i}/4"))
            driver.refresh()
            continue
    else:
        return 0
    
    hist_i, i, limit, speed = 0, 0, 500, 50
    for _ in range(time_scroll):
        hist_i, i = smooth_scroll(driver, hist_i, i, limit, speed)
        limit += 500
        time.sleep(1)
        print(system_color(f"[>] scroll lần {_+1}/{time_scroll}"))
        
        while True:
            if not rdn_do():
                print("[>] chờ 1s...")
                time.sleep(1)
            else:
                break

def simulate(driver, time_scroll=5):
    choice = random.choice(["e", "p"])
    if choice == "e":
        print(purple_color("[>] simulate in Explore"))
        explore_scroll(driver, time_scroll)
    elif choice == "p":
        print(purple_color("[>] simulate in Post"))
        post_scroll(driver, time_scroll)

if __name__ == "__main__":
    driver = driver_init(r"E:\MySRC\golike-tools\golike_instagram_selenium\tteteyk")
    driver.get("https://instagram.com/")
    print(explore_scroll(driver, 10))
    input(">>> ")