import os
import country_code_3166
from enum import Enum, auto

#TODO LIST
#handle fields on multiple lines
#Handle nation in address fields correctly
#check the correctness of pref field for every field		  

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
	ORG = auto()
	INSTANTMESSAGING = auto()

class Contact:
	def __init__(self):
		self.name=""
		self.displayname=""
		self.nickname=""
		self.uid=""
		
		#Handling emails
		self.emailtype=[]
		self.emailaddr=[]
		self.prefemail = 0
		
		#Handling URLs
		self.urltype=[]
		self.urladdr=[]
				
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
		
		self.birthday={}
		self.anniversary=[]
		
		self.note=""
		
		#Organization property
		self.title=""
		self.role=""
		self.org=""
		
		#Instant messaging
		self.im=[]
		
		#Last attribute Acquired
		self.LastAttrAcq=Status.NONE
		
	def _parse_date(self,line,dict):
		#This function allow to parse a date and split it in a dictionary with 3 entries
		#day, month, year. This function parse the line after colon character
		#
		#	A	M	G	Layout
		#	0	0	0	<no field>
		#	0	0	1	---XX				<= day
		#	0	1	0	--XX				<= month
		#	0	1	1	--XXXX				<= month,day
		#	1	0	0	XXXX				<= year
		#	1	0	1	<not allowed
		#	1	1	0	XXXX-XX				<= year,month 
		#	1	1	1	XXXXXXXX			<= year,month,day
		#Note:months and days have always two digits, year has always 4 digits
	
		#Index when the value of date field start
		base_index = line.find(":")
		
		if line.count("-")==0:
			#complete date or year only date
			if len(line[base_index+1:])==8+1:	#+1 is the new line character
				#complete date
				dict["year"]=line[base_index+1:base_index+5]
				dict["month"]=line[base_index+5:base_index+7]
				dict["day"]=line[base_index+7:base_index+9]
			
			if len(line[base_index+1:])==4+1:	#+1 is the new line character
				#year only date
				dict["year"]=line[base_index+1:base_index+5]
				dict["month"]=""
				dict["day"]=""
							
		if line.count("-")==1:
			#year,month date
			dict["year"]=line[base_index+1:base_index+5]
			dict["month"]=line[base_index+6:base_index+8]
			dict["day"]=""
			
		if line.count("-")==2:
			#month only or month,day date
			dict["year"]=""
			
			if len(line[base_index+1:])==4+1:	#+1 is the new line character
				#month only date
				dict["month"]=line[base_index+3:base_index+5]
				dict["day"]=""
				
			if len(line[base_index+1:])==6+1:	#+1 is the new line character
				#month,day date
				dict["month"]=line[base_index+3:base_index+5]
				dict["day"]=line[base_index+5:base_index+7]
			
		if line.count("-")==3:
			#day only date
			dict["year"]=""
			dict["month"]=""
			dict["day"]=line[base_index+4:base_index+6]	
		
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
			
		if line[0:4]=="ORG:":
			self.org=line
			self.LastAttrAcq=Status.ORG
		
		if line[0:5]=="ROLE:":
			self.role=line
			self.LastAttrAcq=Status.ROLE
		
		if line[0:6]=="TITLE:":
			self.title=line
			self.LastAttrAcq=Status.TITLE
						
		if line[0:5]=="NOTE:":
			self.note=line
			self.LastAttrAcq=Status.NOTE
			
		if line[0:10]=="X-CUSTOM1;":
			self.custom1=line	
			self.LastAttrAcq=Status.CUSTOM1
			
		if line[0:10]=="X-CUSTOM2;":
			self.custom2=line	
			self.LastAttrAcq=Status.CUSTOM2	
			
		if line[0:10]=="X-CUSTOM3;":
			self.custom3=line	
			self.LastAttrAcq=Status.CUSTOM3	
			
		if line[0:10]=="X-CUSTOM4;":
			self.custom4=line	
			self.LastAttrAcq=Status.CUSTOM4	
			
		if line[0:2]=="TZ":
			#This file is not handled
			self.timezone=line
			self.LastAttrAcq=Status.CUSTOM4
			
		#Handle telephone fields
		if line[0:3]=="TEL":
			if line[3:15]==";VALUE=TEXT:":
				#There aren't attributes
				self.teltype.append("NOTHING")
				self.tel.append(line[15:])
			else:
				#There is an attribute
				temp=line[9:line.find(";",10,15)]
				self.teltype.append(temp)
				
				#Chatch from the first character AFTER ":"
				temp=line[line.find(":",16)+1:]
				self.tel.append(temp)
			self.LastAttrAcq=Status.TEL

		if line[0:5]=="EMAIL":
			#Check if this is the PREF email
			if line.find("PREF=1")!=-1:
				self.prefemail = len(self.emailaddr)			

			#Check for attribute
			if line.find("TYPE=")!=-1:
				base_index=line.find("TYPE=")+5
				self.emailtype.append(line[base_index:base_index+4])
				self.emailaddr.append(line[line.find(":")+1:])
			else:
				#There aren't other parameters
				self.emailtype.append("NOTHING")
				self.emailaddr.append(line[line.find(":")+1:])
			self.LastAttrAcq=Status.EMAIL
						
		#Parse URL fields
		if line[0:3]=="URL":
			if line[3]==":" :
				#There aren't other attributes
				self.urltype.append("NOTHING")
				self.urladdr.append(line[4:])
			else:
				#There is a parameter
				self.urltype.append(line[line.find(":")-4:line.find(":")])
				self.urladdr.append(line[line.find(":")+1:])
			self.LastAttrAcq=Status.URL
			
		if line[0:11]=="ANNIVERSARY":
			dict={}		#dictionary for year, month and day data
			self._parse_date(line[line.find(":"):],dict)
			self.anniversary.append(dict)
		
		if line[0:4]=="BDAY":
			dict={}		#dictionary for year, month and day data
			self._parse_date(line[line.find(":"):],dict)
			self.birthday=dict
		
		if line[0:3]=="ADR":
			#Check for attribute
			if line.find("TYPE=")!=-1:
				base_index=line.find("TYPE=")+5
				self.addrtype.append(line[base_index:base_index+4])
				self.address.append(line[line.find(":")+1:])
			else:
				#There aren't other parameters
				self.addrtype.append("NOTHING")
				self.address.append(line[line.find(":")+1:])
			self.LastAttrAcq=Status.ADDRESS	
			
		#Field is in more than one line
		if line[0:1]==" ":
			if self.LastAttrAcq==Status.ADDRESS:
				self.address[-1]=self.address[-1][:-1]+line[1:]
						
	def print_data(self):
		print("Name line => "+self.name)
		print("Displayname line => "+self.displayname)
		print("Nickname line => "+self.nickname)
		print("UID line => "+self.uid)
			
		print("ORG line => "+self.org)		
		print("ROLE line => "+self.role)	
		print("TITLE line => "+self.title)	
			
		print("NOTE line => "+self.note)
		print("Custom1 line => "+self.custom1)
		print("Custom2 line => "+self.custom2)
		print("Custom3 line => "+self.custom3)
		print("Custom4 line => "+self.custom4)
		
		#Print all telephone
		for i in range(0,len(self.tel)):
			print("TELEPHONE: "+self.teltype[i]+" "+self.tel[i])
		
		#Print all emails
		for i in range(0,len(self.emailaddr)):
			if self.prefemail==i:
				print("Preferred:")
			print("EMAIL: "+self.emailtype[i]+" "+self.emailaddr[i])
		
		print("Time zone => "+self.timezone)
		
		for i in range(0,len(self.urladdr)):
			print("URL: "+self.urltype[i]+" "+self.urladdr[i])
		
		for i in range(0,len(self.anniversary)):
			print("ANNIVERSARY: YEAR="+self.anniversary[i]["year"]+"\t MONTH="+self.anniversary[i]["month"]+"\t DAY="+self.anniversary[i]["day"])
		
		if len(self.birthday)!=0:
			print("BIRTHDAY: YEAR="+self.birthday["year"]+"\t MONTH="+self.birthday["month"]+"\t DAY="+self.birthday["day"])
				
		for i in range(0,len(self.address)):
			print("ADDRESS: "+self.addrtype[i]+" "+self.address[i])
						
#Write header of *.vcf file
def header(file):
	file.write("BEGIN:VCARD\n")
	file.write("VERSION:3.0\n")
	file.write("PRODID:-//Apple Inc.//iPhone OS 15.7.7//EN\n")

#Write tail of *.vcf file
def tail(file):
	dest.write("END:VCARD\n")


#iphonize function
def iphonize(file,contact):
	#temporary field for note and other line building
	temp = ""
	itemcounter = 1
	
	#Flag for preferred anniversary item
	preferred = False
	
	file.write(contact.name)
	file.write(contact.displayname)
	file.write(contact.nickname)
	
	dest.write(contact.org)
	#process role and title
	if contact.role=="" and contact.title== "":
		None 
	if contact.role=="" and contact.title!= "":
		dest.write(contact.title)
	if contact.role!="" and contact.title== "":
		dest.write("TITLE:"+contact.role[5:])
	if contact.role!="" and contact.title!= "":
		dest.write(contact.title[:-1]+" "+contact.role[5:])
	
	#Process birthday
	if len(contact.birthday)!=0:
		#process only valid birthday date
		if contact.birthday["year"]!="" and contact.birthday["month"]!="" and contact.birthday["day"]!="":
			dest.write("BDAY:"+contact.birthday["year"]+"-"+contact.birthday["month"]+"-"+contact.birthday["day"]+"\n")
		
		if contact.birthday["year"]=="" and contact.birthday["month"]!="" and contact.birthday["day"]!="":
			dest.write("BDAY;X-APPLE-OMIT-YEAR=1604:1604-"+contact.birthday["month"]+"-"+contact.birthday["day"]+"\n")
		
	for i in range(0,len(contact.anniversary)):
		#Allowable anniversaries have year, month, day or month and year
		#OTHER CONFIGURATION ARE FORBIDDEN AND WILL NOT IMPORTED
		if contact.anniversary[i]["year"]!="" and contact.anniversary[i]["month"]!="" and contact.anniversary[i]["day"]!="":
			temp="item"+str(itemcounter)+".X-ABDATE"
			if preferred == False:
				#First item is the preferred item
				temp=temp+";type=pref"
				preferred = True
			temp=temp+":"+contact.anniversary[i]["year"]+"-"+contact.anniversary[i]["month"]+"-"+contact.anniversary[i]["day"]+"\n"
			dest.write(temp)
			temp="item"+str(itemcounter)+".X-ABLabel:_$!<Anniversary>!$_\n"
			dest.write(temp)
			itemcounter=itemcounter+1
		#Reset for other stuff
		preferred == False	
		
		if contact.anniversary[i]["year"]=="" and contact.anniversary[i]["month"]!="" and contact.anniversary[i]["day"]!="":
			temp="item"+str(itemcounter)+".X-ABDATE;X-APPLE-OMIT-YEAR=1604"
			if preferred == False:
				#First item is the preferred item
				temp=temp+";type=pref"
				preferred = True				
			temp=temp+":1604-"+contact.anniversary[i]["month"]+"-"+contact.anniversary[i]["day"]+"\n"
			dest.write(temp)
			temp="item"+str(itemcounter)+".X-ABLabel:_$!<Anniversary>!$_\n"
			dest.write(temp)
			itemcounter=itemcounter+1
	#Reset for other stuff
	preferred == False			   
	temp = ""
	
	#Write email fields
	for i in range(0,len(contact.emailaddr)):
		temp="EMAIL;type=INTERNET"
		if contact.emailtype[i]=="home":
			temp=temp+";type=HOME"
		if contact.emailtype[i]=="work":
			temp=temp+";type=WORK"
		
		if contact.prefemail==i:
			temp=temp+";type=pref"
		
		temp=temp+":"
		
		temp=temp+contact.emailaddr[i]
			
		dest.write(temp)
	#Reset for other stuff
	temp = ""
	
	#Write telephone fields
	for i in range(0,len(contact.tel)):
		if contact.teltype[i]=="work":
			dest.write("TEL;type=WORK;type=VOICE;type=pref:"+contact.tel[i])
		if contact.teltype[i]=="home":
			dest.write("TEL;type=HOME;type=VOICE:"+contact.tel[i])
		if contact.teltype[i]=="cell":
			dest.write("TEL;type=CELL;type=VOICE:"+contact.tel[i])
		if contact.teltype[i]=="fax":
			dest.write("item"+str(itemcounter)+".TEL:"+contact.tel[i])
			dest.write("item"+str(itemcounter)+".X-ABLabel:fax\n")
			itemcounter=itemcounter+1
		if contact.teltype[i]=="pager":	
			dest.write("TEL;type=PAGER:"+contact.tel[i])
		if contact.teltype[i]=="NOTHING":
			dest.write("TEL:"+contact.tel[i])
	#Reset for other stuff
	preferred == False
	temp = ""
	
	#Process addresses
	for i in range(0,len(contact.address)):
		temp="item"+str(itemcounter)+".ADR;type="+contact.addrtype[i]
		if preferred == False:
			temp=temp+";type=pref"
			preferred=True
		temp=temp+":"+contact.address[i]
		dest.write(temp)
		temp="item"+str(itemcounter)+".X-ABADR:"+countrycodeinstance.get_country_code(str(contact.address[i][contact.address[i].rfind(";")+1:-1]))+"\n"
		dest.write(temp)
		itemcounter=itemcounter+1
	#Reset for other stuff
	preferred == False
	temp = ""
	
	#Process URLs			
	for i in range(0,len(contact.urladdr)):
		if contact.urltype[i]=="NOTHING":
			dest.write("item"+str(itemcounter)+".URL:"+contact.urladdr[i])
			dest.write("item"+str(itemcounter)+".X-ABLabel:_$!<HomePage>!$_\n")
			itemcounter=itemcounter+1			
		if contact.urltype[i]=="work":
			dest.write("URL;type=HOME:"+contact.urladdr[i])
		if contact.urltype[i]=="home":
			dest.write("URL;type=WORK:"+contact.urladdr[i])
	#Reset for other stuff
	preferred == False
	
	#Process notes and custom fields	
	if contact.note!="":
		temp = contact.note[:-1]
	
	if contact.custom1!="":
		buffer=contact.custom1[21:]
		if temp!="":
			temp=temp+"\\n\\nPersonalizzato 1:\\n"+buffer[:-1]
		else:
			temp="NOTE:Personalizzato 1:\\n"+buffer[:-1]
			
	if contact.custom2!="":
		buffer=contact.custom2[21:]
		if temp!="":
			temp=temp+"\\n\\nPersonalizzato 2:\\n"+buffer[:-1]
		else:
			temp="NOTE:Personalizzato 2:\\n"+buffer[:-1]
		
	if contact.custom3!="":
		buffer=contact.custom3[21:]
		if temp!="":
			temp=temp+"\\n\\nPersonalizzato 3:\\n"+buffer[:-1]
		else:
			temp="NOTE:Personalizzato 3:\\n"+buffer[:-1]	
		
	if contact.custom4!="":
		buffer=contact.custom4[21:]
		if temp!="":
			temp=temp+"\\n\\nPersonalizzato 4:\\n"+buffer[:-1]
		else:
			temp="NOTE:Personalizzato 4:\\n"+buffer[:-1]	
	
	#Write note field
	if temp!="":
		dest.write(temp)
		dest.write("\n")
		temp = ""
	
	

		
#Main
collectedcontacts=[]	#Contact collected in the current file
#Extract contry code according to iso 3166. If a valid value isn't
#found the instance return a fallback value (the string of constructor)
countrycodeinstance=country_code_3166.country_code("Italia")

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
		
		with open(path+"\\"+k,"r") as source:
			with open(path+"\\"+k[:-4]+" - iphonize.vcf","w") as dest:
				#Read lines and fill the instance members
				line=source.readline()
				while line != "":
					#Parse only valid data
					if line != "END:VCARD\n" and line != "BEGIN:VCARD\n" and line[0:8] != "VERSION:":
						C.parse(line)
			
					#A contact was finished to be acquired
					if line == "END:VCARD\n":
						collectedcontacts.append(C)
						C=Contact()	#Create new contact object
				
					#sample new line
					line=source.readline()
		
				#Now all contacts in the current file were acquired. Print some infos
				print("Found "+str(len(collectedcontacts))+" contact in file '"+k+"'")
				
				#Create an "iphonize" *.vcf with all contacts
				header(dest)
				for i in collectedcontacts:
					iphonize(dest,i)
					i.print_data()
				tail(dest)
		
				#Close files
				source.close()
				dest.close()
		
				#Reset contacts
				collectedcontacts=[]