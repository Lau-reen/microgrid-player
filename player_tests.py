# python 3
# this class combines all basic features of a generic player
import numpy as np
import pandas
from scipy import optimize
from math import *

# def f(alpha):
#	res = 0
#	for i in range(0,48):
#		res += random_lambda[i]*(1+1/(4*dt))*l_it[i] + alpha[i] * h_r[i] * (1/((COP_hp -1)*dt)) * (random_lambda[i] - phw[i]*COP_hp * dt)
#	return res



class Player:

	def __init__(self):
		# some player might not have parameters
		self.parameters = 0
		self.horizon = 48
		l_i = pandas.read_csv('data_center_scenarios.csv', ";")
		l_i[l_i["scenario"] == 1]
		self.l_it = np.array(l_i["cons (kW)"])
		self.COP_hp = (0.4 * 60) / (60 - 35)
		self.COP_cs = 5
		self.random_lambda = np.random.rand(48)
		self.prices_purchase = np.ones(self.horizon)
		self.prices_sale = np.ones(self.horizon)
		self.prices_purchase =np.random.rand(self.horizon)
		self.prices_sale =np.random.rand(self.horizon)
		self.dt = 0.5
		self.MaxProd = 10
		#self.l_cs = self.l_it / (4 * self.dt)
		#self.h_r = self.l_cs * self.COP_cs * self.dt
		self.l_cs = np.ones(48)
		self.h_r = np.ones(48)
		self.l_hp = np.ones(self.horizon)
		self.h_dc = np.ones(self.horizon)
		self.alpha = np.zeros(48)
		self.alpha_0 = np.zeros(48)

	def set_scenario(self, scenario_data):
		self.data = scenario_data

	def set_prices(self, prices):
		self.prices = prices

	def compute_all_loads(self):
		load = np.zeros(self.horizon)
		for time in range(self.horizon):
			load[time] = self.compute_load(time)
		return load

	def take_decision(self, time):
		self.l_cs[time] = self.l_it[time] / (4 * self.dt)
		self.h_r[time] = self.l_cs[time] * self.COP_cs * self.dt

		if self.prices_purchase[time] * self.h_r[time] < self.MaxProd * self.prices_sale[time]:
			self.h_dc[time] = self.MaxProd
			self.l_hp[time] = self.h_dc[time] / (self.COP_hp * self.dt)
			self.alpha[time] = self.l_hp[time] * (self.COP_hp - 1) * self.dt / self.h_r[
					time]
		return self.alpha[time]

	def compute_opt(self, alpha):
		res = 0
		for i in range(0, 48):
			res += self.random_lambda[i] * (1 + 1 / (4 * self.dt)) * self.l_it[i] + alpha[i] * self.h_r[i] * (1 / ((self.COP_hp - 1) * self.dt)) * (
				self.random_lambda[i] - self.prices_sale[i] * self.COP_hp * self.dt)
		return res

	def fun(self):
		res = optimize.minimize(self.compute_opt, np.zeros(48))
		return res.x

	def compute_all_load(self):
		load = np.zeros(self.horizon)
		alpha = self.fun()
		for time in range(self.horizon):
			load += self.random_lambda[time] * (1 + 1 / (4 * self.dt)) * self.l_it[time] + alpha[time] * self.h_r[time] * (
						1 / ((self.COP_hp - 1) * self.dt)) * (
						   self.random_lambda[time] - self.prices_sale[time] * self.COP_hp * self.dt)

		return load




	def reset(self):
		# reset all observed data
		pass


if __name__ == "__main__":
	myplayer = Player()
	myload = myplayer.compute_all_load()
	print(myload)


##22.769