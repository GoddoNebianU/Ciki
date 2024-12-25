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

class SpeakType(Enum):
    ENGLISH_WORD = 0
    CHINESE = 1

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

    while True:
        print('\n----------------------------------------------------------------------\n')

        word = random.choice(data)
        print(word['word'], end='\t\t\t')
        if not SILENT_MODE: speak_word(word['word'])
        else: print('\n'+word['usphone'], end='')

        ins = input()
        if ins in ['q', 'quit']:
            break
        if not ins:
            print(word['trans'][0]['tranCn'])
            continue

        print(json.dumps(word['trans'], indent=4, ensure_ascii=False))
        print(word['sentences'][0]['sContent'], end='')
        if not SILENT_MODE: speak_zh(word['trans'][0]['tranCn'])
        input()

if __name__ == '__main__':
    translation()