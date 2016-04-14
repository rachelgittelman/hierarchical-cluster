'''This script will do clustering of all points within a certain distance of eachother, such that
the distance between groups will always be greater than this distance. However, the distance
between non-consecutive points within the group may end up being larger than the distance threshold.
This script was originally imagined to be a way of lumping together SNPs in LD with eachother,
but can be used more generally.'''

'''
The format for the data file containing distances between points is:
chr	pos1	pos2	N_chr	distance(R^2)

to use this for data besides the vcftools LD output, just think of pos1 and pos2 as the two
points, and R^2 as distance. The other fields don't matter
'''

import sys

data=open(sys.argv[1])
thresh=float(sys.argv[2])

point_dict={}
clustered={}
for line in data:
	if line.startswith("CHR"):
		continue
	fields=line.strip().split()
	p1=int(fields[1])
	p2=int(fields[2])
	if fields[4] == "-nan" or fields[4] == "R^2":
		continue
	dist=float(fields[4])
	if(dist >= thresh):
		try:
			point_dict[p1].add(p2)
		except:
			point_dict[p1] = set()
			point_dict[p1].add(p2)
			clustered[p1]=0
		try:
			point_dict[p2].add(p1)
		except:
			point_dict[p2] = set()
			point_dict[p2].add(p1)
			clustered[p2]=0
	
current_cluster=[]

def find_all_points_in_cluster(point):
	if clustered[point] == 1:
		return
	else:
		current_cluster.append(point)
		clustered[point] = 1
		for partner_point in point_dict[point]:
			find_all_points_in_cluster(partner_point)


def print_cluster(cluster):
	if len(cluster) < 4:
		return
	cluster.sort()
	for point in cluster:
		print str(point)+"\t"+str(cluster[0]-1)+"_"+str(cluster[-1])

first=True
for point in point_dict:
	if clustered[point] == 1:
		continue
	else:
		if first == True:
			first = False
		else: 
			print_cluster(current_cluster)
			current_cluster=[]
		find_all_points_in_cluster(point)
print_cluster(current_cluster)