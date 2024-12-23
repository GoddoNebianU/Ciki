import json

with open('./words.txt', encoding='utf-8') as f:
    words = f.read().split()

cet4luan = []
cet6 = []
with open('./CET4luan_2.json', encoding='utf-8') as f:
    for line in f.readlines():
        cet4luan.append(json.loads(line))
with open('./CET6_2.json', encoding='utf-8') as f:
    for line in f.readlines():
        cet6.append(json.loads(line))

dic1 = dict()
dic2 = dict()

def replaceFran(str):
    fr_en = [['é', 'e'], ['ê', 'e'], ['è', 'e'], ['ë', 'e'], ['à', 'a'], ['â', 'a'], ['ç', 'c'], ['î', 'i'], ['ï', 'i'],
             ['ô', 'o'], ['ù', 'u'], ['û', 'u'], ['ü', 'u'], ['ÿ', 'y']
             ]
    for i in fr_en:
        str = str.replace(i[0], i[1])
    return str

for i in cet4luan:
    i['headWord'] = replaceFran(i['headWord'])
    dic1[i['headWord']] = i

for i in cet6:
    i['headWord'] = replaceFran(i['headWord'])
    dic2[i['headWord']] = i

t = list(dic1.keys())
for k in t:
    if k in dic2.keys():
        dic1.pop(k)

for k in dic2.keys():
    dic1[k] = dic2[k]

dic = dic1



ret = []
#
# dic = dict()
# for i in cet:
#     i['headWord'] = replaceFran(i['headWord'])
#     dic[i['headWord']] = i

for word in words:
    if word in dic.keys():
        ret.append(dic[word])
    else:
        print(word, end='.')
print('')

print(len(ret))

rret = []

c = 0
for word in ret:
    c += 1
    try:
        rret.append({
            'word': word['headWord'],
            'usphone': word['content']['word']['content']['usphone'],
            'ukphone': word['content']['word']['content']['ukphone'],
            'trans': word['content']['word']['content']['trans'],
            'sentences': word['content']['word']['content']['sentence']['sentences']
        })
    except Exception as e:
        print(c)

print(rret)
print(len(rret))

with open('./output.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(rret, ensure_ascii=False, indent=4))