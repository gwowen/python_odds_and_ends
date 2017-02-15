"""
MIT License

Copyright (c) 2017 Gareth Owen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
from bs4 import BeautifulSoup
from collections import Counter

# Get the URL
myurl = input("Please enter a URL: ")

# Get page headers for size info
header_info = requests.head(myurl).headers

#Get content for everything else
content = requests.get(myurl).text

soup =  BeautifulSoup(content, 'lxml')

print("==================================")
print("Report for: " + myurl)
print("==================================")
print("Page title: " + soup.title.string)
print("==================================")

meta_tags = []
print("==================================")
print("Meta tags present:")
for i in soup.find_all('meta'):
    print(i.get('content'))
    meta_tags.append(i.get('content'))
print("==================================")

size_in_kb = float(header_info.get('Content-Length')) * 0.001
print('Page size: ' + str(size_in_kb) + 'kb')

# kill all script and style elements
for script in soup(["script", "style", '[document]','head','title']):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
website_text = '\n'.join(chunk for chunk in chunks if chunk)
page_words = website_text.split()
word_count = Counter(page_words)

# Count words
total_words = 0
unique_words = 0
for key, value in word_count.items():
    total_words += value

    if value == 1:
        unique_words += 1
print("==================================")
print("Total words: " + str(total_words))
print("==================================")
print("Unique words: " + str(unique_words))
print("==================================")

# Find the five most common words
common_dict = dict(word_count)
word_list = [(k, word_count[k]) for k in sorted(word_count, key=word_count.get, reverse=True)]
print("==================================")
print("5 most common words: " +  str(word_list[:5]))
print("==================================")
print("Page links: ")
for i in soup.find_all('a'):
    if i.get("href"):
        if(i.string is not None):
            print("link to: " +i.get("href") + ", text string: " + i.string)
        else:
            print("link to: " +i.get("href"))

print("==================================")

in_page = []
not_in_page = []

# Get all tags in page, and all tags not in page
for i in meta_tags:
    if i in page_words:
        in_page.append(i)
    else:
        not_in_page.append(i)
print("==================================")
print("Meta tags in page: " + str(in_page))
print("==================================")
print("Meta tags not in page" + str(not_in_page))
print("==================================")




