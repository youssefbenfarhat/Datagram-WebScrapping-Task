from bs4 import BeautifulSoup
import requests
import json

get_brand=lambda x:x.split(" ",1)
get_prices=lambda x:x.split("\xa0")

# Return the premoteid
def get_premoteid (soup):
    return soup.find("div",{"class":"value"}).text

#Return sremoteid
def get_sremoteid(soup):
    return soup.find('h2',{"class":"logo-content"}).strong.text

def get_product(soup,src,product):
    product_info_dict={}
    

    name=soup.find("span",{"class":"base"}).text
    brand= get_brand(name)
   
    images=soup.find_all('script', type='text/x-magento-init')
   
    products_info=soup.find("tbody")
    for row in products_info.find_all('tr'):


        key=row.find('th').text
        value=row.find('td').text
        product_info_dict[key]=value
  
     #image_url=soup.findAll("div",{"class":"product media"})
    #image_url=soup.findAll("div",{"class":"fotorama__stage__shaft fotorama__grab"})
    #print('gggg',image_url)
    #print(price[2].text)
    
    #print("fdcdfdcc",images[7].contents[0])
    #a=images[7].contents[0]
   
    #aa=json.loads(a)
    #c=aa.items()
    '''
    for key, value in c:
        ccc=value.items()
        for key1,value1 in ccc:
            print('rrrrrrr',value1)
    '''
   
    
    product['name']=name
    product['url']=src.url
    product['brand']=brand[0]
    product['gtin']=None
    product['mpn']=None
    
    product['premoteid']=get_premoteid(soup)
    product['data']=product_info_dict

   
# Price details 
def get_price(soup,dict_price):
    
    price=soup.findAll("span",{"class":"price"})
    button=soup.find('button',{"id":"product-addtocart-button"})
    
    if button!=None: 
        exist=True
    else:
        exist=False

    #print(exist)
    price=float(get_prices(price[1].text)[0].replace(',','.'))
    dict_price['premoteid']=get_premoteid(soup)
    dict_price['price']=price
    dict_price['avaible']=exist
    dict_price['sremoteid']=get_sremoteid(soup).replace("\n","").replace(".","_")
    
    
#Promo details
def get_promo(soup,dict_promo):
    
  
    button=soup.find('button',{"id":"product-addtocart-button"})
    price=soup.findAll("span",{"class":"price"})
    price_after=float(get_prices(price[1].text)[0].replace(',','.'))
    print('after',price_after)
    #RETURN 110.0
    price_before2=get_prices(price[2].text)[1].replace(',','.')
    #RETURN 1 
    price_before1=get_prices(price[2].text)[0]
    #CONCAT 1 with 110.0
    before=float(price_before1+price_before2)


    if button!=None: 
        exist=True
    else:
        exist=False



    dict_promo['sremoteid']=get_sremoteid(soup).replace("\n","").replace(".","_")
    dict_promo['promotion_remoteid']=get_premoteid(soup)
    dict_promo['before']=before
    dict_promo['after']=price_after
    dict_promo['url']=None
    dict_promo['label']='-{} %'.format(price_after*100/before)
    dict_promo['image_url']=None
    dict_promo['available']=exist
    products=[]
    dict_products={}
    dict_products['premoteid']=get_premoteid(soup)
    dict_products['quantity']=1
    products.append(dict_products)
    dict_promo['products']=products




src=requests.get('https://www.pneu.ma/hankook-kinergy-eco-2-k435-195-55r16-87h.html')
soup=BeautifulSoup(src.text,"lxml")
dict_product={}
dict_price={}
dict_promo={}
get_product(soup,src,dict_product)

get_price(soup,dict_price)

get_promo(soup,dict_promo)
print('product = ',dict_product)
print('price = ',dict_price)
print('promo =',dict_promo)

#
try:
    file = open('output.txt', 'wt')
    file.write("product = ")
    file.write('\n'+str(dict_product))

    file.write("\n price = ")
    file.write('\n'+str(dict_price))

    file.write("\n promo = ")
    file.write('\n'+str(dict_promo))
    file.close()
  
except:
    print("Unable to write to file")