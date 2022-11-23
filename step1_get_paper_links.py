from magic_google import MagicGoogle
import pprint

# Or PROXIES = None
PROXIES = [{
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}]
# export https_proxy= http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
# PROXIES = None

# Or MagicGoogle()
mg = MagicGoogle(PROXIES)

#  Crawling the whole page
# result = mg.search_page(query='python')

# # Crawling url
# for url in mg.search_url(query='python'):
#     pprint.pprint(url)
    


def get_paper_lst():
    data_lst = []
    with open("paper.txt", 'r') as f:
        data_lst = [line.strip() for line in f.readlines()]
    return data_lst

def log(paper_name, url):
    with open("output.log", 'a') as f:
        f.write(f"{paper_name}| {url}\n")

import numpy as np 


paper_lst = get_paper_lst()
print(f"[debug] get {len(paper_lst)} papers")
import time
for _idx, paper in enumerate(paper_lst):
    print(f"[debug] begin work on {paper}, {_idx+1}/{len(paper_lst)}")
    for i in mg.search(query= f"{paper}, pdf", num=1):
        cur_url = i["url"]
        log(paper, cur_url)
        print(f"[debug] get paper from {cur_url}")
    sleep_elapsed = np.random.randint(5)
    print(f"[debug] sleep {sleep_elapsed}")
    time.sleep(sleep_elapsed)
    