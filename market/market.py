from inventory.inventory import Inventory
from environment.plant import Plant

class Market:
    def __init__(self):
        self.prices = {}
        self.generate_prices()

    def generate_prices(self):
        # метод генерации цен на рынке
        # цены на растения
        for plant_class in Plant.subclasses():
            plant = plant_class()
            self.prices[plant.name] = plant.sell_price
        # цены на продукты животноводства
        self.prices['молоко'] = random.randint(50, 100)
        self.prices['шерсть'] = random.randint(50, 150)
        self.prices['яйца'] = random.randint(5, 15)
        # цена на корм
        self.prices['корм'] = random.randint(10,30)

    def sell_products(self, inventory):
        # метод продажи продуктов из инвентаря
        print('Рыночные цены:')
        for item, price in self.prices.items():
            print(f'{item}: {price} монет')

        category = 'продукция'  
        if not inventory.resources[category]:
            print(f'В категории {category} нет ресурсов для продажи')
            return

        for item, amount in inventory.resources[category].items():
            print(f'{item}: {amount} в наличии')

        item_to_sell = input('Что хотите продать? ')
        if item_to_sell in inventory.resources[category]:
            amount_to_sell = int(input(f'Сколько {item_to_sell} продать? '))
            if amount_to_sell <= inventory.resources[category][item_to_sell]:
                total_price = self.prices[item_to_sell] * amount_to_sell
                inventory.remove_resource(category, item_to_sell, amount_to_sell)
                inventory.earn_money(total_price)
                print(f'Продано {amount_to_sell} {item_to_sell} за {total_price} монет')
            else:
                print(f'Недостаточно {item_to_sell} для продажи')
        else:
            print('Такого товара нет в инвентаре')

    def buy_feed(self, inventory):
        # метод покупки корма
        feed_price = self.prices['корм'] # получаем цену корма
        print(f'Цена корма: {feed_price} монет') 

        amount_to_buy = int(input(f'Сколько корма купить? '))
        item_to_buy = 'корм' 
        total_price = self.prices[item_to_buy] * amount_to_buy
        if inventory.money >= total_price:
            inventory.spend_money(total_price)
            inventory.add_resource('корма', item_to_buy, amount_to_buy)
            print(f'Куплено {amount_to_buy} {item_to_buy} за {total_price} монет')
        else:
            print(f'Недостаточно денег для покупки {item_to_buy}')

    def update_prices(self):
        # метод обновления цен на рынке
        for item in self.prices:
            change = random.uniform(0.9, 1.1)  # изменение цены на +/- 10%
            self.prices[item] = int(self.prices[item] * change) # цена должна быть целым числом