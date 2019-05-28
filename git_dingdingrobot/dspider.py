import requests
from bs4 import BeautifulSoup
from dingtalkchatbot.chatbot import DingtalkChatbot

def Senddingmsg(a):
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=d510ce6f991f850a0d94c5a9787599661a957c34056727c86e0d15db8803cf76'
    dd = DingtalkChatbot(webhook)
    dd.send_markdown(title='有楼盘开始登记', text='### 正在登记\n'+a+'\n\n'
                     '> ![img](http://124.115.228.93/zfrgdjpt/resources/images/topimg00.jpg)\n'
                     '> #### 详情查看[房管局意向登记平台](http://124.115.228.93/zfrgdjpt/xmgs.aspx?state=1)\n')

def spider():
    url = 'http://124.115.228.93/zfrgdjpt/xmgs.aspx?state=1'

    res = requests.get(url).text
    bshtml = BeautifulSoup(res, features="lxml")
    # key = bshtml.body.form.find_all('div')[5].find_all('div')[11].find_all('span','isInlineblock textOverflow vm')
    key = bshtml.find_all(attrs={"class", "isInlineblock textOverflow vm"})
    profile = open('profile.txt', 'wt', encoding='utf-8')  # 存储爬取新开盘楼的结果
    prolist = []
    for pro_name in key:
        prodata = pro_name.get('title') #
        prolist.append(prodata)
        profile.write(pro_name.get('title'))
        profile.write('\n')
        all_project_name = "\n\n".join(str(x) for x in prolist) #将prolist拼接成字符串；为正在登记的所有楼盘

    with open('new.txt', 'wt', encoding='utf-8') as f1:
            f1.write(all_project_name)
    with open('new.txt', 'r', encoding='utf-8') as f1:
            lineone = f1.readline() #为正在登记的排序最靠前的第一个楼盘

    return all_project_name, lineone


def old():
    with open('old.txt', 'r', encoding='utf-8') as linesfile:
        lines = linesfile.read()
    with open('old.txt', 'r', encoding='utf-8') as lineone_file:
        lineone = lineone_file.readline()
    return lines, lineone


def main():
    all_oldline, one_oldline = old()
    all_newline, one_newline = spider()
#    print(all_oldline)
#    print('-----------line-------------')
#    print(all_newline)
#    print('***********line*************')
    if one_newline == one_oldline:
        print('No Update')
    else:
        with open('old.txt', 'wt', encoding='utf-8') as linesfile:
            print(all_newline)
            linesfile.write(all_newline)
            Senddingmsg(all_newline)

if __name__ == '__main__':
    main()
