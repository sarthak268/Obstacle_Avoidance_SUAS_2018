import math
from sympy.solvers import solve
from sympy import Symbol

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

	x = Symbol('x')
	a1 = -(cons11)*(x-x0-p) + q + y0
	a2 = -(cons12)*(x-x0-p) + q + y0
	b1 = -(cons21)*(x-x0-a) + b + y0
	b2 = -(cons22)*(x-x0-a) + b + y0
	
	ans1 = solve(a1,b1)
	ans2 = solve(a1,b2)
	ans3 = solve(a2,b1)
	ans4 = solve(a2,b2)
	#print("fcgvhb,",ans4)

	d1 = distance(p,q,ans1[0],ans1[1])
	d2 = distance(p,q,ans2[0],ans2[1])
	d3 = distance(p,q,ans3[0],ans3[1])
	d4 = distance(p,q,ans4[0],ans4[1])

	if(d1<=min(d2,d3,d4)):
		return ans1[0], ans1[1]
	elif(d2<=min(d1,d3,d4)):
		return ans2[0], ans2[1]
	elif(d3<=min(d2,d1,d4)):
		return ans3[0], ans3[1]
	elif(d4<=min(d2,d3,d1)):
		return ans4[0], ans4[1]
