# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 12:49:18 2022

@author: User
"""

import requests
import re
from bs4 import BeautifulSoup
import json
from csv import writer

regex = re.compile(r'<[^>]+>')

def remove_html(string):
    return regex.sub('', string)

def get_contents(url):
    r = requests.get(url)
    html_text = r.text
    html_text = re.sub("\s+"," ",html_text)
    return html_text

def get_contents_beautifulsoup(url):
    r = requests.get(url)
    doc = BeautifulSoup(r.text, "html.parser")
    return doc

def extract_product_links(content):
    product_url_regex = re.compile(r"<a class='lpc-teaserCarousel_link' href='(.*?)' data-ga-event-action=.*?")
    result = re.findall(product_url_regex, content)
    remove_items = []
    for i in result:
        if (i.startswith('https://') or i.startswith('/products/')): 
            remove_items.append(i)    
    for element in remove_items:
        if element in result:
            result.remove(element)
    links = ["https://shop.adidas.jp" + x + "&limit=120" for x in result]
    return links

def extract_product_details_link(url):
    content = get_contents(url)
    product_details_url_regex = re.compile(r'<a href="/products/(.*?)" class="image_link test-image_link test-product_id_.*?" data-ga-event-action="click" data-ga-event-category="eec_productlist" data-ga-eec-list-index=".*?" data-ga-eec-product-id=".*?" aria-label=".*?">')
    rest_product_details_url_regex = re.compile(r'.*?"item_store_limited_flag":0,"link_detail_page":"(.*?)","marking_flag":.*?,"master_item_status":.*?,"model_code":.*?,"optional_label":.*?,"optional_label_code":.*?,"price":{"badge":{"color":.*?,"text":.*?},"price_discount":.*?,"price_discount_status":.*?,"price_discount_tax":.*?,"price_fixed":.*?,"price_fixed_tax":.*?,"price_status_memo":.*?,"specially_sells_price_disp_type":.*?}')
    result = re.findall(product_details_url_regex, content)
    rest_result = re.findall(rest_product_details_url_regex, content)
    partial_url = ["/products/" + x for x in result]
    links = ["https://shop.adidas.jp" + x for x in (partial_url+rest_result)]
    return links

def get_product_category_breadcrumb_or_product_name(url, name = 0):
    content = get_contents(url)
    product_cat_breadcrumb_top_regex = re.compile(r'<li class="top"><a href="/">(.*?)</a></li>')
    product_cat_breadcrumb_rest_regex = re.compile(r'<li class="breadcrumbLink test-breadcrumbLink"><a href=.*?>(.*?)</a></li>')
    top = re.findall(product_cat_breadcrumb_top_regex, content)
    result = re.findall(product_cat_breadcrumb_rest_regex, content)
    string_breadcrumb = ""
    breadcrumb = top+result
    string_breadcrumb = '/'.join(map(str,breadcrumb))
    if name:
        return breadcrumb[-1]
    else:
        return string_breadcrumb

def get_product_category_name(url):
    content = get_contents(url)
    product_cat_name_regex = re.compile(r'<span class="categoryName test-categoryName">(.*?)</span>')
    cat_name = re.findall(product_cat_name_regex, content)
    return cat_name[0]

def get_product_price(url):
    content = get_contents(url)
    product_price_regex = re.compile(r'<span class="price-value test-price-value">(.*?)</span>')
    price = re.findall(product_price_regex, content)
    return price[0]

def get_product_available_sizes(url):
    content = get_contents(url)
    sizes_regex = re.compile(r'<li class=".*?"><button type="button" class="">(.*?)</button></li>')
    sizes = re.findall(sizes_regex, content)
    if sizes:
        return ','.join(map(str,sizes))
    else:
        return 'Not Available'

def get_sense_of_sizes(url):
    content = get_contents(url)
    sense_regex = re.compile(r'.css-1fyd4co .bar .marker.mod-marker_3_0{left:(.*?);')
    sense = re.findall(sense_regex, content)
    if sense:
        return sense[0]
    else:
        return 'Not available'
def get_product_image_url(url):
    content = get_contents(url)
    product_img_regex = re.compile(r'<li class="slider-slide test-slider-slide">.*?src="(.*?)".*?</li>')
    img = re.findall(product_img_regex, content)
    img_url_links = ["https://shop.adidas.jp" + x for x in img]
    if img_url_links:
        return ','.join(map(str,img_url_links))
    else:
        return "Not Available"

def get_product_coordinates_codes(url):
    content = get_contents(url)
    product_coords_codes_regex = re.compile(r'.*?{"articleCode":"(.*?)","badge":.*?')
    codes = re.findall(product_coords_codes_regex, content)
    coord_product_url_links = ["https://shop.adidas.jp/products/" + x + '/' for x in codes]
    if codes:
        return ','.join(map(str,codes))
    else:
        return "Not found"

def get_product_coordinates_urls(url):
    content = get_contents(url)
    product_coords_codes_regex = re.compile(r'.*?{"articleCode":"(.*?)","badge":.*?')
    codes = re.findall(product_coords_codes_regex, content)
    coord_product_url_links = ["https://shop.adidas.jp/products/" + x + '/' for x in codes]
    if coord_product_url_links:
        return ','.join(map(str,coord_product_url_links))
    else:
        return 'Not Found'

def get_product_coordinates_img_urls(url):
    content = get_contents(url)
    product_coords_img_regex = re.compile(r'.*?{"articleCode":".*?","badge":.*?,"image":"(.*?)"')
    img_partial_url_list = re.findall(product_coords_img_regex, content)
    coord_product_image_url_links = ["https://shop.adidas.jp/" + x for x in img_partial_url_list]
    if coord_product_image_url_links:
        return ','.join(map(str, coord_product_image_url_links))
    else:
        return 'Not Found'

def get_product_coordinates_names(url):
    content = get_contents(url)
    product_coords_name_regex = re.compile(r'.*?{"articleCode":".*?","badge":.*?,"image":.*?,"name":"(.*?)".*?')
    product_coords_name = re.findall(product_coords_name_regex, content)
    if product_coords_name:
        return ','.join(map(str,product_coords_name))
    else:
        return 'Not Found'

def get_product_coordinates_price(url):
    content = get_contents(url)
    product_coords_price_regex = re.compile(r'.*?{"articleCode":".*?","badge":.*?,"image":.*?,"name":".*?".*?{"withTax":"(.*?)"')
    product_coords_price = re.findall(product_coords_price_regex, content)
    if product_coords_price:
        return ';'.join(map(str,product_coords_price))
    else:
        return 'Not Found'

def get_general_desc(url):
    content = get_contents_beautifulsoup(url)
    product_desc = content.find_all(class_="commentItem-mainText test-commentItem-mainText")
    if product_desc:
        return remove_html(' '.join(map(str, (product_desc[0].contents))))
    else:
        return "Not Found."

def get_heading(url):
    content = get_contents_beautifulsoup(url)
    sub_heading_tag = content.find_all(class_="itemFeature heading test-commentItem-subheading")
    if sub_heading_tag:
        return sub_heading_tag[0].string
    else:
        return "Not found."

def get_general_desc_itemization(url):
    content = get_contents_beautifulsoup(url)
    general_desc_itemization = content.find_all(class_="articleFeatures description_part css-woei2r")
    li_regex = re.compile(r'<li class=".*?">(.*?)</li>')
    stringg = ' '.join(map(str, (list(general_desc_itemization[0].contents))))
    itemization = re.findall(li_regex, stringg)
    new_itemization_list=[]
    for item in itemization:
        item = remove_html(item)
        new_itemization_list.append(item)
    return new_itemization_list

def get_tale_of_size(url):
    content = get_contents(url)
    product_id_regex = re.compile(r'<li class="breadcrumbLink test-breadcrumbLink"><a href="/model/(.*?)/"')
    product_id = re.findall(product_id_regex, content)
    api_url = ["https://shop.adidas.jp/f/v1/pub/size_chart/" + x for x in product_id]
    if api_url:
        api_content = get_contents(api_url[0])
        json_data = json.loads(api_content)
        return json_data['size_chart']
    else:
        return "Not Found."

def get_aggregate_review(url):
    content = get_contents(url)
    product_reviews_regex = re.compile(r'"aggregateRating":{"@type":"AggregateRating","ratingValue":"(.*?)","reviewCount":"(.*?)"}')
    reviews = re.findall(product_reviews_regex, content)
    if reviews:
        return reviews
    else:
        return "No review available"

def get_each_review(url):
    content = get_contents(url)
    product_reviews_regex = re.compile(r'"aggregateRating":{"@type":"AggregateRating","ratingValue":"(.*?)","reviewCount":"(.*?)"}')
    reviews = re.findall(product_reviews_regex, content)
    if reviews:
        return reviews
    else:
        return "No review available"



def get_all_kws(url):
    content = get_contents(url)
    product_kw_regex = re.compile(r'class="css-1ka7r5v">(.*?)</a>')
    kw = re.findall(product_kw_regex, content)
    if kw:
        kw_str = ','.join(map(str, kw))
    else:
        kw_str = "Nothing Found"
    return kw_str

url1 = "https://shop.adidas.jp/men/"
# url = "https://shop.adidas.jp/products/HB9386/"
# url3 = "https://shop.adidas.jp/f/v1/pub/size_chart/28898"
content = get_contents(url1)
with open('product_details.csv', 'w', encoding='utf8') as f:
    the_writer = writer(f)
    header = ['Product Details Links', 'Category Breadcrumb', 'Category Name', 'Product Name', 'Price', 'Sizes', 'Sense', 'Image URL', 'Coordinate Product Codes','Coordinate Product urls','Coordinate Product img urls','Coordinate Product names', 'Coordinate Product Prices', 'Description', 'Heading', 'Itemization', 'Taleof Size', 'Overall Review', 'Each Review', 'Product Keywords']
    the_writer.writerow(header)
    prod_links = extract_product_links(content)
    all_product_detail_links= []
    for i in prod_links:
        all_product_detail_links.extend(extract_product_details_link(i))
    for url in all_product_detail_links[:200]:
        breadcrumb = get_product_category_breadcrumb_or_product_name(url)
        cat_name = get_product_category_name(url)
        product_name = get_product_category_breadcrumb_or_product_name(url,1)
        product_price = get_product_price(url)
        product_sizes = get_product_available_sizes(url)
        product_sense = get_sense_of_sizes(url)
        product_img_url = get_product_image_url(url)
        product_coords_codes = get_product_coordinates_codes(url)
        product_coords_urls = get_product_coordinates_urls(url)
        product_coords_img_urls = get_product_coordinates_img_urls(url)
        product_coords_name = get_product_coordinates_names(url)
        product_coords_price = get_product_coordinates_price(url)
        product_description = get_general_desc(url)
        product_heading = get_heading(url)
        product_description_item = get_general_desc_itemization(url)
        tale_of_size = get_tale_of_size(url)
        aggregate_review = get_aggregate_review(url)
        each_review = get_each_review(url)
        product_kw = get_all_kws(url)
        product_row = [url, breadcrumb, cat_name, product_name, product_price, product_sizes, product_sense, product_img_url, product_coords_codes, product_coords_urls, product_coords_img_urls, product_coords_name, product_coords_price, product_description, product_heading, product_description_item, tale_of_size, aggregate_review, each_review, product_kw]
        the_writer.writerow(product_row)
url = "https://shop.adidas.jp/products/HQ4540/"

# content2 = get_contents_beautifulsoup(url)
# content3 = get_contents_beautifulsoup(url1)
# stud_obj = json.loads(content)
# print(stud_obj['size_chart']['0']['header']['0'])
# breadcrumb = get_product_category_breadcrumb_or_product_name(url)
# print(breadcrumb)
# cat_name = get_product_category_name(url)
# print(cat_name)
# product_name = get_product_category_breadcrumb_or_product_name(url,1)
# print(product_name)
# product_price = get_product_price(url)
# print(product_price)
# product_sizes = get_product_available_sizes(url)
# print(product_sizes)
# product_sense = get_sense_of_sizes(url)
# print(product_sense)
# product_img_url = get_product_image_url(url)
# print(product_img_url)
product_coords = get_product_coordinates_price(url)
print(product_coords)
# product_description = get_general_desc(url)
# print(product_description)
# product_heading = get_heading(url)
# print(product_heading)
# product_description_item = get_general_desc_itemization(url)
# print(product_description_item)
# product_tale_of_size = get_tale_of_size(url)
# print(product_tale_of_size)
# product_kw = get_all_kws(url)
# print(product_kw)
# product_aggregate_review = get_aggregate_review(url)
# print(product_aggregate_review)
#item_tile_wrapper test-item_tile_wrapper clearfix

#https://shop.adidas.jp/f/v1/pub/size_chart/28898