import json
import random
import urllib.parse
import threading
from enum import Enum
from playsound3 import playsound

SILENT_MODE = False
MULTITHREADED = True

with open('output.json', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    item['deleted'] = False

class SpeakType(Enum):
    ENGLISH_WORD = 0
    CHINESE = 1

def sprint(*args, **kwargs):
    if 'end' not in kwargs.keys():
        kwargs['end'] = ''
    print(*args, **kwargs)

def tchandler(fun, args):
    try:
        fun(*args)
    except:
        pass

def speak(text: str, t: SpeakType):
    if t == SpeakType.ENGLISH_WORD:
        url = f'https://dict.youdao.com/dictvoice?audio={text}&type=2'
    elif t == SpeakType.CHINESE:
        url = f'https://fanyi.baidu.com/gettts?lan=zh&text={urllib.parse.quote(text)}&spd=5'
    else:
        raise Exception
    if MULTITHREADED:
        threading.Thread(target=tchandler, args=(playsound, (url,))).start()
    else:
        playsound(url)


def speak_word(text):
    tchandler(speak, (text, SpeakType.ENGLISH_WORD))

def speak_zh(text):
    tchandler(speak, (text, SpeakType.CHINESE))

def translation(silent_mode=False, multithreaded=True):
    global SILENT_MODE
    SILENT_MODE = silent_mode
    global MULTITHREADED
    MULTITHREADED = multithreaded

    class Flag(Enum):
        EXIT = 0
        BLANK = 1
        NEXT = 2
        READ = 3
        READED = 4
        PAUSE = 5

    rollback_words = []
    last_word = None
    while True:
        sprint('\n\n------------------------------------------------------------------------------------\n\n')


        word = random.choice(data)
        while word['deleted']: word = random.choice(data)
        for i, v in enumerate(rollback_words):
            if v[0] <= 0:
                word = v[1]
                del rollback_words[i]
                break
        sprint(word['word'])
        if not SILENT_MODE: speak_word(word['word'])
        else: sprint(word['usphone'])

        ins = ''
        flag = Flag.READ
        while True:
            match flag:
                case Flag.BLANK:
                    continue
                case Flag.NEXT:
                    for i, v in enumerate(rollback_words):
                        rollback_words[i][0] -= 1
                    break
                case Flag.READ:
                    sprint('    ')
                    ins = input()
                    flag = Flag.READED
                case Flag.READED:
                    if ins == 'rb' and last_word is not None:
                        # 单词重现
                        rollback_words.append([5, last_word])
                        sprint(f'单词{last_word['word']}将在5回合后重现。')
                        flag = Flag.READ
                    elif ins in ['q', 'quit']:
                        # 退出程序
                        exit()
                    elif not ins:
                        # 输出中文翻译
                        sprint(word['trans'][0]['tranCn'])
                        last_word = word
                        flag = Flag.NEXT
                    elif ins in ['r', 'rm']:
                        ins = input(f'确定删除{word['word']}吗？')
                        if ins in ['y', 'Y', 'yes', 'YES', 'Yes']:
                            word['deleted'] = True
                            sprint('删除了')
                        else:
                            sprint('好')
                        flag = Flag.NEXT
                    elif ins in ['\'', '\\', ']', '/']:
                        # 输出单词详情，朗读中文翻译
                        sprint(json.dumps(word['trans'], indent=4, ensure_ascii=False))
                        sprint(word['sentences'][0]['sContent'])
                        if not SILENT_MODE: speak_zh(word['trans'][0]['tranCn'])
                        flag = Flag.PAUSE
                    else:
                        flag = Flag.READ
                case Flag.PAUSE:
                    input()
                    flag = Flag.NEXT


if __name__ == '__main__':
    translation()
