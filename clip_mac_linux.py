#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Clipboard_FTP 
@File    ：clip_mac_linux.py
@IDE     ：PyCharm 
@Author  ：Naihe
@Date    ：2021/11/14 21:47 
"""
import base64
import io

import gtk

CLIP_NONE = 0
CLIP_TEXT = 1
CLIP_IMAGE = 2


class ClipboardGTK():
    """基于GTK的剪贴板类
    需要安装pygtk，支持剪贴板纯文本，图像的操作
    """

    def __init__(self):
        self.clipboard = gtk.Clipboard()

    def get_content(self):
        """ 获取剪贴板内容，返回 CLIP_TYPTE, content """
        text = self.get_text()
        if text is not None:
            return CLIP_TEXT, text

        image = self.get_image()
        if image is not None:
            return CLIP_IMAGE, image

        return CLIP_NONE, None

    def set_content(self, mimetype, content):
        if mimetype == CLIP_TEXT:
            self.set_text(content)
        elif mimetype == CLIP_IMAGE:
            self.set_image(content)

    def get_text(self):
        try:
            content = self.clipboard.wait_for_text() if self.clipboard.wait_is_text_available() else None
        except Exception as e:
            raise Exception("get text err: %s", e)

        return content

    def get_image(self):
        content = None
        try:
            if self.clipboard.wait_is_image_available():
                pixbuf = self.clipboard.wait_for_image()
                # Mac 下测试获取截图为空
                if pixbuf is None:
                    pixbuf = self.clipboard.wait_for_contents("image/tiff").get_pixbuf()

                content = self._pixbuf2b64(pixbuf)
        except Exception as e:
            raise Exception("get image err: %s", e)

        return content

    def set_text(self, text):
        self.clipboard.set_text(text)
        self.clipboard.store()

    def set_image(self, b64_pixbuf):
        pixbuf = self._b642pixbuf(b64_pixbuf)
        self.clipboard.set_image(pixbuf)
        self.clipboard.store()

    def _pixbuf2b64(self, pixbuf):
        """ gtk.gdk.Pixbuf对象转化为base64编码字符串 """
        fh = io.BytesIO()
        pixbuf.save_to_callback(fh.write, 'png')
        return base64.b64encode(fh.getvalue())

    def _b642pixbuf(self, b64):
        """ base64编码字符串转换为gtk.gdk.Pixbuf """
        pixloader = gtk.gdk.PixbufLoader('png')
        pixloader.write(base64.b64decode(b64))
        pixloader.close()
        return pixloader.get_pixbuf()
