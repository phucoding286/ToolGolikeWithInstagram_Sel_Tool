from golike import (
    check_instagram_account_id,
    get_jobs,
    drop_job,
    verify_complete_job,
    GOLIKE_HEADERS
)
from instagram import (
    follow
)
from simulator import (
    simulate
)

from modules import *


sessions_manager_file = "sessions.json"
if not os.path.exists(sessions_manager_file):
    with open(sessions_manager_file, "w", encoding="utf-8") as file:
        json.dump({"data": {}}, file)


def add_new_session():
    global sessions_manager_file
    r = check_instagram_account_id()
    username_id_ins_gl = {account_id[1]: account_id[0] for account_id in r}
    # nhập đường dẫn lưu trữ phiên trình duyệt chưa thông tin đã thiết lập
    path = input(system_color("[?] nhập đường dẫn đến phiên của bạn\n-> "))
    data = json.load(open(sessions_manager_file))
    # nhập tên người dùng instagram làm tên phiên
    while True:
        session_name = input(system_color("[?] Nhập username instagram của bạn\n-> "))
        if session_name in data['data']:
            print(error_color(f"[!] username {session_name} đã tồn tại vui lòng nhập username instagram mới!"))
            continue
        elif session_name not in username_id_ins_gl:
            print(error_color(f"[!] username {session_name} chưa tồn tại vui lòng nhập username instagram đúng!"))
            continue
        else:
            break
    # mở trình duyệt và yêu cầu nhập thông tin thiết lập
    driver = driver_init(path + "\\" + session_name)
    instagram_login(driver)
    driver.get("https://chromewebstore.google.com/detail/urban-vpn-proxy/eppiocemhmnlbhjplcgkofciiegomcon")
    input(system_color("[?] Tải extension urban-vpn về và nhấn enter\n-> "))
    # lưu lại tên phiên và phiên đã thiết lập
    data["data"][session_name] = path + "\\" + session_name
    json.dump(data, open(sessions_manager_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    # thông báo hoàn tất
    input(success_color("[#] Đã hoàn tất quy trình thêm phiên của bạn, nhấn enter để thoát\n->"))
    storage_cookies(driver, cookie_f_name=session_name)
    try:
        driver.quit()
    except:
        pass


def add_golike_auth(filename="auth.txt"):
    while True:
        inp = input(system_color("[?] Nhập vào auth golike của bạn\n-> "))

        if len(inp) < 10:
            print(error_color("[!] Chúng tôi không nghĩ bạn đã nhập auth hợp lệ!"))
            continue

        with open(filename, "w") as file:
            file.write(inp)
        
        print(success_color("[#] Đã lưu auth golike thành công!"))
        waiting_ui(4, "4s...")
        break


def add_golike_t(filename="t.txt"):
    while True:
        inp = input(system_color("[?] Nhập vào t golike của bạn\n-> "))

        if len(inp) < 4:
            print(error_color("[!] Chúng tôi không nghĩ bạn đã nhập t hợp lệ!"))
            continue

        with open(filename, "w") as file:
            file.write(inp)
        
        print(success_color("[#] Đã lưu t golike thành công!"))
        waiting_ui(4, "4s...")
        break


def storage_cookies(driver, cookie_f_name="session_name.pkl"):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    driver.get("https://www.instagram.com")
    pickle.dump(driver.get_cookies(), open("instagram_cookie_" + cookie_f_name + ".pkl", "wb"))
    print(success_color("[#] Đã lưu cookie thành công."))

def load_cookies(driver, cookie_f_name="session_name"):
    if not os.path.exists("instagram_cookie_" + cookie_f_name + ".pkl"):
        print(error_color("[!] File cookie chưa tồn lại"))
        return 0
    driver.get("https://www.instagram.com")
    cookies = pickle.load(open("instagram_cookie_" + cookie_f_name + ".pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    print(success_color("[#] Đã load cookie thành công."))


def __run(
        driver,
        account_id,
        max_times_rgj=5,
        max_wait_block=2
    ):
    """
    this function can return one in values
    'error_get_job' or 'error_drop_job' or
    'follow_block' or 'followed' or 
    'unknow_follow_error' or 'error_verify_job' or 'success')
    """

    try:
        simulate(driver)
    except:
        return "error"

    for i in range(max_times_rgj):
        rgj = get_jobs(account_id)
        if "error" in rgj:
            print(error_color(f"[!] Đã có lỗi nhận job, thử lại ({i+1}/{max_times_rgj})"))
            time.sleep(1)
        elif rgj[2] != "follow":
            print(error_color(f"[!] Không phải nhiệm vụ follow, thử lại ({i+1}/{max_times_rgj})"))
            rdj =  drop_job(rgj[1], rgj[3], account_id, rgj[2])
            if "success" in rdj:
                print(success_color(f"[#] {rdj['success']}"))
            else:
                print(error_color(f"[!] {rdj['color']}"))
                return "error_drop_job"
            time.sleep(1)
        else:
            break
    else:
        if "error" in rgj:
            return "error_get_job"
        
    print(system_color(f"[>] mục tiêu -> {rgj[0]}"))
        
    if "error" in rgj:
        rdj =  drop_job(rgj[1], rgj[3], account_id, rgj[2])
        if "success" in rdj:
            print(success_color(f"[#] {rdj['success']}"))
        else:
            print(error_color(f"[!] {rdj['color']}"))
            return "error_drop_job"

    rfl = follow(driver, rgj[0])
    if isinstance(rfl, dict) and "follow_block" in rfl:
        print(error_color(f"[!] {rfl['follow_block']}"))
        rdj = drop_job(rgj[1], rgj[3], account_id, rgj[2])
        if "success" in rdj:
            print(success_color(f"[#] {rdj['success']}"))
        else:
            print(error_color(f"[!] {rdj['color']}"))
            return "error_drop_job"
        waiting_ui(max_wait_block, text=f"Hãy đợi {max_wait_block} để tiếp tục do instagram bắt đầu block follow")
        return "follow_block"
    
    elif isinstance(rfl, dict) and "followed" in rfl:
        print(error_color(f"[!] {rfl['followed']}"))
        return "followed"
    elif isinstance(rfl, dict) and "success" in rfl:
        print(success_color(f"[$] {rfl['success']}"))
        pass

    else:
        print(error_color("[!] Có lỗi không xác định khi follow"))
        rdj =  drop_job(rgj[1], rgj[3], account_id, rgj[2])
        if "success" in rdj:
            print(success_color(f"[#] {rdj['success']}"))
        else:
            print(error_color(f"[!] {rdj['color']}"))
            return "error_drop_job"
        return "unknow_follow_error"
    
    rvrf = verify_complete_job(rgj[1], account_id)

    if isinstance(rvrf, dict) and "error" in rvrf:
        print(error_color(f"[!] {rvrf['error']}"))
        return "error_verify_job"
    else:
        print(success_color(f"[$] {rvrf[1]}"))
        print(success_color(f"[$] {rvrf[2]}"))
        from golike import prices
        print(success_color(f"[$] tổng thu thập -> {prices}đ"))
        return "success"

def __main(username_id_ins_gl, data, waitime, max_wait_block, headless, hide_chrome):
    for username_ins, session_path in data.items():
        try:
            print(system_color(f"[>] account đang chạy -> {username_ins}"))
            driver = driver_init(session_path, headless, hide_chrome)
            load_cookies(driver, cookie_f_name=username_ins)
            __run(driver, username_id_ins_gl[username_ins], 5, max_wait_block)
            storage_cookies(driver, cookie_f_name=username_ins)
            driver.quit()
            waiting_ui(waitime, f"đợi {waitime}s để tiếp tục")
        except:
            try:
                driver.quit()
            except:
                pass
            waiting_ui(waitime, f"Có lỗi không xác định hãy đợi {waitime}s để tiếp tục")
            try:
                r = requests.get("https://www.google.com/")
            except:
                print(error_color("\n[!] Không có mạng!"))
                input(system_color("[!] Phát hiện không có mạng, chương trình tạm dừng, chờ can thiệp, enter để tiếp tục chạy\n-> "))

def main_program():
    waitime = int(input(system_color("[?] Nhập số thời gian delay giữa mỗi lần tương tác\n-> ")))
    max_wait_block = int(input(system_color("[?] Nhập số thời gian chờ khi có dấu hiệu bị chặn follow\n-> ")))
    headless = True if input(system_color("[?] Dùng headless? (y/N)\n-> ")).lower().strip() == "y" else False
    if not headless: hide_chrome = True if input(system_color("Nếu bạn không dùng headless thì dùng hide chrome chứ? (y/n)\n-> ")).lower().strip() == "y" else False
    else: hide_chrome = False
    print()
    rchk = check_instagram_account_id()
    username_id_ins_gl = {account_id[1]: account_id[0] for account_id in rchk}
    data = json.load(open(sessions_manager_file))['data']
    while True:
        try:
            __main(username_id_ins_gl, data, waitime, max_wait_block, headless, hide_chrome)
        except:
            continue
    
if __name__ == "__main__":
    GOLIKE_HEADERS['Authorization'] = open("auth.txt").read()
    GOLIKE_HEADERS['t'] = open("t.txt").read()

    while True:
        account_id = check_instagram_account_id()
        print(system_color(" ----------------------------------------------------"))
        print(system_color("| Tool Golike Instagram By PhuTech (Programing-Sama) |"))
        print(system_color("|     Công cụ được xây dựng dựa trên APPIUM          |"))
        print(system_color(" ----------------------------------------------------"))
        print(system_color("| # Các nguồn tài nguyên phụ thuộc                |"))
        print(system_color("|  $ undetected-chromedriver (python package)     |"))
        print(system_color("|  $ cloudscraper (python package)                |"))
        print(system_color("|  $ selenium (python package)                    |"))
        print(system_color(" -------------------------------------------------"))
        print(system_color("| ? Các lựa chọn theo index                       |"))
        print(system_color("| [0] Thêm golike authorization                   |"))
        print(system_color("| [1] Thêm golike t                               |"))
        print(system_color("| [2] Thêm phiên                                  |"))
        print(system_color("| [3] Chạy tool                                   |"))
        print(system_color(f"| [{len(account_id)}] <- Tổng số lượng accounts                  |"))
        print(system_color(" -------------------------------------------------"))
        print()

        inp = int(input(system_color("[?] Nhập lựa chọn của bạn\n-> ")))
        print()

        if inp == 0:
            add_golike_auth()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
        elif inp == 1:
            add_golike_t()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
        elif inp == 2:
            add_new_session()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
        elif inp == 3:
            main_program()