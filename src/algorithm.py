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


def extract_xpath(xpath):
    extract_list = xpath.split("/")
    while extract_list[0] == "":
        extract_list = extract_list[1:]
    for i in range(len(extract_list)):
        if extract_list[i][-1] != "]":
            extract_list[i] = (extract_list[i], 0)
        else:
            tlist = extract_list[i].split("[")
            extract_list[i] = (tlist[0], int(tlist[1][:-1]))
    return extract_list


def combine_xpath(extract_list):
    xpath = ""
    if extract_list[0][0] == "html":
        xpath = "/"
    for item in extract_list:
        xpath += "/" + item[0]
        if item[1] > 0:
            xpath += "[" + str(item[1]) + "]"
    return xpath


def great_common_prefix(xpath1, xpath2):
    common_list = []
    for i in range(min(len(xpath1), len(xpath2))):
        if xpath1[i][0] != xpath2[i][0]:
            break
        if xpath1[i][1] == xpath2[i][1]:
            common_list.append(xpath1[i])
        else:
            common_list.append((xpath1[i][0], 0))
    return common_list


def parse_document(element, block_xpath, sample):
    document = SearchResult()
    document.alignment = "LEFT"

    block_xpath = extract_xpath(block_xpath)

    page_url_xpath = extract_xpath(sample.page_url.xpath)[len(block_xpath):]
    document.page_url = FullPath(get_path(element) + combine_xpath(page_url_xpath), sample.page_url.attr)

    title_xpath = extract_xpath(sample.title.xpath)[len(block_xpath):]
    document.title = FullPath(get_path(element) + combine_xpath(title_xpath), sample.title.attr)

    snippet_xpath = extract_xpath(sample.snippet.xpath)[len(block_xpath):]
    document.snippet = FullPath(get_path(element) + combine_xpath(snippet_xpath), sample.snippet.attr)

    view_url_xpath = extract_xpath(sample.view_url.xpath)[len(block_xpath):]
    document.view_url = FullPath(get_path(element) + combine_xpath(view_url_xpath), sample.view_url.attr)
    return document


def parse_wizard_image(element, block_xpath, sample):
    wizard = WizardImage()
    wizard.alignment = "LEFT"

    block_xpath = extract_xpath(block_xpath)

    inner_xpath = extract_xpath(sample.media_links[0].xpath)
    for img in sample.media_links:
        inner_xpath = great_common_prefix(inner_xpath, extract_xpath(img.xpath))
    inner_xpath = combine_xpath(inner_xpath[len(block_xpath):])

    img_list = element.xpath("." + inner_xpath)
    for img in img_list:
        wizard.media_links.append(FullPath(get_path(img), sample.media_links[0].attr))

    page_url_xpath = extract_xpath(sample.page_url.xpath)[len(block_xpath):]
    wizard.page_url = FullPath(get_path(element) + combine_xpath(page_url_xpath), sample.page_url.attr)

    title_xpath = extract_xpath(sample.title.xpath)[len(block_xpath):]
    wizard.title = FullPath(get_path(element) + combine_xpath(title_xpath), sample.title.attr)
    return wizard


def parse_page(file_name, markup_list):
    with open(file_name, "r") as file:
        tree = html.document_fromstring(file.read())
    result_markup = Markup()
    result_markup.file = file_name

    block_xpath = extract_xpath(markup_list[0].components[0].title.xpath)
    document_xpath = []
    sample_document = None
    wizard_xpath = []
    sample_wizard = None
    for markup in markup_list:
        for component in markup.components:
            block_xpath = great_common_prefix(block_xpath, extract_xpath(component.title.xpath))
            if component.type == "SEARCH_RESULT":
                if document_xpath == []:
                    document_xpath = extract_xpath(component.title.xpath)
                    sample_document = component
                else:
                    document_xpath = great_common_prefix(document_xpath, extract_xpath(component.title.xpath))
            if component.type == "WIZARD":
                if wizard_xpath == []:
                    wizard_xpath = extract_xpath(component.title.xpath)
                    sample_wizard = component
                else:
                    wizard_xpath = great_common_prefix(wizard_xpath, extract_xpath(component.title.xpath))

    document_xpath = combine_xpath(document_xpath[len(block_xpath):])
    wizard_xpath = combine_xpath(wizard_xpath[len(block_xpath):])
    block_xpath = combine_xpath(block_xpath)

    block_list = tree.xpath(block_xpath)
    for block in block_list:
        if len(block.xpath("." + document_xpath)) > 0:
            result = parse_document(block, block_xpath, sample_document)
            result_markup.add(result)
        elif len(block.xpath("." + wizard_xpath)) > 0:
            result = parse_wizard_image(block, block_xpath, sample_wizard)
            result_markup.add(result)
    return result_markup
