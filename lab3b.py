import json
import datetime

MIN_NUMB=0

class Pizza_day:
    def __init__(self):
        self.day=str(datetime.datetime.now().weekday())

    def __str__(self):
        pizza_string="Pizza of the day\n"
        with open('third.json', 'r') as open_first:
            json_pizza=json.load(open_first)
            for key in json_pizza[self.day]:
                if key=='ingredients':
                    pizza_string+=key+": "
                    for key2 in json_pizza[self.day]['ingredients']:
                        pizza_string+=key2+', '
                else:
                    pizza_string+=key+": "+str(json_pizza[self.day][key])+'\n'
        return pizza_string+'\n'

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self,day):
        if not isinstance(day,str):
            raise TypeError
        self.__day = day

class Order(Pizza_day):

    def __init__(self,**extra_order):
        super().__init__()
        self.extra_order=extra_order
        self.price=0

    def __str__(self):
        return self.buy_pizza()+" and you've also added "+self.buy_ingredients()+"\nYou must pay "+'{:.2f}'.format(self.price)+" bucks"
        #return super().__str__()+'\n'+self.buy_pizza()+" and you've also added "+self.buy_ingredients()+"\nYou must pay "+'{:.2f}'.format(self.price)+" bucks"

    @property
    def extra_order(self):
        return self.__extra_order

    @extra_order.setter
    def extra_order(self,extra_order):
        if not isinstance(extra_order,dict):
                raise TypeError
        if len(extra_order)>0:
            for key in extra_order:
                if not isinstance(extra_order[key],float) and not isinstance(extra_order[key],int):
                    if extra_order[key].isdigit():
                        extra_order[key]=float(extra_order[key])
                    else:
                        raise TypeError
        self.__extra_order = extra_order

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self,price):
        if not isinstance(price,float) and not isinstance(price,int):
                if price.isdigit():
                    price=float(price)
                else:
                    raise TypeError
        self.__price = price

    def buy_pizza(self):
        with open('third.json', 'r') as open_first:
            json_pizza=json.load(open_first)
        with open('fourth.json', 'r') as open_second:
            json_ingredients=json.load(open_second)
        for key1 in json_pizza[self.day]['ingredients']:
            for key2 in json_ingredients:
                if key1==key2:
                    if json_ingredients[key2]['weight']-json_pizza[self.day]['ingredients'][key1]>=MIN_NUMB:
                        json_ingredients[key2]['weight']-=json_pizza[self.day]['ingredients'][key1]
                    else:
                        raise RuntimeError("Sold out!")
        self.price+=json_pizza[self.day]['price']
        with open('third.json', 'w') as open_first:
            json.dump(json_pizza,open_first,indent=4)
        with open('fourth.json', 'w') as open_second:
            json.dump(json_ingredients,open_second,indent=4)
        return "You've just bought a "+json_pizza[self.day]['name']

    def buy_ingredients(self):
        ind=0
        if len(self.extra_order)<=MIN_NUMB:
            return "nothing"
        with open('third.json', 'r') as open_first:
            json_pizza=json.load(open_first)
        with open('fourth.json', 'r') as open_second:
            json_ingredients=json.load(open_second)
        for key1 in self.extra_order:
            for key3 in json_pizza[self.day]['ingredients']:
                if key1==key3:
                    raise RuntimeError("You can't add this!")
            for key2 in json_ingredients:
                if key1==key2:
                    ind=1
                    if json_ingredients[key2]['weight']-self.extra_order[key1]<MIN_NUMB:
                        raise RuntimeError("Sold out!")
                    json_ingredients[key2]['weight']-=self.extra_order[key1]
                    self.price+=json_ingredients[key2]['price']*self.extra_order[key1]
            if ind==0:
                raise RuntimeError("You can't add this!")
            ind=0
        with open('third.json', 'w') as open_first:
            json.dump(json_pizza,open_first,indent=4)
        with open('fourth.json', 'w') as open_second:
            json.dump(json_ingredients,open_second,indent=4)
        return ','.join(i for i in self.extra_order.keys())
            



pizza=Pizza_day()
customer1=Order(bacon=300,veal=100,feta=150.5)
print(pizza)
print(customer1)
