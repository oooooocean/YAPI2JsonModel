# Y-API 2 Json Model
`1.0.0` `自动构建.swift` `支持嵌套类型` `支持批量操作`

## 说明
- 开发环境: `Python 3.9.6` `macOS Ventura`
### 安装依赖
```shell
pip3 install -r requirements.txt
```

### 脚本配置
使用前需要在`config.py`中配置 UID, TOKEN等, 如果有疑惑, 请联系我

### 脚本使用

以`/project/xxx/interface/api/5496`接口为例:
```shell
$ python3 main.py -h           
🚀START
usage: main.py [-h] [-i] [-a] [--file] ids [ids ...]

Y-API 2 JSON BEAN🚀🚀🚀

positional arguments:
  ids            需要转换的Y-api的接口id, 可多传

optional arguments:
  -h, --help     show this help message and exit
  -i, --ios      生成iOS平台 Swift Decodable Model
  -a, --android  生成Android平台 Kotlin Json Bean
  --file         将结果保存到文件中


$ python3 main.py 5496 --file
```

## 功能
- [x] 支持 Swift
- [x] 支持输入结果到文件中
- [x] 支持嵌套类型
- [ ] 优化异常捕获
- [ ] 支持多线程
- [ ] 配置信息本地缓存, 支持自动登录, 不需要手动配置
- [ ] 支持 Kotlin
- [ ] 支持 Js
- [ ] 多线程转协程

## 联系我
WX: chenqiangsf