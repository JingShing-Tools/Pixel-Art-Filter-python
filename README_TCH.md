
# Pixel-Art-transform-in-python
[English](https://github.com/JingShing/Pixel-Art-transform-in-python) | 繁體中文

一個像素風格的藝術濾鏡工具，使用python製作。可以幫助你將圖片轉換成像素風格。

你可以在這取得應用程式 : https://jingshing.itch.io/pixel-art-filter
# Update更新

## Ver 1.0

* 發布程式
* 功能
  * 顏色數
  * 向素尺寸
  * 光滑化
  * 外框輪廓線
  * 向素抖動(人工筆觸)

## Ver 1.1

* 新增中文提示
* 增加壓縮圖片功能
* 功能
  * 新增飽和度
  * 新增對比度
  * 新增明亮度

## Ver 1.2

* 新增更多選項調節

## Ver 1.2.1

* 新增作者名

## Ver 1.3

* 新增頁面系統
* 新增模式選擇
* 新增自定義模式 -> 可以隨意更改數值

## Ver1.4

* 增進抖動向素效果，減少噪點

## Ver1.5

* 新增gif模塊
* 如果導入圖片為gif，則自動切換gif模式。會在轉換完成後自動保存檔案
* 現已支持gif

## Ver1.6

* Working on Video module -> can edit mp4 and avi with experiment module.
  * flv file save has some bug.
  * This module will eat most of your cpu. So i will wrapped it as another tool.
* Found bug can't save as chinese character name file.
* [video module](https://github.com/JingShing/Opencv-Video-edit-module)

## Ver1.6.1

* GIF

  * Fixed gif duration error.

  * now can support ".gif "  and " .GIF "

* Video

  * Try to add video module in pixel art filter.
  * It's an experimental area. Use it wisely and trust your computer.
  * Now can transform video but there are some rules and thing you should know:
    * If it start it won't stop and cannot pause so you need to use it wisely.
    * It will take more time and ate almost your cpu when you use setting that are complex.
    * If it done video cover will display on window. And it will automatically save at the folder you put the exe.
    * Edited video will lost sound and become ultimately large. So be careful.
  * I add cmd for process hint. It will be there until I removed video edit part.

## Usage
You can click pic to watch vid.
[![Usage](https://img.youtube.com/vi/HpTbwjZv2y0/maxresdefault.jpg)](https://youtu.be/HpTbwjZv2y0)

## Video supported now
[![Video](https://i0.hdslb.com/bfs/archive/7220c2155a7e8550a7766eafead297b43cf93426.jpg@640w_400h_1c_!web-space-index-myvideo.webp)](https://youtu.be/W8HxlqgLQnQ)

## GIF supported now
* ![gif1 gif1](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/gif1.gif)
* ![gif2 gif2](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/gif2.gif)

## Mode Switch
* ![custom_mode custom_mode](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/custom_mode.png)
* ![simple_mode simple_mode](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/simple_mode.png)

## New UI
![UI2 UI2](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/UI2.png)

## UI
![UI UI](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/UI.png)

## Original image
![OR OR](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/or.jpg)

## Effect 16bit
![1 1](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/1.png)
## Effect 4bit
![2 2](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/2.png)
## Effect 2bit
![3 3](https://github.com/JingShing/Pixel-Art-transform-in-python/blob/main/sample/3.png)
