PiRadio
=========
##介绍

PiRadio是一个在树莓派上可以搭建的一个小型FM电台项目。本项目是在[PiFMRds](https://github.com/ChristopheJacquet/PiFmRds)
基础上做了一下扩展，主要是封装了对网络mp3的处理，以API的方式直接展现操作，方便进一步集成微信公众平台和其他小应用做准备。

##安装和运行

1. 首先安装[PiFMRds](https://github.com/ChristopheJacquet/PiFmRds)
2. 为了方便使用做了一个软连接 `sudo ln -s /opt/PiFmRds/srcpi_fm_rds  /usr/sbin/fm`
3. 在GPIO4上插上一个杜邦线,20厘米即可
4. 下载本项目并执行如下脚本 
   <pre><code>
   # install the flask framwork
   	cd PiRadio
	virtualenv flask
	flask/bin/pip install flask
   chmod a+x *.sh
   chmod a+x *.py
   </code></pr>
5. 运行start.sh
6. 打开浏览器访问`http://{host}:1234/search?name=hello`


##后期计划

1. 做一个页面展示播放列表，可以选择自由播放的曲目
