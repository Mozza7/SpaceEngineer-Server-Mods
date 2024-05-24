import requests
from bs4 import BeautifulSoup


def import_steam(steam_collection):
    response = requests.get(steam_collection)

    soup = BeautifulSoup(response.content, 'lxml')

    collection_items = ('html.responsive body.apphub_blue.responsive_page div.responsive_page_frame.with_header '
                        'div.responsive_page_content div#responsive_page_template_content.responsive_page_template_content '
                        'div#ig_bottom.smallheader.nobg div#mainContentsCollection div#sharedfiles_content_ctn '
                        'div#profileBlock.clearfix.collection div.detailBox div.collectionChildren')

    elements = soup.select(collection_items + ' a')
    urls = [element.get('href') for element in elements]

    duplicate_url = []
    mods_file = open('mods.txt', 'w+', encoding='utf-8')
    for url in urls:
        if url is None:
            pass
        elif 'appid' in url:
            # This will not be a correct url
            pass
        else:
            if url in duplicate_url:
                # Response usually brings back 2 of each entry, this eliminates that chance
                pass
            else:
                mods_file.write(f'{url}\n')
                duplicate_url.append(url)
    return 'Steam collection written to mods.txt'
