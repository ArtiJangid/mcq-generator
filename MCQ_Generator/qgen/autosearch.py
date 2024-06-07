def autosearch(search):
    try:
        import wikipedia
        return wikipedia.page(search).content
    except:
        return "Page Not Found"