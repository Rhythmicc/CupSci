# CupSci

通过 CUP webvpn 下载文献。需要配置 selenium，支持使用远程的 selenium 服务，或者本机配置 Chromium。(仅支持在校园网环境中下载)

## 安装

```shell
pip3 install git+https://github.com/Rhythmicc/CupSci.git -U
```

## 使用

### 初次运行会引导配置

```shell
cup-sci --help
```

1. remote_url 表示远程的 selenium 服务 URL，没有可以不填
   - 格式 1：`http://<用户名>:<密码>@<ip或域名>:<端口>/wd/hub`
   - 格式 2: `http://<ip或域名>:<端口>/wd/hub`
2. work_path 表示论文下载的文件夹，本工具会按照`会议 > 年份 > 文章` 自动组织下载。（记得填写绝对路径）

### 通过论文链接下载论文

```shell
cup-sci dl
```

论文链接比如：`https://doi.org/10.1145/3470496.3527432`
暂时只支持 ACM 和 IEEE 两个网站（因为我暂时还用不到别的）
