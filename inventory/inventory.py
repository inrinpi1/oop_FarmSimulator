class Inventory:
    def __init__(self):
        self.resources = {
            # 'семена': {},
            'корма': {},
            'продукция': {},
        }
        self.money = 0

    def earn_money(self, amount):
        self.money += amount
        print(f'Заработано {amount}. Текущий баланс: {self.money}')

    def spend_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            print(f'Потрачено {amount}. Текущий баланс: {self.money}')
        else:
            print(f'Недостаточно денег для покупки. Баланс: {self.money}')

    def add_resource(self, category, resource_name, amount):  # если надо что-то добавить
        if resource_name not in self.resources[category]:
            self.resources[category][resource_name] = 0
        self.resources[category][resource_name] += amount
        print(f'Добавлено {amount} {resource_name}. Текущий запас: {self.resources[category][resource_name]}')

    def remove_resource(self, category, resource_name, amount):
        if resource_name in self.resources[category]:
            if self.resources[category][resource_name] >= amount:
                self.resources[category][resource_name] -= amount
                if self.resources[category][resource_name] == 0:
                    del self.resources[category][resource_name]
                print(f'Удалено {amount} {resource_name}. Остаток: {self.resources[category].get(resource_name, 0)}')
            else:
                print(f'Недостаточно {resource_name} для удаления. В наличии: {self.resources[category][resource_name]}')
        else:
            print(f'Ресурс {resource_name} не найден в категории {category}')
    
    def show_inventory(self):  # показывает что есть в инвентаре
        print('\nТекущий инвентарь:')
        for category, resources in self.resources.items():
            print(f'\nКатегория: {category}')
            if resources:
                for resource, amount in resources.items():
                    print(f'{resource}: {amount}')
            else:
                print('Нет ресурсов')
        print(f'\nДеньги: {self.money} монет\n')