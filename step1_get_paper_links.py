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
    


def get_paper_lst(paper_name_lst):
    data_lst = []
    with open(paper_name_lst, 'r') as f:
        data_lst = [line.strip() for line in f.readlines()]
    return data_lst


def log(output_paper_url, paper_name, url):
    with open(output_paper_url, 'a') as f:
        f.write(f"{paper_name}| {url}\n")

import numpy as np

def is_downloadable(url):
    if url.find("dl.acm.org") != -1 or url.find("researchgate") != -1 or url.find("youtube") != -1:
        return False
    else:
        return True

def get_url(paper_name, selection = 5):
    urls = [i['url'] for i in mg.search(query= f"{paper_name}, pdf download", num=selection)]
    ok_urls = []
    for i in urls:
        if is_downloadable(i):
            print(f"{i} is ok")
            ok_urls.append(i)
    return ok_urls
        
        
if __name__ == "__main__":
    paper_input = "paper_name.txt"
    output_paper_url = "paper_url.txt"

    paper_lst = get_paper_lst(paper_input)
    print(f"[debug] get {len(paper_lst)} papers")
    import time
    for _idx, paper in enumerate(paper_lst):
        print(f"[debug] begin work on {paper}, {_idx+1}/{len(paper_lst)}")
        ok_urls = get_url(paper)
        for url in ok_urls:
            log(output_paper_url, paper, url)
        
        sleep_elapsed = np.random.randint(5)
        print(f"[debug] sleep {sleep_elapsed}")
        time.sleep(sleep_elapsed)
        