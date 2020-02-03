import urllib.request
import re
import time
import vk_api
from PIL import Image

UPDATE_TIME = 43200

MESSAGE = "Existential comics"

OWNER_ID = "-184539490"

FILENAME = "save_file.txt"

# ДАННЫЕ ДЛЯ АВТОРИЗАЦИИ

NUMBER = "+77087564462"
PASSWORD = "adlo1975Z"

# КЛЮЧ (НУЖНЫ РАЗРЕШЕНИЯ СТЕНА И ФОТОГРАФИИ В НАСТРОЙКАХ ГРУППЫ, ЛЮБОЙ СОЙДЕТ)

KEY = "d39539f27ca4665023499ea794185ea836b213c3eb0fed27105a7293f5dbd9d3fbfc281877cc3bb92f80e"

# СПЕЦИАЛЬНАЯ ШТУКА ОТ СТАНДАЛОН ПРИЛОЖЕНИЯ, ЛУЧШЕ НЕ ТРОГАТЬ

ID = 7060805
SCOPE = 401477




def login():
    session = vk_api.VkApi(NUMBER, PASSWORD, KEY, app_id=ID, scope=SCOPE)
    session.auth(reauth=True, token_only=True)
    vk = session.get_api()
    print("lulwdone")
    return vk


def post(vk, pics):
    # загрузчик
    print(pics)
    loader = vk_api.VkUpload(vk)


    # загрузка изображений во временное хранилище на стороне сервера

    x = (loader.photo_wall(photos=pics[0]))
    # формирование поста
    attach = []

    for each in x:
        attach.append("photo{}_{}".format(each["owner_id"], each["id"]))

    # отправка поста

    post_id = vk.wall.post(owner_id=OWNER_ID, message=pics[1]+"\n"+MESSAGE, from_group=True, attachments=attach)
    print("posted")

def phy():

    vk = login()

    s = open(FILENAME, "r+")
    save = s.read()

    r = r".+\n"
    everything = re.findall(r, save)

    cop = []
    for each in everything:
        cop.append(each[:-1])


    numer = r"\[\d+,"
    x = re.findall(numer, cop[-1])
    x = str(int(x[0][1:-1])+1)

    f = urllib.request.urlopen("http://existentialcomics.com/comic/"+x)
    file = str(f.read())

    r = r"<img class=\"comicImg\".+<div id=\"bottom"
    presort = re.findall(r, file)
    r = r"src=\S+\""
    prepics = re.findall(r, presort[0])
    pics = []
    for each in prepics:
        pics.append(each[7:-1])



    titler = r"<h3>.+</h3>"

    title = re.findall(titler, file)[0][4:-5]
    print(title)



    downl = []



    for each in pics:
        wer = True
        while wer:
            try:

                res = urllib.request.urlopen("http://"+each, None, 100)

                wer = False
                print(each)
                written = open("{}".format(each[36:]), "wb+")

                written.write(res.read())
                written.close()
                downl.append("{}".format(each[36:]))
            except:
                pass

    post(vk, (downl, title))

    stringa = "["+str(x)+", "+title+", ["
    for each in downl:
        stringa = stringa+"\""+str(each)+"\", "
    stringa = stringa[0:-2] + "]]\n"

    s.write(stringa)

    s.close()







def main():

    while True:
        try:
            phy()
        except:
            try:
                phy()
            except:
                pass

        time.sleep(UPDATE_TIME)


if __name__ == "__main__":
    main()