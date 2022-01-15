#!/usr/bin/env python3
import segno
from segno import helpers
import csv
import io

#########
#
# qrvcardge.py  Author: Joel Wisner  January 15, 2022
#
# This is qrvcardgen.py a Python script to take a csv file and 
# generate vCard 3.0 in QR code format.  It then builds a simple local
# html file to display the QR code with the display name of the vCard 
# in a table with borders (3 columns).
#
# It was intended to help easily import a small (dozen or so) list of contacts
# into a new iPhone *before* the phone is enrolled in iCloud, *and* so that
# the contacts will remain after the iphone is signed into iCloud. 
#
# Trying to build a vCard QR code with Segno library resulted in poor results
# when importing to an iOS contacts app when multiple phone numbers were imported.
# The phone field in iOS contacts app would show as a string with vCard syntax 
# rather than creating proper dialable phone entries.  So I resorted to building
# a vCard that is compatible with iPhone vCard exports and using that to generate
# the QR code using segno module functions.
#
# Future improvements should include tying the csv import to the standard
# Outlook.com csv export format including key field names.  It would also be nice
# to have more export formats like PDF.
#
# Export to a multiple vCard format file would also be useful but not for the 
# initial problem of getting contacts onto iPhone prior to iCloud sign-in.  
#
#########

# Open local files for writing.

vcardsfile = open('vcards.vcf', 'w')
htmlfile = open('qrvcards.html', 'w')

# Build the HTML file starting at the top.
# This should be improved with modern CSS styling and syntax.
# Create a table and first table row tag for iterating below.

htmlfile.write('<!DOCTYPE html><HTML>\n')
htmlfile.write('<HEAD><TITLE>QRvCards</TITLE>')
htmlfile.write('<style>\ntable, td, th {\n  border: 1px solid black;')
htmlfile.write('}\ntable {\nborder-collapse: collapse; width: 100%;}')
htmlfile.write('\n }')
htmlfile.write('</style></HEAD>\n<BODY><TABLE><TR>\n')

# thecount is a variable to use for modulus operation below to close each table row
thecount = 0

# numcolumns is how many columns we want in the local html file.  Should be made into an argv later.
numcolumns = 3

# Iterate over the contacts.  Use a dictionary for key/value pair convenience below.
with open('contacts.csv', newline='') as csvfile:
   vcardreader = csv.DictReader(csvfile)
   for row in vcardreader:
      thecount += 1   # Increment thecount on every loop.
      thevcard = ""   # Empty strings to hold data as we build them below.
      thephone = ""

      thename = row['fname'] + ";" + row['lname'] + ";;;"  # iPhone vcf exports have these semicolons

      dispname = row['fname'] + " " + row['lname']         # display name is required for vCard

      if(len(row['office_phone'])>0):                      # check if there's one or two phones
         thephone += "'" + row['office_phone'] + "'"

      if(len(row['mobile_phone'])>0):
         thephone += ", '" + row['mobile_phone'] + "'"     # this writes the vCard multi-phone string

# Build the filename from csv fields, use .png extension to tell segno to write a PNG file. 
      filename = row['fname'] + "-" + row['lname'] + 'vcard-qr.png'

# Start buildin the vCard formatted string in thevcard variable
      thevcard = "BEGIN:VCARD\nVERSION:3.0\nPRODID:-//Joel Wisner//US Embassy//EN\n"
      thevcard += "N:" + row['lname'] + ";" + row['fname'] + ";;;\nFN:" + dispname + "\n"
      thevcard += "TEL;type=CELL;type=VOICE;type=pref:" + row['mobile_phone']  + "\n"
      thevcard += "TEL;type=WORK;type=VOICE:" + row['office_phone'] + "\n"
      thevcard += "ORG:" + row['org'] + "\n"
      thevcard += "TITLE:" + row['title'] + "\n"
      thevcard += "EMAIL;type=INTERNET;type=WORK;type=pref:"
      thevcard += str(row['email']) + "\n"
      thevcard += "END:VCARD\n"

# This is a file to record all of the vCards.  Could be useful but really a debugging tool.
      print(thevcard, file = vcardsfile)

# Here's where the QR codes are generated.
      qrcode = segno.make(thevcard, error='H')
      qrcode.save(filename,scale=1)

# Write the next table data cell as the vCard QR code image with name in the same cell.
      htmlfile.write('<TD align=center><DIV><IMG SRC="' + filename + '"></IMG>\n')
      htmlfile.write('<H3>' + dispname + '</H3></DIV><TD>\n')

# If we are at the numcolumns level, close the table row and open a new one.
      if(thecount % numcolums == 0):
         htmlfile.write('</TR><TR>')

# End of the iteration
# close the local files 

vcardsfile.close()
htmlfile.write('</BODY></HTML>')
htmlfile.close()
