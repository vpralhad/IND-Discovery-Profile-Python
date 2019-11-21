[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/vpralhad/IND-Discovery-Profile-Python)

# Cisco IND-Discovery-Profile-Python
Create, Scan, Print and Delete the IND (Industrial Network Director) Discovery Profiles using Python

# Pre-requisites -
	1.	The python script is tested with 3.6.5 version
	2.	requirements.txt (included in the repo)
	3. 	devices.csv file (included in the repo)
	4.	WebEx Teams account (along with room id and user token)
	5. 	Cisco Industrial Network Director (in this case, IND 1.7.1 was installed on local computer)
	6. 	Access Prfoile must have been created in IND prior to running script

# Cisco Industrial Network Director -

The Cisco Industrial Network Director is an easy-to-adopt network management system for industrial automation. It is specifically designed to help operations teams manage automation by providing full visibility and control of the Industrial Ethernet infrastructure in the context of the automation process.
For information, please visit https://www.cisco.com/c/en/us/products/cloud-systems-management/industrial-network-director/index.html

# Script Summary -

The goal of the python script is create, print and delete the discovery profiles and output the result in command prompt as well as in WebEx Teams room.

# Detailed Explanation -

When you clone the repo, it includes folowing files -
1.	env_lab.py (IND dteails are defined including credentials)
2.	env_user.py (your WebEx Teams user token and room ID are defined in this file)
3.	devices.csv (discovery profile fields are defined here)
There is one more file called as JasonRecords.json which will be created when you run discovery.py

discovery.py (this is the file you will run)
2.	
# Steps -

Run following commands on your computer (in this case, Windows machine is used so)
1.	git clone https://github.com/vpralhad/IND-Discovery-Profile-Python
2.	cd IND-Discovery-Profile-Python
3.	python -m venv venv
4.	pip install requirements.txt

For WebEx Teams -
1.	go to https://developer.webex.com/
2.	Make sure you are loogedn in click on Documentation on top and go to Getting Started page
3.	By scrolling further down, copy the Bearer token ()

![Screenshot]
