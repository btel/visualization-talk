#!/usr/bin/env python
#coding=utf-8

from Bio import Entrez
import pickle
import re
from progressbar import progressBar

Entrez.email = "muchatel@poczta.com" 

def list_keys(data, spaces=""):
    keys = data.keys()
    for k in keys:
        print spaces, k
        try:
            list_keys(data[k], spaces+"    ")
        except AttributeError:
            pass

def load_countries():
    with  open("iso_countries.csv") as f:
        country_list = []
        for line in f.readlines():
            country, code = line.split(';')
            country_list.append(country)
    return country_list

countries = load_countries()
#countries = set(['USA', 'Canada', 'UK', 'Australia', 'Germany',
#                 'Switzerland', 'Portugal', 'Finland', 'Belgium',
#                'Japan'])
def country2csv(count_dict, fname):
    with open(fname, 'w') as f:
        for country, count in count_dict.items():
            f.write("%s,%d\n" % (country, count))
    
alternative_spellings = {
    "UNITED KINGDOM": "GB",
    "UNITED STATES" : "US",
    "USA" : "US",
    "UK" : "GB",
    "U.S.A." : "US"
}
    
def search_countries(affiliations):

    def find_country(aff_string):
        for c in countries:
            if aff_string.upper().find(c)>0:
                return c
        return "N/A"

    count = {}

    for aff in affiliations:
        country = find_country(aff)
        try:
            country = alternative_spellings[country]
        except KeyError:
            pass
        if country=="N/A": print aff
        count[country] = count.setdefault(country,0)+1
    return count

def pubmed_search(term, max_count=0, batch_size=10, progress=True):
    search_handle = Entrez.esearch(db="pubmed", term=term, usehistory='y')

    search_results = Entrez.read(search_handle)
    search_handle.close()

    count = int(search_results["Count"])
    if max_count:
        count = max_count if max_count < count else count

    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"] 

    affiliations = []
    data = []
    if progress:
        p_bar = progressBar(0, count, 60, message="Downloading: ")
    else:
        #dummy function
        p_bar = lambda x: None
    for start in range(0,count,batch_size):
        end = min(count, start+batch_size)
        fetch_handle = Entrez.efetch(db="pubmed", retmode="xml",
                                     retstart=start, retmax=batch_size,
                                     webenv=webenv, query_key=query_key)
        data += Entrez.read(fetch_handle)
        for el in data:
            try:
                affiliations.append(el['MedlineCitation']['Article']['Affiliation'])
            except KeyError:
                pass
        fetch_handle.close()
        p_bar(start)
    return data

def save_search(fname, results):
    with open(fname, 'w') as f:
        pickle.dump(results,f)

def load_search(fname, results):
    with open(fname, 'r') as f:
        results = pickle.load(f)
    return results


def get_affiliations(search_data):
    affiliations = []
    for entry in search_data:
        try:
            affiliations.append(entry['MedlineCitation']['Article']['Affiliation'])
        except KeyError:
            affiliations.append("N/A")
    return affiliations






if __name__ == "__main__":

    handle = Entrez.esearch(db="pubmed", term="biopython")
    record = Entrez.read(handle)
    print record['IdList']

    handle = Entrez.efetch(db="pubmed", id="21689439", retmode='xml')
    xml_parsed = Entrez.read(handle)

    list_keys(xml_parsed[0])
    print xml_parsed[0]['MedlineCitation']['Article']['Affiliation']

    search_results = pubmed_search("hippocampus", max_count=100) 
    aff = get_affiliations(search_results)
    countries = search_countries(aff)
    country2csv(countries, "country.csv")

