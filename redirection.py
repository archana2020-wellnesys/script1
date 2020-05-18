import httplib, smtplib, sys

from email.mime.text import MIMEText

# Determine if we're online
sites = ['www.google.com', 'www.amazon.com', 'www.ebay.com']
online = False
for s in sites:
	conn = httplib.HTTPConnection(s)
	conn.request("GET", "/")
	res = conn.getresponse()
	if (res.status == 200):
		online = True
		break
	print s, res.status, res.reason

if (online == False):
	print "Client is not connected to the internet."
	sys.exit(1)
	
	
# List of sites to check
sites = ['example.com', 'example.net']
down = []
for s in sites:
	try:
		conn = httplib.HTTPConnection(s)
		conn.request("GET", "/")
		res = conn.getresponse()
	except BadStatusLine, e:
		# Do nothing
		print ''
	if (res.status != 200):
		down.append({'url':s, 'status':res.status, 'reason':res.reason})
	print s, res.status, res.reason


if (len(down) > 0):
	# There are some sites that appear down; connect to an SMTP server and send some messages
	svr = smtplib.SMTP('smtp.gmail.com:587')
	svr.starttls()
	svr.login('daemon@example.com', 'mysecurepassword')
	from_addr = 'daemon@example.com'
	to_addr = 'webmaster@example.com'
	for s in down:
		msg = MIMEText("The site %s appears to be down (%s %s), you might want to check in on it.\n" % (s['url'], s['status'], s['reason']))
		msg['Subject'] = "Site not responding: %s" % s['url']
		msg['From'] = 'Daemon <%s>' % from_addr
		msg['To'] = 'Webmaster <%s>' % to_addr
		#print msg.as_string()
	
		svr.sendmail(from_addr, to_addr, msg.as_string())
	svr.quit() # Close SMTP connection
