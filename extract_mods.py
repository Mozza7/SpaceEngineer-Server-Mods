from main import read_file
import re


def extract_mods():
    sbc, read_data = read_file(sbc_file=None)
    print(read_data)
    mod_id = set(re.findall(r'<PublishedFileId>(\d+)</PublishedFileId>', read_data))
    with open('mods_extracted.txt', 'w+', encoding='utf-8') as f:
        for i in mod_id:
            i = f'https://steamcommunity.com/workshop/filedetails/?id={i}\n'
            f.write(i)


if __name__ == '__main__':
    extract_mods()
