import sys
import boto.ses
AWS_KEY='AKIAJT7UGP5BJCIT7QZQ',
ACCESS_KEY='Oio1VqeifqxUX3HgrhCRqdN8QRsdWuCo/niQ7fTy'

FROM_ADDR = 'ospdev.aws@samsung.com'
FROM_ADDR = 'daehee00.han@samsung.com'
FROM_ADDR = 'hjguy.han@samsung.com'
TO_ADDR = [
'hseok7.shim@samsung.com',
'hjguy.han@samsung.com',
'sukhoo.hong@samsung.com',
'jy7340.jung@samsung.com',
'shawn.s.park@samsung.com',
'daehee00.han@samsung.com'
]


#AWS_KEY = 'AKIAILHNCYCVT6OGN5JA'
#ACCESS_KEY = 'hUyiO8l9ygCynyBsWsX4LKWyqkJKz9jVaNc1xexF'

conn = boto.ses.connect_to_region(
	'us-east-1',
	#'us-west-2',
	aws_access_key_id=AWS_KEY,
	aws_secret_access_key=ACCESS_KEY
	)
print conn

conn = boto.ses.SESConnection(AWS_KEY, ACCESS_KEY)
print conn

senders = conn.list_verified_email_addresses()
#senders = filter(lambda e: not e.find('samsung.com')==-1, senders)
#print senders

sys.exit()


try:
	res = conn.send_email(source=FROM_ADDR,  subject='Hi',
		body='Body. HiHi', to_addresses=TO_ADDR,
		bcc_addresses=None, format='text', reply_addresses=[FROM_ADDR], return_path=None)
	print res
except Exception, e:
	print e



# IAMConnection is not supported in an old version of boto
#conn = boto.iam.connection.IAMConnection(AWS_KEY, ACCESS_KEY)
#print conn
#print conn.get_account_summary()
#print conn.get_all_access_keys('ssp.search.s3')
