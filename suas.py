import math
from tangent import *

safety_distance = 2.5

waypoint_file = ("./2016-06-17 17-14-00-0.waypoints")
obstacle_file = ("./obstacle.txt")

waypoint = []
obstacle = []
waypoint_final = []
waypoint_final_ = []

def read_waypoint(waypoint_file):
	waypoint_ = []
	wp = []
	with open(waypoint_file) as wf:
		line = wf.readline()
		waypoint_.append(line.split(" "))
		while line:
			line = wf.readline()
			waypoint_.append(line.split(" "))
	wp = waypoint_[3:]
	for hi in range(len(wp)):
		wp[hi][0] = wp[hi][0].split('\t')
	wp = wp[:-1]
	for hello in range(len(wp)):
		longi = wp[hello][0][8]
		lati = wp[hello][0][9]
		waypoint.append([longi,lati])

def read_obstacle(obstacle_file):
	obstacle_ = []
	ob = []
	with open(obstacle_file) as of:
		line = of.readline()
		obstacle_.append(line.split(" "))
		while line:
			line = of.readline()
			obstacle_.append(line.split(" "))
	ob = obstacle_[2:]
	for hi in range(len(ob)):
		ob[hi][0] = ob[hi][0].split('\t')
	ob = ob[:-1]
	for hello in range(len(ob)):
		longi = ob[hello][0][8]
		lati = ob[hello][0][9]
		rad = ob[hello][0][10]
		obstacle.append([longi,lati,rad])

read_waypoint(waypoint_file)
#print ("waypoint = ", waypoint)
read_obstacle(obstacle_file)
#print ("obstacle = ",obstacle)


########################################################################
def convert(arr):
	for m in range(len(arr)):
		for n in range(len(arr[0])):
			arr[m][n] = float(arr[m][n])
convert(waypoint)
convert(obstacle)

########################################################################
#change to x-y coordinate system
ref_long = waypoint[0][0]
ref_lat = waypoint[0][1]

def toXY_waypoint(arr):
	longi = arr[0]
	lat = arr[1]
	x = (longi - ref_long) * (40075000 / 2*math.pi) * math.cos(ref_lat)
	y = (lat - ref_lat) * (4007000 / 2*math.pi)
	return [x,y]

def toXY_obstacle(arr):
	longi = arr[0]
	lat = arr[1]
	r_ = arr[2]
	x = (longi - ref_long) * (40075000 / 2*math.pi) * math.cos(ref_lat)
	y = (lat - ref_lat) * (4007000 / 2*math.pi)
	r = 0.3048 * r_
	return [x,y,r]

def toGPS(arr):
	arrr = []
	for o in range(len(arr)):
		xn = arr[o][0]
		yn = arr[o][1]
		longi = (xn / math.cos(ref_lat)*(40075000.0 / (2.0 * math.pi))) + ref_long
		lati = (yn / (40007000.0 / (2.0 * math.pi))) + ref_lat
		arrr.append([longi,lati])
	return arrr

for k1 in range(len(waypoint)):
	waypoint[k1] = toXY_waypoint(waypoint[k1])

for k2 in range(len(obstacle)):
	obstacle[k2] = toXY_obstacle(obstacle[k2])

#print ("waypoint",waypoint)
#print ("obstacle",obstacle)
########################################################################

# obstacle avoidance
def distance(p1,p2,co):
	x1 = p1[0]
	y1 = p1[1]
	x2 = p2[0]
	y2 = p2[1]
	x0 = co[0]
	y0 = co[1]
	num = abs((y0 - y1)*(x2 - x1) - (x0 - x1)*(y2 - y1))
	den = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
	return (num/den)

def main():
	for i in range(len(waypoint)):
		if (i == 0):
			waypoint_final.append(waypoint[i])
			#print ("sabse pehla daala")
		else:
			safe = True
			for j in range(len(obstacle)):
				d = distance(waypoint[i-1],waypoint[i],obstacle[j][:-1])
				r = obstacle[j][2]
				if (d < r + safety_distance):
					safe = False
					#print ("thukka")
					break
			if (safe):
				waypoint_final.append(waypoint[i])
				#print ("safe tha")
			else:
				for l in range(len(obstacle)):
					d = distance(waypoint[i-1],waypoint[i],obstacle[l][:-1])
					r = obstacle[l][2]
					if (d < r + safety_distance):
						##################################################
						# finding the point to be added to waypoint file 
						# using intersection of two tangents from both the 
						# waypoints.
						a, b = find_point(waypoint[i-1],waypoint[i],r,[obstacle[l][0], obstacle[l][1]])
						##################################################
						intersection = [a,b]
						waypoint_final.append(intersection)
						#print ("naya daala")
				waypoint_final.append(waypoint[i])
	waypoint_final_ = toGPS(waypoint_final)
	#print (waypoint_final_)
##########################################################################

def write():
	final_wp_file = "./new_waypoint.txt"
	file = open(final_wp_file,"w")
	for p in range(len(waypoint_final_)):
		file.write(str(waypoint_final_[p][0]) + " " + str(waypoint_final_[p][1]) + "\n")

main()
write()				


















