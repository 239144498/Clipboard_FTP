#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：Clipboard.py
@IDE     ：PyCharm
@Author  ：Naihe
@Date    ：2021/10/27 11:21
"""
import io
import os
import sys

from ftplib import FTP
from pathlib import Path
from os import environ

IP = "服务器ip"  # 例如：10.0.11.3
PORT = 21
USER = "账号"
PWD = "密码"

if 'win' in sys.platform:
    import win32con
    import win32clipboard


    def copy(data):
        """复制"""
        win32clipboard.OpenClipboard()  # 打开剪贴板
        win32clipboard.EmptyClipboard()  # 清空剪贴板内容。可以忽略这步操作，但是最好加上清除粘贴板这一步
        if type(data) == str:
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)  # 以Unicode文本形式放入剪切板
        elif type(data) == bytes:
            win32clipboard.SetClipboardData(win32con.CF_DIB, data)
        else:
            raise Exception("复制到剪贴板出错")
        win32clipboard.CloseClipboard()  # 关闭剪贴板


    def paste():
        """粘贴"""
        win32clipboard.OpenClipboard()  # 打开剪贴板
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):  # 图片
            data = win32clipboard.GetClipboardData(win32con.CF_DIB)
        elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):  # 文本
            data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT).encode('utf-8')  # 读取剪切板内容，读取为Unicode文本形式
        else:
            data = None
        win32clipboard.CloseClipboard()  # 关闭剪贴板
        return data
elif 'ios' in sys.platform:
    import clipboard


    def copy(text):
        """复制"""
        if clipboard.get_image():
            clipboard.set_image(text)
        else:
            clipboard.set(text)


    def paste():
        """粘贴"""
        if clipboard.get_image():
            return clipboard.get_image()
        else:
            return clipboard.get().encode('utf-8')
elif 'ANDROID_STORAGE' in environ:
    pass
elif 'linux' == sys.platform:
    import pyperclip


    def copy(data):
        pyperclip.copy(data)


    def paste():
        return pyperclip.paste()


class FtpClient(object):
    def __init__(self, host, port, username, passwd):
        self.ftp = self.__connect(host, port, username, passwd)
        try:
            self.ftp.cwd('share')
        except:
            self.ftp.mkd('share')
            self.ftp.cwd('share')
        self.bufsize = 1024

    def __connect(self, host, port, username, passwd):
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(username, passwd)
        return ftp

    def downloadfile(self, remotepath: str):
        if 'Clipboard' in str(self.files_name()):
            chunk_io = io.BytesIO()
            self.ftp.retrbinary('RETR ' + remotepath, chunk_io.write, self.bufsize)
            self.ftp.delete(remotepath)  # 下载后删除文件
            try:
                return chunk_io.getvalue().decode('utf-8')
            except:
                return chunk_io.getvalue()

    def uploadfile(self, remotepath: str, data: bytes):
        chunk_io = io.BytesIO(data)
        self.ftp.storbinary('STOR ' + remotepath, chunk_io, self.bufsize)

    def files_name(self):
        return self.ftp.nlst()

    def close(self, base: Path):
        self.ftp.close()

    def _clean(self, base: Path):
        """
        清空base目录中的文件
        """
        for h, dirs, files in os.walk(base):
            h = Path(h)
            for f in files:
                (h / f).unlink()


def main():
    base = Path()  # 项目根目录的tmp目录
    ftp = FtpClient(IP, PORT, USER, PWD)
    if len(sys.argv) > 1:
        data = sys.argv[1][:1].lower()
        if data == 'p':  # 上传
            ftp.uploadfile('Clipboard', paste())
        elif data == 'g':  # 下载
            copy(ftp.downloadfile('Clipboard'))
        else:
            print("""
    参数      例子           功能
    G/g     project.py g    FTP复制到剪贴板
    P/p     project.py p    粘贴剪贴板到FTP
            """)
    else:
        copy(ftp.downloadfile('Clipboard'))
    ftp.close(base)


if __name__ == '__main__':
    #  功能    命令执行：
    # 上传：Clipboard.py p
    # 下载：Clipboard.py g
    main()
