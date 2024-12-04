import pygame                                                                                   # Импорт библиотпек
import random
import os

from pygame import draw

WIDTH  = 1280                                                                                   # Ширина игрового окна
HEIGHT = 960                                                                                    # Высота игрового окна
FPS    = 60                                                                                     # Частота кадров в секунду

# создаем игру и окно

COLOR               = (23, 233, 89)                                                             # Цвет квартиры
SIZE_Y              = 120                                                                       # Высота квартиры
SIZE_X              = 240                                                                       # Ширина квартиры
LOWER_Y_BORDER      = 500                                                                       # Граница, на которой стоят прошлые квартиры
X_PIVOT_OF_NEW_FLAT = 300                                                                       # Х координата, на которой появляются квартиры
Y_PIVOT_OF_NEW_FLAT = 180                                                                       # Y координата, на которой появляются квартиры
CENTER              = 520                                                                       # Координата, где здание по центру
DOWN_MOVE           = 4                                                                         # Скорость движения вниз
xMOVE               = -10                                                                       # Скорость движения по Х координате
BUILD_DOWN_MOVE     = 0.2                                                                       # Скорость движения всего дома вниз

COORDS_Y_1_FLAT     = 620                                                                       # оУ 1го этаже (того этажа, который уже в здании)
COORDS_Y_2_FLAT     = 740                                                                       # оУ 2го этаже (того этажа, который уже в здании)
COORDS_Y_3_FLAT     = 860                                                                       # оУ 3го этаже (того этажа, который уже в здании)

global x_current, y_current                                                                     # Объявляем переменные глобальными, потому что по другому ты не придумала как сделать
global img_size_x, img_size_y
global score

def CheckIvent ():                                                                              # Функция, проверяет, что нажал и нажал ли вообще пользователь
    for event in pygame.event.get():                                                            # Проходится по каждому событию, т.е. по каждой нажатой клавише, клике мыши
        if event.type == pygame.QUIT:                                                           # Если пользователь ввел QUIT, то выход
            os.abort ()
        if event.type == pygame.KEYDOWN:                                                        # Если пользователь ввел esc, то выход
            if event.key == pygame.K_ESCAPE:    
                os.abort ()
            elif event.key == pygame.K_SPACE:                                                   # Если пользователь нажал пробел, то возвращается True, True также = 1
                return True
            elif event.key == pygame.K_r:                                                       # Если пользователь нажал "R", то возвращается -1
                return -1
            elif event.key == pygame.K_1:                                                       # Если нажать 1, то поставит музыку на паузу
                pygame.mixer.music.pause()
            elif event.key == pygame.K_2:                                                       # Если нажать 2, уберет с паузы, уменьшит значение звука 
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_volume(0.5)  
            elif event.key == pygame.K_3:                                                       # Если нажать 3, уберет с паузы, увеличит значение звука
                pygame.mixer.music.unpause()    
                pygame.mixer.music.set_volume(1)
    return False                                                                                # Если ничего из этого не подошло, возвращается False = 0

def FlatCut (coord_x_flat_1):                                                                   # Функция, которая отвечает за то, что этаж падает вниз
    global x_current, img_size_x                                                                # Говорим, что эти переменные объявлены глобально

    if x_current < coord_x_flat_1:                                                              # Вообще это можно упростить, но я говнокожу, чтобы не идеально
        img_size_x = img_size_x - (coord_x_flat_1 - x_current)                                  # Отвечает за то, где упал дом. Если чуть ближе начала башни, то вот это
        return coord_x_flat_1
    elif x_current > coord_x_flat_1:                                                            # Если после начала башни, то вот это
        img_size_x = img_size_x - (x_current - coord_x_flat_1)
        return x_current
    else:
        return x_current                                                                        # Функция возвращает позицию по оХ
    
def GameOver ():                                                                                # Функция, которая вызывается в конце игры, когда проиграл
    game_is_vse = pygame.font.Font ("inc/Texts/CubicPixel.otf", 150)                            # Инициализируем шрифт. То, что inc - путь до файла, дальше - размер
    vse_surf  = game_is_vse.render (f"Game Over!", False, (255, 13, 10))                        # Теперь задаем текст, сглаживание = False, цвет

    over_score_text = pygame.font.Font ("inc/Texts/CubicPixel.otf", 100)
    text_surf  = over_score_text.render (f"Your score: {score}", False, (255, 255, 255))

    retry_text_surf = pygame.font.Font ("inc/Texts/CubicPixel.otf", 50)
    text_retry = retry_text_surf.render ("To play again press \"R\"", False, (255, 255, 255))

    screen.blit (backfront, (0, 0))                                                             # Стираем с экрана все, что было до этого

    screen.blit (vse_surf, (300, 300))                                                          # Выводим на экран Game Over
    screen.blit (text_surf, (350, 500))                                                         # Выводим на экран Score                                                         
    screen.blit (text_retry, (400, 700))                                                        # Выводим на экран To play press R

    pygame.display.flip ()                                                                      # Обновляем экран для пользователя

    while True:                                                                                 # Постоянно проверяем, нажал ли пользователь что-то
        res = CheckIvent ()

        if res == -1:
            __main__ ()                                                                         # Если нажал, вызываем main, где запускается игра
            return

def __main__ ():
    global x_current, y_current                                                                 # Объявляем, какие переменные глобальные
    global img_size_x, img_size_y
    global score, xMOVE

    score = 0                                                                                   # Счет пользователя

    score_text = pygame.font.Font ("inc/Texts/CubicPixel.otf", 75)                              # Текст, как чуть ранее
    text_surf  = score_text.render (f"Your score: {score}", False, (255, 255, 255))

    y_current   = Y_PIVOT_OF_NEW_FLAT                                                           # Переменная, в которой хранится текущее положение по оY 
    x_current   = X_PIVOT_OF_NEW_FLAT                                                           # Переменная, в которой хранится текущее положение по оХ

    img_size_x = SIZE_X                                                                         # Размер картинки с этажем по оХ
    img_size_y = SIZE_Y                                                                         # Размер картинки с этажем по оУ

    pygame.mixer.music.load("inc/Sounds/Subway.mp3")                                            # Загружает аудио
    pygame.mixer.music.play(-1)                                                                 # Закольцованно проигрывает, тк стоит -1

    flat1 = pygame.image.load ("inc/Imgs/flat.png").convert ()                                  # Достаем картинки с вариантами квартир
    flat1 = pygame.transform.scale(flat1, (img_size_x, img_size_y))                             # Устанавливаем самый начальный размер каждой

    flat2 = pygame.image.load ("inc/Imgs/flat2.jpg").convert ()                             
    flat2 = pygame.transform.scale(flat2, (img_size_x, img_size_y))  

    flat3 = pygame.image.load ("inc/Imgs/flat3.jpg").convert ()                             
    flat3 = pygame.transform.scale(flat3, (img_size_x, img_size_y))             

    flat4 = pygame.image.load ("inc/Imgs/flat4.jpg").convert ()                             
    flat4 = pygame.transform.scale(flat4, (img_size_x, img_size_y))  

    flat5 = pygame.image.load ("inc/Imgs/flat5.jpg").convert ()                             
    flat5 = pygame.transform.scale(flat5, (img_size_x, img_size_y))  

    flat = flat1                                                                                # Наша квартира - тоже меняетмя, поэтому ее скин - переменная

    key_pressed = False                                                                         # Булева переменная (принимает значения только True = 1 или False = 0), отвечает за то, нажал ли пользователь клавишу
    go_down     = False                                                                         # Отвечает за то, идет ли весь столб с квартирами вниз, тоже булева

    screen.blit (backfront, (0, 0))                                                             # Чистим экран

    coord_y_flat_1 = COORDS_Y_1_FLAT                                                            # Начальные координаты самой высокой квартиры в башне по оY
    coord_y_flat_2 = COORDS_Y_2_FLAT                                                            # Начальные координаты средней квартиры в башне по оY
    coord_y_flat_3 = COORDS_Y_3_FLAT                                                            # Начальные координаты самой нижней квартиры в башне по оY

    coord_x_flat_1 = CENTER                                                                     # Начальные координаты соответствующих квартир по оХ                                              
    coord_x_flat_2 = CENTER
    coord_x_flat_3 = CENTER

    screen_flat_1 = flat3                                                                       # Эти вещи - переменные. Они будут меняться, когда у тебя упадет твой блок
    screen_flat_2 = flat1                                                                       # А почему они имеют такие значения сейчас - просто начальное значение задал на рандом
    screen_flat_3 = flat5

    # Это функция Это то, что выводится Это координаты того, что выводится
    screen.blit (screen_flat_1, (coord_x_flat_1, coord_y_flat_1))                               # Выводим этажи на экран
    screen.blit (screen_flat_2, (coord_x_flat_2, coord_y_flat_2))
    screen.blit (screen_flat_3, (coord_x_flat_3, coord_y_flat_3))

    screen.blit (text_surf, (430, 100))                                                         # Ставим текст

    while True:                                                                                 # Входим в цикл
        if go_down:                                                                             # Метка на то, если падает твоя квартира
            if coord_y_flat_2 >= COORDS_Y_3_FLAT:                                               # Если координата 2го этажа стала координатой 3го этажа, то
                go_down       = False

                coord_x_flat_3 = coord_x_flat_2                                                 # Меняем 2 -> 3, 1 -> 2, та квартира, которая падала -> 1 этажом
                coord_x_flat_2 = coord_x_flat_1
                coord_x_flat_1 = new_x_coord_flat_1

                coord_y_flat_1 = COORDS_Y_1_FLAT                                                # Выравниваем оY координату квартир
                coord_y_flat_2 = COORDS_Y_2_FLAT
                coord_y_flat_3 = COORDS_Y_3_FLAT

                screen_flat_3 = screen_flat_2                                                   # Меняем значения переменных
                screen_flat_2 = screen_flat_1

                screen_flat_1 = pygame.transform.scale(flat, (img_size_x, img_size_y))          # Рисуем на экран наш новый первый этаж

                y_current     = Y_PIVOT_OF_NEW_FLAT                                             # Возвращаем координаты двигающегося этажа на стандартные
                x_current     = X_PIVOT_OF_NEW_FLAT

                num = random.randint (1, 5)                                                     # Рандомом выбираем число от 1 до 5, чтобы дальше выбрать новый скин этажа

                if num == 1:
                    flat = pygame.transform.scale(flat1, (img_size_x, img_size_y))              # transform - меняет размер изображения
                elif num == 2:
                    flat = pygame.transform.scale(flat2, (img_size_x, img_size_y))
                elif num == 3:
                    flat = pygame.transform.scale(flat3, (img_size_x, img_size_y))
                elif num == 4:
                    flat = pygame.transform.scale(flat4, (img_size_x, img_size_y))
                elif num == 5:
                    flat = pygame.transform.scale(flat5, (img_size_x, img_size_y))

                continue                                                                        # Следующая итерация цикла
            else:
                screen.blit (backfront, (0, 0))                                                 # Обновляем экран

                screen.blit (screen_flat_1, (coord_x_flat_1, coord_y_flat_1))                   # Рисуем этажи
                screen.blit (screen_flat_2, (coord_x_flat_2, coord_y_flat_2))
                screen.blit (screen_flat_3, (coord_x_flat_3, coord_y_flat_3))

                screen.blit (flat, (new_x_coord_flat_1, y_current))                             # Наш упавший этаж

                screen.blit (text_surf, (430, 100))                                             # Текст со счетом выводим на экран

                coord_y_flat_1 += BUILD_DOWN_MOVE                                               # Смещаем все этажи немного вниз экрана
                coord_y_flat_2 += BUILD_DOWN_MOVE
                coord_y_flat_3 += BUILD_DOWN_MOVE
                y_current      += BUILD_DOWN_MOVE

                pygame.display.flip ()                                                          # Показываем то, что получилось в эту итерацию пользователю

                continue
        elif key_pressed == True:                                                               # Если пользователь нажал пробел
            if y_current >= LOWER_Y_BORDER:                                                     # Если наш этаж уже опустился до уровня верхнего стоячего этажа, то входим в if
                key_pressed = False                                                             # Убираем метку того, что пользователь нажал клавишу

                new_x_coord_flat_1 = FlatCut (coord_x_flat_1)                                   # Обрезаем картинку

                if img_size_x <= 0:                                                             # Если размер квартиры стал 0, то пользователь проиграл
                    GameOver ()
                    return 0
                
                flat = pygame.transform.scale (flat, (img_size_x, img_size_y))                  # Иначе меняем размер на тот, что обрезали

                score = score + 1                                                               # +1 к счету
                text_surf  = score_text.render (f"Your score: {score}", False, (255, 255, 255)) # Выводим счет

                screen.blit (flat, (new_x_coord_flat_1, y_current))                             # Выводим на экран новый этаж квартиры

                go_down = True                                                                  # Говорим, что наш дом сейчас будет опускаться

                continue                                                                        # Следующая итерация
                
            y_current += DOWN_MOVE                                                              # Если квартира еще не дошла до дома, то опускаем ее ниже
        else:
            key_pressed = CheckIvent ()                                                         # Если ни одно из выше перечисленных условий не верно, то проверяем, что вводит пользователь

        if key_pressed  == False:                                                               # Если пользователь ничего нам нужного не нажал, то двигаем квартиру по оХ координает вправо влево
            x_current += xMOVE        

        if x_current >= WIDTH - img_size_x:                                                     # Если квартира дошла до края экрана, меняем направление движения
            xMOVE = -xMOVE
        elif x_current <= 0:
            xMOVE = abs (xMOVE) 

        screen.blit (backfront, (0, 0))                                                         # Чистим экран

        screen.blit (screen_flat_1, (coord_x_flat_1, coord_y_flat_1))                           # Рисуем дом заново
        screen.blit (screen_flat_2, (coord_x_flat_2, coord_y_flat_2))
        screen.blit (screen_flat_3, (coord_x_flat_3, coord_y_flat_3))

        screen.blit (flat, (x_current, y_current))                                              # Рисуем квартиру

        screen.blit (text_surf, (430, 100))                                                     # Пишем текст
        
        pygame.display.flip ()                                                                  # Выводим это все пользователю

        clock.tick (FPS)                                                                        # Контролирует число FPS (кадров в секунду, количество обновлений монитора за 1 секунду)

pygame.init()                                                                                   # Инициируем игру

pygame.mixer.init()                                                                             # Инициируем звук

screen = pygame.display.set_mode((WIDTH, HEIGHT))                                               # Создаем окно

pygame.display.set_caption("Bild your home!")                                                   # Название игры

clock = pygame.time.Clock()                                                                     # Чтобы убедиться, что игра работает с заданной частотой кадров

backfront  = pygame.image.load("inc/Imgs/backgraund.png").convert ()                            # Загружаем задний фон

screen.blit (backfront, (0, 0))                                                                 # Рисуем задний фон

__main__ ()                                                                                     # Запускаем игру