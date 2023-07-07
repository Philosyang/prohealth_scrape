from bs4 import BeautifulSoup
import urllib.request
import time

with open('out.csv', mode='w', encoding="utf-8") as file:
    file.write(
        'name, link, price, rating, review_count, Anti-Inflammatory Support, Antioxidant Health, Blood Sugar Support, Body, Bone Health, Brain Health, Cellular Health, DNA Health, Detoxification, Fertility Support, Gut Health, Healthy Aging, Healthy Metabolism, Heart Health, Improved Energy, Joint Health, Liver Support, Mood Support, Muscle Health, Skin Health, Soul, Stress Management'
    )
    file.write('\n')

page_count = 4

for i in range(1, page_count+1):

    page = urllib.request.urlopen(
        'https://www.prohealth.com/collections/all?page=' + str(i))
    pr = page.read()

    soup = BeautifulSoup(pr, 'html.parser')
    sp = soup.prettify()

    # path_w = 'temp.html'
    # with open(path_w, mode='w', encoding="utf-8") as f:
    #     f.write(sp)

    # temp_formatted.html:

    # name & href
    # <div class="product-grid--title" data-block-type="product_card_title">
    base_url = 'https://www.prohealth.com'  # needed for proper product href

    # price
    # <span class="money">

    # star count
    # <div class="jdgm-prev-badge" data-average-rating="

    # review count
    # <span class="jdgm-prev-badge__text">

    # product name, product link, price, star count, review count

    # print(soup.body)    # correct
    # <div data-cart-action="page" data-editor-open="false" data-language-url="/" id="PageContainer">

    # cut the page
    # print(sp)   # good
    # print(type(sp)) # <class 'str'>

    # print(sp[sp.index('<div data-cart-action="page" data-editor-open="false" data-language-url="/" id="PageContainer">'): sp.index('<div class="footer-wrapper">')])    # good, = temp_formatted_v2.html
    items = sp[sp.index('<div data-cart-action="page" data-editor-open="false" data-language-url="/" id="PageContainer">')
                        :sp.index('<div class="footer-wrapper">')]

    # print(items[items.index('<div class="grid-area--collection"'):])  # good, = temp_formatted_v3.html
    collection = items[items.index(
        '<div class="product-grid--title" data-block-type="product_card_title">'):]

    clist = collection.split(
        '<div class="product-grid--title" data-block-type="product_card_title">')
    # print(clist[0])
    # print(clist[1])
    # print(clist[-1])

    out_list = []
    # print(clist)
    for item in clist:
        if len(item) < 2:
            continue

        ci = item.replace('\n', '')
        # print(ci)
        latter_url = ci[ci.index('/collections'):ci.index('">')]

        item_name = ci[ci.index('">')+len('">')
                                :ci.index('</a>')].strip().replace(',', '')

        item_rating = float(ci[ci.index('data-average-rating="') +
                            len('data-average-rating="'):ci.index('" data-number-of-questions')])

        item_review_count = int(ci[ci.index('data-number-of-reviews="') +
                                len('data-number-of-reviews="'):ci.index('style="display:none"')].strip()[:-1])

        ipt = ci[ci.index('<span class="money">') +
                 len('<span class="money">'):ci.index('<div class="unit-price hide"')].strip()
        # $58.00    </span>
        item_price = float(ipt[ipt.index('$') + len('$'):ipt.index('</span>')].strip().replace(',', ''))

        # name, link, price, rating, review_count
        out_list.append([item_name, base_url+latter_url,
                        item_price, item_rating, item_review_count])

    # print(out_list)
    for item in out_list:
        with open('out.csv', mode='a', encoding="utf-8") as file:
            file.write(str(item)[1:-1].replace('\'', ''))
            file.write(', 0' * 22)
            file.write('\n')

    if i < page_count:
        print('sleep 5 seconds before next scrape...')
        time.sleep(5)
