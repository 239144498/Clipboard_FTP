# Clipboard_FTP

## 这是通过 FTP 服务实现的跨平台远程剪贴板功能

---

_创建起初是为了有效利用学校分配的 FTP 空间，虽然只给了 50MB，但是作为剪贴板共享也足够了_

**它能够获取剪贴板文字或图片上传到 FTP，并且另一台设备能够自动将内容复制到剪贴板，以此实现远程共享**

实现剪贴板共享已支持平台：

- [x] todo Windows
- [x] todo Linux
- [x] todo Android
- [x] todo Ios
- [ ] todo Mac OS

后续会把 Mac OS 也加入进来

---

## 注意：

你需要做的是在服务器开启 FTP，并且开放该 FTP 用户上传和下载权限

如果你是学生并且学校分配了 FTP，就可以使用学校提供的 FTP 以此程序来实现剪贴板共享功能

值得一提的是 IOS 设备使用的是 PythonIsta，你需要 pip install clipboard 模块
而安卓使用的是QPython软件，需要用到 androidhelper 模块
