import io
import os
import time
from peewee import *
import cv2
import serial
import telebot
from keyboa import Keyboa

import photoredaktor

bot = telebot.TeleBot('5180282626:AAEDq-6h8OxZkX55tbPkMvgMPMX91AMAajc')
ser = serial.Serial('COM11', baudrate=9600, timeout=1)
ser.flush()
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
sio.flush()
udid = 5120633740
conn = SqliteDatabase('project.db')
cursor = conn.cursor()


class BaseModel(Model):
    class Meta:
        database = conn


class date(BaseModel):
    artist_id = AutoField(column_name='Date')
    name = TextField(column_name='photo_name', null=True)

    class Meta:
        table_name = 'photodata'


@bot.message_handler(content_types=['text'])
def message(message):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 800)  # set Width
    cap.set(4, 480)  # set Height
    pasttime = 0
    facephoto = 0
    buttonswithids = [
        {"вывести данные": "1"}]
    global kb
    kb = Keyboa(items=buttonswithids).keyboard
    door = [
        {"Да": "3"}, {"Нет": "4"}]
    doorkb = Keyboa(items=door).keyboard
    bot.send_message(chat_id=message.chat.id, reply_markup=kb, text="Что вам нужно")
    while True:
        thistime = time.time()
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            if int(thistime) - pasttime > 10:
                pasttime = thistime
                return_value, img = cap.read()
                times = time.asctime().split(' ')
                times2 = times[3]
                times.pop(3)
                times = times2.split(':') + times
                times = '_'.join(times)
                global path
                path = r'C:\\work\\faceid\\python_photos\\'
                global fpath
                fpath = f'{str(times)}.jpg'
                cv2.imwrite(os.path.join(path, fpath), img)
                facephoto = 1
        if facephoto == 1:
            bot.send_photo(chat_id=udid, photo=open(path + fpath, 'rb'))
            bot.send_message(chat_id=udid, reply_markup=doorkb, text="Открыть дверь?")
            date.create(
                artist_id=f'{time.gmtime(1575721830).tm_year}-{time.gmtime(1575721830).tm_mon}-{time.gmtime(1575721830).tm_mday}',
                name=f'{path + fpath}')
            facephoto = 0
        cv2.imshow('video', img)


@bot.message_handler(content_types=['photo', 'document'])
def handler_file(message):
    from pathlib import Path
    Path(f'files/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        global src
        src = r'C:\\work\\faceid\\obrabotka\\' + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            style = [
                {"сепия": "5"}, {"Чёрно-белый": "6"}, {"резкость": "7"}, {"контур": "8"}, {"негатив": "9"}]
            stylekb = Keyboa(items=style).keyboard
            bot.send_message(chat_id=message.chat.id, reply_markup=stylekb, text="Выберите стиль")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src1 = r'C:\\work\\faceid\\obrabotka\\' + message.document.file_name
        with open(src1, 'wb') as new_file:
            new_file.write(downloaded_file)
            bot.send_message(chat_id=udid, text="Резервная копия сделана на ваш пк")


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == '1':
        senddata(1)
    elif call.data == '2':
        senddata(2)
    elif call.data == '3':
        senddata(3)
    elif call.data == '4':
        senddata(4)
    elif call.data == '5':
        print(src)
        a = photoredaktor.photo_import(src, 5)
        sendphoto(a)
    elif call.data == '6':
        a = photoredaktor.photo_import(src, 2)
        sendphoto(a)
    elif call.data == '7':
        a = photoredaktor.photo_import(src, 3)
        sendphoto(a)
    elif call.data == '8':
        a = photoredaktor.photo_import(src, 4)
        sendphoto(a)
    elif call.data == '9':
        a = photoredaktor.photo_import(src, 1)
        sendphoto(a)

def sendphoto(filename):
    bot.send_photo(chat_id=udid, photo=open(filename, 'rb'))
    bot.send_message(chat_id=udid, text='Фото обработано')


def senddata(number):
    if number == 1:
        ser.write(b'1')
        line = ser.readline().decode('ASCII').split('-')
        bot.send_message(chat_id=udid, text=f'''
    Температура = {line[0]}
    Влажность   = {line[1]}
    ''')
    elif number == 2:
        raise SystemExit
    elif number == 3:
        ser.write(b'2')
        bot.send_message(udid, text='Дверь открыта')
        bot.send_message(chat_id=udid, reply_markup=kb, text="Что вам нужно")
    elif number == 4:
        bot.send_message(udid, text='Полиция вызвана,дверь Заблокирована')
        bot.send_message(chat_id=udid, reply_markup=kb, text="Что вам нужно")


bot.polling(none_stop=True, interval=0)
