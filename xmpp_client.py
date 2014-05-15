import sys
import logging 
import getpass
import RPi.GPIO as GPIO
import thread
import time


from optparse import OptionParser

import sleekxmpp


if sys.version_info < (3,0):
	reload(sys)
	sys.setdefaultencoding('utf8')
else:
	raw_input=input


class client_class(sleekxmpp.ClientXMPP):
	last_recipient=''
	def __init__(self,jid,password):
		sleekxmpp.ClientXMPP.__init__(self,jid,password)
		self.recipient=""
		self.msg=""
		self.add_event_handler("session_start",self.start)
		self.add_event_handler("message",self.receive)
	def start(self,event):
		GPIO.setmode(GPIO.BOARD)
		self.send_presence()
		self.get_roster()
		

	def mysend(self,recipient,msg):
		if recipient != "":
			self.recipient=recipient
		else:
			print "you havn't specify recipient"
			return

		self.msg=msg;
		self.send_message(mto=self.recipient,mbody=self.msg,mtype='chat')
	

	def receive(self, msg):
		print "get somthing"
		if msg['type'] in ('chat','normal'):
		
			try:
				if msg['body']=="forward":
					thread.start_new_thread(run_motor,(0,0.3,))
				elif msg['body']=="back":
					thread.start_new_thread(run_motor,(1,0.3,))
			except Exception, e:
				print "ERROR: Cannot allocate thread"
				print e
#			xmpp.mysend(recipient,message)
			print msg['from'],  " reply: ",msg['body']
		return	

	def disconnect(self):
		self.disconnect(wait=True)


def run_motor(direction, delay):
	if direction==0:
		
		GPIO.output(8,True)
		GPIO.output(12,False)
		GPIO.output(16,True)
		GPIO.output(15,False)
		time.sleep(delay)
		GPIO.output(8,False)
		GPIO.output(12,False)
		GPIO.output(16,False)
		GPIO.output(15,False)
	elif direction==1:
		GPIO.output(12,True)
		GPIO.output(8,False)
		GPIO.output(15,True)
		GPIO.output(16,False)
		time.sleep(delay)
		GPIO.output(12,False)
		GPIO.output(8,False)
		GPIO.output(15,False)
		GPIO.output(16,False)	



def get_user_list(xmpp):
	global resp
	resp=xmpp.get_roster()
	for jid in resp['roster']['items']:
		name=resp['roster']['items'][jid]['name']
		print jid,"     ",name
		
	



if __name__=='__main__':
	optp=OptionParser()
	recipient=""
	
	optp.add_option("-j", "--jid", dest="jid", help="jid to use")
	optp.add_option("-p", "--password", dest="password", help="psw to use")
	optp.add_option("-t", "--to", dest="to", help="to")
	optp.add_option("-m", "--message", dest="message", help="message")
 	opts, args=optp.parse_args()
	logging.basicConfig()

	if opts.jid is None:
		opts.jid=""
	
	if opts.password is None:
		opts.password=""

#	setup the GPIO port
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(8,GPIO.OUT)
	GPIO.setup(12,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)
	GPIO.setup(16,GPIO.OUT)
		

	xmpp=client_class(opts.jid, opts.password)
	xmpp.register_plugin('xep_0030')
	xmpp.register_plugin('xep_0004')
	xmpp.register_plugin('xep_0060')
	xmpp.register_plugin('xep_0199')


	if xmpp.connect(('talk.google.com', 5222)):
		xmpp.process(threaded=True)
		print("Connect successful")

	else:
		print("Unable to connect.")
	

	get_user_list(xmpp)
	while True:
		flag=0
		message=raw_input()
		messagelist=message.split(' ')
		
		if message=="ls":
			get_user_list(xmpp)
			continue

		elif messagelist[0]=="to":
			import re
			matches=re.findall(r'\"(.+?)\"',message)
			if matches == None:
				matches[0]=""
			print matches[0]
			for jid in resp['roster']['items']:
				print jid
				if matches[0] == str(jid) or matches[0]==resp['roster']['items'][jid]['name']:
					recipient=jid
					flag=1
					print "you are now chatting to  ",jid
					break

		if flag==1:
			continue									

		if message!="exit client":
			try:
				if message=="forward":
					thread.start_new_thread(run_motor,(0,0.3,))
				elif message=="back":
					thread.start_new_thread(run_motor,(1,0.3,))
			except Exception, e:
				print "ERROR: Cannot allocate thread"
				print e
			xmpp.mysend(recipient,message)
		else :
			xmpp.disconnect	
			GPIO.cleanup()	
			print("you disconnect!")
			break
	sys.exit(0)
	


