# SDWAN Uplink Automation
Using SDWAN device template APIs we can automate the selection of uplinks on all SDWAN nodes, for this pourpus we can create difrent templates that activate difrent upalinks and use the device tempale API to automate the switching of uplinks from other programs 
a very stright forward usecase is cost optimisation on uplinks where a customer can link its cost monitoring app to SDWAN using this API and keep switching between Uplinks based on teh pricing

This prototype is a sciprt that can be trgred by another prgram and activate one template on a selcted device.
![Prototype][Prototype]

[Prototype]:./workflow.png "Prototype workflow"
## Install:

#### Clone the repo :
```
$ git clone https://github.com/gve-sw/sdwan-uplink-automation
```

#### Install dependencies :
```
$ pip install requests
$ pip install click
```

## Setup:
#### Retrive template Id and device UUID :
Using the [sdwan.py](./sdwan.py) device template toolkit you can retrive the template id and device uuid, you can discover more about sdwan API here [LINK](https://github.com/CiscoDevNet/Getting-started-with-Cisco-SD-WAN-REST-APIs)

- Retrive your device UUID:
update 'Nyiregyhaza' with your device name and copy the device ID
```
$ python3 sdwan.py device-list --search 'Nyiregyhaza'
Retrieving the devices.
╒═════════════╤═══════════════╤═══════════════════════════╤═════════════╤═══════════╤═══════════════╤═════════════════════╕
│ Host-Name   │ Device Type   │ Device ID                 │ System IP   │   Site ID │ Version       │ Device Model        │
╞═════════════╪═══════════════╪═══════════════════════════╪═════════════╪═══════════╪═══════════════╪═════════════════════╡
│ Nyiregyhaza │ vedge         │ C1117-                    │ 10.10.10.30 │       300 │ 16.12.1d.0.32 │ vedge-C1117         │
╘═════════════╧═══════════════╧═══════════════════════════╧═════════════╧═══════════╧═══════════════╧═════════════════════╛
```

- Retrive your template ID:
update 'Nyiregyhaza' with your template name and copy the selcted template ID:
```
$ python3 sdwan.py template-list --search 'Nyiregyhaza'
Retrieving the templates available.
╒════════════════════════════╤═════════════════════╤══════════════════════════════════════╤════════════════════╤════════════════════╕
│ Template Name              │ Device Type         │ Template ID                          │   Attached devices │   Template version │

```

#### Update the script [attach_template_script.py](./attach_template_script.py):
Update the flwoing section with your details:
```python
SDWAN_IP = "your vmanage host here"
SDWAN_USERNAME = "your user name here"
SDWAN_PASSWORD = "you pasword here"
#Update target device and template 
TEMPLATEID = "your template id here"  
DEVICEID = "your device UUID here"
```
You can test this script using the SDWAN sandbox on devent [LINK](https://developer.cisco.com/sdwan/)


## Usage:

Launch the script by issuing 
```
$ python3 attach_template_script.py
```
Notice the change of attched devices to your template using the sdwan.py
```
$ python3 sdwan.py template-list --search 'Nyiregyhaza'
Retrieving the templates available.
╒════════════════════════════╤═════════════════════╤══════════════════════════════════════╤════════════════════╤════════════════════╕
│ Template Name              │ Device Type         │ Template ID                          │   Attached devices │   Template version │

```
