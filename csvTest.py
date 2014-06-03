import numpy as np
import time

def main():
	try:
		testname = "data\\outputTestAll.csv"
		mat = outtrain(testname)
		printtest(mat, "data\\outTest-05+05.txt")		
	
	except Exception, e:
		print str(e)
		
def meannorm(arr):
	min = np.amin(arr)
	max = np.amax(arr)
	av = arr.sum()/len(arr)
	arr = (arr-av)/(max-min)
	return arr
	
def printtest(mat, fileout):
	fo = open(fileout, 'w')
	print len(mat[0,:]), mat[25,1]
	for i in range(len(mat[0,:])):
		saveLine = "%.0f"%mat[1,i]
		for j in range(2, len(mat[:,0])):
			saveLine = saveLine + ' '+str(j-1)+':'+"%.6f"%mat[j,i]
		saveLine = saveLine + '\n'
		fo.write(saveLine)
	fo.close()


def outtrain(fname):
	with open(fname) as f:
		f.next()
		#id,chain,offer,market,repid,sumid,avid,repchain,sumchain,avchain,repcategory,sumcategory,avcategory,repcompany,sumcompany,avcompany,repbrand,sumbrand,avbrand,month,repmonth,summonth,avmonth,weekday,repweekday,sumweekday,avweekday = np.loadtxt(f, delimiter=',', unpack='true', dtype='float')

		mat = np.loadtxt(f, delimiter=',', unpack='true', dtype='float')
			
		for i in range(2, len(mat[:,0])):
			mat[i,:] = meannorm(mat[i,:])
		#print mat
		return mat

start_time = time.time()
main()
print time.time() - start_time, "seconds"