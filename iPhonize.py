import os
from enum import Enum, auto

class Status(Enum):
	NONE = auto()
	NAME = auto()
	DISPLAYNAME = auto()
	NICKNAME = auto()
	UID = auto()
	EMAIL = auto()
	URL = auto()
	ADDRESS = auto()
	CUSTOM1 = auto()
	CUSTOM2 = auto()
	CUSTOM3 = auto()
	CUSTOM4 = auto()
	TEL = auto()
	TIMEZONE = auto()
	BIRTHDAY = auto()
	ANNIVERSARY = auto()
	NOTE = auto()
	TITLE = auto()
	ROLE = auto()
	DEPARTMENT = auto()
	ORGNAME = auto()
	INSTANTMESSAGING = auto()

class Contact:
	def __init__(self):
		self.name=""
		self.displayname=""
		self.nickname=""
		self.uid=""
		
		#Handling emails
		self.emailtypes=[]
		self.emailaddr=[]
		self.email_index=0
		
		#Handling URLs
		self.urltype=[]
		self.urladdr=[]
		self.url_index=0
		
		#Handling addresses
		self.addrtype=[]
		self.address=[]
		self.addr_index=0
		
		#Custom fields
		self.custom1=""
		self.custom2=""
		self.custom3=""
		self.custom4=""
		
		#Handling telephone
		self.teltype=[]
		self.tel=[]
		
		self.timezone=""
		
		self.birthday=""
		self.anniversary=[]
		
		self.note=""
		
		#Organization property
		self.title=""
		self.role=""
		self.org_name=""
		self.department=""
		
		#Instant messaging
		self.im=[]
		
		#Last attribute Acquired
		self.LastAttrAcq=Status.NONE
		
	def parse(self,line):
		#Parse the content of the line
		if line[0:2]=="N:":
			self.name=line
			self.LastAttrAcq=Status.NAME
				
		if line[0:3]=="FN:":
			self.displayname=line
			self.LastAttrAcq=Status.DISPLAYNAME
				
		if line[0:9]=="NICKNAME:":
			self.nickname=line
			self.LastAttrAcq=Status.NICKNAME
			
		if line[0:4]=="UID:":
			self.uid=line
			self.LastAttrAcq=Status.UID
	
	def print_data(self):
		print("Name line => "+self.name)
		print("Displayname line => "+self.displayname)
		print("Nickname line => "+self.nickname)
		print("UID line => "+self.uid)
			
			
			
			
			
			
			
			# if line[0:4]=="ORG:":
				# org=riga
				# prosegui=4
				
			# if line[0:5]=="ROLE:":
				# ruolo=riga
				# prosegui=5
			
			# if line[0:6]=="TITLE:":
				# titolo=riga
				# prosegui=6
			
			# if line[0:5]=="NOTE:":
				# note=riga
				# prosegui=7
			
			# if line[0:10]"X-CUSTOM1:":
				# pers1=riga
				# prosegui=8
			
			# if line[0:10]"X-CUSTOM2:":
				# pers2=riga
				# prosegui=9
			
			# if line[0:10]=="X-CUSTOM3:":
				# pers3=riga
				# prosegui=10
			
			# if line[0:10]=="X-CUSTOM4:":
				# pers4=riga
				# prosegui=11
			
			# if line[0:4]=="TEL:":
				# tel.append(riga)
				# prosegui=12
				
			# if line[0:4]=="ADR:":
				# addr.append(riga)
				# prosegui=13
					
			# if line[0:4]=="URL:":
				# web.append(riga)
				# prosegui=14
			
			# if line[0:6]=="EMAIL:":
				# email.append(riga)
				# prosegui=15
				
			
				
			# if line[0:5]==BDAY:":
				# bday=riga
				# prosegui=17
				
			# if line[0:12]=="ANNIVERSARY:":
				# anniv=riga
				# prosegui=18
				
		
#Main
collectedcontacts=[]	#Contact collected in the current file

#Path where original *.vcf are stored
path="."
#Extract the list of all files in current directory
file_list=os.listdir(path)

# for each .vcf file the "iphonize" procedure will be performed
for k in file_list:
	if k[-4:]!=".vcf":
		continue		#If current file isn't a *.vcf file skip to next item
	else:
		#Create a contact
		C=Contact()
		
		source=open(path+"\\"+k,"r")
		dest=open(path+"\\"+k[:-4]+" - iphonize.vcf","w")
		
		#Read lines and fill the instance members
		line=source.readline()
		while line != "":
			#Parse only valid data
			if line != "END:VCARD\n" and line != "BEGIN:VCARD\n" and line[0:8] != "VERSION:":
				C.parse(line)
			
			#A contact was finished to be acquired
			if line == "END:VCARD\n":
				#C.print_data()
				collectedcontacts.append(C)
				C=Contact()	#Create new contact object
				
			#sample new line
			line=source.readline()
		
		#Now all contacts in the current file were acquired. Print some infos
		print("Found "+str(len(collectedcontacts))+" contact in file '"+k+"'")
			
		#Reset contacts
		collectedcontacts=[]
		
		
		
		
		
		
		