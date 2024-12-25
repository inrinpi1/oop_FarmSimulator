import random

class Weather:
    def __init__(self):
        self.current_condition = self.generate_weather()

    def generate_weather(self):
        conditions = ['солнечно', 'дождливо', 'облачно', 'ветрено', 'аномальная жара', 'нашествие насекомых']
        self.current_condition = random.choice(conditions)
        print(f'Текущая погода: {self.current_condition}')
        return self.current_condition

    def get_growth_multiplier(self):
        # метод, который возвращает коэффициент роста в зависимости от погоды
        if self.current_condition == 'солнечно':
            return 1.5  # увеличиваю рост на 50%
        elif self.current_condition == 'дождливо':
            return 1.2  # увеличиваю рост на 20%
        elif self.current_condition == 'облачно':
            return 1.0  # стандартный рост
        elif self.current_condition == 'ветрено':
            return 0.5  # уменьшение роста на 50%
        elif self.current_condition == 'аномальная жара':
            return 0.0  # нет роста
        elif self.current_condition == 'нашествие насекомых':
            return 0.0  # нет роста
        return 1.0  # пусть по умолчанию будет такой показатель