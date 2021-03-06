#!/usr/bin/python
 
import xmpp, sys
from time import sleep
from datetime import datetime
 
class GchatStatus():
    def __init__(self, username='', password=''):
        self.username = username
        self.password = password
        self.jid = xmpp.protocol.JID(self.username)
        if not self.jid.getNode():
            print 'You must supply a username in the form of username@server.com'
            exit(1)
        self.connect()
 
    def connect(self, debug=''):
        self.client = xmpp.Client(self.jid.getDomain(), debug=debug)
        if not self.client.connect(('gmail.com', 5223)):
            raise IOError('Could not connect to server.')
        if not self.client.auth(self.jid.getNode(), self.password):
            raise IOError('Could not authenticate to server.')
 
    def set_status(self, new_status):
        # Thanks to http://blog.thecybershadow.net/2010/05/08/setting-shared-google-talk-gmail-status-programmatically/
        resp = self.client.SendAndWaitForResponse(xmpp.Iq('get','google:shared-status', payload=[]))
        current_show = resp.getTag('query').getTagData('show')
        if new_status:
            print 'changing status to:', new_status
        else:
            print 'resetting status:', '[%s]'%current_show
            new_status = ''
        self.client.SendAndWaitForResponse(xmpp.Iq('set','google:shared-status', payload=[
            xmpp.Node('show',payload=[current_show]),
            xmpp.Node('status',payload=[new_status])
        ]))
 
def DateRangeQuery(email, password, start_date, end_date):
    day = {}
    import gdata.calendar.client
    cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
    cal_client.ClientLogin(email, password, cal_client.source);
    query = gdata.calendar.client.CalendarEventQuery(start_min=start_date, start_max=end_date)
    feed =cal_client.GetCalendarEventFeed(q=query)
    for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
      if an_event.content.text!=None and an_event.content.text!='':
      	for a_when in an_event.when:
		end = int(a_when.end[11:-16])
		if end == 0: end = 24
		for i in range(int(a_when.start[11:-16]), end):
			day[i] = '@%s' % ( an_event.content.text,)
    for i in range(24):
	if not day.has_key(i):
		day[i] = '@home'
    return day
 
def main(user, psw):
    last = ''
    while True:
		next = int(datetime.now().strftime('%Y-%m-%d')[-2:])+1
		st = GchatStatus(user,psw)
		day = DateRangeQuery(user, psw, datetime.now().strftime('%Y-%m-%d'), str(datetime.now().strftime('%Y-%m-%d'))[:-2]+'%02d' % (next))
		if day[datetime.now().hour] is not last:
			st.set_status(day[datetime.now().hour])
			last = day[datetime.now().hour]
		sleep(60)
 
try:
    if __name__ == "__main__":
        main(sys.argv[1],sys.argv[2])
except KeyboardInterrupt:
    print 'Exiting...'
