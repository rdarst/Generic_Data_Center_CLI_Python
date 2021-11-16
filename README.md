# Generic Data Center CLI Python

This simple tool will update a JSON file with ip addresses (v4 and v6) used with the Generic Data Center Objects as described in SK167210 for Check Point release R81 or R81.10.

Simple lists of IP's can also be added/deleted by using the -l option.

Change the path for Python if running on Gaia to the location of Python 3.
###
Example : /opt/CPsuite-R81/fw1/Python/bin/python3
###
Examples of using the CLI tool:

Add a new IP address to a Generic Data Center to an existing JSON file
```
gdc.py -g GDC_LIST1 -j gdc.json -f AddIP -i 10.2.0.1
```
Add a new IP addresses to a Generic Data Center to an existing JSON file from a list of ip's
```
gdc.py -g GDC_LIST1 -j gdc.json -f AddIP -l listofip_address.txt
```

Delete an IP address to a Generic Data Center to an existing JSON file
```
gdc.py -g GDC_LIST1 -j gdc.json -f DelIP -i 10.2.0.1
```

Add a new Generic Data Center to an existing JSON file.  IP address must be included.
```
gdc.py -g GDC_LIST_New -j gdc.json -f AddGDC -d GDC_LIST_NEW_Description -i 10.2.0.1
```

Delete a Generic Data Center in an existing JSON file. 
```
gdc.py -g GDC_LIST_New -j gdc.json -f DelGDC
```
