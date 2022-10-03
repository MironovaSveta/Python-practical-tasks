import pandas as pd
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup as bs
from tqdm.notebook import tqdm
import time
from lxml import html
from collections import defaultdict

FILE_MARKER = '<files>'

def attach(branch, trunk):
    '''
    Insert a branch of directories on its trunk.
    '''
    parts = branch.split('/', 1)
    if len(parts) == 1:  # branch is a file
        trunk[FILE_MARKER].append(parts[0])
    else:
        node, others = parts
        if node not in trunk:
            trunk[node] = defaultdict(dict, ((FILE_MARKER, []),))
        attach(others, trunk[node])

def prettify(d, indent=0):
    '''
    Print the file tree structure with proper indentation.
    '''
    isLastCategory = True
    for key, value in d.items():
        if key != FILE_MARKER:
            isLastCategory = False
            out.write('  ' * indent + str(key) + '\n')
            if isinstance(value, dict):
                prettify(value, indent+1)
    
    if isLastCategory:
        value = set(value)
        out.write('  ' * indent + "Number of elements = " + str(len(value)) + ": " + str(value) + '\n')

#------------------------------------------------------------------------------
# task:
# 1. read sitemap
# 2. store paths to csv file
# 3. create tree structure of paths
xml_list = []
urls_titles = []

xml = "https://www.agilent.com/products0.xml"
ua = "Mozilla/5.0 (Linux; {Android Version}; {Build Tag etc.}) AppleWebKit/{WebKit Rev} (KHTML, like Gecko) Chrome/{Chrome Rev} Mobile Safari/{WebKit Rev}"
xml_response = requests.get(xml,headers={"User-Agent":ua})
xml_content = bs(xml_response.text,"xml")
xml_loc = xml_content.find_all("loc")
for item in tqdm(xml_loc):
        uploads = item.text.find("wp-content")
        if uploads == -1:
            xml_list.append(unquote(item.text))
            urls_titles.append(unquote(item.text.split("/")[-2].replace("-"," ").title()))
xml_data = {"URL":xml_list,"Title":urls_titles}
xml_list_df = pd.DataFrame(xml_data,columns=["URL","Title"])
xml_list_df.to_csv("xml_files_results.csv",index=False)

# make tree
main_dict = defaultdict(dict, ((FILE_MARKER, []),))
for line in [i.split('/product/')[1] for i in xml_list]:
    attach(line, main_dict)

out = open('fileTreeStructure.txt','w')
prettify(main_dict)
out.close()
#------------------------------------------------------------------------------

