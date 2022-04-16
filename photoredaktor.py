from PIL import Image, ImageFilter, ImageDraw

a = ''
def photo_import(filename, type):
    if type == 1:
        a = negativ(filename)
        return a
    elif type == 2:
        a =chb(filename)
        return a
    elif type == 3:
        a = rezkost(filename)
        return a
    elif type == 4:
        a = contour(filename)
        return a
    elif type == 5:
        a = sepia(filename)
        return a


def rezkost(filename):
    image = Image.open(filename)
    blurred_jelly = image.filter(ImageFilter.SHARPEN)
    a = r"C:\\work\\faceid\\obrabotka\\" + "119" + ".jpg"
    blurred_jelly.save(r"C:\\work\\faceid\\obrabotka\\" + "119" + ".jpg")
    return a


def negativ(filename):
    image = Image.open(filename)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            draw.point((i, j), (255 - a, 255 - b, 255 - c))
    a = r"C:\\work\\faceid\\obrabotka\\" + "120" + ".jpg"
    image.save(r"C:\\work\\faceid\\obrabotka\\" + "120" + ".jpg")
    del draw
    return a


def sepia(filename):
    image = Image.open(filename)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей
    depth = 20
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            a = S + depth * 2
            b = S + depth
            c = S
            if (a > 255):
                a = 255
            if (b > 255):
                b = 255
            if (c > 255):
                c = 255
            draw.point((i, j), (a, b, c))

    a = r"C:\\work\\faceid\\obrabotka\\" + "121" + ".jpg"
    image.save(r"C:\\work\\faceid\\obrabotka\\" + "121" + ".jpg")
    del draw
    return a

def chb(filename):
    image = Image.open(filename)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))

    a = r"C:\\work\\faceid\\obrabotka\\" + "122" + ".jpg"
    image.save(r"C:\\work\\faceid\\obrabotka\\" + "122" + ".jpg")
    del draw
    return a


def contour(filename):
    original = Image.open(filename)
    original = original.filter(ImageFilter.CONTOUR)

    a = r"C:\\work\\faceid\\obrabotka\\" + "123" + ".jpg"
    original.save(r"C:\\work\\faceid\\obrabotka\\" + "123" + ".jpg")
    return a


