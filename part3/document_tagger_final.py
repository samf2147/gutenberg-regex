import re
import os
import sys

#global regex objects that will be reused by the functions
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


#file handling functions
def file_paths(directory):
    ''' Return the full paths for the text files in the directory'''
    file_names = os.listdir(directory)
    all_files = [os.path.join(directory,file_name) for file_name in file_names]
    return filter(lambda file_name : file_name[-4:] == '.txt', all_files)

def text(file_path):
    """Returns the full text of the file at the given path"""
    with open(file_path,'r') as f:
        text = f.read()
    return text



#functions for extracting metadata
def title(doc):
    '''Return the title of the document'''
    title_string = title_search.search(doc)
    if title_string:
        title_string = title_string.group('title')
    return title_string

def author(doc):
    '''Return the author of the document'''
    auth = author_search.search(doc)
    if auth:
        auth = auth.group('author')
    return auth

def translator(doc):
    '''Return the translator of the document'''
    trans = translator_search.search(doc)
    if trans:
        trans = trans.group('translator')
    return trans

def illustrator(doc):
    '''Return the illustrator of the document'''
    ill = illustrator_search.search(doc)
    if ill:
        ill = ill.group('illustrator')
    return ill


#functions used to count keywords
def text_body(doc):
    """Return the portion of document b/t ***START...*** and ***END...***"""
    counts = {}
    content_pattern = re.compile(r'''
                            ([*][*][*]\ ?START.*?[*][*]+) #start of text
                            (.*)                           #body of text
                            ([*][*][*]\ ?END.*?[*][*]+)   #end of text
                            ''', re.IGNORECASE|re.DOTALL|re.VERBOSE)
    return content_pattern.search(doc).group(2)

def keyword_count(content_body,keyword):
    """Return the count of the keyword in the text of the content body"""
    keyword_pattern = re.compile(r'\b{}\b'.format(keyword),re.IGNORECASE)
    matches = keyword_pattern.findall(content_body)
    return len(matches)

def keyword_list_counts(doc, keywords):
    """Return counts for keywords
    
    doc is the original, full doc
    keywords is a list of the keywords to be counted
    returns a dictionary mapping keywords to counts
    """
    content_body = text_body(doc)
    counts = {}
    for keyword in keywords:
        counts[keyword] = keyword_count(content_body,keyword)
    return counts

def print_metadata(doc):
    """Print title, author, and translator of document"""
    print 'The title of the text is {}'.format(title(doc))
    print 'The author is {}'.format(author(doc))
    print 'The translator is {}'.format(translator(doc))

def print_keyword_counts(doc,keywords):
    """Print the counts for the keywords for the doc"""
    counts = keyword_list_counts(doc,keywords)
    for keyword in keywords:
        print '"{0}" : {1}'.format(keyword,counts[keyword])

def print_info(doc,keywords):
    """Print all info about a document"""
    print_metadata(doc)
    print
    print_keyword_counts(doc,keywords)

def main():
    gutenberg_directory = sys.argv[1]
    keywords = sys.argv[2:]
    paths = file_paths(gutenberg_directory)
    for path in paths:
        print '***' * 25
        print_info(text(path),keywords)
        print

if __name__ == '__main__':
    main()
    

        