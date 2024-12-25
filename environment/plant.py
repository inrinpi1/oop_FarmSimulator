from environment.weather import Weather

class Plant:
    def __init__(self, name, growth_days, sell_price):
        self.name = name
        self.growth_days = growth_days  # сколько дней требуется для роста растений до готовности к сбору
        self.current_growth = 0  # текущий прогресс растений (в днях)
        self.sell_price = sell_price  # цена продажи за штуку

    def grow(self, weather_condition):
        growth_multiplier = weather_condition.get_growth_multiplier()
        self.current_growth += growth_multiplier  # за один день увеличиваем рост коэффициент погоды
        # ограничение на максимальный рост
        if self.current_growth > self.growth_days:
            self.current_growth = self.growth_days
        # ограничение на минимальный рост
        elif self.current_growth < 0:
            self.current_growth = 0
        print(f'Растение {self.name} выросло на {growth_multiplier:.2f}. Текущий прогресс роста: {self.current_growth:.2f}')

    def harvest(self):
        # проверяем, созрело ли растение
        if self.current_growth >= self.growth_days:
            self.current_growth = 0  # сбрасываю прогресс после сбора
            return 1  # 1 штука
        return 0  # если не готово, вернуть 0

    @classmethod
    def subclasses(cls):
        # возвращает список подклассов
        return cls.__subclasses__()

class Carrot(Plant):
    def __init__(self):
        super().__init__(name='Морковь', growth_days=5, sell_price=50)

class Tomato(Plant):
    def __init__(self):
        super().__init__(name='Помидор', growth_days=4, sell_price=336)

class Potato(Plant):
    def __init__(self):
        super().__init__(name='Картофель', growth_days=5, sell_price=44)

class Cabbage(Plant):
    def __init__(self):
        super().__init__(name='Капуста', growth_days=6, sell_price=62)

class Eggplant(Plant):
    def __init__(self):
        super().__init__(name='Баклажан', growth_days=5, sell_price=580)

class Apple(Plant):
    def __init__(self):
        super().__init__(name='Яблоко', growth_days=3, sell_price=170)

class Pear(Plant):
    def __init__(self):
        super().__init__(name='Груша', growth_days=3, sell_price=300)

class Beet(Plant):
    def __init__(self):
        super().__init__(name='Свекла', growth_days=4, sell_price=90)

class Wheat(Plant):
    def __init__(self):
        super().__init__(name='Пшеница', growth_days=2, sell_price=14)

class Pepper(Plant):
    def __init__(self):
        super().__init__(name='Перец', growth_days=5, sell_price=570)

class Onion(Plant):
    def __init__(self):
        super().__init__(name='Лук', growth_days=5, sell_price=89)

class Plum(Plant):
    def __init__(self):
        super().__init__(name='Слива', growth_days=3, sell_price=177)

class Pumpkin(Plant):
    def __init__(self):
        super().__init__(name='Тыква', growth_days=6, sell_price=110)

class Cucumber(Plant):
    def __init__(self):
        super().__init__(name='Огурец', growth_days=3, sell_price=140)