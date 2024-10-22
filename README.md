# README

Smart-Wardrobe —— an AIoT project

Fore more details: https://github.com/Cheese-Bar/Smart-Wardrobe

Main Structure：

![图片aiot](https://s2.loli.net/2022/07/28/dEpg8VtI1r4TRHy.png)

<img src="https://s2.loli.net/2022/07/28/SQwtpgRknioAqB3.png" style="zoom:80%;" />

## 硬件

- [x] 室外部分 
  - [x] 温湿度传感器
  - [x] 气压传感器
- [x] 室内部分
  - [x] 温湿度传感器
  - [x] 小风扇
    - [x] 继电器控制
- [x] 树莓派摄像机
  - [x] 调通可用
  - [x] 按键控制
  - [x] 远程入库，自动更新
- [x] 传感器设备通信：
  - [x] 室外(sensor + microbit) -->
  - [x] 室内(sensor + microbit + 树莓派) --> 
  - [x] PC --> 
  - [x] Database -->
  - [x] 后端Sever -->

## 模型
- [x] 服装识别
    - [x] 初期模型
    - [x] 训练数据
      - [x] 调整训练图片 （只保留四种需要识别的款式）
    - [x] 模型调优
    - [x] 模型部署
- [x] 温度预测模型
    - [x] 数据处理
        - [x] 数据收集
    - [x] 模型调优
    - [x] 模型部署
- [x] 温度 -> 款式 模型 
    - [x] 数据处理（问卷）
    - [x] 初期模型
    - [x] 模型调优
    - [x] 模型部署

## 前端
- [x] 网页设计

  - [x] 整体架构
  - [x] 添加温度页面
    - [x] 当前室外状态（温度 湿度 压强）
    - [x] 添加折线图显示温度 （24h+1h)
  - [ ] ~~修改登录界面~~
  - [x] 修改衣柜界面
    - [x] 显示衣柜状态 （温度 湿度 小风扇情况）

- [x] 通信

  - [x] 数据库
  
  

## 后端
- [x] 数据库建立
  - [x] 室内温度
  - [x] 室外温度
  - [x] 服装图像 以及 分类信息？
  - [ ] ~~用户信息~~ 
- [x] 数据库通信
- [x] 服务
  - [x] 显示当前室内外温湿度
  - [x] 历史数据及预测 
  - [x] 图片上传 图床及数据库
  - [x] 获取整个衣橱
  - [x] 推荐服饰（需要整合模型）

## 接口
- [x] Swagger api 文档

