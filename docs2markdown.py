#!/usr/bin/env python3

input_filename = 'Airwindopedia.txt'
output_filename = 'AirwindoPedia.md'


def paragraphify(contents):
    output = ''
    for n, paragraph in enumerate(contents.split('############ ')):
        if n == 0:
            introduction, categories = paragraph.split('# Categories', maxsplit=1)

            # leading space simplifies adding header IDs
            output = '\n# AirwindoPedia\n\n'
            output += f'{introduction}\n\n'
            output += '## Categories\n'

            for subparagraph in categories.split('\n'):
                if not subparagraph:
                    continue

                category, plugins = subparagraph.split(': ', maxsplit=1)
                output += f'### {category}\n\n'
                output += f'{plugins}\n\n'

            output += '\n## Plugins'
        else:
            title, paragraph = paragraph.split('\n', maxsplit=1)
            header = title.split(' ', maxsplit=1)[0]
            output += f'\n### {header}\n'
            output += f'\n_{title}_\n'

            conclusion_start = 'This concludes the Airwindo'
            if paragraph.find(conclusion_start) != -1:
                paragraph = paragraph.replace(conclusion_start, f'## Conclusion\n\n{conclusion_start}')
                paragraph = paragraph.replace('-chris', '_-chris_')

            output += paragraph

    return output


header_ids = {}

def add_header_ids(contents):
    global header_ids

    output = ''
    current_h2_id = ''
    for line in contents.split('\n#'):
        if not line:
            continue

        header = line.split('\n', maxsplit=1)[0]
        header_level, header = header.split(' ', maxsplit=1)

        header_id = header.translate(str.maketrans(' -', '__'))
        header_id = header_id.lower()

        header_id_test = header_id.replace('_', '')
        assert header_id_test.isalnum(), f'header ID "{header_id}" is invalid'

        # prevent duplicate header IDs
        header_level = len(header_level.strip()) + 1
        if header_level == 2:
            current_h2_id = header_id
        elif header_level > 2:
            header_id = f'{current_h2_id}_{header_id}'

        assert header_id not in header_ids, f'duplicate header "{header_id}"'
        header_ids[header_id] = header

        # https://stackoverflow.com/a/7015050
        output += f'<a name="{header_id}"></a>\n'
        output += f'#{line}' + '\n'

    return output


def clean_whitespace(contents):
    # clean up whitespace before paragraphs
    contents = contents.replace('\n\n\n\n', '\n\n\n')
    contents = contents.replace('\n\n\n\n', '\n\n\n')

    # convert double tabs to code blocks
    contents = contents.replace('\t\t', '    ')

    # remove trailing and leading whitespace
    contents = contents.strip()

    # remove trailing whitespace from lines
    output = ''
    for line in contents.split('\n'):
        output += line.rstrip() + '\n'

    return output


if __name__ == '__main__':
    print()
    with open(input_filename, 'r') as f:
        contents = f.read()

    result = paragraphify(contents)

    result = result.replace('AirwindowsPedia', 'AirwindoPedia')
    result = result.replace('Airwindowspedia', 'AirwindoPedia')
    result = result.replace('Airwindopedia', 'AirwindoPedia')
    result = result.replace('AirwindowPedia', 'AirwindoPedia')

    result = add_header_ids(result)
    result = clean_whitespace(result)

    with open(output_filename, 'w') as f:
        print(f'Writing "{output_filename}" ...')
        f.write(result)

    print('Done.')
    print()
