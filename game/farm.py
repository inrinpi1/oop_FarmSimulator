from buildings.buildings import ChickenCoop, CowShed, Sheepfold, GoatHouse
from animals.animals import Cow, Sheep, Goat, Chicken, Duck, Goose, BabyAnimal


class Farm:
    def __init__(self):
        self.plants = []
        self.animals = []
        self.buildings = []

    def add_plant(self, plant_class, quantity=1):
        # метод добавления растений на ферму
        for _ in range(quantity):
            plant_instance = plant_class()  # создаем отдельный экземпляр для каждого растения
            self.plants.append(plant_instance)
        print(f'Посажено {quantity} растений {plant_class.__name__}')

    def remove_plant(self, plant):
        self.plants.remove(plant)

    def get_ready_to_harvest(self):
        # метод получения списка созревших растений
        ready_to_harvest = {}
        for plant in self.plants:
            if plant.current_growth >= plant.growth_days:
                if plant.name not in ready_to_harvest:
                    ready_to_harvest[plant.name] = []
                ready_to_harvest[plant.name].append(plant)
        return ready_to_harvest

    def add_animal(self, animal, building_type):
        # метод добавления животного на ферму

        # проверяем, есть ли здание для данного типа животных
        building = self.find_building(building_type)
        if building:
            if building.add_animal(animal): # проверяем вместимость
                self.animals.append(animal) # добавляем животное в список если все ок
                print(f'Животное {animal.name} добавлено на ферму')
            else:
                print(f'{building.name} переполнено')
        else:
            print(f'Нет подходящего здания для {animal.name}')

    def find_building(self, building_type):
        # метод поиска здания по типу
        for building in self.buildings:
            if isinstance(building, building_type):
                return building
        return None