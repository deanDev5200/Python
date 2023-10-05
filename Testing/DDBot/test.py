import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('DDBot (deanhebat.id@gmail.com)', 'id')

page_py = wiki_wiki.page('Joko Widodo')
print("Page - Exists: %s" % page_py.exists())
# Page - Exists: True

page_missing = wiki_wiki.page('NonExistingPageWithStrangeName')
print("Page - Exists: %s" %     page_missing.exists())

print("Page - Title: %s" % page_py.title)
# Page - Title: Python (programming language)

print("Page - Summary: %s" % page_py.summary)
# Page - Summary: Python is a widely used high-level programming language for