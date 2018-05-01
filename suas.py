import math

safety_distance = 2.5

waypoint_file = ("/Users/sarthakbhagat/Desktop/suas/waypoint.txt")
obstacle_file = ("/Users/sarthakbhagat/Desktop/suas/obstacle.txt")

waypoint = []
obstacle = []
waypoint_final = []

with open(waypoint_file) as wf:  
   line = wf.readline()
   waypoint.append(line.split(" "))
   while line:
       line = wf.readline()
       waypoint.append(line.split(" "))

waypoint = waypoint[0:len(waypoint)-1]
waypoint[0][1] = waypoint[0][1][:-2]

for i in range(len(waypoint)):
	waypoint[i] = waypoint[i][0:2]

with open(obstacle_file) as of:  
   line = of.readline()
   obstacle.append(line.split(" "))
   while line:
       line = of.readline()
       obstacle.append(line.split(" "))

obstacle = obstacle[0:len(obstacle)-1]

for i in range(len(obstacle)-1):
	obstacle[i] = obstacle[i][0:3]
	obstacle[i][2] = obstacle[i][2][:-1]

#print ("waypoint = ", waypoint)
#print ("obstacle = ",obstacle)


########################################################################
def convert(arr):
	for m in range(len(arr)):
		for n in range(len(arr[0])):
			arr[m][n] = float(arr[m][n])
convert(waypoint)
convert(obstacle)

########################################################################
# change to x-y coordinate system
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
			print ("sabse pehla daala")
		else:
			safe = True
			for j in range(len(obstacle)):
				d = distance(waypoint[i-1],waypoint[i],obstacle[j][:-1])
				r = obstacle[j][2]
				if (d < r + safety_distance):
					safe = False
					print ("thukka")
					break
			if (safe):
				waypoint_final.append(waypoint[i])
				print ("safe tha")
			else:
				for l in range(len(obstacle)):
					d = distance(waypoint[i-1],waypoint[i],obstacle[l][:-1])
					r = obstacle[l][2]
					if (d < r + safety_distance):
						a = 10
						b = 10
						intersection = [a,b]
						waypoint_final.append(intersection)
						print ("naya daala")
				waypoint_final.append(waypoint[i])
		print (waypoint_final)
##########################################################################

def write():
	final_wp_file = "/Users/sarthakbhagat/Desktop/suas/new_waypoint.txt"
	file = open(final_wp_file,"w")
	for p in range(len(waypoint_final)):
		file.write(str(waypoint_final[p][0]) + " " + str(waypoint_final[p][1]) + "\n")

main()
write()				


















