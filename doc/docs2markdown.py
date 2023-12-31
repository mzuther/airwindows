#!/usr/bin/env python3

import textwrap
import re


input_filename = '../Airwindopedia.txt'
output_filename = 'AirwindoPedia.md'

headers = {}


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


def add_header_ids(contents):
    global headers

    output = ''
    current_h2_id = ''
    header_ids = []

    headers['SurgeSynthesizer'] = ['surge_synthesizer', 'https://surge-synthesizer.github.io/']

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

        header_ids.append(header_id)
        if header_id.startswith('plugins_'):
            header_link = f'#{header_id}'
            headers[header] = [header_id, header_link]

        # https://stackoverflow.com/a/7015050
        output += f'<a name="{header_id}"></a>\n'
        output += f'#{line}' + '\n'

    return output


def add_internal_links(contents):
    link_definitions = ''

    for header in sorted(headers.keys(), key=str.lower):
        _, header_link = headers[header]
        link_definitions += f'[{header}]: {header_link}\n'

    # add guards to headers
    contents = re.sub(r'([#]+) (\w+)', r'\1\2', contents)

    output = ''
    for word in re.split(r'([#]?\w+)', contents):
        if word in headers:
            word = f'[{word}][]'
        output += word

    # remove guards from headers
    output = re.sub(r'([#]+)(\w+)', r'\1 \2', output)

    # add link definitions to end of document
    output += f'\n\n{link_definitions}'
    return output


def clean_whitespace(contents):
    # clean up whitespace before paragraphs
    contents = contents.replace('\n\n\n\n', '\n\n\n')
    contents = contents.replace('\n\n\n\n', '\n\n\n')

    # convert double tabs to code blocks
    contents = contents.replace('\t\t', '    ')

    temp = ''
    for paragraph in contents.splitlines():
        if paragraph:
            temp += textwrap.fill(
                paragraph,
                width=80,
                replace_whitespace=False,
                break_long_words=False,
                drop_whitespace=False,
                break_on_hyphens=False)
        temp += '\n'
    contents = temp

    # remove trailing and leading whitespace
    contents = contents.strip()

    # remove trailing whitespace from lines
    output = ''
    for line in contents.split('\n'):
        output += line.rstrip() + '\n'

    return output


if __name__ == '__main__':
    with open(input_filename, 'r') as f:
        contents = f.read()

    contents = contents.replace('AirwindowsPedia', 'AirwindoPedia')
    contents = contents.replace('Airwindowspedia', 'AirwindoPedia')
    contents = contents.replace('Airwindopedia', 'AirwindoPedia')
    contents = contents.replace('AirwindowPedia', 'AirwindoPedia')

    contents = contents.replace('Hard Vacuum', 'HardVacuum')
    contents = contents.replace('High Impact', 'HighImpact')
    contents = contents.replace('Surge Synthesizer', 'SurgeSynthesizer')

    result = paragraphify(contents)
    result = add_header_ids(result)
    result = add_internal_links(result)
    result = clean_whitespace(result)

    with open(output_filename, 'w') as f:
        print(f'AirwindoPedia: Text -> Markdown...')
        f.write(result)
