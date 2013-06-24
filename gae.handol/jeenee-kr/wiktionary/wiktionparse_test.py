# -*- coding: utf-8 -*-
import wiktionparse


AAA = '''
{{trans-top|to present again or anew}}
* Catalan: {{t+|ca|representar}}
* Dutch: {{t+|nl|voorstellen}}
* French: {{t+|fr|représenter}}
{{trans-mid}}
* Romanian: {{t-|ro|reprezenta}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-bottom}}

{{trans-top|to portray by pictorial or plastic art}}
* Catalan: {{t+|ca|representar}}
* Dutch: [[voorstellen]], [[uitbeelden]], ergens [[voor staan]]
* Finnish: {{t+|fi|kuvata}}
* French: {{t+|fr|représenter}}
{{trans-mid}}
* Romanian: {{t-|ro|reprezenta}}
* [[Scottish Gaelic]]: {{t-|gd|riochdaich}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-bottom}}

{{trans-top|to portray by mimicry or action of any kind}}
* Dutch: {{t+|nl|voorstellen}}
* Finnish: {{t+|fi|kuvata}}
* French: {{t+|fr|jouer}}
{{trans-mid}}
* [[Scottish Gaelic]]: {{t-|gd|riochdaich}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-bottom}}

{{trans-top|to stand in the place of}}
* Arabic: {{Arab|[[مثل]]}} {{IPAchar|(máθθala)}}
* Catalan: {{t+|ca|representar}}
* Chinese: [[代表]] (dàibiǎo)
* Czech: {{t-|cs|reprezentovat}}, {{t-|cs|zastupovat}}
* Dutch: {{t+|nl|vertegenwoordigen}}, {{t+|nl|representeren}}
* Finnish: {{t+|fi|edustaa}}
* French: {{t+|fr|représenter}}
* German: {{t+|de|darstellen}}, {{t+|de|repräsentieren}}
* Hungarian: {{t+|hu|képvisel}}
{{trans-mid}}
* Italian: {{t+|it|rappresentare}}
* Japanese: [[代表]]する (daihyō suru)
* Korean: [[대표하다]] (daepyohada)
* Portuguese: {{t+|pt|representar}}
* Romanian: {{t-|ro|reprezenta}}
* Russian: [[представлять]] (predstavlját’)
* [[Scottish Gaelic]]: {{t-|gd|riochdaich}}
* Spanish: {{t+|es|representar}}
* Swahili: {{t+|sw|wakilisha}}
* Swedish: {{t+|sv|representera}}
{{trans-bottom}}

{{trans-top|to exhibit to another mind in language}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-mid}}
{{trans-bottom}}

{{trans-top|to serve as a sign or symbol of}}
* Dutch: {{t+|nl|voorstellen}}
* Finnish: {{t+|fi|edustaa}}
* Portuguese: {{t+|pt|representar}}
{{trans-mid}}
* Romanian: {{t-|ro|reprezenta}}
* [[Scottish Gaelic]]: {{t-|gd|riochdaich}}
* Spanish: {{t|es|representar}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-bottom}}

{{trans-top|to bring a sensation of into the mind or sensorium}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-mid}}
{{trans-bottom}}

{{trans-top|to form or image again in consciousness, as an object of cognition or apprehension}}
* Romanian: {{t-|ro|reprezenta}}
* Swahili: {{t+|sw|wakilisha}}
{{trans-mid}}
{{trans-bottom}}

{{checktrans-top}}
* {{ttbc|eo}}: [[reprezenti]]
* {{ttbc|it}}: [[rappresentare]]
{{trans-bottom}}

'''


### run the test
if __name__=='__main__':
	trinfo = wiktionparse.TrInfo()

	for line in AAA.splitlines():
		trinfo.proc(line)
	print trinfo.html()
