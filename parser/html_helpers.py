from lxml.etree import ElementTree


def get_html_content(html: ElementTree, insert_string=' '):
    text = insert_string.join(html.itertext())
    text = ' '.join(text.split())
    return text
