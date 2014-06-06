import numpy as np
import time
from datetime import datetime as dt

def main():
	try:
		testname = "data\\outputTestAll.csv"
		histname = "data\\testHistory.csv"
		mat, mat1 = outtest(testname, histname)
		mat = zerorows(mat, mat1)
		mat = meannorm(mat)
		printtest(mat, "data\\outTest-05+05.txt")		
	
	except Exception, e:
		print str(e)
		
def meannorm(mat):	
	for i in range(len(mat[:,0])):
		arr = mat[i,:]
		# print "before", arr
		min = np.amin(arr)
		max = np.amax(arr)
		av = arr.sum()/len(arr)
		if max == 0 and min == 0:
			arr = np.zeros(arr.shape)
		else:
			arr = (arr-av)/(max-min)
		mat[i,:] = arr
		# print "after", arr
	return mat
	
# def meannorm(arr):
	# min = np.amin(arr)
	# max = np.amax(arr)
	# av = arr.sum()/len(arr)
	# if max == 0 and min == 0:
		# arr = 0
	# else:
		# arr = (arr-av)/(max-min)
	# return arr
	
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


def outtest(fname, fname1):
	with open(fname) as f, open(fname1) as f1:
		f.next()
		f1.next()

		mat = np.loadtxt(f, delimiter=',', unpack='true', dtype='float')
		mat1 = np.loadtxt(f1, delimiter=',', unpack='true', dtype='str')
		
		#print len(mat)		
		return mat, mat1
		
def zerorows(mat, mat_test):
	fname_test = "data\\testHistory.csv"
	fname_off = "data\\offers.csv"
	with open(fname_off) as f:
		f.next()

		mat_off = np.loadtxt(f, delimiter=',', unpack='true', dtype='int')
		
		unique_category = np.unique(mat_off[1,:])
		# print "category", len(unique_category)
		unique_company = np.unique(mat_off[3,:])
		# print "company", len(unique_company)
		unique_brand = np.unique(mat_off[5,:])
		# print "brand", len(unique_brand)
		
		#print "len offer file", len(mat_off)
		for i in range(len(mat[0,:])):
			idx = np.where(mat_off[0,:]==mat[3,i])
			category = mat_off[1,idx]
			company = mat_off[3,idx]
			brand = mat_off[5,idx]
			
			date = mat_test[4,i]
			# print "date", date
			
			month, weekday = dat(date)
			
			# category
			# mat = zerocategory(mat, unique_category, cat, i)
			mat = zero(mat, unique_category, category, 11, 71, i)
			
			# company
			# mat = zerocompany(mat, unique_company, comp, i)
			mat = zero(mat, unique_company, company, 71, 125, i)
			
			# brand
			mat = zero(mat, unique_brand, brand, 125, 182, i)
			
			# month
			mat = zero(mat, np.arange(1,13), month, 182, 218, i)
			
			# weekday
			mat = zero(mat, np.arange(1,8), weekday, 218, 239, i)
			
	return mat

def dat(date):
	d = dt.strptime(date, '%Y-%m-%d').date()
	month = d.month
	weekday = d.isoweekday()	
	return month, weekday
	
def zero(mat, unique, feature, idx1, idx2, i):
	idxcat = np.where(unique==int(feature))
	tmat = np.reshape(mat[idx1:idx2,i],(-1,3))
	# print tmat, type(unique), unique, type(feature), feature, idxcat
	tarr = tmat[idxcat,:]
	tmat = np.zeros(tmat.shape)
	tmat[idxcat,:] = tarr
	# print mat
	mat[idx1:idx2,i] = np.reshape(tmat,idx2-idx1)
	# print idx1, idx2, idxcat, tarr
	# print "iter", i, idxcat, tmat, tmat[idxcat[1],:], tarr
	return mat

start_time = time.time()
main()
print time.time() - start_time, "seconds"