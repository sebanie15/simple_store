# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""

# from functools import wraps


def is_logged_in(func):
	# @wraps(func)
	def wrapper(self, user):
		if user in self.logged_users:
			return func(self, user)
		else:
			return False

	return wrapper

def is_registered_to(func):
	def wrapper(self, user):
		if user in self.registered_users:
			return func(self, user)
		return False
	return wrapper


class User:
	def __init__(self, name):
		self.name = name



class Store(object):

	def __init__(self, name: str):
		self.name = name
		self.logged_users = []
		self.registered_users = []

	def register(self, user):
		if user not in self.registered_users:
			self.registered_users.append(user)
			return True
		return False

	# def is_registered_to(func):
	#	def wrapper(self, user):
	#		if user in self.registered_users:
	#			return func(self, user)
	#		return False
	#	return wrapper

	@is_registered_to
	def login(self, user):
		if user not in self.logged_users:
			self.logged_users.append(user)
			return True
		return False

	def logout(self, user):
		if user in self.logged_users:
			del (self.logged_users[self.logged_users.index(user)])
			return True

	#def is_logged_in(func):
		# @wraps(func)
	#	def wrapper(self, user):
	#		if user in self.logged_users:
	#			return func(self, user)
	#		else:
	#			return False
	#	return wrapper

	@is_logged_in
	def buy(self, user):
		return f'Bought by {user}'


user1 = User(name='Sebastian')

sklep1 = Store('Biedronka')
print('logging before registration: ', sklep1.login('Sebastian'))
print('buying after logging in but before registration: ', sklep1.buy('Sebastian'))

print('register: ', sklep1.register(user=user1))
print('logging after register: ', sklep1.login(user=user1))
print('buying after logging in: ', sklep1.buy(user=user1))
print('re-login without logging out: ', sklep1.login(user=user1))
print('logout: ', sklep1.logout(user=user1))
print('buy after logout: ', sklep1.buy(user=user1))
print(' : ', sklep1.register(user=user1))

