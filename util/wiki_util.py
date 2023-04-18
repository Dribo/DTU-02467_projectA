
def hyperlink_cleanup(str_link, language):
    link_prefix = f"https://{language}.wikipedia.org"
    if "/wiki/" in str_link:
        out = link_prefix + str_link
        if '#' in out:
            out = out.split('#')[0]
        if 'Wikipedia' in out:
            return False
        if 'Template' in out:
            return False
        return out
    else:
        return False


