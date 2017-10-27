from lxml import html
from markup import MarkupSearchResult, FullPath, MarkupWizardImage, Markup
from ideal_parser import IdealParser
from algorithm import Algorithm


class PrimitiveAlgorithm(Algorithm):
    def __init__(self):
        self.sample_document = None
        self.sample_wizard = None
        self.block_xpath = None
        self.document_xpath = None
        self.wizard_xpath = None

    def get_index(self, parent, tag):
        index = 1
        for child in parent.iterchildren():
            if child == tag:
                return index
            if child.tag == tag.tag:
                index += 1
        return None

    def get_path(self, element):
        path = ""
        while element.tag != "html":
            path = "/" + element.tag + "[" + str(self.get_index(element.getparent(), element)) + "]" + path
            element = element.getparent()
        path = "//html" + path
        return path

    def extract_xpath(self, xpath):
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

    def combine_xpath(self, extract_list):
        xpath = ""
        if len(extract_list) > 0 and extract_list[0][0] == "html":
            xpath = "/"
        for item in extract_list:
            xpath += "/" + item[0]
            if item[1] > 0:
                xpath += "[" + str(item[1]) + "]"
        return xpath

    def great_common_prefix(self, xpath1, xpath2):
        common_list = []
        for i in range(min(len(xpath1), len(xpath2))):
            if xpath1[i][0] != xpath2[i][0]:
                break
            if xpath1[i][1] == xpath2[i][1]:
                common_list.append(xpath1[i])
            else:
                common_list.append((xpath1[i][0], 0))
        return common_list

    def parse_document(self, element, block_xpath, sample):
        document = MarkupSearchResult()
        document.alignment = "LEFT"

        block_xpath = self.extract_xpath(block_xpath)

        page_url_xpath = self.extract_xpath(sample.page_url.xpath)[len(block_xpath):]
        document.page_url = FullPath(self.get_path(element) + self.combine_xpath(page_url_xpath), sample.page_url.attr)

        title_xpath = self.extract_xpath(sample.title.xpath)[len(block_xpath):]
        document.title = FullPath(self.get_path(element) + self.combine_xpath(title_xpath), sample.title.attr)

        snippet_xpath = self.extract_xpath(sample.snippet.xpath)[len(block_xpath):]
        document.snippet = FullPath(self.get_path(element) + self.combine_xpath(snippet_xpath), sample.snippet.attr)

        view_url_xpath = self.extract_xpath(sample.view_url.xpath)[len(block_xpath):]
        document.view_url = FullPath(self.get_path(element) + self.combine_xpath(view_url_xpath), sample.view_url.attr)
        return document

    def parse_wizard_image(self, element, block_xpath, sample):
        wizard = MarkupWizardImage()
        wizard.alignment = "LEFT"

        block_xpath = self.extract_xpath(block_xpath)

        inner_xpath = self.extract_xpath(sample.media_links[0].xpath)
        for img in sample.media_links:
            inner_xpath = self.great_common_prefix(inner_xpath, self.extract_xpath(img.xpath))
        inner_xpath = self.combine_xpath(inner_xpath[len(block_xpath):])

        img_list = element.xpath("." + inner_xpath)
        for img in img_list:
            wizard.media_links.append(FullPath(self.get_path(img), sample.media_links[0].attr))

        page_url_xpath = self.extract_xpath(sample.page_url.xpath)[len(block_xpath):]
        wizard.page_url = FullPath(self.get_path(element) + self.combine_xpath(page_url_xpath), sample.page_url.attr)

        title_xpath = self.extract_xpath(sample.title.xpath)[len(block_xpath):]
        wizard.title = FullPath(self.get_path(element) + self.combine_xpath(title_xpath), sample.title.attr)
        return wizard

    def learn(self, markup_list):
        self.block_xpath = self.extract_xpath(markup_list[0].components[0].title.xpath)
        self.document_xpath = []
        self.sample_document = None
        self.wizard_xpath = []
        self.sample_wizard = None
        for markup in markup_list:
            for component in markup.components:
                self.block_xpath = self.great_common_prefix(self.block_xpath, self.extract_xpath(component.title.xpath))
                if component.type == "SEARCH_RESULT":
                    if self.document_xpath == []:
                        self.document_xpath = self.extract_xpath(component.title.xpath)
                        self.sample_document = component
                    else:
                        self.document_xpath = self.great_common_prefix(self.document_xpath,
                                                                       self.extract_xpath(component.title.xpath))
                if component.type == "WIZARD":
                    if self.wizard_xpath == []:
                        self.wizard_xpath = self.extract_xpath(component.title.xpath)
                        self.sample_wizard = component
                    else:
                        self.wizard_xpath = self.great_common_prefix(self.wizard_xpath,
                                                                     self.extract_xpath(component.title.xpath))

        self.document_xpath = self.combine_xpath(self.document_xpath[len(self.block_xpath):])
        self.wizard_xpath = self.combine_xpath(self.wizard_xpath[len(self.block_xpath):])
        self.block_xpath = self.combine_xpath(self.block_xpath)
        return self

    def parse(self, file_name):
        with open(file_name, "r") as file:
            tree = html.document_fromstring(file.read())
        result_markup = Markup()
        result_markup.file = file_name

        block_list = tree.xpath(self.block_xpath)
        for block in block_list:
            if len(block.xpath("." + self.document_xpath)) > 0:
                result = self.parse_document(block, self.block_xpath, self.sample_document)
                result_markup.add(result)
            elif len(block.xpath("." + self.wizard_xpath)) > 0:
                result = self.parse_wizard_image(block, self.block_xpath, self.sample_wizard)
                result_markup.add(result)

        ideal = IdealParser()
        return ideal.get_substitution(result_markup)
