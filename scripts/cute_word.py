# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import division
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
newline_word_pattern = re.compile(
    r'''\r?\n[ \r\t\n]*'''
)
alphanumerical_word_pattern = re.compile(
    r'''[^!"#$%&'()*+,\-./:;<=>?@[\\\]^`{|}~ \t\r\n]+'''
)


def _round(n, step=100, direction=-1):
    assert isinstance(n, int)
    low = (n // step) * step
    high = low + step
    if low == n:
        return low
    elif high == n:
        return high
    elif direction == 1:
        return high
    else:
        assert direction == -1
        return low


def _find_spans(pattern, text):
    return [(match.span()[0], match.span()[1] - 1)
                                           for match in pattern.finditer(text)]
    

@shared.lru_cache(maxsize=20)
def get_word_spans_in_text(text, post_offset=0):
    '''
    
    '''
    #print('post_offset is %s' %  post_offset)
    #print(repr(text))
    word_spans = _find_spans(punctuation_word_pattern, text) + \
                                        _find_spans(newline_word_pattern, text)

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
    #print(alphanumerical_word_spans)
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
        for i, character in reversed(enumerated):
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
        # Finished separating using middle underscores, now separating using
        # case.
        
        # We're popping word spans out of `sub_word_spans` one-by-one. We
        # analyze them, sometimes we throw them into `sub_sub_word_spans`,
        # which means they're words that are already separated by case, and
        # sometimes we throw one part of them into `sub_sub_word_spans`, and
        # throw the remaining substring back into `sub_word_spans`, where it
        # will be analyzed on a later run of the loop.
        
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
                            break
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
                            break
                    
            else:
                sub_sub_word_spans.append(sub_word_span)
                continue
                
        #######################################################################
        word_spans += sub_sub_word_spans
        # We've finished separating into case-separated words; we throw them
        # into the large list of words, and continue the loop to do the same
        # process to the next unseparated alphanumeric word.
        
    word_spans.sort()
        
    if post_offset:
        word_spans = [
            (word_span[0] + post_offset, word_span[1] + post_offset)
                                                    for word_span in word_spans
        ]

    return word_spans




def cute_word(direction=1, extend=False, delete=False,
              select_current=False, 
              editor=wingapi.kArgEditor, app=wingapi.kArgApplication):
    '''
    blocktododoc
    '''    
    
    assert isinstance(editor, wingapi.CAPIEditor)
    
    assert direction in (-1, 1)
    assert (delete, extend, select_current).count(True) in (0, 1)
    
    selection_start, selection_end = editor.GetSelection()
    document = editor.GetDocument()
    anchor_position, caret_position = editor.GetAnchorAndCaret()
    current_selection_direction = \
                                 1 if caret_position >= anchor_position else -1
    
    
    # Trying to round the text startpoint and endpoint, so it'll more likely to
    # be cached when doing many word-movings rapidly.
    
    text_start = max(
        _round(selection_start - 70, step=100, direction=-1),
        0
    )
    text_end = min(
        _round(selection_end + 70, step=100, direction=1),
        document.GetLength()
    )
    
    #caret_position = 0
    #text_start = 0
    #text_end = 100
    
    text = document.GetCharRange(text_start, text_end)
    
    word_spans = get_word_spans_in_text(text, post_offset=text_start)
    word_starts = zip(*word_spans)[0]
    #print(word_starts)
    bisector = bisect.bisect_right if direction == 1 else bisect.bisect_left
    word_start_index = bisector(word_starts, caret_position)
    if direction == 1:
        if word_start_index == len(word_starts):
            target_word_start = document.GetLength()
        else:
            target_word_start = word_starts[word_start_index]
    else: # direction == -1:
        if word_start_index == 0:
            target_word_start = 0
        else:
            target_word_start = word_starts[word_start_index - 1]
            
    
    #print(next_word_start)
    if select_current:
        nominal_position = (selection_start + selection_end) // 2
        words_we_are_in = [
            (word_start, word_end + 1) for (word_start, word_end) in word_spans
            if word_start <= nominal_position <= word_end + 1
        ]
        if words_we_are_in:
            word_we_are_in = words_we_are_in[0]
            app.ExecuteCommand('set-visit-history-anchor')
            editor.SetSelection(*word_we_are_in)
    elif extend:
        editor.SetSelection(anchor_position, target_word_start)
    elif delete:
        with shared.UndoableAction(document):
            if direction == 1:
                target_word_start -= 1
            else: # direction == -1
                caret_position -= 1
            document.DeleteChars(
                *sorted((
                    max(caret_position, 0),
                    max(target_word_start, 0)
                ))
            )
    else:
        editor.SetSelection(target_word_start, target_word_start)
        
    
    
    
    
    