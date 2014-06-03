import numpy as np
import time
from datetime import datetime as dt

#fname_tr = "data\\reduced_category_s.csv"
#fname_train = "data\\trainHistory_s.csv"
#fname_tr = "data\\reduced_category.csv"
fname_train = "data\\trainHistory.csv"
fname_tr = "data\\transactions.csv"
fname_off = "data\\offers.csv"
fname_out = "data\\outputTrainAll.csv"

def main():
	try:		
		with open(fname_train) as f1:
			id_tr,chain_tr,offer_tr,market_tr,repeattrips_tr,repeater_tr,offerdate_tr = np.loadtxt(fname_train, delimiter=',', unpack='true', dtype='str')
		print "len train file", len(offer_tr)
			
		with open(fname_off) as f2:
			offer_off,category_off,quantity_off,company_off,offervalue_off,brand_off = np.loadtxt(fname_off, delimiter=',', unpack='true', dtype='str')
		print "len offer file", len(offer_off)
		
		unique_category = np.unique(category_off[1:len(category_off)])
		unique_company = np.unique(company_off[1:len(company_off)])
		unique_brand = np.unique(brand_off[1:len(brand_off)])
		#print len(company_off), len(unique_company), unique_company


		with open(fname_tr) as f:
			f.next()
			fo = open(fname_out, 'w')
			saveLine = 'id'+','+'repeater'+','+'chain'+','+'offer'+','+'market'+','+'repid'+','+'sumid'+','+'avid'+','+'repchain'+','+'sumchain'+','+'avchain'
			for i in range(1,len(unique_category)+1):
				saveLine = saveLine+','+'repcategory'+str(i)+','+'sumcategory'+str(i)+','+'avcategory'+str(i)
			for i in range(1, len(unique_company)+1):
				saveLine = saveLine+','+'repcompany'+str(i)+','+'sumcompany'+str(i)+','+'avcompany'+str(i)
			for i in range(1,len(unique_brand)+1):
				saveLine = saveLine+','+'repbrand'+str(i)+','+'sumbrand'+str(i)+','+'avbrand'+str(i)
			for i in range(1,13):
				saveLine = saveLine+','+'repmonth'+str(i)+','+'summonth'+str(i)+','+'avmonth'+str(i)
			for i in range(1,8):
				saveLine = saveLine+','+'repweekday'+str(i)+','+'sumweekday'+str(i)+','+'avweekday'+str(i)
			saveLine = saveLine +'\n'
			fo.write(saveLine)
			x=1
			b=set()
			mat = []
			print "id", id_tr
			for idx, line in enumerate(f):
				id,chain,dept,category,company,brand,date,productsize,productmeasure,purchasequantity,purchaseamount = line.split(',')
				#print id_tr[1]
				if idx == 0:
					tmp = id
				if id == tmp:
					b.add(line)
					datt = dat(date)
					appe(mat,id,chain,dept,category,company,brand,datt,productsize,purchasequantity,purchaseamount)
				if id != tmp:
					if tmp == id_tr[x]:
						if x%1000 == 0:
							print "id=", tmp, "count=",len(b), "#train", x
						
						matt = np.array(mat)
						
						if repeater_tr[x] == 'f':
							rep = '0'
						else:
							rep = '1'
						#print rep

						#repid, sumid, avid
						repid = len(mat[:])
						sumid = sum(matt[:,10])
						avid = sumid/repid
						#print repid, sumid, avid
						
						#repchain, sumchain, avchain
						repchain = np.asscalar((matt[:,1]==int(chain_tr[x])).sum())		
						idxs = np.where(matt[:,1]==int(chain_tr[x]))
						sumchain = matt[idxs,10].sum()
						avchain = av(sumchain,repchain)
						#print repchain, sumchain, avchain
						
						#repcategory, sumcategory, avcategory
						repcategory, sumcategory, avcategory = retarr(matt, unique_category, 3)
									
						#repcompany, sumcompany, avcompany
						repcompany, sumcompany, avcompany = retarr(matt, unique_company, 4)
						
						#repbrand, sumbrand, avbrand
						repbrand, sumbrand, avbrand = retarr(matt, unique_brand, 5)
							
						#date: moth and weekday
						datt = dat(str(offerdate_tr[x]))
						
						#repmonth, summonth, avmonth: datt[0] - month
						repmonth, summonth, avmonth = retarr(matt, range(1,13), 6)
						
						#repweekday, sumweekday, avweekday: datt[1] - weekday
						repweekday, sumweekday, avweekday = retarr(matt, range(1,8), 7)
						
						#npline = [chain_tr[x],offer_tr[x],market_tr[x],repid,sumid,avid,repchain,sumchain,avchain]
						#npline = np.array(npline)
						#print type(npline)
												
						saveLine = tmp+','+rep+','+chain_tr[x]+','+offer_tr[x]+','+market_tr[x]+','+"%d"%repid+','+"%.6f"%sumid+','+"%.6f"%avid+','+"%d"%repchain+','+"%.6f"%sumchain+','+"%.6f"%avchain
						for i in range(0,len(unique_category)):
							saveLine = saveLine+','+"%d"%repcategory[i]+','+"%.6f"%sumcategory[i]+','+"%.6f"%avcategory[i]
						for i in range(0, len(unique_company)):
							saveLine = saveLine+','+"%d"%repcompany[i]+','+"%.6f"%sumcompany[i]+','+"%.6f"%avcompany[i]
						for i in range(0,len(unique_brand)):
							saveLine = saveLine+','+"%d"%repbrand[i]+','+"%.6f"%sumbrand[i]+','+"%.6f"%avbrand[i]
						for i in range(0,12):
							saveLine = saveLine + ','+ "%d"%repmonth[i]+','+"%.6f"%summonth[i]+','+"%.6f"%avmonth[i]
						for i in range(0,7):
							saveLine = saveLine + ','+ "%d"%repweekday[i]+','+"%.6f"%sumweekday[i]+','+"%.6f"%avweekday[i]
						saveLine = saveLine + '\n'
						npline = saveLine.split(',')
						npline = np.array(npline)
						'''sLine = rep
						for i, elem in enumerate(npline[2:len(npline)]):
							#print type(elem)
							if float(elem) != 0:
								sLine = sLine + ' ' +str(i+1)+':'+elem
						#print sLine
						sLine = sLine + '\n'
						fo.write(sLine)'''
						fo.write(saveLine)
						x+=1
						#raw_input("Press Enter to continue...")
					del b 
					b = set()
					b.add(line)
					del mat
					mat = []
					datt = dat(date)
					appe(mat,id,chain,dept,category,company,brand,datt,productsize,purchasequantity,purchaseamount)
					tmp = id
				if x == len(id_tr):
					break
				if idx%500000 == 0 and idx !=0:
					print idx/1000000., time.time() - start_time
				
			fo.close()
			#print len(b)
	except Exception, e:
		print str(e)

def appe(mat,id,chain,dept,category,company,brand,datt,productsize,purchasequantity,purchaseamount):
	arr = [int(id),int(chain),int(dept),int(category),int(company),int(brand),datt[0],datt[1],float(productsize),int(purchasequantity),float(purchaseamount)]
	mat.append(arr)
	return mat

def dat(date):
	d = dt.strptime(date, '%Y-%m-%d').date()
	month = d.month
	weekday = d.isoweekday()	
	return month, weekday

def av(sum,rep):
	if rep == 0:
		av = 0
	else:
		av = sum/rep
	return av

def retarr(matt, arr, number_col):
	reparr={}
	sumarr={}
	avarr={}
	for i in range(0, len(arr)):
		reparr[i] = (matt[:,number_col]==int(arr[i])).sum()				
		idxs = np.where(matt[:,number_col]==int(arr[i]))
		sumarr[i] = matt[idxs,10].sum()
		avarr[i] = av(sumarr[i],reparr[i])
	return reparr, sumarr, avarr


start_time = time.time()	
main()
print time.time() - start_time, "seconds"	
