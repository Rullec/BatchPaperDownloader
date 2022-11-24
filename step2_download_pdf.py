import requests
import tqdm
import os.path as osp
import os 
import io
import urllib
from scholarly import ProxyGenerator, scholarly
fail_lst = []
from pdfminer.high_level import extract_text

def validate_pdf(pdf_name):
    try:
        text = extract_text(pdf_name)
        print(f"succ {pdf_name}")
        return True
    except Exception as e:
        print(f"fail to parse pdf as {e}")
        return False


def search_paper(paper):
    try:
        print(f"[debug] begin to get paper info {paper}")
        
        pg = ProxyGenerator()
        pg.FreeProxies()
        print(f"begin to use proxy")
        scholarly.use_proxy(pg)
        print(f"succ to use proxy")
        # print(f"[debug] begin to search for {_idx+1}/{len(papers)}")
        # Now search Google Scholar from behind a proxy
        search_query = next(scholarly.search_pubs(paper))
        # info = search_query
        bib = search_query['bib']
        author = bib["author"]
        year = bib["pub_year"]
        
        print(f"[debug] get {paper} for year {year}")
        return [paper, author, year]
    except Exception as e:
        print(f"fail to get info of {paper}, exception {e}")
        return None


def get_file_from_url(url, pdf_name):
    try:
        new_url = url
        print(f"[debug] get new url {new_url}")
        output_name = f"{pdf_name}.pdf"
        
        return True
    except Exception as e:
        print(f"fail to download from {url}, exception {e}")
        return [url, pdf_name]

def have_this_paper(tar_dir, paper_name):
    for i in os.listdir(tar_dir):
        if i.find(paper_name) and i.endswith(".pdf"):
            return True
    return False

def get_file_from_url_multi(param):
    paper, url_lst = param
    fail_lst = []
    if have_this_paper(".", paper):
        print(f"{paper} exists, ignore")
        return True 
    
    # 1. get paper's author and pub year
    ret = search_paper(paper)
    if ret is not None:
        try:
            _, author_lst, year = ret 
            author = author_lst[0]
            author_surname = author.strip().split(" ")[-1]
            year = int(year)
            output_name = f"{year} - {paper} - {author_surname}.pdf"
        except:
            print(f"fail to parse paper info {ret}")
    
    if osp.exists(output_name):
        print(f"{output_name} exists, ignore")
        return True 
    print(f"[debug] output name {output_name}")

    # 2. begin to download
    
    for url in url_lst:
        succ_download_url = False
        succ_download = False
        try:
            proxy = urllib.request.ProxyHandler({
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890'
            })
            opener = urllib.request.build_opener(proxy)
            urllib.request.install_opener(opener)
            print(f"[debug] try to download {output_name} from {url}...")
            urllib.request.urlretrieve(url, output_name)
            succ_download_url = True 
        except Exception as e :
            print(f"[error] fail to download as {e}")
        ## 2.0 check download succ or not
        if succ_download_url == False:
            continue 
        else:
            ## 2.1 check file size (200KB)
            size_kB = os.stat(output_name).st_size / 1024
            if size_kB < 200:
                succ_download = False
            else:
                ## 2.2 validate pdf file
                if False == validate_pdf(output_name):
                    succ_download = False
                else:
                    succ_download = True 

        if succ_download is True:
            print(f"succ to download paper {paper} from url {url}")
            return  True
        else:
            if osp.exists(output_name):
                os.remove(output_name)
    
    return False

def handle_url(url):
    url = url.strip()
    if url.find("scholar.google.com") != -1:
        st = url.find("url=")
        ed = url.find("&hl")
        return url[st+4:ed]
    else:
        return url

def load_paper_urls(paper_urls):
    paper_lst = {}
    with open(paper_urls, 'r') as f:
        for line in f.readlines():
            paper_name, url = line.strip().split("|")
            url = handle_url(url)
            paper_name = paper_name.strip()

            if paper_name not in paper_lst:
                paper_lst[paper_name] = []
            paper_lst[paper_name].append(url)
    from functools import cmp_to_key
    def mycmp(url0, url1):
        has_pdf0 = url0.find(".pdf") != -1
        has_pdf1 = url1.find(".pdf") != -1
        if has_pdf0 == has_pdf1:
            if url0 < url1:
                return -1
            elif url0 > url1:
                return 1
            else:
                return 0
        else:
            if has_pdf0 == True:
                return -1
            else:
                return 1
    for paper in paper_lst:
        paper_lst[paper].sort(key = cmp_to_key(mycmp))
    return paper_lst

if __name__ == "__main__":
    paper_urls = "paper_url.txt"
    paper_lst = load_paper_urls(paper_urls)
    print(f"[debug] get {len(paper_lst)} papers")
    
    param_lst = []
    for _idx, paper in enumerate(paper_lst):
        urls = paper_lst[paper]
        # print(paper, urls)
        param_lst.append((paper, urls))
    succ_lst = []
    fail_lst = []
    for param in param_lst:
        paper = param[0]
        if get_file_from_url_multi(param):
            succ_lst.append(paper)
        else:
            fail_lst.append(paper)
    
    with open("fail.log", 'w') as f:
        for i in fail_lst:
            f.write(i + "\n")
    print(f"succ download {len(succ_lst)} fail {len(fail_lst)}, record to fail.log")

    # from multiprocessing import Pool
    # with Pool(4) as p:
    #     ret = list(
    #         tqdm.tqdm(p.imap(get_file_from_url_multi, param_lst),
    #                 total=len(param_lst)))
    # print("------fail download info begin------")
    # for i in ret:
    #     if len(i) != 0:
    #         print(i)
    # print("------fail download info end------")