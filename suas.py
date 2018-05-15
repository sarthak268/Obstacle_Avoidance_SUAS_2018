import math
from tangent import *
from geotransform import *

safety_distance = 10

waypoint_file = ("./mission.txt")
obstacle_file = ("./obstacle")

waypoint = []
obstacle = []
waypoint_final = []
waypoint_final_ = []

def toM(feet):
	return (0.3048*feet)

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
print ("initial", waypoint)
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
for i in range(len(waypoint)):
	cwp = waypoint[i]
	clong = cwp[0]
	clat = cwp[1]
	cx,cy = translatell2xy(clat,clong)
	waypoint[i] = [cx,cy]
#print ("old : ",waypoint,"\n")

for j in range(len(obstacle)):
	cobs = obstacle[j]
	clong = cobs[0]
	clat = cobs[1]
	cx, cy = translatell2xy(clat, clong)
	crad = toM(cobs[2])
	obstacle[j] = [cx,cy,crad]
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
	#print (waypoint)
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
						a, b = find_point(waypoint[i-1],waypoint[i],r + safety_distance,[obstacle[l][0], obstacle[l][1]])
						##################################################
						intersection = [a,b]
						waypoint_final.append(intersection)
						#print ("naya daala")
				waypoint_final.append(waypoint[i])
	#print (waypoint_final)
	for k in range(len(waypoint_final)):
		cx = waypoint_final[i][0]
		cy = waypoint_final[i][1]
		lat, lng = translatexy2ll(cx,cy)
		waypoint_final_.append([lng,lat])
	print ("final",waypoint_final_)
	
	######################################################################
	final_wp_file = "./new_waypoint.txt"
	file = open(final_wp_file,"w")
	file.write('QGC' + '\t' + 'WPL' + '\t' + '110' + '\n')
	for p in range(len(waypoint_final_)):
		file.write(str(p) + '\t' + str(0) + '\t' + str(0) + '\t' + str(16) + '\t' + str(0) + '\t' + str(0) + '\t' + str(0) + '\t' + str(0) + '\t' + str(waypoint_final_[p][0]) + '\t' + str(waypoint_final_[p][1]) + '\t' + str(550) + '\t' + str(1) + "\n")
	file.close()

##########################################################################
main()



















