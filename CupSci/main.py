from QuickProject.Commander import Commander
from . import *


app = Commander(executable_name, seg_flag=True)
rt_url = "https://webvpn.cup.edu.cn"


def getUrl():
    try:
        default = requirePackage("pyperclip", "paste")()
        if not default.startswith("http://") and not default.startswith("https://"):
            default = ""
    except:
        default = ""
    from . import _ask as ask

    return ask(
        {
            "type": "input",
            "message": "请输入论文链接 / DOI",
            "default": default,
        }
    )


@app.command()
def dl(
    url: str = "", folder: str = "", auto_login: bool = False, auto_open: bool = False
):
    """
    下载论文

    :param url: 论文链接
    :param folder: 保存目录
    :param auto_login: 自动登录
    :param auto_open: 自动打开
    """
    import re
    import time
    from selenium.webdriver.common.by import By

    if not url:
        url = getUrl()
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://www.doi.org/" + url

    QproDefaultStatus("打开浏览器").start()
    driver = getDriver()
    QproDefaultStatus.update("正在获取真实链接")
    driver.get(url)
    url = driver.current_url

    QproDefaultStatus.update("判断页面类型")

    try:
        is_acm_paper = (
            driver.find_element(By.TAG_NAME, "a").get_attribute("title")
            == "ACM Digital Library home"
        )
    except:
        is_acm_paper = False

    if is_acm_paper:
        QproDefaultStatus.update("正在解析ACM论文信息")
        doi = "/".join(url.split("/")[-2:])
        title = driver.find_element(By.CLASS_NAME, "citation__title").text.replace(
            ": ", "："
        )
        meeting = driver.find_element(By.CLASS_NAME, "epub-section__title").text
        year = (
            driver.find_element(By.CLASS_NAME, "CitationCoverDate")
            .text.strip()
            .split()[-1]
        )
    else:
        QproDefaultStatus.update("正在解析IEEE论文信息")
        arnumber = url.split("/")[-1]
        try:
            title = driver.find_element(
                By.XPATH,
                '//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span',
            ).text
        except:
            title = driver.find_element(
                By.XPATH,
                '//*[@id="LayoutWrapper"]/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span',
            ).text
        _info = (
            driver.find_element(By.CLASS_NAME, "stats-document-abstract-publishedIn")
            .find_element(By.TAG_NAME, "a")
            .text.strip()
        )
        meeting = _info.split()[-1][1:-1]
        year = _info.split()[0]

    QproDefaultStatus.update("正在查询论文哈希值")
    driver.get(rt_url)
    if auto_login:
        QproDefaultStatus.update("正在自动登录")
        driver.switch_to.frame("loginIframe")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        inputs[0].send_keys(config.select("username"))
        inputs[1].send_keys(config.select("password"))

        driver.find_element(By.CLASS_NAME, "login_btn").click()
        driver.switch_to.default_content()

    js = f'return encrypUrl("https", "{url}")'
    time.sleep(3)  # 等待JS加载完成
    url_hash = re.findall("https/(.*?)/", driver.execute_script(js))[0]

    part_url = (
        f"https/{url_hash}/doi/pdf/{doi}"
        if is_acm_paper
        else f"https/{url_hash}/stampPDF/getPDF.jsp?tp=&arnumber={arnumber}&ref="
    )

    QproDefaultStatus.update("下载论文")

    if not folder:
        work_path = config.select("work_path")
        meeting_dir = os.path.join(work_path, meeting)
        if not os.path.exists(meeting_dir):
            os.mkdir(meeting_dir)
        year_dir = os.path.join(meeting_dir, year)
        if not os.path.exists(year_dir):
            os.mkdir(year_dir)
    else:
        year_dir = folder.replace("~", user_root)

    path = os.path.join(year_dir, f"{title.replace('/', '-')}.pdf")

    # PDF文件链接：f"{rt_url}/{part_url}"，保存路径：path
    # 通过 selenium 打开浏览器下载 PDF 文件

    driver.get(f"{rt_url}/{part_url}")

    QproDefaultStatus.update("等待下载完成")
    import re
    from . import _ask

    time.sleep(3)
    guess_filepath = re.sub("[^a-zA-Z-]", "_", title).replace("__", "_")
    while (file_name := _ask(
        {
            "type": "list",
            "message": "请选择文件名",
            "choices": [i for i in os.listdir(os.path.join(user_root, "Downloads")) if i.endswith(".pdf")] + ['-1'],
            "default": f"{guess_filepath}.pdf" if os.path.exists(os.path.join(user_root, "Downloads", f"{guess_filepath}.pdf")) else None,
        }
    )) == "-1":
        time.sleep(3)
        continue
    QproDefaultStatus.update("关闭浏览器")
    closeDriver()
    local_path = os.path.join(user_root, "Downloads", file_name)
    if not os.path.exists(local_path):
        raise FileNotFoundError("文件不存在")
    requirePackage("shutil", "move")(local_path, path)

    QproDefaultConsole.print(QproInfoString, f'文件已保存到: "{path}"')
    if auto_open:
        QproDefaultStatus.update("正在打开文件")

    QproDefaultStatus.stop()


@app.command()
def update():
    """
    更新工具
    """
    with QproDefaultConsole.status("正在更新"):
        external_exec(
            f"{user_pip} install git+https://github.com/Rhythmicc/CupSci.git -U", True
        )
    QproDefaultConsole.print(QproInfoString, "更新完成")


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
