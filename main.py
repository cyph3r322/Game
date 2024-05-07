import pygame
import random

# Инициализация Pygame
pygame.init()

# Установка размера экрана
screen_width = 1000
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка изображений
bird_image = pygame.image.load("images/icon1.png").convert_alpha()
enemy_image = pygame.image.load("images/icon3.png").convert_alpha()
food_image = pygame.image.load("images/icon2.png").convert_alpha()

# Создание спрайта птицы
bird = pygame.sprite.Sprite()
bird.image = bird_image
bird.rect = bird.image.get_rect()
bird.rect.center = (screen_width / 2, screen_height / 2)

# Создание группы для хранения всех спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(bird)

# Создание группы для хранения хищников
enemies = pygame.sprite.Group()

# Создание группы для хранения еды
food = pygame.sprite.Group()

# Установка начального счета
score = 0
font = pygame.font.SysFont("Arial", 25)

# Создание хищников
for i in range(5):
    enemy = pygame.sprite.Sprite()
    enemy.image = enemy_image
    enemy.rect = enemy.image.get_rect()
    enemy.rect.x = random.randrange(screen_width)
    enemy.rect.y = random.randrange(screen_height)
    enemy.speed_x = random.randint(-3, 3)  # Добавление случайной начальной скорости по оси X
    enemy.speed_y = random.randint(-3, 3)  # Добавление случайной начальной скорости по оси Y
    enemies.add(enemy)
    all_sprites.add(enemy)

# Создание еды
for i in range(10):
    food_item = pygame.sprite.Sprite()
    food_item.image = food_image
    food_item.rect = food_item.image.get_rect()
    food_item.rect.x = random.randrange(screen_width)
    food_item.rect.y = random.randrange(screen_height)
    food.add(food_item)
    all_sprites.add(food_item)

# Игровой цикл
running = True
while running:

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление птицей
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        bird.rect.y -= 5
    if keys[pygame.K_s]:
        bird.rect.y += 5
    if keys[pygame.K_d]:
        bird.rect.x += 5
    if keys[pygame.K_a]:
        bird.rect.x -= 5

    # Обновление спрайтов
    all_sprites.update()

    # Обновление позиций хищников
    for enemy in enemies:
        enemy.rect.x += enemy.speed_x
        enemy.rect.y += enemy.speed_y

        # Ограничение движения хищников в пределах экрана
        if enemy.rect.left < 0 or enemy.rect.right > screen_width:
            enemy.speed_x = -enemy.speed_x
        if enemy.rect.top < 0 or enemy.rect.bottom > screen_height:
            enemy.speed_y = -enemy.speed_y

    # Проверка столкновений между птицей и хищниками
    for enemy in enemies:
        if pygame.sprite.collide_rect(bird, enemy):
            print("Столкновение с хищником!")
            running = False

    # Проверка столкновений между птицей и едой
    for food_item in food:
        if pygame.sprite.collide_rect(bird, food_item):
            print("Получена еда!")
            food_item.kill()  # Удаление еды после столкновения
            score += 1

    # Ограничение движения птицы в пределах экрана
    if bird.rect.left < 0:
        bird.rect.left = 0
    if bird.rect.right > screen_width:
        bird.rect.right = screen_width
    if bird.rect.top < 0:
        bird.rect.top = 0
    if bird.rect.bottom > screen_height:
        bird.rect.bottom = screen_height

    # Отрисовка экрана
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    enemies.draw(screen)
    food.draw(screen)

    # Отрисовка счета
    score_text = font.render("Счет: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (5, 5))

    # Добавление задержки в игровой цикл
    pygame.time.Clock().tick(60)  # Ограничение скорости цикла до 60 кадров в секунду

    pygame.display.flip()

# Завершение Pygame
pygame.quit()