#! /usr/bin/env python
"""
This is a prototype script to attched sdwan device templates to devices using device template APIs
this was created based on the work of work of cisco DevNet team https://github.com/CiscoDevNet/Getting-started-with-Cisco-SD-WAN-REST-APIs
"""
import time
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Update loging cridentials paswwords!
SDWAN_IP = "your vmanage host here"
SDWAN_USERNAME = "your user name here"
SDWAN_PASSWORD = "you pasword here"
#Update target device and template 
TEMPLATEID = "your template id here"  
DEVICEID = "your device UUID here"



class rest_api_lib:
	def __init__(self, vmanage_ip, username, password):
		self.vmanage_ip = vmanage_ip
		self.session = {}
		self.login(self.vmanage_ip, username, password)

	def login(self, vmanage_ip, username, password):
		"""Login to vmanage"""
		base_url_str = 'https://%s:443/'%vmanage_ip

		login_action = '/j_security_check'

		#Format data for loginForm
		login_data = {'j_username' : username, 'j_password' : password}

		#Url for posting login data
		login_url = base_url_str + login_action
		url = base_url_str + login_url

		#URL for retrieving client token
		token_url = base_url_str + 'dataservice/client/token'

		sess = requests.session()
		sess.cookies.clear()
		#If the vmanage has a certificate signed by a trusted authority change verify to True
		login_response = sess.post(url=login_url, data=login_data, verify=False)

	
		if b'<html>' in login_response.content:
			print ("Login Failed")
			sys.exit(0)

		#update token to session headers
		login_token = sess.get(url=token_url, verify=False)

		if login_token.status_code == 200:
			if b'<html>' in login_token.content:
				print ("Login Token Failed")
				exit(0)

			sess.headers['X-XSRF-TOKEN'] = login_token.content

		#pprint.pprint(vars(sess), indent=2)
		self.session[vmanage_ip] = sess

	def get_request(self, mount_point):
		"""GET request"""
		url = "https://%s:443/dataservice/%s"%(self.vmanage_ip, mount_point)
		#print url
		response = self.session[self.vmanage_ip].get(url, verify=False)
		data = response.content
		return data

	def post_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
		"""POST request"""
		url = "https://%s:443/dataservice/%s"%(self.vmanage_ip, mount_point)
		payload = json.dumps(payload)
		#print (payload)

		response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
		try:
			data = response.json()
		except Exception as e:
			data = response.text
		return data


sdwanp = rest_api_lib(SDWAN_IP, SDWAN_USERNAME, SDWAN_PASSWORD)


#--template "d3c289a3-a698-422c-a9c9-bf625e1e4251" --deviceid "C1117-4PLTEEA-FGL224013B0"
#Step1: Genrating device confugration input 
#==========================================
print(">> Attempting to genrate input for device template attach.")

payload = {"templateId":TEMPLATEID,"deviceIds":[DEVICEID],"isEdited":"False","isMasterEdited":"False"}

response = sdwanp.post_request('template/device/config/input', payload)

if "data" in response.keys(): #if reqest was succful we will have data
	print(">> Input for device template attach genrated! Attempting to attche template")
else:
	print("error")
	#TODO break here


#Step2: Attaching template to device
#===================================
payload = {
	"deviceTemplateList":[
	{
		"templateId":TEMPLATEID,	
		"device":[],
		"isEdited":"false", 
		"isMasterEdited":"false" 
	}
	]
}
payload['deviceTemplateList'][0]['device'].append(response['data'][0])
response = sdwanp.post_request('template/device/config/attachfeature', payload)
print (response)

if "id" in response.keys():
	status="0"		
	while status!="done":
		time.sleep(5)
		resp = json.loads( sdwanp.get_request("device/action/status/"+str(response["id"])) )
		status=resp["summary"]["status"]
		print("-", end='')
	print(">> done")
else:
	print("error!")
	#TODO break here