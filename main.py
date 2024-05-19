import re


def read_file():
    cf = open('Sandbox_config.sbc', 'r')
    sandbox = cf.read()
    mods_pattern = re.compile(r'<Mods>(.*?)</Mods>', re.DOTALL)
    mods_match = mods_pattern.search(sandbox)
    ff = open('parsed_mods.xml', 'w+', encoding='utf-8')
    if mods_match:
        mods_content = mods_match.group(1)
        ff.write(mods_content)


def read_mod_input():
    with open('mods.txt', 'r') as mi:
        mr = mi.readlines()
    with open('parsed_mods.xml', 'r') as pf:
        existing_mods = pf.read()
    existing_mod_ids = set(re.findall(r'<PublishedFileId>(\d+)</PublishedFileId>', existing_mods))
    with open('mods.tmp', 'w+') as mods_object:
        mods_object.write(existing_mods)
        for i in mr:
            remove_searchtext = re.sub(r'&searchtext=.*', '', i)
            mod_id = str(re.findall(r'id=(\d+)', remove_searchtext))
            mod_id = mod_id[2:-2]
            if mod_id not in existing_mod_ids:
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
    if start_index is not None and end_index is not None:
        sandbox_lines = (
            sandbox_lines[:start_index + 1] +  # Include <Mods> tag
            [mods_content] +  # New mods content
            sandbox_lines[end_index:]  # Include </Mods> tag
        )

    with open('Sandbox_config.sbc', 'w') as file:
        file.writelines(sandbox_lines)


def cleanup():
    import os
    os.remove('parsed_mods.xml')
    os.remove('mods.tmp')


if __name__ == '__main__':
    read_file()
    read_mod_input()
    remove_blank_lines('mods.tmp')
    with open('mods.tmp', 'r') as f:
        result = f.read()
    write_file(result)
    cleanup()
    print('MODS WRITTEN TO Sandbox_config.sbc SUCCESSFULLY')
