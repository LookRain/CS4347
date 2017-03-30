def is_subseq(query, model):
    query = query.replace(" ", "").lower()
    model = model.replace(" ", "").lower()

    it = iter(model)
    return all(c in it for c in query)
dirty = ['fuck','狗日','犊子','麻批','仙人板板','你妈','操你','草你','shit','卧槽','我操','妈的','妈逼','我日','傻逼','靠','妈卖批','日死','我干','法克','屌','suck','我贼','贼你','傻吊','弱智','智障']
def check(str):
    for i in dirty:
        if (i in str):
            return True
    return False

print(check("Fuck you"))
print('大发大ASDFASD'.lower())
