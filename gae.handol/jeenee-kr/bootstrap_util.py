def pagination(urls, size='', align='centered'):
	'''size: large, small, mini
	'''align: centers, right, left
	if size != '': size="pagination-" + size
	if align != '': align="pagination-" + align
	html = '''<div class="pagination %s %s">
		<ul> </ul>
	</div>''' % (size, align)
	return html

LABEL_COLOR = { 
	'gray':'',
	'green':'success',
	'orange':'warning',
	'red':'important',
	'blue':'info',
	'inverse':'inverse',

def label(color='gray', name):
	color = LABEL_COLOR.get(color, '')
	if color != '':
		color = 'label-%s' % (color)
	html = '<span class="label %s">%s</span>' % (name)
	return html

def badge(color='gray', name):
	color = LABEL_COLOR.get(color, '')
	if color != '':
		color = 'badge-%s' % (color)
	html = '<span class="badge %s">%s</span>' % (name)
	return html
