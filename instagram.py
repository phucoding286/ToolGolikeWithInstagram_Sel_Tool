from modules import *
from simulator import random_scroll

def follow(driver, link, time_scroll=5):
    try:
        username = link.split("/")[-1]

        find_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='x9f619 x3nfvp2 xr9ek0c xjpr12u xo237n4 x6pnmvc x7nr27j x12dmmrz xz9dl7a xn6708d xsag5q8 x1ye3gou x80pfx3 x159b3zp x1dn74xm xif99yt x172qv1o x10djquj x1lhsz42 xzauu7c xdoji71 x1dejxi8 x9k3k5o xs3sg5q x11hdxyr x12ldp4w x1wj20lx x1lq5wgf xgqcy7u x30kzoy x9jhf4c']")
            )
        )[1]
        find_btn.click()
        time.sleep(2)
        
        find_cell = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[aria-label="Search input"]')
            )
        )
        find_cell.send_keys(username)
        time.sleep(2)
        
        error_find_username = True
        for _ in range(10):
            try:
                first_user = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xxbr6pl xbbxn1n xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
                    )
                )[0]
                first_user.click()
                error_find_username = False
                break
            except:
                time.sleep(1)
                print(error_color(f"[!] có lỗi khi tìm kiếm đối tượng username, thử lại..."))
                continue
        if error_find_username:
            return {"error": "Có lỗi khi find và check username"}
        
        username_correct = False
        for _ in range(5):
            try:
                check_username = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//span[@class='x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft']")
                    )
                )
                print(system_color(f"[..] Đang detect username -> {check_username[0].text}"))
                if check_username[0].text == username:
                    username_correct = True
                    break
                time.sleep(1)
            except:
                time.sleep(1)
                continue
        if not username_correct:
            print(error_color("[!] Khác username!"))
            return {"error": "Có lỗi khi follow"}
        
        # scroll xuôi
        out = random_scroll(driver)
        if "error" in out: return out
        # scroll ngược
        driver.execute_script(f"window.scrollTo(1000, 0);")

        follow_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='_ap3a _aaco _aacw _aad6 _aade']")
            )
        )
        if follow_btn.text == "Follow" or follow_btn.text == "Theo dõi":
            follow_btn.click()

            for _ in range(10):
                follow_btn = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='_ap3a _aaco _aacw _aad6 _aade']")
                    )
                )
                if follow_btn.text == "Following" or follow_btn.text == "Đang theo dõi":
                    break
                time.sleep(1)

            if follow_btn.text == "Follow" or follow_btn.text == "Theo dõi":
                return {"follow_block": "Không thể follow"}
            else:
                return {"success": "Follow thành công"}
        
        elif follow_btn.text == "Following" or follow_btn.text == "Đang theo dõi":
            return {"followed": "Đã follow trước đó"}
        
    except:
        return {"error": "Có lỗi khi follow"}

if __name__ == "__main__":
    driver = driver_init(r"E:\MySRC\golike-tools\golike_instagram_selenium\ntam123456_", False)
    driver.get("https://instagram.com/")
    input(">>> ")
    print(follow(driver, "https://www.instagram.com/alva.order"))
    input(">>> ")