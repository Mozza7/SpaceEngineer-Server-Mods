import re
import os


def read_file():
    cf = open('Sandbox_config.sbc', 'r')
    sandbox = cf.read()
    # Checks if <Mods /> is present, and if so converts to <Mods>\n</Mods> as required
    sandbox = re.sub(r'<Mods\s*/>', '<Mods>\n  </Mods>', sandbox)
    with open('Sandbox_config.sbc', 'w') as cf:
        cf.write(sandbox)
    # Pulls data from sandbox_config.sbc for existing mods and writes them to a temporary xml file for later usage
    mods_pattern = re.compile(r'<Mods>(.*?)</Mods>', re.DOTALL)
    mods_match = mods_pattern.search(sandbox)
    # Creates a temporary xml file with existing mods inside
    ff = open('parsed_mods.xml', 'w+', encoding='utf-8')
    if mods_match:
        mods_content = mods_match.group(1)
        ff.write(mods_content)
    ff.close()


def read_mod_input():
    # Reads mods.txt and parsed_mods.xml to find any existing mods, and ensure they are not written to avoid duplicates
    with open('mods.txt', 'r') as mi:
        mr = mi.readlines()
    with open('parsed_mods.xml', 'r') as pf:
        existing_mods = pf.read()
    existing_mod_ids = set(re.findall(r'<PublishedFileId>(\d+)</PublishedFileId>', existing_mods))
    with open('mods.tmp', 'w+') as mods_object:
        # Writes existing mods to ensure they remain with all data
        mods_object.write(existing_mods)
        for i in mr:
            # Removes items after the mod ID in a steam link
            remove_searchtext = re.sub(r'&searchtext=.*', '', i)
            mod_id = str(re.findall(r'id=(\d+)', remove_searchtext))
            mod_id = mod_id[2:-2]
            # Only write new mods if items do not already exist
            if mod_id and mod_id not in existing_mod_ids:
                mods_object.write('    <ModItem FriendlyName="*Unknown*">\n'
                                  f'      <Name>{mod_id}.sbm</Name>\n'
                                  f'      <PublishedFileId>{mod_id}</PublishedFileId>\n'
                                  f'      <PublishedServiceName>Steam</PublishedServiceName>\n'
                                  f'    </ModItem>\n')
                existing_mod_ids.add(mod_id)


def remove_blank_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    non_blank_lines = [line for line in lines if line.strip()]
    with open(file_path, 'w') as file:
        file.writelines(non_blank_lines)
    return file


def write_file(mods_content):
    # Writes data to Sandbox_config.sbc from temp files including existing mods from Sandbox_config.sbc
    with open('Sandbox_config.sbc', 'r') as file:
        sandbox_lines = file.readlines()
    start_index = None
    end_index = None
    for i, line in enumerate(sandbox_lines):
        if line.strip() == "<Mods>":
            start_index = i
        elif line.strip() == "</Mods>":
            end_index = i
            break
    # Keeps the data ordered from existing mods to new mods
    if start_index is not None and end_index is not None:
        sandbox_lines = (
            sandbox_lines[:start_index + 1] +
            [mods_content] +
            sandbox_lines[end_index:]
        )
    # Write lines to Sandbox_config.sbc
    with open('Sandbox_config.sbc', 'w') as file:
        file.writelines(sandbox_lines)


def remove_duplicate_lines(file_path):
    # remove duplicate lines from mods.txt
    with open(file_path, 'r') as file:
        lines = file.readlines()
    seen = set()
    unique_lines = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)
    with open(file_path, 'w') as file:
        file.writelines(unique_lines)


def cleanup():
    try:
        os.remove('parsed_mods.xml')
    except FileNotFoundError:
        pass
    try:
        os.remove('mods.tmp')
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    # removes any duplicate lines from mods.txt
    remove_duplicate_lines('mods.txt')
    # Read Sandbox_config.sbc
    read_file()
    # Read mods.txt
    read_mod_input()
    # Remove blank lines from temp mods file (to ensure correct formatting in Sandbox_config.sbc)
    remove_blank_lines('mods.tmp')
    # Read temp mods file to write later
    with open('mods.tmp', 'r') as f:
        result = f.read()
    # Write data from temp mods file
    write_file(result)
    # Cleanup temp files
    cleanup()
    print('MODS WRITTEN TO Sandbox_config.sbc SUCCESSFULLY')
