import lxml.etree as ET

def parse_mets_url(mets_url):
    r = requests.get(
        mets_url,
        headers={
            "Content-type": "application/xml; charset=utf-8",
            "Accept-Charset": "utf-8",
        },
    )
    try:
        mets = ET.fromstring(r.content.decode("utf-8"))
    except ValueError:
        mets = ET.fromstring(r.content.decode("utf-8").encode("utf-8"))
    return mets
    
    
def make_nsmap(base_nsmap=None):
    """extends given ns-map with mods/mets/xlinks ns"""
    if base_nsmap is None:
        base_nsmap = {}
    nsmap = base_nsmap
    nsmap["mets"] = "http://www.loc.gov/METS/"
    nsmap["mods"] = "http://www.loc.gov/mods/v3"
    nsmap["xlink"] = "http://www.w3.org/1999/xlink"
    return nsmap


def get_title_from_mets(
    mets_url, title_xpaht=".//mods:title/text()", nsmap=make_nsmap()
):
    doc = parse_mets_url(mets_url)
    tree = doc.tree
    mets_title = tree.xpath(title_xpaht, namespaces=nsmap)[0]
    return mets_title


def remove_unresolved_fptrs(doc: ET, nsmap=make_nsmap()):
    """deltes fptr-elemets referencing an id that can't be resolved in doc"""
    # # find all existing fptr FILEID-attribute values
    fptr_target_ids = doc.tree.xpath("//mets:div/mets:fptr/@FILEID", namespaces=nsmap)
    # # find all existing IDs of file-elements
    existing_file_ids = doc.tree.xpath("//mets:fileGrp/mets:file/@ID", namespaces=nsmap)
    for fptr_target_id in fptr_target_ids:
        if fptr_target_id not in existing_file_ids:
            # # remove invalid fptrs
            fptr_element = fptr_target_id.getparent()
            fptr_element.getparent().remove(fptr_element)


def replace_img_urls_in_mets(
    mets_url, replacement_pattern='', nsmap=make_nsmap()
):
    doc = parse_mets_url(mets_url)
    new_uris = []
    for x in doc.tree.xpath(
        ".//mets:fileGrp[@USE='PRESENTATION']//mets:FLocat/@xlink:href",
        namespaces=nsmap,
    ):
        collection_id, image_id = x.split("/")[-2:]
        new_uri = replacement_pattern.format(collection_id, image_id)
        new_uris.append(new_uri)
    for i, x in enumerate(
        doc.tree.xpath(".//mets:fileGrp[@USE='DEFAULT']//mets:FLocat", namespaces=nsmap)
    ):
        x.attrib["{http://www.w3.org/1999/xlink}href"] = new_uris[i]
    remove_unresolved_fptrs(doc)
    return doc.return_byte_like_object().decode("utf-8")
