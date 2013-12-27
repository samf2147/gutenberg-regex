import re
import sys
from pg_sample_texts import DIV_COMM, MAG_CART

docs = [DIV_COMM, MAG_CART]

#regexes for title, author, translator, illustrator
title_search = re.compile(r'''
(title:\s*)         #title, with optional whitespace after
(?P<title>          #group name
.*                  #first line of title can have anything
(\n.*\w.*)*         #subsequent lines have at least one alphanumeric character.  
                    #we can have arbitrarily many lines in the title
)
''', re.IGNORECASE|re.VERBOSE)
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)
illustrator_search = re.compile(r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)

keywords = sys.argv[1:]

for i,doc in enumerate(docs):
    print "***" * 25
    print 'Here\'s the info for document {}'.format(i)
    
    #title, author, translator info
    title = re.search(title_search, doc).group('title')
    author = re.search(author_search, doc)
    translator = re.search(translator_search, doc)
    illustrator = re.search(illustrator_search, doc)
    if author: 
        author = author.group('author')
    if translator:
        translator = translator.group('translator')
    if illustrator:
        illustrator = illustrator.group('illustrator')
    print "Title:  {}".format(title)
    print "Author(s): {}".format(author)
    print "Translator(s): {}".format(translator)
    print "Illustrator(s): {}".format(illustrator)
    print "\n"
    
    #keyword info
    print 'Here are the counts for your keywords:'
    for keyword in keywords:
        pattern = re.compile(r'\b' + keyword + r'\b', re.IGNORECASE)
        num_matches = len(pattern.findall(doc))
        print '"{}" : {}'.format(keyword, num_matches)
    
    

