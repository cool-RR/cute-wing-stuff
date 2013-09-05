# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import sys
import inspect
import bisect
import collections
import re
import string

import wingapi

import shared


punctuation_word_pattern = re.compile(
    r'''[!"#$%&'()*+,\-./:;<=>?@[\\\]^`{|}~]+'''
    # (This is `string.punctuation` without `_`.)
)
whitespace_word_pattern = re.compile(
    r'''[ \r\t\n]+'''
)
alphanumerical_word_pattern = re.compile(
    r'''[^!"#$%&'()*+,\-./:;<=>?@[\\\]^`{|}~ \t\r\n]+'''
)


def _find_spans(pattern, text):
    return [(match.span()[0], match.span()[1] - 1)
                                           for match in pattern.finditer(text)]
    

def get_word_spans_in_text(text, post_offset=0):
    print(repr(text))
    word_spans = _find_spans(punctuation_word_pattern, text)

    #word_spans.sort()
    #print(word_spans)
    #for word_span in word_spans:
        #if not isinstance(word_span, tuple):
            #raise Exception
        #if not len(word_span) == 2:
            #raise Exception
        #if not word_span[0] < word_span[1]:
            #print(word_span)
            #raise Exception
    
    alphanumerical_word_spans = _find_spans(alphanumerical_word_pattern, text)
    print(alphanumerical_word_spans)
    for alphanumerical_word_span in alphanumerical_word_spans:
        alphanumerical_word = text[alphanumerical_word_span[0]:
                                                   alphanumerical_word_span[1]]
        relative_middle_underscore_indices = []
        assert isinstance(alphanumerical_word, basestring)
        
        ### Finding middle underscores: #######################################
        #                                                                     #
        saw_non_underscore = False
        enumerated = list(enumerate(alphanumerical_word))
        for i, character in enumerated:
            if character == '_':
                if saw_non_underscore:
                    relative_middle_underscore_indices.append(i)
            else: # character != '_'
                saw_non_underscore = True
        for i in reversed(enumerated):
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
        
        if any(i >= len(text) for i in non_middle_underscore_indices):
            print(non_middle_underscore_indices)
            raise Exception
        
        sub_word_spans = collections.deque()
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
            
        ######################################################################
        # Finished separating using underscores, now separating using case.
            
        sub_sub_word_spans = []
        
        while sub_word_spans:
            sub_word_span = sub_word_spans.pop()
            sub_word = text[sub_word_span[0] : sub_word_span[1] + 1]
            alpha_characters = filter(str.isalpha, sub_word)
            if not alpha_characters:
                sub_sub_word_spans.append(sub_word_span)
                continue
            could_be_lower_case = True
            could_be_upper_case = True
            could_be_camel_case = True
            saw_first_alpha = False

            for i in xrange(sub_word_span[0], sub_word_span[1] + 1):
                character = text[i]
                if not character.isalpha():
                    continue
                assert character.isalpha()
                if character.islower():
                    if not saw_first_alpha:
                        saw_first_alpha = True
                        could_be_camel_case = could_be_upper_case = False
                    else: # saw_first_alpha is True
                        if could_be_lower_case or could_be_camel_case:
                            could_be_upper_case = False
                        else:
                            sub_sub_word_spans.append((
                                sub_word_span[0], 
                                i - 1
                            ))
                            sub_word_spans.append((
                                i, 
                                sub_word_span[1], 
                            ))
                            continue
                else:
                    assert character.isupper()
                    if not saw_first_alpha:
                        saw_first_alpha = True
                        could_be_lower_case = False
                    else: # saw_first_alpha is True
                        if could_be_upper_case:
                            could_be_camel_case = could_be_lower_case = False
                        else:
                            sub_sub_word_spans.append((
                                sub_word_span[0], 
                                i - 1
                            ))
                            sub_word_spans.append((
                                i, 
                                sub_word_span[1], 
                            ))
                            continue
                    
            else:
                sub_sub_word_spans.append(sub_word_span)
                continue
                
        #######################################################################
                
        word_spans += sub_sub_word_spans
        
    word_spans.sort()
    print(word_spans)
    for word_span in word_spans:
        if not isinstance(word_span, tuple):
            raise Exception
        if not len(word_span) == 2:
            raise Exception
        if not word_span[0] < word_span[1]:
            print(word_span)
            raise Exception
        
    if post_offset:
        word_spans = [
            (word_spans[0] + post_offset, word_spans[1] + post_offset)
                                                    for word_span in word_spans
        ]
    return word_spans




def cute_forward_word(editor=wingapi.kArgEditor,
                      app=wingapi.kArgApplication):
    '''
    blocktododoc
    '''    
    
    assert isinstance(editor, wingapi.CAPIEditor)
    
    selection_start, selection_end = editor.GetSelection()
    document = editor.GetDocument()
    _, caret_position = editor.GetAnchorAndCaret()
    
    #text_start = max(selection_start - 70, 0)
    #text_end = min(selection_end + 70, document.GetLength())
    
    #caret_position = 0
    text_start = 0
    text_end = 100
    
    text = document.GetCharRange(text_start, text_end)
    
    word_spans = get_word_spans_in_text(text, post_offset=text_start)
    word_starts = zip(*word_spans)[0]
    print(word_starts)
    next_word_start = word_starts[
        bisect.bisect_right(word_starts, caret_position)
    ]
    
    print(next_word_start)
    editor.SetSelection(next_word_start, next_word_start)
    
    
    
    
    