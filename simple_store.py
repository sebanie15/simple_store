# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""
from functools import wraps
from datetime import datetime as dt
from utilities.utilities import encrypt, is_email_valid, is_phone_valid


def is_logged_in(func):
	@wraps(func)
	def wrapper(self, user):
		if user in self.logged_users:
			return func(self, user)
		else:
			return False

	return wrapper


def is_registered_to(func):
	@wraps(func)
	def wrapper(self, login, password):
		for user in self.registered_users:
			if user.email == login and user.password == encrypt(password):
				return func(self, login, password)
	return wrapper


def on_changing_product_price(func):
	@wraps(func)
	def wrapper(self, price):
		self.price_history[dt.now()] = price
		return func(self, price)
	return wrapper


class Product:
	auto_id = 0
	# price_history = {}

	def __init__(self, name: str, price: float = 0.0, _product_id: int = 0) -> None:
		if _product_id == 0:
			Product.auto_id += 1
			self.id = self.auto_id
		else:
			self.id = _product_id
			if _product_id > self.auto_id:
				self.auto_id = _product_id
		self.name = name
		self._price_history = dict()
		self._price_history[dt.now()] = price
		self._price = price

	@property
	def price(self):
		return self._price

	@price.setter
	@on_changing_product_price
	def price(self, new_price):
		if new_price > 0:
			self._price = new_price


class Stock:

	def __init__(self, stock_id):
		self.id = stock_id
		self.products = {}

	def add_product(self, product: Product, quantity: float, price: float = 0) -> bool:
		"""method adding product to stock

		Args:
			product: Product
			quantity: float
			price: float
		Returns:
			bool
		"""
		if product not in self.products:
			self.products[product] = quantity
			if price > 0:
				self.products[product].change_price(price)
			return True
		else:
			return self.increase_amount_of_product(product, quantity) and self.update_product_price(product, price)

	def increase_amount_of_product(self, product: Product, quantity: float) -> bool:
		"""the method increases the amount of product in stock

		Args:
			product: Product
			quantity: float
		Returns:
			bool
		"""
		if product in self.products:
			last_quantity = self.products[product]
			self.products.update({product: last_quantity + quantity})
			return True
		return False

	def sub_product(self, product: Product, quantity: float) -> None:
		"""the method subtracts the quantity of the product indicated in the quantity argument

		Args:
			product: Product
			quantity: float
		Returns:
			None
		"""
		if product in self.products:
			self.products.update({product: self.products[product] - quantity})

	def update_product_price(self, product: Product, price: float) -> bool:
		"""this method update price of product

		Args:
			product: Product
			price: float

		Returns:
			bool
		"""
		if product in self.products:
			self.products[product].change_price(price)
			return True
		return False

	def print_products(self, parameters: tuple = ('product_name', 'price', 'quantity')):
		print(f'magazyn: {self.id}')
		for product in self.products:
			print(product.first_name, product.price, self.products[product])
			# TODO: expand the functionality of the print_products function
		# print(self.products)


class User:

	def __init__(self, first_name, second_name, email, phone_number, password):
		self.first_name = first_name
		self.second_name = second_name
		self.email = email
		self.phone_number = phone_number
		self.password = encrypt(password)
		self.basket = {}

	# TODO: @Product.is_available_in_stock
	def add_to_basket(self, product: Product, quantity: float) -> None:
		"""
		This method is to add the product to the buyer's basket

		TODO: perhaps I should check how much product is in stock, or I can specify a longer delivery date in the
			following	functions. These are issues to be resolved later.

		Args:
			product: Product
			quantity: float
		Returns:
			None
		"""
		if product not in self.basket:
			self.basket[product] = quantity
		else:
			old_quantity = self.basket[product]
			self.basket.update({product: old_quantity + quantity})


class Store(object):

	def __init__(self, name: str):
		self.name = name
		self.logged_users = []
		self.registered_users = []
		self.stocks = []

	def register(self, first_name, second_name, email, phone_number, password) -> bool:
		"""The method is used to register the user in the store, his account is created - adding the user to
		registered_users list

		Args:
			first_name: str
			second_name: str
			email: str
			phone_number: int
			password: str

		Returns:
			bool
		"""

		# TODO: validation of email and phone_number

		if self.find_user_by_login(email):
			return True

		if is_phone_valid(phone_number) and is_email_valid(email):
			self.registered_users.append(
				User(
					first_name=first_name,
					second_name=second_name,
					email=email,
					phone_number=phone_number,
					password=encrypt(password)
				)
			)
			return True
		return False

	@is_registered_to
	def login(self, login: str, password: str) -> bool:
		"""the method allows the user to log into the store

		Args:
			login: str
			password: str

		Returns:
			bool
		"""
		found_user = self.find_user_by_login(login)
		if found_user and found_user.password == encrypt(password):
			self.logged_users.append(found_user)
			return True
		return False

	def logout(self, user: User) -> None:
		"""the method allows the user to log out of the store

		Args:
			user: User
		Returns:
			None
		"""
		# TODO: the method is not finished, how to mark an active user - need a server?
		if user in self.logged_users:
			del (self.logged_users[self.logged_users.index(user)])

	def which_stock(self, product: Product) -> Stock:
		"""the method checks which stock the product is on

		Args:
			product: Product

		Returns:
			Stock
		"""
		for stock in self.stocks:
			if product in stock:
				return stock

	def find_user_by_login(self, login: str) -> User:
		"""the method finding user as User

		Args:
			login: str

		Returns:
			USer
		"""
		for user in self.registered_users:
			if user.email == login:
				return user

	def product_amount(self, product: Product) -> float:
		"""the method returns the quantity of the product in stock

		Args:
			product: Product

		Returns:
			float
		"""
		return self.which_stock(product).products[product]

	@is_logged_in
	def buy(self, user):
		# TODO: operation of buying
		if user.basket:
			for product, amount in user.basket:
				self.which_stock(product).sub_product(product, amount)
		return f'Bought by {user}'

	def load_from_file(self, filename):
		# TODO: develop a method to load the store (users, products, etc.) from a file
		pass

	def save_to_file(self, filename):
		# TODO: develop a method to save the store (users, products, etc.) to a file
		pass



