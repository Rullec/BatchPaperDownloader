import requests
import io
import urllib
def get_file_from_url(url, pdf_name):
    # send_headers = {
    #     "User-Agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    #     "Connection": "keep-alive"
    # }
    # req = requests.get(url_file, headers = send_headers)
    # bytes_io = io.BytesIO(req.content)
    # with open("temp.pdf",'wb') as f:
    #     f.write(bytes_io.getvalue())
    # import requests
    # proxies = {'http': 'http://127.0.0.1:7890'}
    # import urllib.request
    # urllib.request.urlretrieve(url, "filename.pdf", proxies=proxies)
    
    proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:7890'})
    # construct a new opener using your proxy settings
    opener = urllib.request.build_opener(proxy)
    # install the openen on the module-level
    urllib.request.install_opener(opener)
    # make a request
    output_name = f"{pdf_name}.pdf"
    print(f"[debug] download {output_name}")
    urllib.request.urlretrieve(url, output_name)

    # url = 'http://www.hrecos.org//images/Data/forweb/HRTVBSH.Metadata.pdf'
    # r = requests.get(url, stream=True)
    # from tqdm import tqdm
    # with open('metadata.pdf', 'wb') as fd:
    #     for chunk in tqdm(r.iter_content(chunk_size)):
    #         fd.write(chunk) 

def load_urls():
    paper_lst = {}
    with open("output1.log", 'r') as f:
        for line in f.readlines():
            # try:
            paper_name, url = line.strip().split("|")
            paper_name = paper_name.strip()
            
            
            if paper_name not in paper_lst:
                paper_lst[paper_name] = [ ]
            paper_lst[paper_name].append(url)

    return paper_lst
paper_lst = load_urls()
print(f"[debug] get {len(paper_lst)} papers")
for _idx, paper in enumerate(paper_lst):
    urls = paper_lst[paper]
    print(f"[debug] begin to work on paper {_idx+1}/{len(paper_lst)}")
    get_file_from_url(paper, urls[0])
        
    break

# 