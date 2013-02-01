#!/usr/bin/python
 
import xmpp, sys
 
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
            print 'setting status:', new_status, '[%s]'%current_show
        else:
            print 'resetting status:', '[%s]'%current_show
            new_status = ''
        self.client.SendAndWaitForResponse(xmpp.Iq('set','google:shared-status', payload=[
            xmpp.Node('show',payload=[current_show]),
            xmpp.Node('status',payload=[new_status])
        ]))
 
 
def main():
    if len(sys.argv) < 3:
        print 'Usage: status.py username password [New Status]'
        exit(1)
    new_status = ' '.join(sys.argv[3:]).strip() if len(sys.argv) > 3 else ''
    st = GchatStatus(sys.argv[1] if len(sys.argv) > 1 else '', sys.argv[2] if len(sys.argv) > 2 else '' )
    st.set_status(new_status)
 
try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print 'Exiting...'