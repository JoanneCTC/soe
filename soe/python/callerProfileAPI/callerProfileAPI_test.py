import os, json, string, datetime, logging, time, csv, collections,urllib,urllib2, ast, pymssql, pyodbc, requests

#--------- READ FROM DB -------------
def readProfiles2():
    #conn = pymssql.connect(server='10.11.0.101,1433', user='sa', password='sdbP@ssw0rd', database='watsondb')  
    #cursor = conn.cursor()  
    #cursor.execute('select * from customer_profile')  
    #row = cursor.fetchone()  
    
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.11.0.101,1433;DATABASE=watsondb;UID=sa;PWD=sdbP@ssw0rd')
    cursor = cnxn.cursor()
    cursor.execute("select * from customer_profile")
    rows = cursor.fetchall()
    profiles = []
    for row in rows:
        #print row.Firstname
        json = {
            'Firstname':row.Firstname,
            'passcode':row.passcode,
            'checking':row.checking,
            'savings':row.savings,
            'moneymarket':row.moneymarket,
            'autoloan':row.autoloan,
            'studentloan':row.studentloan,
            'mortgage':row.mortgage,
            'autopayment':row.autopayment,
            'studentpayment':row.studentpayment,
            'mortgagepayment':row.mortgagepayment}
        profiles.append(json)
    return profiles       

#print("========== FROM DB ===============")
#testprofile = readProfiles2()
#for row in testprofile:
#    if row['Firstname'] == 'Brian':
#        print(row)

#------- READ FROM EXCEL ------------
def readProfiles1():
	with open(os.path.join('callerProfile.csv'), 'rb') as csvfile:
		csvprofiles = csv.DictReader(csvfile)
		profiles = []
		for row in csvprofiles:
			#print(row)
			profiles.append(row)	
		csvfile.close()
		return profiles
		
	csvfile.close()
	return None

#print("***********JSON FROM CSV *************")
#profile = readProfiles1()
#for row in profile:
#       if row['Firstname'] == 'Brian':
#                print(row) 

#-------- READ FROM API for python 3 -------------
#def readProfiles():
#         data =  urllib.urlopen("http://10.11.0.101/php/watson/api.php")
#            data = json.loads(url.read().decode())
#                profiles = []
#                for row in data:
#                        newrow = collections.OrderedDict(row)
#                        profiles.append(newrow)
#                return profiles
            


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


#    -------- READ FROM API for python 2 , v1-------------
def readProfiles111():
          data = urllib2.urlopen("http://10.11.0.101/php/watson/api.php")
          response = json.load(data)
          #return response
          profile = []
          for row in response:
              #newrow = json.dumps(row,default=set_default)
              #newrow = json.dumps(row)
              #newrow = newrow.replace('"', "'")
              newrow = ast.literal_eval(json.dumps(row))
              #print newrow
              profile.append(newrow)
          return profile
          

             
#print("***********JSON FROM URL *************")
#ppprofile = readProfiles111()
#for row in ppprofile:
#   if row['Firstname'] == 'Peter':
#       print(row)

def readProfilesttt():
    m = {'studentloan': '1000.00', 'mortgage': '10.00', 'Firstname': 'Peter', 'autoloan': '100.00', 'checking': '50000.00', 'savings': '60000000.00', 'studentpayment': '10.00', 'moneymarket': '30000.00', 'passcode': 'swimming', 'autopayment': '10.00', 'mortgagepayment': '10.00'}
    return m

#a = readProfiles()
#print(a['Firstname'])

def readProfilesExample():
    url = 'http://10.11.0.101/php/watson/api.php'
    r = requests.get(url,headers={'content-type':'application/json'})
    if r.status_code == 200:
        msg = r.json()
        return msg

print("***********JSON FROM Request GET Example *************")
ppprofile = readProfilesExample()
for row in ppprofile:
       print(row)
            

def writeProfiles(profiles):
	with open(os.path.join(APP_PROFILE_API, file_name), 'w') as csvfile:
		fieldnames = ['Firstname', 'passcode','checking','savings','moneymarket','autoloan','studentloan','mortgage','autopayment','studentpayment','mortgagepayment']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for row in profiles:
			writer.writerow(row)
		csvfile.close()

def getProfileByName(name):
	profiles = readProfiles()
	profile = findProfileByFirstName(profiles, name)
	return profile
	
def updateProfile(profile):
	profiles = readProfiles()
	for ix, row in enumerate(profiles):
		if row['Firstname'] == profile['Firstname']:
			profiles[ix] = profile
	writeProfiles(profiles)

def findProfileByFirstName(profiles, firstname):
	for row in profiles:
		if row['Firstname'] == firstname:
			return row
	return None	
	
def findAttrInProfile(profile,attr):
	if attr in profile:
		return profile[attr]
	return None
		
def getAccountBalance(profile, account):
	if findAttrInProfile(profile,account) and findAttrInProfile(profile,account) != '0':
		return int(findAttrInProfile(profile,account))
	else:
		return 0

def getLoanBalance(profile, loan):
	if findAttrInProfile(profile,loan) and findAttrInProfile(profile,loan) != '0':
		return int(findAttrInProfile(profile,loan))
	else:
		return 0

def hasLoanType(profile, loan):
	if findAttrInProfile(profile,loan) and findAttrInProfile(profile,loan) != '0':
		return True
	else:
		return False
		
def makePayment(profile, loan, account, amount):
	if hasLoanType(profile,loan) and getLoanBalance(profile,loan) > amount and getAccountBalance(profile,account) > amount:
		decrementAttr(profile,account,amount)
		decrementAttr(profile,loan,amount)	
		return True
	else:
		return False

def decrementAttr(profile,attr,amount):
	profile[attr] = str(int(profile[attr]) - amount)


#print("================ testing getProfileByName ===============")
#test = getProfileByName('Peter')
#print(test)

def runTest():
	print("starting " + logging_comp_name)
	profiles = readProfiles()
	#for row in profiles:
	#	print(row['Firstname'], row['passcode'])

	profile = findProfileByFirstName(profiles, 'Olivia')
	print(profile)
	print("Passcode for Olivia: " + findAttrInProfile(profile,'passcode'))

	loan = 'auto loan'
	account = 'checking'

	print(loan + " balance is " + str(getLoanBalance(profile,loan)))
	print("Your " + account + " balance is " + str(getAccountBalance(profile,account)))

	if hasLoanType(profile,loan):
		print("You have a " + loan + " with a balance.")
		if makePayment(profile,loan,account,550):
			print("Payment Made")
		else:
			print("Payment error")
	print(profile)
	updateProfile(profile)
	profiles = readProfiles()
	for row in profiles:
		print(row)

