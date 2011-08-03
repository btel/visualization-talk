#!/usr/bin/env python
#coding=utf-8

from Bio import Entrez
import pickle
import re
import os, sys

#!!! Change to your email !!!
Entrez.email = "yourname@example.com" 

def load_countries(fname="iso_countries.csv"):
    """Loads country names from a file"""
    path, _ =  os.path.split(__file__)
    with  open(os.path.join(path,fname)) as f:
        country_list = []
        for line in f.readlines():
            country, code = line.split(';')
            country_list.append(country)
    return country_list


def country2csv(count_dict, fname):
    """Save the country/count dictionary to a CSV files"""
    with open(fname, 'w') as f:
        for country, count in count_dict.items():
            f.write("%s,%d\n" % (country, count))
    
def search_countries(affiliations):
    """Identify country names in a list of affiliations (strings) and count number
    of affiliations in which each country appeared. Returns a dictionary whose keys are 
    country names and values are counts"""

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

def pubmed_search(term, max_count=100, batch_size=100, progress=True):
    """
    Perform pubmed search and return a list of results.

    Arguments:
    * term - your search term in a string
    * max_count - maximal number of retrieved entries (if max_count==0 retrive all, it may take very long time for some searches)
    * batch_size - size of packets in which the entries are retrived 
    * progress - whether to show a progress bar.
    """
    
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
        p_bar = ProgressBar(0, count, 60, message="Downloading: ")
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

def get_affiliations(search_data):
    """Obtain affiliation string from a publication list"""
    affiliations = []
    for entry in search_data:
        try:
            affiliations.append(entry['MedlineCitation']['Article']['Affiliation'])
        except KeyError:
            affiliations.append("N/A")
    return affiliations


class ProgressBar:
    """ Creates a text-based progress bar. Call the object with the `print'
        command to see the progress bar, which looks something like this:

        [=======>        22%                  ]

        You may specify the progress bar's width, min and max values on init.
    """

    def __init__(self, minValue = 0, maxValue = 100, totalWidth=80,
                 message=""):
        self.message = message
        self.progBar = "[]"   # This holds the progress bar string
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # When amount == max, we are 100% done
        self.updateAmount(0)  # Build progress bar string

    def updateAmount(self, newAmount = 0):
        """ Update the progress bar with the new amount (with min and max
            values set at initialization; if it is over or under, it takes the
            min or max value as a default. """
        if newAmount < self.min: newAmount = self.min
        if newAmount > self.max: newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
        percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = int(round(percentDone))

        # Figure out how many hash bars the percentage should be
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))

        # Build a progress bar with an arrow of equal signs; special cases for
        # empty and full
        if numHashes == 0:
            self.progBar = "[>%s]" % (' '*(allFull-1))
        elif numHashes == allFull:
            self.progBar = "[%s]" % ('='*allFull)
        else:
            self.progBar = "[%s>%s]" % ('='*(numHashes-1),
                                        ' '*(allFull-numHashes))

        # figure out where to put the percentage, roughly centered
        percentPlace = (len(self.progBar) / 2) - len(str(percentDone))
        percentString = str(percentDone) + "%"

        # slice the percentage into the bar
        self.progBar = ''.join([self.message,
                                self.progBar[0:percentPlace], percentString,
                                self.progBar[percentPlace+len(percentString):]
                                ])
      

    def __str__(self):
        return str(self.progBar)

    def __call__(self, value):
        """ Updates the amount, and writes to stdout. Prints a carriage return
            first, so it will overwrite the current line in stdout."""
        print '\r',
        self.updateAmount(value)
        sys.stdout.write(str(self))
        sys.stdout.flush()

countries = load_countries()

alternative_spellings = {
    "UNITED KINGDOM": "GB",
    "UNITED STATES" : "US",
    "USA" : "US",
    "UK" : "GB",
    "U.S.A." : "US"
}

if __name__ == "__main__":

    search_results = pubmed_search("python", max_count=100) 
    print get_affiliations(search_results)
