import requests
import bs4
def get_num(x):
	return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
def get_dec(x):
	a = (float(''.join(ele for ele in x if ele.isdigit() or ele == '.')))
	a = float("{0:.2f}".format(a))
	return a
def ReturnItem(page):
	item = str(page.title.string.encode("ascii", "ignore"))
	return str(item)
def Target(SKU, ZIP):
	if '-' not in SKU:
		SKU = ('{}-{}-{}'.format(SKU[0:3], SKU[3:5], SKU[5:9]))
	data = {
		'store_type': '1',
		'sku': SKU,
		'zip': ZIP,
		'sort': 'distance'
		}
	res = requests.post('http://brickseek.com/target-inventory-checker/?sku='.format(str(SKU)), data=data)
	page = bs4.BeautifulSoup(res.text, "lxml")
	Information = {
	'Discounted': str(str(page.select('.post-content div div div div')).partition('<b>Discounted: </b> ')[2]).partition('</div>, <div style="width: ')[0],
	'StockPercent': str(str(page.select('.post-content div div div div')).partition('<b>In Stock: </b>')[2]).partition('</div>')[0],
	"MSRP": str(str(page.select('.post-content div div div div')).partition('<b>MSRP: </b>')[2]).partition('</div>, <div style="width:')[0],
	"DCPI": str(str(page.select('.post-content div div div div')).partition('float:left"><b>DPCI </b>')[2]).partition('</div>, <div style="width:')[0]
		}
	print(Information)
	Stores = str(page.select('#content')[0]).split('<tr class="store_row"')
	for Result in Stores:
		try:
			Result = bs4.BeautifulSoup(Result, "lxml")

			Inventory = {
			"Store": str(str(Result).replace('<br/>', " ").partition('30px;"></td><td>')[2]).partition('</td><td ')[0],
			"OnHand": int(get_num(str(str(Result).replace('<br/>', " ").partition('</td><td style="text-align: center">')[2]).partition('</td><td style=')[0])),
			"ForSale": int(get_num(str(str(Result).replace('<br/>', " ").partition('</td><td style="text-align: center">')[2]).partition('</td><td style=')[2].partition('"text-align: center">')[2].partition('</td><td ')[0])),
			"Price": get_dec((str(str(Result)).partition('$')[2]).partition('</a>')[0])
		}
			print(Inventory)
		except BaseException as exp:
			pass
def Walmart(SKU, ZIP):
	data = {
		'store_type': '3',
		'sku': SKU,
		'zip': ZIP,
		'sort': 'distance'
		}
	res = requests.post('http://brickseek.com/walmart-inventory-checker/?sku={}'.format(str(SKU)), data=data)
	page = bs4.BeautifulSoup(res.text, "lxml")
	Information = {
	'Discounted': str(str(page.select('.post-content div div div div')).partition('<b>Discounted: </b> ')[2]).partition('</div>, <div style="width: ')[0],
	'StockPercent': str(str(page.select('.post-content div div div div')).partition('<b>In Stock: </b>')[2]).partition('</div>')[0],
	"MSRP": str(str(page.select('.post-content div div div div')).partition('<b>MSRP: </b>')[2]).partition('</div>, <div style="width:')[0],
	"DCPI": str(str(page.select('.post-content div div div div')).partition('float:left"><b>DPCI </b>')[2]).partition('</div>, <div style="width:')[0]
		}
	print(Information)
	Stores = page.select('tr')[1:]
	for Result in Stores:
		try:
			Rows = Result.select('td')
			Inventory = {
			"Store": str(Rows[1]).replace('<br/>', " ").replace('td>', "").replace('</', '').replace('<', ''),
			"OnHand": int(get_num((Rows[2]).getText())),
			"ForSale": int(get_num((Rows[2]).getText())),
			"Price": get_dec((Rows[3]).getText())
		}
			print(Inventory)
		except BaseException as exp:
			pass
def Staples(SKU, ZIP):
	data = {
		'store_type': '3',
		'sku': SKU,
		'zip': ZIP,
		'sort': 'distance'
		}

	res = requests.post('https://brickseek.com/inventory-check/staples/', data=data)
	page = bs4.BeautifulSoup(res.text, "lxml")
	Table = page.select('tr')[1:]
	for rows in Table:
		if 'Stock' not in str(rows):
			Table.remove(rows)
	for rows in Table:
		try:
			Inventory = {
			'Store': str(rows.select('td')[0]).partition(') <br/>')[2].partition('<br/>(')[0].replace('<br/>', ' '),
			'Quantity': int(get_num(rows.select('td')[1].getText()))
			}
			print(Inventory)
		except:
			pass