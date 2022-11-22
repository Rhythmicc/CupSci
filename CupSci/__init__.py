# -*- coding: utf-8 -*-

name = "CupSci"

from .__config__ import *

config: CupSciConfig = None
if enable_config:
    config = CupSciConfig()

import sys
from QuickProject import user_pip, _ask, external_exec, QproErrorString, QproWarnString
from selenium import webdriver


def requirePackage(
    pname: str,
    module: str = "",
    real_name: str = "",
    not_exit: bool = True,
    not_ask: bool = False,
    set_pip: str = user_pip,
):
    """
    获取本机上的python第三方库，如没有则询问安装

    :param not_ask: 不询问，无依赖项则报错
    :param set_pip: 设置pip路径
    :param pname: 库名
    :param module: 待引入的模块名，可缺省
    :param real_name: 用于 pip3 install 的名字
    :param not_exit: 安装后不退出
    :return: 库或模块的地址
    """
    try:
        exec(f"from {pname} import {module}" if module else f"import {pname}")
    except (ModuleNotFoundError, ImportError):
        if not_ask:
            return None
        if _ask(
            {
                "type": "confirm",
                "name": "install",
                "message": f"""{name} require {pname + (' -> ' + module if module else '')}, confirm to install?
  {name} 依赖 {pname + (' -> ' + module if module else '')}, 是否确认安装?""",
                "default": True,
            }
        ):
            with QproDefaultConsole.status(
                "Installing..." if user_lang != "zh" else "正在安装..."
            ):
                external_exec(
                    f"{set_pip} install {pname if not real_name else real_name} -U",
                    True,
                )
            if not_exit:
                exec(f"from {pname} import {module}" if module else f"import {pname}")
            else:
                QproDefaultConsole.print(
                    QproInfoString,
                    f'just run again: "{" ".join(sys.argv)}"'
                    if user_lang != "zh"
                    else f'请重新运行: "{" ".join(sys.argv)}"',
                )
                exit(0)
        else:
            exit(-1)
    finally:
        return eval(f"{module if module else pname}")


_driver = None


def getLocalDriver():
    global _driver

    if _driver is None:
        # headless
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        _driver = webdriver.Chrome(options=options)
    return _driver


def getRemoteDriver():
    global _driver

    if _driver is None:
        _driver = webdriver.Remote(
            command_executor=config.select("remote_url"),
            desired_capabilities=webdriver.DesiredCapabilities.CHROME,
        )
    return _driver


def getDriver():
    if config.select("remote_url"):
        return getRemoteDriver()
    else:
        return getLocalDriver()
    # return getLocalDriver()


def closeDriver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver.quit()
        _driver = None
