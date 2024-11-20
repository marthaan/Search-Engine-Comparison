import requests
import time
from bs4 import BeautifulSoup
from time import sleep
import json
from random import randint
from html.parser import HTMLParser

# USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}


class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep: # prevents loading too many pages too soon
            time.sleep(randint(10, 100))
        temp_url = '+'.join(query.split()) # for adding + between words for the query
        url = 'https://www.duckduckgo.com/html/?q=' + temp_url
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("a", attrs = {"class" : "result__a"}) # avoid people also ask/carousels
        results = []
        for result in raw_results:
            link = result.get('href')

            # avoid ads
            if 'advertisement' or 'ads' or 'sponsored' in link:
                continue # skip this link

            # check that URLs must not be duplicated
            if link and link not in results: 
                results.append(link)

            # implement a check to get only 10 results
            if len(results) >= 10:
                break
        return results

def main():
    print(f"MAIN")

    filename1 = '/Users/marthaannwilliams/Desktop/USC/CSCI 572/HW1/100QueriesSet2.txt'
    with open(filename1, 'r') as file:
        queries = file.read().strip().split('\n')
    results_dict = {}

    query_count = 0

    for query in queries:
        print(f"LOOP")
        #############Driver code############
        results = SearchEngine.search(query)
        #################################### 
        results_dict[query.strip()] = results

        print(f"QUERY " + str(query_count))
        query_count += 1

    filename2 = 'hw1.json'
    with open(filename2, 'w') as file:
        json.dump(results_dict, file, indent=4)

    print(f"DONE")

if __name__ == "__main__":
    main()
