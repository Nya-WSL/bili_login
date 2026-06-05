from nicegui import ui
from version import version
from multiprocessing import freeze_support

import traceback
import api
import log
import os
import re

logger = log.logger

# 删除旧的二维码图片
for file in os.listdir(os.getcwd()):
    if re.match(r"bili_qrcode_\d+\.png", file):
        try:
            os.remove(file)
        except:
            pass

# 检查是否存在cookie.txt
def check_cookie():
    if os.path.exists("cookie.txt"):
        with open("cookie.txt", "r", encoding="utf-8") as f:
            cookies = f.read()

        if cookies:
            return True

    return False

@ui.page("/")
def index():
    def check_auth(loginInfo):
        status = api.login(loginInfo[0])

        if status == True:
            ui.notify("登录成功", type="positive")

            try:
                os.remove(loginInfo[1])
            except:
                pass

            stepper.next()
        else:
            ui.notify(status, type="negative")

    def bili_login():
        global qrcode_ui

        auth_button.set_visibility(False)
        loginInfo = api.get_qrcode("bili_qrcode")

        with auth_step:
            qrcode_ui = ui.image(loginInfo[1])
            ui.label("请使用B站APP扫描二维码登录")
            ui.label("扫码后点击下一步")

            with ui.stepper_navigation():
                ui.button("下一步", on_click=lambda: check_auth(loginInfo))
                ui.button("重新获取", on_click=lambda: (qrcode_ui.set_source(api.get_qrcode("bili_qrcode")[1]), ui.notify("已刷新二维码")))

    def get_info():
        info_button.set_visibility(False)

        if os.path.exists("cookie.txt"):
            with open("cookie.txt", "r", encoding="utf-8") as f:
                cookies = f.read()
            cookies_dict = dict(item.split("=", 1) for item in cookies.split(";"))

            uname = api.get_uname(cookies_dict["DedeUserID"])
            ui.label(f"昵称：{uname}").on("click", lambda: ui.clipboard.write(uname) or ui.notify("已复制昵称到剪贴板", type="positive"))

            for k, v in cookies_dict.items():
                ui.markdown(f"**{k}**：`{v}`").style("word-break: break-all;").on("click", lambda k=k, v=v: ui.clipboard.write(v) or ui.notify(f"已复制{k}的值到剪贴板", type="positive"))

            ui.markdown(f"**完整Cookie**：`{cookies}`").style("word-break: break-all;").on("click", lambda: ui.clipboard.write(cookies) or ui.notify(f"已复制完整Cookie到剪贴板", type="positive"))

            with ui.stepper_navigation():
                ui.button("重新登录", on_click=lambda: ui.navigate.to("/"))
        else:
            ui.label("未找到cookie信息，请先登录")
            with ui.stepper_navigation():
                ui.button("登录", on_click=lambda: ui.navigate.to("/"))

    with ui.stepper().props("vertical").classes("absolute-center") as stepper:
        with ui.step("登录B站") as auth_step:
            with ui.row():
                auth_button = ui.button("扫码登录", on_click=lambda: bili_login())
                skip_button = ui.button("重新解析", on_click=lambda: stepper.next())
                if not check_cookie():
                    skip_button.set_enabled(False)

        with ui.step("Cookie信息") as info_step:
            info_button = ui.button("获取Cookie信息", on_click=lambda: get_info())

if __name__ == '__main__':
    freeze_support()
    try:
        ui.run(
            title=f"B站Cookie获取 v{version} | Nya-WSL",
            port=65110,
            reload=False,
            window_size=(800, 1000),
            use_colors=False
        )
    except:
        logger.error(traceback.format_exc())
