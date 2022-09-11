# morning_reminder
天行数据api + 微信公众测试平台 + github action

天行数据的[节假日接口](https://www.tianapi.com/apiview/139)，提供假期距离几天的信息

天行数据的四个内容接口：[土味情话](https://www.tianapi.com/apiview/80)，[彩虹屁](https://www.tianapi.com/apiview/181)，[文案](https://www.tianapi.com/apiview/194)，[ONE 一个 每日一句](https://www.tianapi.com/apiview/129)

西工大疫情填报

通过个人申请的[微信公众测试平台](https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index)接口发送公众号消息

通过 github action 每日自动运行

需要设置secret：

config：
{
"app_id": "",
"app_secret": "",
"template_id_1": "",
"template_id_2": "",
"key": "",
"account": [["", ""]]
}

user:
[""]
接收公众号消息的微信号，如果有多个，需要在[]里用英文逗号间隔，例如["wx1", "wx2"]
