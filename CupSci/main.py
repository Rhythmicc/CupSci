from QuickProject.Commander import Commander
from . import *


app = Commander("cup-sci")
rt_url = "https://webvpn.cup.edu.cn"


@app.command()
def dl():
    """
    下载论文
    """
    import re
    import time
    from . import _ask as ask
    from selenium.webdriver.common.by import By

    url = ask({"type": "input", "message": "请输入论文链接: "})

    status = QproDefaultConsole.status("打开浏览器")
    status.start()
    driver = getDriver()
    status.update("正在获取真实链接")
    driver.get(url)
    url = driver.current_url

    status.update("判断页面类型")

    try:
        is_acm_paper = (
            driver.find_element(By.TAG_NAME, "a").get_attribute("title")
            == "ACM Digital Library home"
        )
    except:
        is_acm_paper = False

    if is_acm_paper:
        status.update("正在解析ACM论文信息")
        doi = "/".join(url.split("/")[-2:])
        title = driver.find_element(By.CLASS_NAME, "citation__title").text.replace(
            ": ", "："
        )
        meeting = driver.find_element(
            By.CLASS_NAME, "epub-section__title"
        ).text.split()[0]
        year = (
            driver.find_element(By.CLASS_NAME, "CitationCoverDate")
            .text.strip()
            .split()[-1]
        )
    else:
        status.update("正在解析IEEE论文信息")
        arnumber = url.split("/")[-1]
        title = driver.find_element(
            By.XPATH,
            '//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span',
        ).text
        _info = (
            driver.find_element(By.CLASS_NAME, "stats-document-abstract-publishedIn")
            .find_element(By.TAG_NAME, "a")
            .text.strip()
        )
        meeting = _info.split()[-1][1:-1]
        year = _info.split()[0]

    status.update("正在查询论文哈希值")
    driver.get(rt_url)
    js = f'return encrypUrl("https", "{url}")'

    time.sleep(3)

    url_hash = re.findall("https/(.*?)/", driver.execute_script(js))[0]

    part_url = (
        f"https/{url_hash}/doi/pdf/{doi}"
        if is_acm_paper
        else f"https/{url_hash}/stamp/stamp.jsp?tp=&arnumber={arnumber}"
    )
    QproDefaultConsole.print(QproInfoString, part_url)

    status.update("关闭浏览器")
    closeDriver()
    status.update("下载论文")

    work_path = config.select("work_path")
    meeting_dir = os.path.join(work_path, meeting)
    if not os.path.exists(meeting_dir):
        os.mkdir(meeting_dir)
    year_dir = os.path.join(meeting_dir, year)
    if not os.path.exists(year_dir):
        os.mkdir(year_dir)

    path = os.path.join(year_dir, f"{title}.pdf")
    if os.path.exists(path):
        status.stop()
        QproDefaultConsole.print(QproInfoString, "文件已存在")
        return

    requirePackage("QuickStart_Rhy.NetTools.NormalDL", "normal_dl", "QuickStart_Rhy")(
        f"{rt_url}/{part_url}",
        path,
        disableStatus=True,
    )
    status.stop()
    QproDefaultConsole.print(QproInfoString, f'下载完成: "{path}"')


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
