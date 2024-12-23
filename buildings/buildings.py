from buildings.buildings import Building

class Building:
    def __init__(self, name, efficiency_bonus=0, upgrade_cost=0, capacity=0):
        self.name = name
        self.efficiency_bonus = efficiency_bonus  # бонусы за улучшение построек
        self.upgrade_cost = upgrade_cost  # стоимсть улучшения постройки
        self.capacity = capacity  # вместимость
        self.current_occupancy = 0  # сколько животных сейчас живет в постройке
        self.level = 1  # изначальный уровень

    def upgrade(self, inventory):
        # метод улучшения постройки
        if self.level == 5:  # считаем что максимальный уровень 5
            print(f'{self.name} уже на максимальном уровне')
            return
        if inventory.money >= self.upgrade_cost:  # достаточно ли денег для улучшения
            inventory.spend_money(self.upgrade_cost)
            self.level += 1
            self.capacity += 10
            self.upgrade_cost *= 2  # каждое улучшение дороже предыдущего
            self.efficiency_bonus += 10
            print(
                f'{self.name} улучшено! Новый уровень: {self.level}, вместимость: {self.capacity}, бонус эффективности: {self.efficiency_bonus}%')
        else:
            print(f'Недостаточно денег для улучшения {self.name}. Нужно {self.upgrade_cost}')

    def add_animal(self, animal):
        # метод добавления животного в постройку
        if self.current_occupancy < self.capacity:
            self.current_occupancy += 1
            print(f'Животное {animal.name} добавлено в {self.name}. Текущее количество животных: {self.current_occupancy}')
            return True
        else:
            print(f'{self.name} переполнено, нельзя добавить больше животных.')
            return False

class ChickenCoop(Building):
    def __init__(self):
        super().__init__(name='Курятник', efficiency_bonus=0, upgrade_cost=3000, capacity=40)

    def add_animal(self, animal):
        # метод добавления птицы в курятник
        if not isinstance(animal, (Bird, BabyAnimal)):
            print(f'{self.name} может содержать только птиц! Невозможно добавить {animal.name}')  # ограничение на виды животных в одном домике
            return False
        return super().add_animal(animal)

class CowShed(Building):
    def __init__(self):
        super().__init__(name='Коровник', efficiency_bonus=0, upgrade_cost=5000, capacity=5)

    def add_animal(self, animal):
        # метод добавления коровы в коровник
        if not isinstance(animal, (Cow, BabyAnimal)):
            print(f'{self.name} может содержать только коров! Невозможно добавить {animal.name}')
            return False
        return super().add_animal(animal)

class Sheepfold(Building):
    def __init__(self):
        super().__init__(name='Овчарня', efficiency_bonus=0, upgrade_cost=3500, capacity=7)

    def add_animal(self, animal):
        # метод добавления овцы в овчарню
        if not isinstance(animal, (Sheep, BabyAnimal)):
            print(f'{self.name} может содержать только овец! Невозможно добавить {animal.name}')
            return False
        return super().add_animal(animal)

class GoatHouse(Building):
    def __init__(self):
        super().__init__(name='Козлятня', efficiency_bonus=0, upgrade_cost=3500, capacity=8)

    def add_animal(self, animal):
        # метод добавления козы в козлятню
        if not isinstance(animal, (Goat, BabyAnimal)):
            print(f'{self.name} может содержать только коз! Невозможно добавить {animal.name}')
            return False
        return super().add_animal(animal)