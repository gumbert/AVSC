import numpy as np
import time

def main():
	try:
		testname = "data\\outputTestAll_v9.csv"
		mat = outtest(testname)
		mat = zerorows(mat)
		printtest(mat, "data\\outTest-05+05.txt")		
	
	except Exception, e:
		print str(e)
		
def meannorm(arr):
	min = np.amin(arr)
	max = np.amax(arr)
	av = arr.sum()/len(arr)
	if max == 0 and min == 0:
		arr = 0
	else:
		arr = (arr-av)/(max-min)
	return arr
	
def printtest(mat, fileout):
	fo = open(fileout, 'w')
	#print len(mat[0,:]), mat[25,1]
	for i in range(len(mat[0,:])):
		saveLine = "%.0f"%mat[1,i]
		for j in range(2, len(mat[:,0])):
			saveLine = saveLine + ' '+str(j-1)+':'+"%.6f"%mat[j,i]
		saveLine = saveLine + '\n'
		fo.write(saveLine)
	fo.close()


def outtest(fname):
	with open(fname) as f:
		f.next()
		#id,chain,offer,market,repid,sumid,avid,repchain,sumchain,avchain,repcategory,sumcategory,avcategory,repcompany,sumcompany,avcompany,repbrand,sumbrand,avbrand,month,repmonth,summonth,avmonth,weekday,repweekday,sumweekday,avweekday = np.loadtxt(f, delimiter=',', unpack='true', dtype='float')

		mat = np.loadtxt(f, delimiter=',', unpack='true', dtype='float')
		#print len(mat)
			
		#for i in range(2, len(mat[:,0])):
		#	mat[i,:] = meannorm(mat[i,:])
		#print mat
		return mat
		
def zerorows(mat):
	fname_off = "data\\offers.csv"
	with open(fname_off) as f:
		f.next()
		mat_off = np.loadtxt(f, delimiter=',', unpack='true', dtype='int')
		
		unique_category = np.unique(mat_off[1,:])
		print "category", len(unique_category)
		unique_company = np.unique(mat_off[3,:])
		unique_brand = np.unique(mat_off[5,:])
		
		#print "len offer file", len(mat_off)
		for i in range(len(mat[0,:])):
			idx = np.where(mat_off[0,:]==mat[3,i])
			cat = mat_off[1,idx]
			comp = mat_off[3,idx]
			brand = mat_off[5,idx]
			
			# category
			idxcat = np.where(unique_category==cat)
			idx1 = 11
			idx2 = (len(unique_category))*3+idx1
			tmat = np.reshape(mat[idx1:idx2,i],(-1,3))
			# print tmat
			tarr = tmat[idxcat[1],:]
			tmat = np.zeros(tmat.shape)
			tmat[idxcat[1],:] = tarr
			# print mat
			mat[idx1:idx2,i] = np.reshape(tmat,idx2-idx1)
			print idx1, idx2, idxcat[1], tarr
			# print "iter", i, idxcat, tmat, tmat[idxcat[1],:], tarr
				
	return mat


start_time = time.time()
main()
print time.time() - start_time, "seconds"