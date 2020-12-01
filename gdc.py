#!/usr/bin/python3                                                               

import sys
import json
import os
import getopt
import ipaddress
import uuid

ip = ''
function = ''
gdc = None
description = ''
listofips = None

if len(sys.argv) <= 4:
   print("Error - Format should be - gdc.py -g <Generic_Data_Center_Name> -j <Json_File> -f <AddGDC/DelGDC/AddIP/DelIP> -i <ip> -d <GDC_Description>")
   print("")
   print("This simple tool will update a JSON file with ip addresses (v4 and v6) used with the Generic Data Center Objects as described in SK167210 for R81.")
   print("Examples:")
   print("Add a new IP address to a Generic Data Center to an existing JSON file")
   print("gdc.py -g GDC_LIST1 -j gdc.json -f AddIP -i 10.2.0.1")
   print("")
   print("Add a new IP addresses to a Generic Data Center to an existing JSON file from a list of ip's")
   print("gdc.py -g GDC_LIST1 -j gdc.json -f AddIP -l listofip_address.txt")
   print("")
   print("Delete an IP address to a Generic Data Center to an existing JSON file")
   print("gdc.py -g GDC_LIST1 -j gdc.json -f DelIP -i 10.2.0.1")
   print("")
   print("Add a new Generic Data Center to an existing JSON file.  IP address must be included.")
   print("gdc.py -g GDC_LIST_New -j gdc.json -f AddGDC -d GDC_LIST_NEW_Description -i 10.2.0.1")
   print("")
   print("Delete a Generic Data Center in an existing JSON file. ")
   print("gdc.py -g GDC_LIST_New -j gdc.json -f DelGDC")
   print("")
   exit(1)

try:
   opts, args = getopt.getopt(sys.argv[1:],"g:j:f:i:d:l:", ['gdc=','function=','ip=','desc=','listofips' 'help'])
except getopt.GetoptError:
   print('Error - Format should be - gdc.py -g <Generic_Data_Center_Name> -j <Json_File> -f <AddGDC/DelGDC/AddIP/DelIP> -i <ip> -l <list_of_ip_in_File> -d <GDC_Description>')
   sys.exit(2)
for opt, arg in opts:
   if opt in ('-h', '--help'):
      print('Format should be - gdc.py -g <Generic_Data_Center_Name> -j <Json_File> -f <AddGDC/DelGDC/AddIP/DelIP> -i <ip> -l <list_of_ip_in_File> -d <GDC_Description>')
      sys.exit()
   elif opt in ("-g", "--gdc"):
      gdc = arg
   elif opt in ("-f", "--function"):
      function = arg
   elif opt in ("-j", "--json"):
      jsonfile = arg
   elif opt in ('-i', '--ip'):
      ip = arg
   elif opt in ('-d', '--desc'):
      desc = arg
   elif opt in ('-l', '--listofips'):
      listofips = arg

### Functions
# Function to Remove Duplicates - Used to make sure IP's are uniuqe
def remove_dupe_dicts(l):
  list_of_strings = [
    json.dumps(d, sort_keys=True)
    for d in l
  ]
  list_of_strings = set(list_of_strings)
  return [
    json.loads(s)
    for s in list_of_strings
  ]

# Function to Check for name in json 
def gdc_exist(gdc,jsondata):
   match = False
   for dc in jsondata:
      if dc["name"] == gdc:
         match = True
   return match

# Function to check if JSON file exists
def fileexists(fn):
  try: 
     open(fn,"r")
  except IOError:
     print('File: %s - specified does not appear to exist' % fn)
     sys.exit()

# Function to check for valid ip address
def check_ip(checkip):
  # Check if range is provided by a dash in the ip address
  isrange = ("-" in checkip)
  if isrange == True:
     range = checkip.split("-")
     # Check if range ip 1 is less than 2
     ip = (ipaddress.ip_address(range[0]) < ipaddress.ip_address(range[1]))
     if ip == True:
        return
     else:
       print('address/netmask is invalid: %s' % checkip)
       print('If adding a new Generic Data Center Object an IP has to be defined!')
       sys.exit()
  try:
    ip = ipaddress.ip_address(checkip)
  except ValueError:
    try: 
       ip = ipaddress.ip_network(checkip)
    except ValueError:
      print('address/netmask is invalid: %s' % checkip)
      print('If adding a new Generic Data Center Object an IP has to be defined!')
      sys.exit()

#### Verify that GDC was passed from CLI ####
if not gdc:
   print("Generic Data Center was not passed as a flag to the command.  Include -g <Data_Center_Name>")
   sys.exit()

#### Add IP to Data Center ####
if function == "AddIP":
  filecheck = fileexists(jsonfile)
  obj = json.load(open(jsonfile))
  
  # Check and see if the name of the Data Center exists  
  match = gdc_exist(gdc,obj['objects'])     
  if match == False:
     print('Data Center Object : %s was not found in file : %s' % (gdc,jsonfile))
     print('No updates were made')
     sys.exit()
  
  # Check to see if this is a list of ips from a file
  if not listofips:
  # Add an IP to the list 
     check_ip(ip)                                                
     for item in obj['objects']:
         if item["name"] == gdc:
            item['ranges'].append(ip)
         item['ranges'] = remove_dupe_dicts(item['ranges'])
  else:
     # Read list of ip addresses from file and extend
     filecheck = fileexists(listofips)
     iplist = {}
     with open(listofips) as f:
       iplist = f.read().splitlines()
     for checkip in iplist:
        check_ip(checkip)
     for item in obj['objects']:
         if item["name"] == gdc:
            item['ranges'].extend(iplist)
         item['ranges'] = remove_dupe_dicts(item['ranges']) 
  # Output the updated file with pretty JSON                                      
  open(jsonfile, "w").write(
      json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    )

#### Remove IP from Data Center ####
if function == "DelIP":
  filecheck = fileexists(jsonfile)
  obj = json.load(open(jsonfile))
  
  # Check and see if the name of the Data Center exists  
  match = gdc_exist(gdc,obj['objects'])     
  if match == False:
     print('Data Center Object : %s was not found in file : %s' % (gdc,jsonfile))
     print('No updates were made')
     sys.exit()

  item = obj['objects']
  if not listofips:
     check_ip(ip)
     for item in obj['objects']:
         if item["name"] == gdc:
            for a in item['ranges'][:]:
                if (a == ip):
                    item['ranges'].remove(a)
  else:
     # Read list of ip addresses from file and extend
     filecheck = fileexists(listofips)
     iplist = {}
     with open(listofips) as f:
       iplist = f.read().splitlines()
     for checkip in iplist:
        check_ip(checkip)
     for item in obj['objects']:
         if item["name"] == gdc:
            for t in iplist:
               try:
                  item['ranges'].remove(t) 
               except:
                  print('IP address %s is not in the file %s.' % (t, listofips))
         item['ranges'] = remove_dupe_dicts(item['ranges']) 
  # Output the updated file with pretty JSON                                      
  open(jsonfile, "w").write(
      json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    )

#### Add Data Center ####
if function == "AddGDC":
  filecheck = fileexists(jsonfile)
  obj = json.load(open(jsonfile))
  item = obj['objects']
  uuid = uuid.uuid4()
  
  # Make sure Description is set
  try:
     desc
  except NameError:
      print("Description was not provided as a paramater, please use -d to add the description while adding a new Data Center")
      sys.exit()

  # Check and see if the name of the Data Center already exists 
  match = gdc_exist(gdc,obj['objects'])                                               
  if match == True:
      print('Data Center Object : %s already exists in file : %s' % (gdc,jsonfile))
      print('No updates were made')
      sys.exit()
  
  # Add GDC data to JSON       
  item = obj['objects']  
  add = {"description": desc,
       "id": str(uuid),
       "name": gdc,
       "ranges": []}
  item.append(add)

  # Check to see if this is a list of ips from a file
  if not listofips:
  # Add an IP to the list 
     check_ip(ip)                                                
     for item in obj['objects']:
         if item["name"] == gdc:
            item['ranges'].append(ip)
         item['ranges'] = remove_dupe_dicts(item['ranges'])
  else:
     # Read list of ip addresses from file and extend
     filecheck = fileexists(listofips)
     iplist = {}
     with open(listofips) as f:
       iplist = f.read().splitlines()
     for checkip in iplist:
        check_ip(checkip)
     for item in obj['objects']:
         if item["name"] == gdc:
            item['ranges'].extend(iplist)
         item['ranges'] = remove_dupe_dicts(item['ranges']) 

  # Output the updated file with pretty JSON                                      
  open(jsonfile, "w").write(
      json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    )

#### Delete Data Center ####
if function == "DelGDC":
    filecheck = fileexists(jsonfile)
    obj = json.load(open(jsonfile))
    # Check if Data Center exists before deletion
    match = gdc_exist(gdc,obj['objects'])                                               
    if match == False:
      print('Data Center Object : %s does not exist in file : %s' % (gdc,jsonfile))
      print('No updates were made')
      sys.exit()
    for i in range(len(obj['objects'])):
      if obj['objects'][i]['name'] == gdc:
        obj['objects'].pop(i)
        break
    open(jsonfile, "w").write(
      json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    )
