#!/usr/bin/python




    

def DateRangeQuery(email, password, start_date='2013-02-04', end_date='2013-02-05'):
    day = {}
    import gdata.calendar.client
    cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
    cal_client.ClientLogin(email, password, cal_client.source);
    print 'Date range query for events on Primary Calendar: %s to %s' % (
        start_date, end_date,)
    query = gdata.calendar.client.CalendarEventQuery(start_min=start_date, start_max=end_date)
    feed =cal_client.GetCalendarEventFeed(q=query)
    for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
      if an_event.content.text!=None and an_event.content.text!='':
      	for a_when in an_event.when:
		for i in range(int(a_when.start[11:-16]), int(a_when.end[11:-16])):
			day[i] = '@%s' % ( an_event.content.text,)
    for i in range(24):
	if not day.has_key(i):
		day[i] = '@home'
    print day


   


def main():

  DateRangeQuery('joopeeds@gmail.com', ' dsxlwiyzqzjosuzp', start_date='2013-02-04', end_date='2013-02-05')

if __name__ == '__main__':
  main()


