from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

import json
from bs4 import BeautifulSoup
soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello from Flask!'
@app.route('/get')
def get():
  q = request.args.get("q")
  res = requests.get("https://www.mayoclinic.org/diseases-conditions/search-results?q=" + str(q))
  html = res.text
  soup = BeautifulSoup(html,"html.parser")
  if (len(soup.find_all("ul", class_="cmp-search-results__results-list")) == 0):
    response = jsonify([])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response   
  dat = soup.find_all("ul", class_="cmp-search-results__results-list")[0]
  eda = []
  for li in dat.findAll('li'):
    try:
      link = li.findAll("a")
      st = link[0].findAll("strong")
  
      lidat = {}
      lidat["link"] = str(link[0]["href"])
      lidat["name"] = (json.loads(link[0]["data-cmp-data-layer"])['target'])
      lidat["symptoms"] = []
      lidat["prevention"] = []

      res2 = requests.get(lidat["link"])
      html2 = res2.text
      soup2 = BeautifulSoup(html2,"html.parser")
      span = soup2.select("#redpoint_emailform_1")[0]
      cbox = soup2.select(".contentbox")[0]
      a2 = (cbox.find_all_next("h2"))
      for ite in a2:
        if (ite.text=="Prevention"):
          print('---')
          after2 = (ite.find_all_next("ul"))[0]
          for lii in after2.findAll('li'):
            lidat["prevention"].append(lii.text)
            


      
          



  
      # Find all elements after the `span` element that have the tag - p
      after = (span.find_all_next("ul"))[0]
      for li2 in after.findAll('li'):
        lidat["symptoms"].append(li2.text)
      eda.append(lidat)
    except Exception as e:
      print(e)
    

    
  
  response = jsonify(eda)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response  
  

app.run(host='0.0.0.0', port=81)
