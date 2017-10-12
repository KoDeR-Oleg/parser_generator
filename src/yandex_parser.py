from lxml import html
from src.Markup import SearchResult, FullPath, Markup, WizardImage


def get_index(parent, tag):
    index = 1
    for child in parent.iterchildren():
        if child == tag:
            return index
        if child.tag == tag.tag:
            index += 1
    return None


def get_path(element):
    path = ""
    while element.tag != "html":
        path = "/" + element.tag + "[" + str(get_index(element.getparent(), element)) + "]" + path
        element = element.getparent()
    path = "//html" + path
    return path


def parse_document(element):
    document = SearchResult()
    document.alignment = "LEFT"
    document.page_url = FullPath(get_path(element) + "/h2/a", "href")
    document.title = FullPath(get_path(element) + "/h2/a", "string")
    document.snippet = FullPath(get_path(element) + "/div[2]/div[1]", "string")
    document.view_url = FullPath(get_path(element) + "/div[1]/div[1]/a[last()]", "href")
    return document


def parse_wizard_image(element):
    wizard = WizardImage()
    wizard.alignment = "LEFT"
    img_list = element.xpath("./div[2]/div/div/div/a")
    for img in img_list:
        wizard.media_links.append(FullPath(get_path(img) + "/div[1]/div[1]", "style"))
    wizard.page_url = FullPath(get_path(element) + "/div[1]/h2/a", "href")
    wizard.title = FullPath(get_path(element) + "/div[1]/h2/a", "string")
    return wizard


def parse_page(file_name):
    with open(file_name, "r") as file:
        tree = html.document_fromstring(file.read())
    markup = Markup()
    markup.file = file_name
    block_list = tree.xpath("//html/body/div[3]/div[1]/div[2]/div[1]/div[1]/ul/li/div")
    for block in block_list:
        result = None
        if len(block.xpath("./div[2]/div[2]")) > 0 and block.xpath("./div[2]/div[2]")[0].text == "реклама":
            continue
        if len(block.xpath("./h2/a")) > 0:
            result = parse_document(block)
            markup.add(result)
        elif len(block.xpath("./div[1]/h2/a")) > 0 and len(block.xpath("./div[2]/div[@class='gallery']")):
            result = parse_wizard_image(block)
            markup.add(result)
    return markup
