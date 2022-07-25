# README

Smart-Wardrobe —— an AIoT project

test taspberrypi



## 硬件

- [x] 室外部分 
  - [x] 温湿度传感器
  - [x] 气压传感器
- [x] 室内部分
  - [x] 温湿度传感器
  - [x] 小风扇
    - [x] 继电器控制
- [ ] 树莓派摄像机
  - [x] 调通可用
  - [ ] 远程控制
- [x] 传感器设备通信：
  - [x] 室外(sensor + microbit) -->
  - [x] 室内(sensor + microbit + 树莓派) --> 
  - [x] PC --> 
  - [x] Database -->
  - [x] 后端Sever -->

## 模型
- [ ] 服装识别
    - [x] 初期模型
    - [ ] 训练数据
      - [ ] 调整训练图片 （只保留五种需要识别的款式）
    - [ ] 模型调优
    - [ ] 模型部署
- [ ] 温度预测模型
    - [ ] 数据处理
        - [ ] 数据收集
    - [x] 模型调优
    - [ ] 模型部署
- [ ] 温度 -> 款式 模型 
    - [x] 数据处理（问卷）
    - [ ] 初期模型
    - [ ] 模型调优
    - [ ] 模型部署

## 前端
- [ ] 网页设计

  - [x] 整体架构
  - [ ] 添加温度页面
    - [ ] 当前室外状态（温度 湿度 压强）
    - [ ] 添加折线图显示 （24h+1h)
  - [ ] 修改登录界面
  - [ ] 修改衣柜界面
    - [ ] 显示衣柜状态 （温度 湿度 小风扇情况）

- [ ] 通信

  - [ ] 数据库
  
  

## 后端
- [ ] 数据库建立
  - [x] 室内温度
  - [x] 室外温度
  - [ ] 服装图像 以及 分类信息？
  - [ ] 用户信息 ？
- [x] 数据库通信
- [ ] 服务
  - [x] 显示当前室内外温湿度
  - [ ] 