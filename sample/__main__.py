#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __main__.py
Description: main script for Python sample.
"""
from wxasync import WxAsyncApp
from view import MyFrame, base
import asyncio


if __name__ == "__main__":

    async def main():            
        app = WxAsyncApp()
        frame = MyFrame(None, base.WEIGHTS_PATH)
        frame.Show()
        await app.MainLoop()

asyncio.run(main())

