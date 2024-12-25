import random
import pickle

from game.farm import Farm
from environment.weather import Weather
from environment.plants import Plant
from market.market import Market
from inventory.inventory import Inventory
from animals.animals import Animal, Cow, Sheep, Goat, Chicken, Duck, Goose, BabyAnimal, Mammal, Bird 
from buildings.buildings import ChickenCoop, CowShed, Sheepfold, GoatHouse  


class Game:
    def __init__(self, max_actions=4):
        self.farm = Farm()
        self.market = Market() # тут мы пытаемся хоть немного заработать
        self.weather = Weather()
        self.inventory = Inventory()
        self.current_day = 1
        self.max_actions = max_actions # максимальное количество действий в день
        self.actions_left = self.max_actions # оставшееся количество действий
        self.is_running = True
        self.create_buildings()

    def create_buildings(self):
        # добавляем здания в начале игры
        self.farm.buildings.append(ChickenCoop())
        self.farm.buildings.append(CowShed())
        self.farm.buildings.append(Sheepfold())
        self.farm.buildings.append(GoatHouse())

    def display_menu(self):
        # отображение меню действий
        print(f'День {self.current_day}')
        print(f'Доступные действия: {self.actions_left}/{self.max_actions}')
        print('1. Посадить растение')
        print('2. Собрать урожай')
        print('3. Добавить животное')
        print('4. Покормить животное')
        print('5. Продать продукты')
        print('6. Купить корм')
        print('7. Улучшить постройки')
        print('8. Состояние фермы')
        print('9. Просмотреть инвентарь')
        print('10. Завершить день')
        print('11. Сохранить игру') 
        print('12. Загрузить игру') 
        print('13. Выйти')

    def run(self):
        # основной цикл игры
        while self.is_running:
            self.display_menu()
            choice = input('Выберите действие: ')
            self.process_action(choice)

    def process_action(self, choice):
        # обработка выбранного действия
        if choice == '1':
            self.perform_action(self.plant_crop)
        elif choice == '2':
            self.perform_action(self.harvest_crop)
        elif choice == '3':
            self.perform_action(self.add_animal)
        elif choice == '4':
            self.perform_action(self.feed_animal)
        elif choice == '5':
            self.perform_action(self.sell_products)
        elif choice == '6':
            self.perform_action(self.buy_feed)
        elif choice == '7':
            self.perform_action(self.upgrade_building)
        elif choice == '8':
            self.farm_status()
        elif choice == '9':
            self.inventory.show_inventory()
        elif choice == '10':
            self.end_day()
        elif choice == '11':
            self.save_game()
        elif choice == '12':
            self.load_game()
        elif choice == '13':
            self.is_running = False
            print('Выход из игры')
        else:
            print('Вы ввели что-то не то')

    def perform_action(self, action):
        # выполнение действия и уменьшение количества оставшихся действий
        action()
        self.actions_left -= 1
        self.update_animals()  # обновляем состояние животных после каждого действия
        if self.actions_left == 0:
            print('Вы хорошо потрудились сегодня! Время отдохнуть')
            self.end_day()

    def plant_crop(self):
        # логика посадки растений
        plant_classes = Plant.subclasses()
        plant_names = [plant_class().name for plant_class in plant_classes] # создаем список русских названий

        for idx, name in enumerate(plant_names, 1):
            print(f'{idx}. {name}')
            
        # выбираем класс растения
        while True:
            try:
                user_input = int(input('Выберите растение (номер): ')) - 1
                selected_plant_class = plant_classes[user_input]
                break
            except (ValueError, IndexError):
                print('Вы ввели что-то не то')
                
        # создаем временный экземпляр растения для расчета стоимости
        temp_plant = selected_plant_class()
        while True:
            try:
                quantity = int(input('Сколько растений посадить? '))
                total_cost = temp_plant.sell_price * quantity / 2  # цена семян = половина цены продажи

                if self.inventory.money >= total_cost:
                    self.inventory.spend_money(total_cost)
                    self.farm.add_plant(selected_plant_class, quantity)
                    break
                else:
                    print(f'Денег нет! Нужно {total_cost} монет')
                    return # возвращаемся к выбору действия
            except ValueError:
                print('Вы ввели что-то не то')

    def harvest_crop(self):
        # логика сбора урожая
        ready_to_harvest = self.farm.get_ready_to_harvest()
        if ready_to_harvest:
            for plant_name, plants in ready_to_harvest.items():
                print(f'{plant_name}: {len(plants)} готовы к сбору')
            selected_crop = input('Введите название растения, которое хотите собрать: ')
            if selected_crop in ready_to_harvest:
                count = 0
                for plant in ready_to_harvest[selected_crop]:
                    self.inventory.add_resource('продукция', plant.name, 1) # добавляем в инвентарь
                    self.farm.remove_plant(plant)
                    count += 1
                print(f'Собрано {count} растений {selected_crop}')
            else:
                print('Некорректный выбор. Это растение еще не готово к сбору')
        else:
            print('Ничего не выросло')

    def add_animal(self):
        # Логика добавления животных
        # получаем все классы, наследующиеся от Animal
        all_animal_classes = get_all_subclasses(Animal)
        # исключаем абстрактные классы (Bird, Mammal) и BabyAnimal
        animal_classes = [cls for cls in all_animal_classes if cls not in (BabyAnimal, Bird, Mammal)]
        animal_names = [animal_class().name for animal_class in animal_classes] # получаем список русских названий

        # выводим список доступных животных
        for idx, name  in enumerate(animal_names, 1):
            print(f'{idx}. {name}')
        
        # обрабатываем ввод пользователя
        while True:
            try:
                user_input = int(input('Выберите животное (номер): ')) - 1
                animal_class = animal_classes[user_input]
                break
            except (ValueError, IndexError):
                print('Вы ввели что-то не то')
        
        # создаем экземпляр животного
        animal = animal_class()

        # определяем тип здания для данного животного
        building_type = None
        if isinstance(animal, Cow):
            building_type = CowShed
        elif isinstance(animal, Sheep):
            building_type = Sheepfold
        elif isinstance(animal, Goat):
            building_type = GoatHouse
        elif isinstance(animal, (Chicken, Duck, Goose)):
            building_type = ChickenCoop

        # добавляем животное на ферму
        self.farm.add_animal(animal, building_type)

    def feed_animal(self):
        # Логика кормления животных
        if not self.farm.animals:
            print('А кормить некого')
            return

        # получаем виды животных по их классам
        animal_types = {}
        for animal in self.farm.animals:
            animal_class = type(animal)
            if animal_class not in animal_types:
                animal_types[animal_class] = 0
            animal_types[animal_class] += 1

        # выводим список классов животных
        animal_classes_list = list(animal_types.keys())
        for idx, a_class in enumerate(animal_classes_list, 1):
            print(f'{idx}. {a_class.__name__} (кол-во: {animal_types[a_class]})')

        while True:
            try:
                choice = int(input('Кого кормить будем? (номер): ')) - 1
                chosen_class = animal_classes_list[choice]
                break
            except (ValueError, IndexError):
                print('Вы ввели что-то не то')

        # кормим всех животных выбранного вида
        for animal in self.farm.animals:
            if isinstance(animal, chosen_class):
                animal.feed(self.inventory)  

    def sell_products(self):
        # торгуем на рынке (если есть чем)
        self.market.sell_products(self.inventory)

    def buy_feed(self):
        # закупаем корм (если есть на что)
        self.market.buy_feed(self.inventory)
    
    def upgrade_building(self):
        # Логика улучшения построек
        if not self.farm.buildings:
            print('На ферме нет построек для улучшения')
            return
        for idx, building in enumerate(self.farm.buildings, 1):
            print(f'{idx}. {building.name} (уровень {building.level}, вместимость {building.capacity}, бонус {building.efficiency_bonus}%, стоимость улучшения {building.upgrade_cost})')
        while True:
            try:
                selected_idx = int(input('Выберите постройку для улучшения (номер): ')) - 1
                building = self.farm.buildings[selected_idx]
                break
            except (ValueError, IndexError):
                print('Вы ввели что-то не то')
        building.upgrade(self.inventory)

    def farm_status(self):
        # отображение состояния фермы
        print(f'\nДенег в кармане: {self.inventory.money}')
        print('Растения:')
        if not self.farm.plants:
            print('Нет посаженных растений')
        for plant in self.farm.plants:
            status = 'Готово к сбору' if plant.current_growth >= plant.growth_days else f'Рост: {plant.current_growth}/{plant.growth_days}'
            print(f'{plant.name}: {status}')
        print('Животные:')
        if not self.farm.animals:
            print('Нет животных')
        for animal in self.farm.animals:
            status = f'Здоровье {animal.health}. Голод {animal.hunger}'
            print(f'{animal.name}: {status}')
        print('Постройки:')
        if not self.farm.buildings:
            print('Нет построек')
        for building in self.farm.buildings:
            print(f'{building.name} (Уровень {building.level}, вместимость {building.capacity}, бонус {building.efficiency_bonus}%)')

    def end_day(self):
        # Логика завершения дня
        print(f'Завершение дня {self.current_day}')
        self.current_day += 1
        self.actions_left = self.max_actions
        print(f'День {self.current_day}. Доступные действия: {self.actions_left}/{self.max_actions}')
        self.weather.generate_weather()
        for plant in self.farm.plants:
            plant.grow(self.weather)
        self.market.update_prices()
        for animal in self.farm.animals:
            if isinstance(animal, BabyAnimal):
                animal.grow() # детеныши растут
            else:
                animal.produce(self.inventory, self.get_building_bonus(animal)) # взрослые производят
        # размножение
        babies_to_add = []
        for animal in self.farm.animals:
            if not isinstance(animal, BabyAnimal):
                offspring = animal.reproduce()
                if offspring:
                    babies_to_add.extend(offspring)

        # добавляем детенышей 
        for baby in babies_to_add:
            building_type = None
            if isinstance(baby.parent, Cow):
                building_type = CowShed
            elif isinstance(baby.parent, Sheep):
                building_type = Sheepfold
            elif isinstance(baby.parent, Goat):
                building_type = GoatHouse
            elif isinstance(baby.parent, (Chicken, Duck, Goose)):
                building_type = ChickenCoop

            if building_type:
                self.farm.add_animal(baby, building_type)
            else:
                print(f'Не удалось определить тип здания для детеныша {baby.name}')

    def get_building_bonus(self, animal):
        # получение бонуса к производству от построек
        for building in self.farm.buildings:
            if isinstance(animal, Cow) and isinstance(building, CowShed):
                return building.efficiency_bonus
            elif isinstance(animal, Sheep) and isinstance(building, Sheepfold):
                return building.efficiency_bonus
            elif isinstance(animal, Goat) and isinstance(building, GoatHouse):
                return building.efficiency_bonus
            elif isinstance(animal, (Chicken, Duck, Goose)) and isinstance(building, ChickenCoop):
                return building.efficiency_bonus
        return 0

    def update_animals(self):
        # обновление состояния животных после каждого действия
        animals_to_remove = [] 
        for animal in self.farm.animals:
            animal.update_state()
            if not animal.is_alive:
                animals_to_remove.append(animal)
        # удаляем мертвых животных (кормите животных, пожалуйста, иначе они умрут...)
        for animal in animals_to_remove:
            self.farm.animals.remove(animal)
    
    def save_game(self, filename='savegame.pkl'):
        with open(filename, 'wb') as file:
            data_to_save = {
                'farm': self.farm,
                'market': self.market,
                'weather': self.weather,
                'inventory': self.inventory,
                'current_day': self.current_day,
                'max_actions': self.max_actions,
                'actions_left': self.actions_left,
                'is_running': self.is_running
            }
            pickle.dump(data_to_save, file)
        print(f'Игра сохранена в файл {filename}')

    def load_game(self, filename='savegame.pkl'):
        try:
            with open(filename, 'rb') as file:
                loaded_data = pickle.load(file)
                self.farm = loaded_data['farm']
                self.market = loaded_data['market']
                self.weather = loaded_data['weather']
                self.inventory = loaded_data['inventory']
                self.current_day = loaded_data['current_day']
                self.max_actions = loaded_data['max_actions']
                self.actions_left = loaded_data['actions_left']
                self.is_running = loaded_data['is_running']
            print(f'Игра загружена из файла {filename}')
        except FileNotFoundError:
            print(f'Не могу найти {filename}')


def get_all_subclasses(cls):
    # функция для получения всех подклассов класса
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_all_subclasses(subclass))
    return subclasses