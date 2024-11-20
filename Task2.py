# get matches and their ranks 
# overlap = # matches / 10 (or max # of urls)
# compute r_s --> get di, di^2, n = # of matching pairs 

# output to a csv file 

import json
import csv

def get_queries(filename):
    with open(filename, 'r') as file:
        return json.load(file)  # returns the data as a dictionary that can be used 
    
def overlap(google_urls, duck_urls):
    google_set = set(google_urls)
    duck_set = set(duck_urls)
    matching_urls = google_set.intersection(duck_set)

    max_urls = max(len(google_urls), len(duck_urls)) # should be 10 bc all google ones should be 10
    total_pairs = len(matching_urls)

    percent_overlap = (total_pairs / max_urls) * 100

    return total_pairs, percent_overlap

def get_matches(google_urls, duck_urls):
    google_set = set(google_urls)
    duck_set = set(duck_urls)
    matching_urls = google_set.intersection(duck_set)

    google_ranks = {item: index for index, item in enumerate(google_set)}
    duck_ranks = {item: index for index, item in enumerate(duck_set)}

    matches = {}

    for url in matching_urls:
        google_index = google_ranks.get(url)
        duck_index = duck_ranks.get(url)

        matches[url] = [google_index, duck_index]
    
    return matches

def spearman(google_urls, duck_urls):
    matches = get_matches(google_urls, duck_urls)
    n = len(matches) # number of matching pairs

    # no overlap
    if n == 0:
        return 0
    
    # if duck rank == google rank, r_s = 1, if != r_s = 0
    if n == 1:
        match = next(iter(matches.values()))
        print(match)

        if match[0] == match[1]:
            return 1
        else: 
            return 0

    sum_d2 = 0
    
    # else
    for match in matches.values():
        google_rank = match[0]
        duck_rank = match[1]

        d_i = google_rank - duck_rank

        sum_d2 += (d_i * d_i)
    
    
    r_s = 1 - ((6 * sum_d2) / (n * (n * n - 1)))

    return r_s
    
def main():
    # get both files' dictionaries --> keys = queries, values = results (urls)
    google_results = get_queries('/Users/marthaannwilliams/Desktop/USC/CSCI 572/HW1/Google_Result2.json')
    duck_results = get_queries('/Users/marthaannwilliams/Desktop/USC/CSCI 572/HW1/hw1.json')

    results = []
    query_num = 1
    total_pairs = 0
    total_overlap = 0
    total_spearman = 0

    results.append(['Queries', 'Number of Overlapping Results', 'Percent Overlap', 'Spearman Coefficient'])

    # get matches, correlation, and spearman
    for query in duck_results:
        google_urls = google_results.get(query.strip(), [])
        duck_urls = duck_results.get(query, [])

        pairs, percent_overlap = overlap(google_urls, duck_urls)
        r_s = spearman(google_urls, duck_urls)

        results.append(['Query ' + str(query_num), pairs, percent_overlap, r_s])
        
        query_num += 1
        total_pairs += pairs
        total_overlap += percent_overlap
        total_spearman += r_s

    results.append(['Averages', total_pairs / (query_num - 1), total_overlap / (query_num - 1), total_spearman / (query_num - 1)])

    # format output / csv 
        # Queries, Number of Overlapping Results, Percent Overlap, Spearman Coefficient 
        # Averages, (results column avg), (percent overlap column avg), (spearman column avg)
    filename = 'hw1.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results)

if __name__ == "__main__":
    main()
