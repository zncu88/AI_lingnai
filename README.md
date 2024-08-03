# AI_lingnai
a repository about Chinese AI vtuber

本项目基于langchain-chatchat 0.3.0和qwen1.5模型进行本地部署，后利用websocket获得哔哩哔哩直播平台弹幕信息实现弹幕互动，文字转语音采用GPT-SOVITS进行语音训练和推理，目前实现了各个接口的正确对接，只能进行初步对话，苦于知识库获取麻烦，尝试了轻小说和微博、贴吧评论微调，但最终结果并不理想，获取适合聊天机器人的中文数据库耗费时间过长。

尝试利用autodl算力平台部署qwen1.5大语言模型和langchain-chatchat，与本地进行数据传输。

### 可修改部分说明：


1.知识库提问的提示词，修改知识库提问提示词在promptsettings.yaml中，提示词的选择很大程度上决定了对话的结果如何

2.GPT-SOVITS使用的模型可在gweight.txt和sweight.txt中修改为需要的模型，训练模型可打开go-webui.bat按照GPT-SOVITS进行操作，修改模型后也要修改对应的示例音频文件和音频文字，需在bililive/main文件中修改handle_input函数中发送请求的位置修改链接和文字。

3.可放入自己的知识库，可以通过start chatchat后在知识库管理里设置自己的知识库并进行添加文件和向量化，修改使用的知识库在send_message_to_chatbot函数中放松请求的database处修改名字。

### 使用方式：


#### 1.大语言模型配置部分：


配置好autodl的langchain-chatchat，手动下载好qwen1.5-chat模型和bge-large-zh-v1.5（bge-large-zh-v1.5选用cpu版本）模型，

##### 配置信息：

<img width="647" alt="f248bf3835f90b7979856b35cdbb538" src="https://github.com/user-attachments/assets/29130190-7567-4f7e-9b2e-3a6e7ba187a7">


<img width="641" alt="e10947142be4b984e5013080df4191a" src="https://github.com/user-attachments/assets/53d5fc6d-c991-4a12-8c09-d98ed20e049a">


也可通过：

```
conda activate xinference

XINFERENCE_HOME=/root/autodl-tmp/xinference XINFERENCE_MODEL_SRC=modelscope xinference-local --host 0.0.0.0 --port 9997 

```
连接本地9997端口并安装对应模型（autodl算力平台下载对应工具连接9997接口）

再在langchain开一个终端：

```
conda activate qwen1.5


chatchat kb -r #(可有可无，当没有放入或改变知识库文件时不需要进行,同时也可在8501接口的webui界面进行手动导入知识库和向量化）


chatchat start -a
```


#### 2.声音部分采用GPT-SOVITS和利用voicemeeter实现：


虚拟声卡voicenmeeter选择：
下载好voicemeeter后，
在声音设置中设置，
输出选择input，
输入选择b1口。

下载和配置好GPT-SOVITS后，将该GPT-SoVITS-beta0706文件夹中的inference_webui.py放入对应的\GPT_SoVITS文件夹中替换


其他文件直接替换


后双击运行GPT-SoVITS-beta0706中的go-api.bat文件

#### 3.虚拟形象采用vtuberstudio：

在vtuberstudio中配置好输入设备为b1口后，刷新一次

#### 4.直播弹幕获取(不使用开放平台):


以哔哩哔哩直播为例，利用obs设置好后推流直播，
开始直播后运行bililive文件夹中的main进行弹幕的实时获取。（目前存在弹幕太快的时候来不及说完这一句就说下一句，无关紧要的回复太多）

### 项目计划：


1.接入ai绘画功能和ai唱歌功能

2.进行更好的虚拟形象动作对接

3.获取适合的知识库和大模型微调

4.利用图像描述功能实现ai看视频

5.开发ai玩游戏功能




本项目使用langchain-chatchat、qwen1.5-chat、GPT-SOVITS等开源项目，只进行了初步调用尝试，只用作学习用途。
