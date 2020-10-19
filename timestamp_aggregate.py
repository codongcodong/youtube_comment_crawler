from collections import defaultdict
import sys

filename = sys.argv[1]
infile = open(filename,'r')
outfile = open('%s_aggregated.txt'%filename.split('.')[0],'w')

for i in range(3):
    line = infile.readline()
    outfile.write(line)

aggregated_statistics = defaultdict(int)

while True:
    line = infile.readline()

    if not line: break
    l = line.split(' - ')
    minute_second = l[0].split(':')
    timeVal = int(minute_second[0])*60+int(minute_second[1])

    aggregated_statistics[timeVal//5]+=int(l[1])

k = list(aggregated_statistics.keys())
k.sort()

for val in k:
    left = val*5
    right = (val+1)*5-1

    left_time = "%02d:%02d" % (left // 60, left % 60)
    right_time = "%02d:%02d" % (right // 60, right % 60)

    outfile.write('%s ~ %s: %d'%(left_time,right_time,aggregated_statistics[val])+'\n')

infile.close()
outfile.close()
