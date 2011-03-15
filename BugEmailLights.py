#!/usr/bin/env python

# BugEmailLights.py
# 
# Simple script using imaplib and theTerg's Bug Von Hippel library to
# light the Von Hippel modules LED's on e-mail.
# obtain theTerg's library from Bug Labs' old wiki
# http://www.bugcommunity.com/wiki/index.php/Develop_with_Python
# (probably moved since the last time I wrote this comment.)
# For best results, use with a cron job to check regularly.
#
# by wwward
# v0.2
# march 14, 2011

import imaplib, re
from VonHippel import *
from time import sleep

# Initialize Von Hippel module; the "_m#" refers to module slot (1-4)
# This device filename should be present in the filesystem /dev path
# when the module is functioning normally.
# *** NOTE *** You'll need to stop Concierge if it is running, since
# the JVM will grab the Von Hippel device and lock out Python
# use /etc/init.d/concierge stop to shut down the JVM!
vh = VonHippel('/dev/bmi_vh_control_m1')

# IMAP4_SSL is for encrypted SSL access.
# open SSL connection to whatever is specified
M = imaplib.IMAP4_SSL('servername')
# it's never good to leave your password in cleartext, k?
M.login('username', 'password')
# This command selects the mailbox and returns the count of messages, 
# INBOX is default when not arguing.
M.select() 

# The following command searches the inbox for messages flagged as
# "UNSEEN" which is managed by the mail reader.
unreadCount = int(re.search("UNSEEN (\d+)", M.status("INBOX", 
			    "(UNSEEN)")[1][0]).group(1)) 

# This simple condition sets the LED on if the unseen count is > 0
# or sets it off if otherwise.
if not unreadCount:
	print '### No new e-mail. ###'
	vh.iox_low(3) #turn on blue LED on Von Hippel
else:
	print 'NEW EMAIL!!!!!!'
	vh.iox_high(3) #turn off blue LED on Von Hippel
M.close() # Close the mailbox to keep the bees out.
M.logout() # Don't forget your keys in the lock!
