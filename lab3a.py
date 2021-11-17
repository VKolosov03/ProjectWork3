import json
import datetime

MIN_DAYS=10
MAX_DAYS=60
MIN_TICKETS=1
ID_LEN=3

class Person:
	def __init__(self,surname,name,ticket_type):
		self.name=name
		self.surname=surname
		self.ticket_type=ticket_type

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self,name):
		if not isinstance(name,str):
			raise TypeError
		self.__name = name

	@property
	def surname(self):
		return self.__surname

	@surname.setter
	def surname(self,surname):
		if not isinstance(surname,str):
			raise TypeError
		self.__surname = surname

	@property
	def ticket_type(self):
		return self.__ticket_type

	@ticket_type.setter
	def ticket_type(self,ticket_type):
		if not isinstance(ticket_type,bool):
			raise TypeError
		self.__ticket_type = ticket_type

	def get_tickets_by_name(self):
		ticket_string=""
		with open('second.json', 'r') as open_second:
			json_customer=json.load(open_second)
			for key1 in json_customer:
				if json_customer[key1]['name']==self.name and json_customer[key1]['surname']==self.surname:
					for key2 in json_customer[key1]:
						ticket_string=ticket_string+key2+": "+str(json_customer[key1][key2])+'\n'
					ticket_string+='\n'
		return ticket_string

class Ticket(Person):

	def __init__(self,surname,name,ticket_type,time):
		super().__init__(surname,name,ticket_type)
		self.time=time

	@property
	def time(self):
		return self.__time

	@time.setter
	def time(self,time):
		if not isinstance(time,datetime.date):
				raise TypeError
		self.__time = time

	def buy(self):
		json_tickets=""""""
		json_customer=""""""
		ticket_id=""
		with open('first.json', 'r') as open_first:
			json_tickets=json.load(open_first)
		with open('second.json', 'r') as open_second:
			json_customer=json.load(open_second)
		if self.ticket_type:
			ticket_id=str(json_tickets['ticket_type']['s']['next_ticket_number'])+'-s'
		else:
			if (datetime.date(year=json_tickets['year'],month=json_tickets['month'],day=json_tickets['day'])-self.time).days>=MAX_DAYS:
				ticket_id=str(json_tickets['ticket_type']['a']['next_ticket_number'])+'-a'
			elif (datetime.date(year=json_tickets['year'],month=json_tickets['month'],day=json_tickets['day'])-self.time).days<MIN_DAYS:
				ticket_id=str(json_tickets['ticket_type']['l']['next_ticket_number'])+'-l'
			else:
				ticket_id=str(json_tickets['ticket_type']['r']['next_ticket_number'])+'-r'
		if json_tickets['ticket_type'][ticket_id[2]]['amount']<MIN_TICKETS:
			raise RuntimeError("Sold out!")
		if ticket_id not in json_customer:
			json_customer[ticket_id] = {}
		json_customer[ticket_id]['ticket_id']=ticket_id
		json_customer[ticket_id]['name']=self.name
		json_customer[ticket_id]['surname']=self.surname
		json_customer[ticket_id]['price']=json_tickets['price']*json_tickets['ticket_type'][ticket_id[2]]['discount']
		json_customer[ticket_id]['year']=self.time.year
		json_customer[ticket_id]['month']=self.time.month
		json_customer[ticket_id]['day']=self.time.day
		json_tickets['ticket_type'][ticket_id[2]]['amount']-=1
		json_tickets['ticket_type'][ticket_id[2]]['next_ticket_number']+=1
		with open('first.json', 'w') as open_first:
			json.dump(json_tickets,open_first, indent=4)
		with open('second.json', 'w') as open_second:
			json.dump(json_customer,open_second, indent=4)

	@staticmethod
	def search_id(ticket_id):
		if not isinstance(ticket_id,str):
			raise TypeError
		if len(ticket_id)!=ID_LEN or not ticket_id[0].isdigit() or ticket_id[1]!='-' or ticket_id[2] not in "asrl":
			raise RuntimeError("Wrong formation!")
		with open('second.json', 'r') as open_second:
			json_customer=json.load(open_second)
			return False if ticket_id not in json_customer else True

	@staticmethod
	def get_price(time):
		price_string=""
		with open('first.json', 'r') as open_first:
			json_tickets=json.load(open_first)
			for key in json_tickets['ticket_type']:
				price_string=price_string+json_tickets['ticket_type'][key]['name']+'-'+str(json_tickets['ticket_type']
					[key]['discount']*json_tickets['price'])+'\n'
			if (datetime.date(year=json_tickets['year'],month=json_tickets['month'],day=json_tickets['day'])-time).days>=MAX_DAYS:
				price_string=price_string+json_tickets['ticket_type']['a']['name']
			elif (datetime.date(year=json_tickets['year'],month=json_tickets['month'],day=json_tickets['day'])-time).days<MIN_DAYS:
				price_string=price_string+json_tickets['ticket_type']['l']['name']
			else:
				price_string=price_string+json_tickets['ticket_type']['r']['name']
			return price_string+" ticket is currently able!"

	def get_string(self,ticket_id):
		ticket_string=""
		if self.search_id(ticket_id):
			with open('second.json', 'r') as open_second:
				json_customer=json.load(open_second)
				for key in json_customer[ticket_id]:
					ticket_string=ticket_string+key+": "+str(json_customer[ticket_id][key])+'\n'
			return ticket_string
		else:
			return "Nobody bought this ticket"
			




customer1 = Ticket("Kolos", "Vlad", True, datetime.date.today())
customer2 = Ticket("Kolosov", "Vladik", False, datetime.date.today())
customer3 = Ticket("Kol", "Vladislav", False, datetime.date(year=2021, month=12, day=20))
customer1.buy()
customer2.buy()
customer3.buy()
print(customer1.get_string('1-s'),"\n")
print(customer2.get_string('2-l'),"\n")
print(customer3.get_tickets_by_name(),"\n")
print(customer1.get_price(datetime.date.today()))
