import io
import os
import time
from peewee import *
import cv2
import serial
import telebot
from keyboa import Keyboa

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


@bot.message_handler(content_types=['text', 'document', 'photo'])
def message(message):
    print(message.chat.id)
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
                path = r'C:\work\faceid\python_photos'
                global fpath
                fpath = f'{str(times)}.jpg'
                cv2.imwrite(os.path.join(path, fpath), img)
                facephoto = 1
        if facephoto == 1:
            bot.send_photo(chat_id=udid, photo=open(path + fpath, 'rb'))
            bot.send_message(chat_id=udid, reply_markup=doorkb, text="Открыть дверь?")
            print(path + fpath)
            date.create(
                artist_id=f'{time.gmtime(1575721830).tm_year}-{time.gmtime(1575721830).tm_mon}-{time.gmtime(1575721830).tm_mday}',
                name=f'{path + fpath}')
            facephoto = 0
        cv2.imshow('video', img)
        if message.text == 'обработка':
            try:
                photo_id = message.photo[-1].file_id
                bot.send_message(message.chat.id, 'получил фото')
            except:
                bot.send_message(message.chat.id, 'получил что угодно, но определенно не фото')


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
