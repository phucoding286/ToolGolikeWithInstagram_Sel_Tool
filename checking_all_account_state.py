from modules import *

sessions_manager_file = "sessions.json"
data = json.load(open(sessions_manager_file))['data']

for ss_name, ss_path in data.items():
    driver = driver_init(ss_path, False, False)
    driver.set_window_position(500, 0)
    print(purple_color(f"[A] Account -> {ss_name}"))
    driver.get("https://www.instagram.com/")
    input(system_color("[>] Nhấn enter để tiếp tục\n-> "))
    driver.quit()

input(success_color("[>] Bạn đã lặp qua hết tất cả các session rồi, enter để đóng\n-> "))
exit()