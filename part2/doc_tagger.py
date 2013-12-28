import os
import sys
import re

#get arguments
path=sys.argv[1]
keywords = sys.argv[2:]

#regex globals
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

#functions for title, author, translator, illustrator
def title(doc):
    title_string = title_search.search(doc)
    if title_string:
        title_string = title_string.group('title')
    return title_string

def author(doc):
    auth = author_search.search(doc)
    if auth:
        auth = auth.group('author')
    return auth

def translator(doc):
    trans = translator_search.search(doc)
    if trans:
        trans = trans.group('translator')
    return trans

def illustrator(doc):
    ill = illustrator_search.search(doc)
    if ill:
        ill = ill.group('illustrator')
    return ill

def keyword_counts(doc):
#return dictionary with counts of all keywords for doc
    counts = {}
    content_pattern = re.compile(r'''
                                 ([*][*][*]\ ?START.*?[*][*]+) #start of text
                                 (.*)                           #body of text
                                 ([*][*][*]\ ?END.*?[*][*]+)   #end of text
                                 ''', re.IGNORECASE|re.DOTALL|re.VERBOSE)
    content_body = content_pattern.search(doc).group(2)  
    for keyword in keywords:
    
        #pattern for searching the actual body
        keyword_pattern = re.compile(r'\b{}\b'.format(keyword),re.IGNORECASE)
        matches = keyword_pattern.findall(content_body)
        num_matches = len(matches)
        counts[keyword] = num_matches
    return counts





#actual script
text_files = [doc for doc in os.listdir(path) if doc[-4:] == '.txt']
for file_name in text_files:

    #get text for gutenberg doc
    file_path = os.path.join(path,file_name)
    with open(file_path,'r') as file:
        text = file.read()
    
    print '***'*25
    print 'The title of the text is {}'.format(title(text))
    print 'The author is {}'.format(author(text))
    print 'The translator is {}\n'.format(translator(text))
    
    
    counts = keyword_counts(text)
    print "Here's the counts for the keywords you searched for:"
    for keyword in keywords:
        print '"{}" : {}'.format(keyword,counts[keyword])
    
    