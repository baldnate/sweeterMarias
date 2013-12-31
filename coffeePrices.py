import json
from bs4 import BeautifulSoup
import re
import urllib2

def get_quants(row):
   for img in row.find_all('img', src=re.compile('add')):
      if 'lb.gif' in img['src']:
         yield img['name'][3:-2], 'lb'
      elif 'lbs.gif' in img['src']:
         yield img['name'][3:-3], 'lb'
      else:
         yield '1', 'ea'


def get_coffee_info():
   SWEET_MARIAS_COFFEE_PRICE_URL = 'http://www.sweetmarias.com/prod.greencoffee.mvc.php'
   html = urllib2.urlopen(SWEET_MARIAS_COFFEE_PRICE_URL).read()
   html = html.replace('%\\', '%"')
   soup = BeautifulSoup(html)

   retval = {}
   for row in soup.find_all('tr', attrs={'class': 'defaultfont14'}):
      coffee = {}      
      cells = [c.text.strip() for c in row.find_all('td') if 'Limit' not in c.text.strip()]
      name = cells[0]
      retval[name] = {}
      retval[name]['prices'] = [{'price':x, 'quant':y, 'unit':z} for (x, (y,z)) in zip(cells[1:6], get_quants(row))]
      retval[name]['link'] = 'http://www.sweetmarias.com/' + row.a['href']
      retval[name]['mini_review'] = row.next_sibling.div.text

   return retval


def print_csv(data):
   import locale
   locale.setlocale( locale.LC_ALL, '' )
   data = get_coffee_info()

   print 'Coffee Name, 1#, 2#, 5#, 10#, 20#'
   for coffee in sorted(data.keys()):
      pricematrix = zip(data[coffee]['prices'], [1.0, 2.0, 5.0, 10.0, 20.0])
      print ", ".join([coffee.replace(',', ' ')] + [data[coffee]['link']] + [locale.currency(float(x[1:])/y) for (x,y) in pricematrix])


if __name__ == '__main__':
   import optparse
   parser = optparse.OptionParser()
   parser.add_option('--json', dest='json', default='./coffee.json', help='name of JSON output file')
   (options, args) = parser.parse_args()
   
   data = get_coffee_info()
   outfile = open(options.json, 'w')
   outfile.write(json.dumps(data, indent=4, separators=(',', ': ')))

