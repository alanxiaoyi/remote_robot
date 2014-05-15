remote_robot
============

Work on Raspberry pi to control a little robot car over XMPP (which google talk based on)
The code should be pretty straight forward. You need sleekXMPP library setup first.



If you havn't built a robot car, you still can use it as a google talk client.

$: How to start?

sudo python xmpp_client.py  -j xxx@gmail.com  -p  password

How to use?

show your contact:
> ls

choose a person to chat:

> to "frined name here"

exit the client

> exit client


Over google talk, the script recognize word like "forward" and "back" to move forward and backward. This script should be a good start point for you to build your own "google talk remotely" controled robot/electronic device.
