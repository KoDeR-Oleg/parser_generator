class Parser(object):
    @staticmethod
    def get_index(parent, tag):
        index = 1
        for child in parent.iterchildren():
            if child == tag:
                return index
            if child.tag == tag.tag:
                index += 1
        return None

    @staticmethod
    def get_path(element):
        path = ""
        while element.tag != "html":
            path = "/" + element.tag + "[" + str(Parser.get_index(element.getparent(), element)) + "]" + path
            element = element.getparent()
        path = "//html" + path
        return path

    @staticmethod
    def get_markup(self, file_name):
        pass

    @staticmethod
    def get_analysis(self, file_name):
        return self.get_markup(file_name).get_substitution()
