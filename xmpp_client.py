import sys
import logging 
import getpass
import RPi.GPIO as GPIO

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
		self.send_presence()
		self.get_roster()
		GPIO.output(8,True)
		
#		self.send_message(mto=self.recipient, mbody=self.msg, mtype='type')
#		self.disconnect(wait=True)


	def mysend(self,recipient,msg):
		if recipient != None:
			self.recipient=recipient
			

		self.msg=msg;

		self.send_message(mto=self.recipient,mbody=self.msg,mtype='chat')
	

	def receive(self, msg):

		if msg['type'] in ('chat','normal'):
			print "reply:"
			print  msg['body']
		return	

	def disconnect(self):
		self.disconnect(wait=True)




if __name__=='__main__':
	optp=OptionParser()

	
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
	GPIO.setup(8,GPIO.OUT,initial=GPIO.LOW)
		

	xmpp=client_class(opts.jid, opts.password)
	xmpp.register_plugin('xep_0030')
	xmpp.register_plugin('xep_0199')



	if xmpp.connect(('talk.google.com', 5222)):
		xmpp.process(threaded=True)
		print("Connect successful")

	else:
		print("Unable to connect.")
	
	
	recipient=raw_input("towhom?")
	while True:
		message=raw_input()
		if message!="exit client":
			xmpp.mysend(recipient,message)
		else :
			xmpp.disconnect		
			print("you disconnect!")
			break
	sys.exit(0)
	


