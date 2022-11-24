# Introduction

Given a list of paper names, `BatchPaperDownloader` try to search their pdf versions on google and download.

It's still very naive, and cannot expect too much on it. Further more improvement can be made later.

# Usage

1. Write paper names that you have interests on in `paper_name.txt`. One paper per line, such as :

   ```
   A novel discretization and numerical solver for non-fourier diffusion
   Anisotropic elasticity for inversion-safety and element rehabilitation
   Computational design and fabrication of soft pneumatic objects with desired deformations
   ```

2. Run `step1_get_paper_links.py`. This script will read `paper_name.txt` and try to get their pdf URL on google. The searched URLs are stored in `paper_url.txt`.

3. Run `step2_download_pdf.py`. It will download potential pdfs from recorded `paper_url.txt`. You will get many papers pdfs in current directory if it works!

4. Check `fail.log` and you can find the failure cases. You can download these failure cases manually.
