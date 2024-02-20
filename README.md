# mirror-webnode
This python script performs a mirror/copy of webpages that are listed on a provided file. This is intended to work better with WEBNODE.COM hosted sites. A copy of listed files are provided in the desired folder WITH the copy of the external resources (so it may be a bit cumbersome, tens of Megs).
The output folder is automatically ZIP-compressed to a file named "PREFIX 202402 webnode site.zip" where 202402 is current time in YYYYMM

Webnode is used in few high school textbooks as an example for web sites design tools. This script permits to store the student works for future reference.

You need: Python3 and the wget command. 

**Command usage:**

usage: download.py [-h] filename name_prefix [dest_folder]

positional arguments:
  filename     Name of the file containing the list of site URLs
  name_prefix  Prefix to add to zip archive name, e.g. it can be one
               class name
  dest_folder  Optional, Cartella di destinazione per le immagini dei siti,
               default: 'mirror' folder in the current execution path
  num_threads  Optional, Number of threads, downloads N sites at same
               time.default: 4
  num_levels   Optional, Number of site levels to dig in (and external
               links/resources).default: 1

options:
  -h, --help   show this help message and exit

**Issues:**
- The Copy is not Perfect, iframes may not be replicated, so you lost the integrated maps and so on.
- I have removed the cookies preference panel from the downloaded HTMLs... it is rougth but it works.
- I have chosen resonable wget options, in case you find better options, please send pull requests or let's post an issue
- YOU need wget in path, so it is a bit simpler to use under linux
