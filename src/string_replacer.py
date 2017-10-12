from bs4 import BeautifulSoup
import json


def get_obj_attr(obj, attr):
    string = "obj" + attr
    return eval(string)


def get_data_from_tag(tag, structure):
    if structure[2] == "string":
        return tag.string
    if structure[2] == "['href']":
        return get_obj_attr(tag, structure[2])
    if structure[2] == "strings":
        res = ""
        for string in tag.stripped_strings:
            res += string + " "
        return res
    if structure[2] == "inner":
        obj = json.loads(tag.string)
        return get_obj_attr(obj, structure[3])
    return "I don\'t know"


def dfs(tag, path):
    for child in tag.children:
        if path[0][0] == child.name and path[0][1] == child.attrs:
            if len(path) == 1:
                return get_data_from_tag(child, path[0])
            else:
                res = dfs(child, path[1:])
                if res is not None:
                    return res
    return None


def schema_to_string(soup, string, debug_output=False):
    path = string.split(" <$> ")
    for i in range(len(path)):
        path[i] = path[i].split(" <@> ")
        path[i][1] = json.loads(path[i][1])
    tag = soup.find("body")
    res = dfs(tag, path[3:])
    if debug_output:
        print(res)
    return res


def schema_document_to_str(soup, component, debug_output=False):
    component['page-url'] = schema_to_string(soup, component['page-url'], debug_output)
    component['title'] = schema_to_string(soup, component['title'], debug_output)
    component['snippet'] = schema_to_string(soup, component['snippet'], debug_output)
    component['view-url'] = schema_to_string(soup, component['view-url'], debug_output)


def schema_wizard_to_str(soup, component, debug_output=False):
    component['page-url'] = schema_to_string(soup, component['page-url'], debug_output)
    component['title'] = schema_to_string(soup, component['title'], debug_output)
    for link in component['media-links']:
        link['url'] = schema_to_string(soup, link['url'], debug_output)


def schema_page_to_string(file_handle, dump, debug_output=False):
    soup = BeautifulSoup(file_handle, "html.parser")
    components = json.loads(dump)
    for one in components:
        if one["type"] == "SEARCH_RESULT":
            schema_document_to_str(soup, one, debug_output)
        if one["type"] == "WIZARD":
            schema_wizard_to_str(soup, one, debug_output)
        if debug_output:
            print("\n=========\n")
    return components


def main():
    with open("./google/3.html", "r") as page, open("schema.txt", "r") as dump:
        components = schema_page_to_string(page, dump.read(), True)

    with open("result.txt", "w") as fo:
        fo.write(json.dumps(components, sort_keys=False, indent=4))


if __name__ == "__main__":
    main()
