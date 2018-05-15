import math
from sympy import *
from sympy.solvers.solveset import linsolve

def distance(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def find_point(p1, p2, r, oc):
	p = p1[0]
	q = p1[1]
	a = p2[0]
	b = p2[1]
	x0 = oc[0]
	y0 = oc[1]
	
	# solution 1
	cons11 = (p*q + r*(math.sqrt(p**2 + q**2 -r**2))) / (r**2 - p**2)
	cons12 = (p*q - r*(math.sqrt(p**2 + q**2 -r**2))) / (r**2 - p**2)
	cons21 = (a*b + r*(math.sqrt(a**2 + b**2 -r**2))) / (r**2 - a**2) 
	cons22 = (a*b - r*(math.sqrt(a**2 + b**2 -r**2))) / (r**2 - a**2)

	x,y = symbols('x,y')
	a1 = -(cons11)*(x-x0-p) + q + y0 - y
	a2 = -(cons12)*(x-x0-p) + q + y0 - y
	b1 = -(cons21)*(x-x0-a) + b + y0 - y 
	b2 = -(cons22)*(x-x0-a) + b + y0 - y 
	
	ans1 = linsolve([a1,b1],(x,y))
	x1,y1 = next(iter(ans1))
	ans2 = linsolve([a1,b2],(x,y))
	x2,y2 = next(iter(ans2))
	ans3 = linsolve([a2,b1],(x,y))
	x3,y3 = next(iter(ans3))
	ans4 = linsolve([a2,b2],(x,y))
	x4,y4 = next(iter(ans4))

	d1 = distance(p,q,x1,y1)
	d2 = distance(p,q,x2,y2)
	d3 = distance(p,q,x3,y3)
	d4 = distance(p,q,x4,y4)

	if(d1<=min(d2,d3,d4)):
		return x1,y1
	elif(d2<=min(d1,d3,d4)):
		return x2,y2
	elif(d3<=min(d2,d1,d4)):
		return x3,y3
	elif(d4<=min(d2,d3,d1)):
		return x4,y4
