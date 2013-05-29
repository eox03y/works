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
	'sblue':'primary',
	'green':'success',
	'orange':'warning',
	'red':'important',
	'blue':'info',
	'black':'inverse'
	}

BUTTON_COLOR = { 
	'gray':'',
	'sblue':'primary',
	'blue':'info',
	'green':'success',
	'orange':'warning',
	'red':'danger',
	'black':'inverse',
	}
def label(color='gray', name):
	color = LABEL_COLOR.get(color, '')
	if color != '':
		color = 'label-%s' % (color)
	html = '<span class="label %s">%s</span>' % (color, name)
	return html

def badge(color='gray', name):
	color = LABEL_COLOR.get(color, '')
	if color != '':
		color = 'badge-%s' % (color)
	html = '<span class="badge %s">%s</span>' % (color, name)
	return html

def button(color='gray', size='primary', name):
	color = BUTTON_COLOR.get(color, '')
	if color != '':
		color = 'btn-%s' % (color)
	size = 'btn-%s' % (size)
	html = '<span class="btn %s %s">%s</span>' % (color, size, name)
	return html
