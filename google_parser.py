from bs4 import BeautifulSoup, element
import json


def get_path(tag):
    path = tag.name + " <@> " + json.dumps(tag.attrs)
    for parent in tag.parents:
        path = parent.name + " <@> " + json.dumps(parent.attrs) + " <$> " + path
    return path


def parse_document(tag):
    document = dict()
    document["type"] = "SEARCH_RESULT"
    document["alignment"] = "LEFT"
    document["page-url"] = get_path(tag.h3.a) + " <@> ['href']"
    document["title"] = get_path(tag.h3.a) + " <@> string"
    document["snippet"] = get_path(tag.find("span", {"class": "st"})) + " <@> strings"
    document["view-url"] = get_path(tag.find("cite")) + " <@> string"
    return document


def parse_wizard_image(tag):
    wizard = dict()
    wizard["type"] = "WIZARD"
    wizard["alignment"] = "LEFT"
    wizard["media-links"] = list()
    for link in tag.find("div", {"class": "rg_ul"}).contents:
        if type(link) == element.Tag:
            wizard["media-links"].append({"url": get_path(link.contents[1]) + " <@> inner <@> ['ou']"})
    wizard["wizard-type"] = "WIZARD_IMAGE"
    wizard["page-url"] = get_path(tag.find("a")) + " <@> ['href']"
    wizard["title"] = get_path(tag.find("a")) + " <@> string"
    return wizard


def parse_page(file_handle):
    soup = BeautifulSoup(file_handle, "html.parser")
    components = list()

    for gclass in soup.find_all("div", {"class": "g"}):
        if gclass.find("div", {"class": "rc"}):
            components.append(parse_document(gclass.find("div", {"class": "rc"})))
        if gclass.get("id") == "imagebox_bigimages":
            components.append(parse_wizard_image(gclass))
    dump = json.dumps(components)
    beauty_dump = json.dumps(components, sort_keys=False, indent=4)
    print(beauty_dump)
    return dump


def main():
    with open("./google/3.html", "r") as file:
        dump = parse_page(file)

    with open("schema.txt", "w") as fo:
        fo.write(dump)


if __name__ == "__main__":
    main()
