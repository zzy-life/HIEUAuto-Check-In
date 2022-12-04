# 涉外易班自动打卡

> 看不到本文档图片请用电脑打开，或[点击](http://www.zhangzhiyu.live:8900/vuepress/guide/python/%E6%B6%89%E5%A4%96%E6%98%93%E7%8F%AD%E8%87%AA%E5%8A%A8%E6%89%93%E5%8D%A1.html)


## 使用selenium

> 此方法使用代码控制浏览器进行打卡，属于模拟操作，比较简单可控

###  :fire: win10系统

#### 依赖

1. 谷歌浏览器

   如果没有可[点击](https://pan.baidu.com/s/1kDepNH15qa64MLwYhNVT3g?pwd=fmg4)

   下载 ChromeStandaloneSetup64 

2. python3环境

   如果没有可[点击](https://pan.baidu.com/s/1kDepNH15qa64MLwYhNVT3g?pwd=fmg4)

   下载 python-3.10.5-amd64 (1)

3. stealth.min.js 

   可点击[下载](https://pan.baidu.com/s/11JoDOsnTrv_0-LB-8ARH2w?pwd=3php)

4. python3环境安装后，需要pip下载selenium，chromedriver_autoinstaller

   ```shell
   pip install chromedriver_autoinstaller
   ```

   ```shell
   pip install selenium
   ```



#### python脚本

> 需要将stealth.min.js 和python脚本放在同一目录
>
> 脚本运行后，第一次比较慢，会下载驱动在当前目录，并生成一个文件夹，不要删除

自行修改代码中学号和身份证后六位

请下载使用yuban.py

#### 定时任务

win系统由于不是24小时运行，所以定时任务有很多局限性，如有需要可[点击](https://blog.csdn.net/junzixing1985/article/details/125613022)自行设置

###  :fire: 服务器部署

> 使用阿里云服务器IP地址要在长沙，否则会出现异地定位
>
> 可以使用阿里云自动打卡之后，可以当天自己手动修改定位，以避免班委早晨催促

#### amd64架构

##### CentOS 安装chrome

```shell
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
yum install -y google-chrome-stable_current_x86_64.rpm  # 默认安装在/opt/google/chrome/ 
# yum autoremove -y google-chrome  卸载
```

安装完成之后会显示版本，或者使用下面的命令查看版本

```bash
/opt/google/chrome/chrome -version
```



##### Ubuntu安装chrome

```shell
apt update
apt install libxss1 libappindicator1 libindicator7  # 安装软件依赖
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb  # 下载最新版chrome
dpkg -i google-chrome-stable_current_amd64.deb
# 如果提示缺少某些依赖无法安装，可以试一下 apt install -f
google-chrome --version  # 查看当前chrome版本
```



##### python依赖项

```shell
pip install selenium 
```

```shell
pip install chromedriver_autoinstaller
```

stealth.min.js

下载地址

链接: https://pan.baidu.com/s/11JoDOsnTrv_0-LB-8ARH2w?pwd=3php 

提取码: 3php 

##### python自动打卡脚本

自行修改代码中

1. **学号和身份证后六位**
2. **日志及stealth.js路径**

请下载使用yuban.py


##### shell脚本

自行更改路径

```shell
#!/bin/bash
python3 /db/yiban/yiban.py
```

##### 定时任务

请自行搜索

宝塔可使用计划任务

![1662265765805](./1662265765805.png)

#### arm64架构（树莓派)

##### 安装Chromium

> Chromium是谷歌Chrome的开源版本，不同与Chrome，Chromium的很多代码由开源社区提供。
>
> Google并没有发布[arm](https://so.csdn.net/so/search?q=arm&spm=1001.2101.3001.7020)版本的桌面版本Chrome；所以，如果要在树莓派的arm64版本Debian安装浏览器，建议安装Chromium

 ***教程适用于Debian系统，不限于基于Debian的系统（如：Ubuntu）。*** 

 [Debian](https://so.csdn.net/so/search?q=Debian&spm=1001.2101.3001.7020)预编译版本Chromium下载：http://ports.ubuntu.com/pool/universe/c/chromium-browser 

 ![Debian预编译版本Chromium](./425bcdcbdaae49b9bdead178dae6edcc.png) 

选择下载文件
我们需要下载什么呢？一般是：

- chromium-codecs-ffmpeg-extra_******arm64.deb：chromium依赖的ffmpeg文件。_
- chromium-browser*****arm64.deb：chromium主体文件。
- chromium-chromedriver******_arm64.deb：chromedrive驱动，如无需代码驱动chromium，可以不安装。



比如，下载95.0版本的chromium： 

 ![下载这些内容](./8984722c132e48c29348d422bf934ca3.png) 

###### 下载

复制下载地址(请自行复制高版本下载链接替换下方)，我们到树莓派上，使用`wget`下载 ：

```shell
# 下载chromium-browser
wget 'http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-browser_95.0.4638.69-0ubuntu0.18.04.1_arm64.deb'
# 下载chromium-codecs-ffmpeg-extra
wget 'http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-codecs-ffmpeg-extra_95.0.4638.69-0ubuntu0.18.04.1_arm64.deb'
# 下载chromium-chromedriver
wget 'http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-chromedriver_95.0.4638.69-0ubuntu0.18.04.1_arm64.deb'
```

![下载到树莓派上](./fd9cd3c1816a47fbaebcb812a8b004ec.png) 

###### 包管理器安装

现在，我们使用Debain的包管理器（dpkg 即package manager for Debian）进行安装，安装顺序是：
chromium-codecs-ffmpeg-extra–>chromium-browser->chromium-chromedriver。

所以，我们使用dkg进行安装为：

```shell
# chromium-codecs-ffmpeg-extra
sudo dpkg -i chromium-codecs-ffmpeg-extra_95.0.4638.69-0ubuntu0.18.04.1_arm64.deb
# chromium-browser
sudo dpkg -i chromium-browser_95.0.4638.69-0ubuntu0.18.04.1_arm64.deb
# chromium-chromedriver
sudo dpkg -i chromium-chromedriver_95.0.4638.69-0ubuntu0.18.04.1_arm64.deb
```

 ![dpkg安装](./63569b1dfb054c72b9271f2dfc0d7fe7.png) 

 为了保险起见，我们再运行一次`apt`包管理器的更新： 

```shell
sudo apt update
sudo apt upgrade
```

 ![apt更新](./2d33b9ff35a54ed298177a98fadff40c.png) 

 到此，我们的Chromium和chromedriver就安装好了。

>  安装过程中可能会遇到依赖关系问题，因为你的树莓派上可能安装了更新的一些lib包。可以尝试运行`apt-get -f install`或`aptitude install`解决

 测试一下 

```shell
# 查看chromedriver版本
chromedriver -v
# 查看chromium版本
chromium-browser -version
```

> 如无法查看版本，请按报错信息下载依赖

##### python依赖项

```shell
pip install selenium 
```

stealth.min.js

下载地址

链接: https://pan.baidu.com/s/11JoDOsnTrv_0-LB-8ARH2w?pwd=3php 

提取码: 3php 

##### python自动打卡脚本

自行修改代码中

1. **学号和身份证后六位**
2. **日志及stealth.js路径**

请下载使用yuban.py

##### shell脚本

自行更改路径

```shell
#!/bin/bash
python3 /db/yiban/yiban.py
```

##### 定时任务

请自行搜索

宝塔可使用计划任务

![1662265765805](./1662265765805.png)
