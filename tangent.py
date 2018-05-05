import math

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
	a1 = (p*q - r*math.sqrt(p**2 + q**2 - r**2)) / r**2 - p**2
	b1 = 1
	c1 = -y0 + (((p + x0)*(-p*q + r*math.sqrt(p**2 + q**2 - r**2))) / r**2 - p**2) - q
	
	a2 = (a*b + r*math.sqrt(a**2 + b**2 - r**2)) / r**2 - a**2
	b2 = 1
	c2 = -y0 + (((a + x0)*(-a*b - r*math.sqrt(a**2 + b**2 - r**2))) / r**2 - a**2) - b

	sol_x_1 = (c1*b2 - c2*b1) / (a1*b2 - a2*b1)
	sol_y_1 = (c2*a1 - c1*a2) / (a1*b2 - a2*b1)


	# solution 2
	a1_ = (p*q + r*math.sqrt(p**2 + q**2 - r**2)) / r**2 - p**2
	b1_ = 1
	c1_ = -y0 + (((p + x0)*(-p*q - r*math.sqrt(p**2 + q**2 - r**2))) / r**2 - p**2) - q
	
	a2_ = (a*b - r*math.sqrt(a**2 + b**2 - r**2)) / r**2 - a**2
	b2_ = 1
	c2_ = -y0 + (((a + x0)*(-a*b + r*math.sqrt(a**2 + b**2 - r**2))) / r**2 - a**2) - b

	sol_x_2 = (c1_*b2_ - c2_*b1_) / (a1_*b2_ - a2_*b1_)
	sol_y_2 = (c2_*a1_ - c1_*a2_) / (a1_*b2_ - a2_*b1_)

	dist_1 = distance(sol_x_1,sol_y_1,p,q)
	dist_2 = distance(sol_x_2,sol_y_2,p,q)

	if (dist_1 < dist_2):
		return sol_x_1, sol_y_1
	else :
		return sol_x_2, sol_y_2