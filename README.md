# CupSci

通过 CUP webvpn 下载文献。需要配置 selenium，支持使用远程的 selenium 服务，或者本机配置 Chromium。(仅支持在校园网环境中下载)

## 安装

```shell
pip3 install git+https://github.com/Rhythmicc/CupSci.git -U
```

## 使用

### 初次运行会引导配置

请在开始前，将 Chrome 浏览器中的 “PDF 文档” 选项设置为 “下载 PDF 文件”

![](https://cos.rhythmlian.cn/ImgBed/b3630cfb4aee0e8aefc088e0cef81dd8.png)

```shell
cup-sci
```

work_path 表示论文下载的文件夹，本工具会按照`会议/期刊 > 年份 > 文章` 自动组织下载。（记得填写绝对路径）

### 通过论文链接下载论文

```shell
cup-sci dl
```

论文链接比如：`https://doi.org/10.1145/3470496.3527432`
暂时只支持 ACM 和 IEEE 两个网站（因为我暂时还用不到别的），会议可以识别准
