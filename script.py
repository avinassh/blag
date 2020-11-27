import os
import sys
import re
from datetime import datetime
import pytz


def replace_meta(content: str):
    # all meta has to be between ---, so lets append that
    content = '---\n' + content
    # match and replace the `Title: <something>` to `title = "<something>"`
    content = re.sub(r'Title: *(.*)\n', r'title: "\1"\n', content)
    # match and replace the `Slug: <something>` to `slug = "<something>"`
    content = re.sub(r'Slug: *(.*)\n', r'slug: "\1"\n', content)
    # match and replace the `FacebookImage: <something>` to `image = "<something>"`
    content = re.sub(r'FacebookImage: *(.*)\n', r'image: "\1"\n', content)

    # to replace Date and Modified, we need to first get the string, parse it and convert it
    # to the format golang wants
    date_regex = re.compile(r'Date: *(?P<date> .*)\n')
    # date_search = date_regex.search(content)
    if match := date_regex.search(content):
        date = match.groupdict().get('date')
        # the date format is like `2016-02-19 23:03`
        date_time = datetime.strptime(date.strip(), '%Y-%m-%d %H:%M').astimezone(pytz.timezone('Asia/Kolkata'))
        content = date_regex.sub(F'date: "{date_time.isoformat()}"\n', content)

    # same like Date, but for Modified
    modified_regex = re.compile(r'Modified: *(?P<date> .*)\n')
    if match := modified_regex.search(content):
        date = match.groupdict().get('date')
        # the date format is like `2016-02-19 23:03`
        date_time = datetime.strptime(date.strip(), '%Y-%m-%d %H:%M').astimezone(pytz.timezone('Asia/Kolkata'))
        content = modified_regex.sub(F'lastmod: "{date_time.isoformat()}"\n', content)

    categories_regex = re.compile(r'Category: *(?P<category> .*)\n')
    if match := categories_regex.search(content):
        categories = match.groupdict().get('category')
        replacement_string = ', '.join([F'"{s.strip().lower()}"' for s in categories.split(',')])
        content = categories_regex.sub(F'categories: [{replacement_string}]\n', content)

    tags_regex = re.compile(r'Tags: *(?P<tags> .*)\n')
    if match := tags_regex.search(content):
        tags = match.groupdict().get('tags')
        replacement_string = ', '.join([F'"{s.strip().lower()}"' for s in tags.split(',')])
        content = tags_regex.sub(F'tags: [{replacement_string}]\n', content)

    # same like how the title was replaced. We will also append it `---` to close the meta
    # block
    content = re.sub(r'Summary: *(.*)\n', r'description: "\1"\n---\n', content)
    return content


def convert(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.md'):
                file = os.path.join(root, name)
                print(file)
                with open(file, 'r') as f:
                    updated_content = replace_meta(f.read())
                with open(file, 'w') as f:
                    f.write(updated_content)


if __name__ == '__main__':
    convert(sys.argv[1])
