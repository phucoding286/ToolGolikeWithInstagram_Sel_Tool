from modules import *

list_emoji = ["hi", "i love you", "how are you", "hi how are you", "hello"]

def like_post_when_scroll(driver: webdriver.Chrome, idx_for_like: int):
    try:
        like_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81']")
            )
        )
        driver.execute_script("arguments[0].click();", like_btn[idx_for_like]) if idx_for_like % 2 == 0 else driver.execute_script("arguments[0].click();", like_btn[idx_for_like+1])
        return ""
    except:
        return {"error": "Lỗi khi like post"}

def comment_post_when_scroll(driver: webdriver.Chrome, idx_for_like: int):
    global list_emoji
    try:
        like_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81']")
            )
        )
        driver.execute_script("arguments[0].click();", like_btn[idx_for_like]) if idx_for_like % 2 == 1 else driver.execute_script("arguments[0].click();", like_btn[idx_for_like+1])
        for _ in range(5):
            try:
                comment_cell = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//textarea[@class='x1i0vuye xvbhtw8 x1ejq31n xd10rxx x1sy0etr x17r0tee x5n08af x78zum5 x1iyjqo2 x1qlqyl8 x1d6elog xlk1fp6 x1a2a7pz xexx8yu x4uap5 x18d9i69 xkhd6sd xtt52l0 xnalus7 xs3hnx8 x1bq4at4 xaqnwrm']")
                    )
                )
                comment_cell[-1].click()
                break
            except:
                time.sleep(1)
                continue
        else:
            return {"error": "Lỗi khi like post"}
        comment_cell = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//textarea[@class='x1i0vuye xvbhtw8 x1ejq31n xd10rxx x1sy0etr x17r0tee x5n08af x78zum5 x1iyjqo2 x1qlqyl8 x1d6elog xlk1fp6 x1a2a7pz xexx8yu x4uap5 x18d9i69 xkhd6sd xtt52l0 xnalus7 xs3hnx8 x1bq4at4 xaqnwrm focus-visible']")
            )
        )
        comment_cell[-1].send_keys(random.choice(list_emoji))
        comment_cell[-1].send_keys(Keys.ENTER)
        
        time.sleep(4)
        driver.back()
        return ""
    except:
        return {"error": "Lỗi khi like post"}

def scroll_to_down(driver: webdriver.Chrome):
    rdn_times_scroll = random.randint(2, 10) # random scroll
    for i in range(rdn_times_scroll):
        driver.execute_script(f"window.scrollTo({i*600}, {(i+1)*600});")
        waiting_ui(random.randint(1, 3), "Đợi để tiếp tục scroll") # random wait
        print(system_color(f"[>] Đã scroll, số lần {i+1}/{rdn_times_scroll}"))
        
        if driver.current_url == "https://www.instagram.com/":
            choose_like_post = random.choice([True] + [False for _ in range(81)])
            like_out = like_post_when_scroll(driver, i) if choose_like_post else ""
            if "error" in like_out: return like_out
            if choose_like_post: print(success_color(f"[#] Đã like post thứ {i}"))
            
            choose_cmt_post = random.choice([True] + [False for _ in range(81)])
            cmt_out = comment_post_when_scroll(driver, i) if choose_cmt_post else ""
            if "error" in cmt_out: return cmt_out
            if choose_cmt_post: print(success_color(f"[#] Đã comment post thứ {i}"))
    return ""

def scroll_to_up(driver: webdriver.Chrome):
    rdn_times_scroll = random.randint(2, 10)
    for i in range(rdn_times_scroll):
        driver.execute_script(f"window.scrollTo({i*-100}, {(i+1)*-100});")
        waiting_ui(random.randint(1, 3), "Đợi để tiếp tục scroll") # random wait
        print(system_color(f"[>] Đã scroll, số lần {i+1}/{rdn_times_scroll}"))
    return ""

def random_scroll(driver: webdriver.Chrome):
    total_scroll = random.randint(1, 3)
    for i in range(total_scroll):
        is_scroll_down = random.choice([True, False])
        scroll_out = scroll_to_down(driver) if is_scroll_down or i == 0 else scroll_to_up(driver)
        if "error" in scroll_out: return scroll_out
        print(system_color(f"[>] Số lần tổng scroll {i+1}/{total_scroll}"))
    return ""

def post_scroll(driver: webdriver.Chrome):
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

    return random_scroll(driver)

def explore_scroll(driver: webdriver.Chrome):
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
    
    return random_scroll(driver)

def simulate(driver):
    choice = random.choice(["e", "p"])
    if choice == "e":
        print(purple_color("[>] simulate in Explore"))
        explore_scroll(driver)
    elif choice == "p":
        print(purple_color("[>] simulate in Post"))
        post_scroll(driver)

if __name__ == "__main__":
    driver = driver_init(r"E:\MySRC\golike-tools\golike_instagram_selenium\tteteyk")
    driver.get("https://instagram.com/")
    print(explore_scroll(driver, 10))
    input(">>> ")
