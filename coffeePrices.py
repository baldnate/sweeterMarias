import json
from bs4 import BeautifulSoup
import re
import urllib2
import locale

html = urllib2.urlopen('http://www.sweetmarias.com/prod.greencoffee.mvc.php').read()
html = html.replace('%\\', '%"')
soup = BeautifulSoup(html)

data = {}
for row in soup.find_all('tr', class_='defaultfont14'):
   coffee = {}
   cs = row.find_all('td')
   cs = [c.text.strip() for c in cs]
   c = [c for c in cs if 'Limit' not in c]
   data[c[0]] = {}
   data[c[0]]['prices'] = c[1:6]

#print json.dumps(data, indent=4, separators=(',', ': '))

locale.setlocale( locale.LC_ALL, '' )

print "Coffee Name, 1#, 2#, 5#, 10#, 20#"
for coffee in sorted(data.keys()):
   pricematrix = zip(data[coffee]["prices"], [1.0, 2.0, 5.0, 10.0, 20.0])
   print ", ".join([coffee.replace(',', ' ')] + [locale.currency(float(x[1:])/y) for (x,y) in pricematrix])
