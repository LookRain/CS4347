from wxpy import *
import datetime

bot = Bot()
tuling = Tuling(api_key='00f11f42280f43f0a88057016f8f0074')

# family_group = bot.groups().search('家')[0]
# family_group2 = bot.groups().search('和谐家园')[0]
# @bot.register([family_group, family_group2])
# def ignore(msg):
#     # 啥也不做
#     return
# dirty = ['fuck','狗日','犊子','麻批','仙人板板','你妈','操你','草你','shit','卧槽','我操','妈的','妈逼','我日','傻逼','靠','妈卖批','日死','我干','法克','屌','suck','我贼','贼你','傻吊','弱智','智障','肏','fk','艹','wtf','尼玛','pussy','dick']
# def check(str):
#     if (str == '干' or str == '靠' or str == '草' or str == '操' or str == '日'):
#         return True
#     for i in dirty:
#         if (i in str):
#             return True
#     return False

def is_subseq(query, model):
    query = query.replace(" ", "").lower()
    model = model.replace(" ", "").lower()
    print(query)
    it = iter(model)
    return all(c in it for c in query)


# @bot.register()
# def dirty_word_detect(msg):
#     text = msg.text.lower()
#     if check(text):
#         print(text)
#         return "讲脏话不好哦。 --- Sent from wxpy"

@bot.register()
def reply_my_friend(msg):
    if (msg.type == TEXT):
        print('text message')
        if (msg.member != None):
            print('grp msg ' + msg.text)
            if (msg.is_at == True):
                print('being @')
                tuling.do_reply(msg,at_member=True)
        else :
            print('friend msg')
            tuling.do_reply(msg, at_member=True)
# @bot.register(msg_types = TEXT, except_self=False)
# def confirm_receive(msg):
#     text = msg.text
#     confirmation = 'Message Received from ' + msg.sender.name + ': ' + text
#     print(confirmation)
#     if (is_subseq('time and date', text)):
#         print(datetime.datetime.now())
#         return datetime.datetime.now()
    # return confirmation
# 堵塞线程，并进入 Python 命令行
embed()