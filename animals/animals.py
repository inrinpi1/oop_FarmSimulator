import random
from animals.animals import Animal


class Animal:
    def __init__(self, name, age, offspring_range, product_type=None, reproduction_prob=0):
        self.name = name
        self.health = 100
        self.hunger = 0
        self.age = age
        self.offspring_range = offspring_range  # возможное количество потомства
        self.product_type = product_type  # тип производимой продукции
        self.reproduction_prob = reproduction_prob  # вероятность размножения
        self.is_alive = True
        self.has_offspring = False  # есть ли потомтво

    @classmethod
    def subclasses(cls):
        return cls.__subclasses__()

    def feed(self, inventory):
        # метод кормления животного
        if self.is_alive:
            if self.hunger > 0:
                # проверяем, есть ли корм в инвентаре
                if 'корм' in inventory.resources['корма']:
                    inventory.remove_resource('корма', 'корм', 1)
                    self.hunger -= 100
                    if self.hunger < 0:
                        self.hunger = 0  # минимальное значение 0
                    print(f'Животное {self.name} накормлено. Голод уменьшился до {self.hunger}')
                else:
                    print(f'Недостаточно корма для кормления {self.name}')
            else:
                print(f'Животное {self.name} не голодно')

    def produce(self, inventory, efficiency_bonus=0):
        # метод для получения продукции от животного
        if self.is_alive and self.product_type:
            if self.product_type not in inventory.resources['продукция']:
                inventory.resources['продукция'][self.product_type] = 0
            print(f'{self.name} производит {self.product_type}')
            return self.product_type
        else:
            print(f'{self.name} не может производить продукцию')
            return None

    def reproduce(self):
        # метод размножения
        if self.is_alive and self.health > 50 and random.random() <= self.reproduction_prob:
            return True
        return False

    def heal(self):
        # метод лечения животного
        if self.is_alive:
            self.health = 100  # уровень здоровья полностью восстанавливается
            print(f'Животное {self.name} вылечено! Уровень здоровья: {self.health}')
        else:
            print(f'К сожалению, животному уже не помочь. Животное {self.name} умерло')

    def die(self):
        self.is_alive = False
        print(f'Животное {self.name} скончалось')

    def update_state(self):
        # обновление состояния животного (голод и здоровье)
        if not self.is_alive:
            return
        self.hunger = min(100, self.hunger + 10)  # чтобы не поднималось выше 100
        if self.hunger == 100:
            self.health = max(0, self.health - 10)  # если голод на максимуме, уменьшаем здоровье, но не ментше 0
            print(f'Животное {self.name} голодает. Уровень здоровья: {self.health}')
        if self.health == 0:
            self.die()
            return

class Mammal(Animal):
    def __init__(self, name, offspring_range, product_type=None, reproduction_prob=0):
        super().__init__(name, age=0, offspring_range=offspring_range, product_type=product_type,
                         reproduction_prob=reproduction_prob)

    def reproduce(self):
        # метод размножения для млекопитающих
        if self.is_alive and self.health > 50 and random.random() <= self.reproduction_prob:
            # рандомно определяем количество потомства в пределах offspring_range
            num_offspring = random.randint(*self.offspring_range)
            offspring = []
            self.has_offspring = True
            for i in range(num_offspring):
                baby_name = f"{self.name}_offspring_{i+1}"
                print(f'Детёныш {self.name} {baby_name} появился на свет!')
                # создаем детеныша
                baby = BabyAnimal(baby_name, self)
                offspring.append(baby)
            return offspring

        return []

class Bird(Animal):
    def __init__(self, name, offspring_range, product_type=None, reproduction_prob=0, egg_prob=0):
        super().__init__(name, age=0, offspring_range=offspring_range, product_type=product_type,
                         reproduction_prob=reproduction_prob)
        self.egg_prob = egg_prob  # вероятность несения яиц

    def produce(self, inventory, efficiency_bonus=0):
        # метод производства продукции для птиц (яиц)
        if self.is_alive and self.product_type:
            if self.product_type not in inventory.resources['продукция']:
                inventory.resources['продукция'][self.product_type] = 0
            if random.random() < self.egg_prob:  

                if random.random() > self.reproduction_prob:  # проверка  вылупится ли птенец
                    base_eggs = random.randint(*self.offspring_range)
                    egg_bonus = 1 + efficiency_bonus / 100  # бонус к количеству яиц
                    total_eggs = int(base_eggs * egg_bonus)  # чтобы было целое число

                    inventory.add_resource('продукция', self.product_type, total_eggs)  # добавляем яйца в инвентарь
                    print(f'{self.name} несет {total_eggs} яиц')

            return self.product_type
        else:
            print(f'{self.name} не может производить продукцию')
            return None

    def reproduce(self):
        # метод размножения для птиц
        if super().reproduce():
            num_offspring = random.randint(*self.offspring_range)
            print(f'Появилось {num_offspring} птенцов!')
            offspring = [BabyAnimal(f'Птенец_{i + 1}', self) for i in range(num_offspring)]
            return offspring

class Cow(Mammal):
    def __init__(self):
        super().__init__(name='Корова', offspring_range=(1, 1), product_type='молоко', reproduction_prob=0.23)

    def produce(self, inventory, efficiency_bonus=0):
        # метод для производства молока
        if self.is_alive:
            if not self.has_offspring:
                print(f'{self.name} не производит молоко, потому что у неё нет потомства')
                return None
            if self.product_type not in inventory.resources['продукция']:
                inventory.resources['продукция'][self.product_type] = 0
            base_production = 20  # базовое количество молока
            production_bonus = 1 + efficiency_bonus / 100  # бонус к количеству молока (зависит от уровня коровника)
            total_production = base_production * production_bonus  # итоговое количество молока

            inventory.add_resource('продукция', self.product_type, total_production)

            print(f'{self.name} производит {total_production} л молока')
            return self.product_type
        else:
            print(f'{self.name} не может производить продукцию')
            return None

class Sheep(Mammal):
    def __init__(self):
        super().__init__(name='Овца', offspring_range=(2, 3), product_type='шерсть', reproduction_prob=0.27)

    def produce(self, inventory, efficiency_bonus=0):
        # метод для производства шерсти
        if self.is_alive:
            if self.product_type not in inventory.resources['продукция']:
                inventory.resources['продукция'][self.product_type] = 0
            base_production = 1  # базовое количество шерсти
            production_bonus = 1 + efficiency_bonus / 100  # бонус к производству
            total_production = base_production * production_bonus  # итоговое количество шерсти

            inventory.add_resource('продукция', self.product_type, total_production)

            print(f'{self.name} производит {total_production} кг шерсти.')
            return self.product_type
        else:
            print(f'{self.name} не может производить продукцию.')
            return None

class Goat(Mammal):
    def __init__(self):
        super().__init__(name='Коза', offspring_range=(1, 2), product_type='молоко', reproduction_prob=0.25)

    def produce(self, inventory, efficiency_bonus=0):
        # метод для производства молока
        if self.is_alive:
            if not self.has_offspring:
                print(f'{self.name} не производит молоко, потому что у неё нет потомства.')
                return None
            if self.product_type not in inventory.resources['продукция']:
                inventory.resources['продукция'][self.product_type] = 0
            base_production = 4  # базовое количество молока
            production_bonus = 1 + efficiency_bonus / 100  # бонус к количеству молока
            total_production = base_production * production_bonus  # итоговое количество молока

            inventory.add_resource('продукция', self.product_type, total_production)

            print(f'{self.name} производит {total_production} литров молока.')
            return self.product_type
        else:
            print(f'{self.name} не может производить продукцию.')
            return None

class Chicken(Bird):
    def __init__(self):
        super().__init__(name='Курица', offspring_range=(7, 12), product_type='яйца', reproduction_prob=0.1, egg_prob=0.6)

class Duck(Bird):
    def __init__(self):
        super().__init__(name='Утка', offspring_range=(8, 16), product_type='яйца', reproduction_prob=0.13, egg_prob=0.5)

class Goose(Bird):
    def __init__(self):
        super().__init__(name='Гусь', offspring_range=(7, 14), product_type='яйца', reproduction_prob=0.12, egg_prob=0.5)

# class BabyName:
#     def __set__(self, instance, value):
#         if not isinstance(value, str) or not value.isalpha():
#             print('Вы ввели что-то не то')
#             raise AttributeError('Имя должно содержать только буквы')
#         instance._name = value

#     def __get__(self, instance, owner):
#         return instance._name

class BabyAnimal(Animal):
    # name = BabyName()  # дескриптор для проверки имени

    def __init__(self, name, parent):
        super().__init__(name=name, age=0, offspring_range=(0, 0))
        self.parent = parent

    def grow(self):
        # метод роста детеныша
        if self.is_alive:
            self.age += 1  # возраст в месяцах
            print(f'{self.name} теперь в возрасте {self.age} месяцев')
            if self.age >= 12:
                self.get_parent_characteristics()  # в год ребенок становится взрослым животным и может производить продукцию

    def get_parent_characteristics(self):
        # метод наследования характеристик от родителя
        self.product_type = self.parent.product_type
        self.reproduction_prob = self.parent.reproduction_prob
        print(f'{self.name} теперь может производить продукцию {self.product_type}')