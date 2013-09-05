# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import sys
import inspect
import re
import string

import wingapi

import shared


punctuation_word_pattern = re.compile(
    r'''[!"#$%&'()*+,\-./:;<=>?@[\\\]^`{|}~]*'''
    # (This is `string.punctuation` without `_`.)
)
whitespace_word_pattern = re.compile(
    r'''[ \r\t\n]*'''
)
alphanumerical_word_pattern = re.compile(
    r'''[^!"#$%&'()*+,\-./:;<=>?@[\\\]^`{|}~ \t\r\n]*'''
)



def get_words_in_text(text):
    word_spans = (
        punctuation_word_pattern.findall(text) +
                                          whitespace_word_pattern.findall(text)
    )
    
    for alphanumerical_word_span in alphanumerical_word_pattern.findall(text):
        alphanumerical_word = text[alphanumerical_word_span[0]:
                                                   alphanumerical_word_span[1]]
        relative_middle_underscore_indices = []
        assert isinstance(alphanumerical_word, basestring)
        
        ### Finding middle underscores: #######################################
        #                                                                     #
        saw_non_underscore = False
        for i, character in enumerate(alphanumerical_word):
            if character == '_':
                if saw_non_underscore:
                    relative_middle_underscore_indices.append(i)
            else: # character != '_'
                saw_non_underscore = True
        for i in reversed(enumerate(alphanumerical_word)):
            if character == '_':
                try:
                    relative_middle_underscore_indices.remove(i)
                except ValueError:
                    pass
            else: # character != '_'
                break
        #                                                                     #
        ### Finished finding middle underscores. ##############################
        
        middle_underscore_indices = map(
            lambda i: i + alphanumerical_word_span[0],
            relative_middle_underscore_indices
        )
        
        non_middle_underscore_indices = filter(
            lambda i: i not in middle_underscore_indices, 
            xrange(
                alphanumerical_word_span[0], 
                alphanumerical_word_span[1]+1, 
            )
        )
        
        sub_word_spans = []
        current_word_span = None
        for i in non_middle_underscore_indices:
            if current_word_span is None:
                current_word_span = [i, i]
            else: # current_word is not None
                if current_word_span[1] == i - 1:
                    current_word_span[1] = i
                else:
                    assert i - current_word_span[1] >= 2
                    sub_word_spans.append(tuple(current_word_span))
                    current_word_span = [i, i]
        if current_word_span:
            sub_word_spans.append(tuple(current_word_span))
                
        word_spans += sub_word_spans
        
    word_spans.sort()
    return word_spans




def cute_replace_string(editor=wingapi.kArgEditor,
                       app=wingapi.kArgApplication):
    '''
    Improved version of `replace-string` for finding and replacing in document.
    
    BUGGY: If text is selected, it will be used as the text to search for, and
    the contents of the clipboard will be offered as the replace value.
    
    Implemented on Windows only.
    
    Suggested key combination: `Alt-Period`
    '''    
    return _cute_general_replace('replace-string', editor=editor, app=app)