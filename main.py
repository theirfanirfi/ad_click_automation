from settings import *
from google_process import Google

# search_keyword = input("Enter the search keyword: ")


f = open("keywords.txt", "r")
search_keywords = f.read().splitlines()
f.close()

f = open("inputs.txt", "r")
inputs = f.read().splitlines()[0].split('\t')
f.close()

site_random = inputs[3]
website = inputs[1]
iter = int(inputs[0])

print('site_random', site_random)
print('website', site_random)
print('iter', iter)

# if len(search_keywords) == 0:
#     print("Please place search keywords one per line in keywords.txt")
#     exit()

# print("Using search keywords")
# print(search_keywords)

# site_random = input("Do you want the ad click to be random? (y/n) ")
if site_random:
    ad_site = None
else:
    ad_site = website


if use_proxy:
    per_proxy = searches_per_proxy
else:
    per_proxy = iter

proxy_count = 0

g = Google()

for _ in range(iter):
    if proxy_count >= per_proxy:
        proxy_count = 0
        g.swap_proxy()

    g.process(search_keywords, ad_site)

    proxy_count += 1

g.close()
