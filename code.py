import codecs

def remove_bom_from_csv(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    content_no_bom = content.replace('\ufeff', '')

    with codecs.open(filename, 'w', encoding='utf-8') as file:
        file.write(content_no_bom)

