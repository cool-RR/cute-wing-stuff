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
alpha_word_pattern = re.compile(
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
    

def get_word_spans_in_text(text, post_offset=0):
    return sorted(
        get_non_alpha_word_spans_in_text(text, post_offset=post_offset) +
        get_alpha_word_spans_in_text(text, post_offset=post_offset)
    )


@shared.lru_cache(maxsize=20)
def get_non_alpha_word_spans_in_text(text, post_offset=0):
    return _offset_word_spans(
        sorted(_find_spans(punctuation_word_pattern, text) + 
               _find_spans(newline_word_pattern, text)),
        post_offset=post_offset
    )


@shared.lru_cache(maxsize=20)
def get_alpha_word_spans_in_text(text, post_offset=0):
    
    # We have three phases here. In the first phase we get words like
    # `IToldYou_soFooBar`, in the second phase we get words like `IToldYou`,
    # `soFooBar`, in the third and final phase we get words like `I`, `Told`,
    # `You`, `so`, `Foo`, `Bar`.
    
    pre_pre_alpha_word_spans = _find_spans(alpha_word_pattern, text)
    pre_alpha_word_spans = collections.deque()
    alpha_word_spans = []
    
    for pre_pre_alpha_word_span in pre_pre_alpha_word_spans:
        pre_pre_alpha_word = \
                    text[pre_pre_alpha_word_span[0]:pre_pre_alpha_word_span[1]]
        relative_middle_underscore_indices = []
        
        ### Finding middle underscores: #######################################
        #                                                                     #
        saw_non_underscore = False
        enumerated = list(enumerate(pre_pre_alpha_word))
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
            lambda i: i + pre_pre_alpha_word_span[0],
            relative_middle_underscore_indices
        )
        
        non_middle_underscore_indices = filter(
            lambda i: i not in middle_underscore_indices, 
            xrange(
                pre_pre_alpha_word_span[0], 
                pre_pre_alpha_word_span[1] + 1, 
            )
        )
        
        current_word_span = None
        for i in non_middle_underscore_indices:
            if current_word_span is None:
                current_word_span = [i, i]
            else: # current_word is not None
                if current_word_span[1] == i - 1:
                    current_word_span[1] = i
                else:
                    assert i - current_word_span[1] >= 2
                    pre_alpha_word_spans.append(tuple(current_word_span))
                    current_word_span = [i, i]
        if current_word_span:
            pre_alpha_word_spans.append(tuple(current_word_span))
        
            
    ######################################################################
    # Finished separating using middle underscores, now separating using
    # case.
    
    # We're popping word spans out of `pre_alpha_word_spans` one-by-one. We
    # analyze them, sometimes we throw them into `pre_alpha_word_spans`,
    # which means they're words that are already separated by case, and
    # sometimes we throw one part of them into `alpha_word_spans`, and
    # throw the remaining substring back into `pre_alpha_word_spans`, where
    # it will be analyzed on a later run of the loop.
    
    while pre_alpha_word_spans:
        pre_alpha_word_span = pre_alpha_word_spans.pop()
        pre_alpha_word = \
                  text[pre_alpha_word_span[0] : pre_alpha_word_span[1] + 1]
        alpha_characters = filter(str.isalpha, pre_alpha_word)
        if not alpha_characters:
            alpha_word_spans.append(pre_alpha_word_span)
            continue
        could_be_lower_case = True
        could_be_upper_case = True
        could_be_camel_case = True
        saw_first_alpha = False

        for i in \
                xrange(pre_alpha_word_span[0], pre_alpha_word_span[1] + 1):
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
                        alpha_word_spans.append((
                            pre_alpha_word_span[0], 
                            i - 1
                        ))
                        pre_alpha_word_spans.append((
                            i, 
                            pre_alpha_word_span[1], 
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
                        alpha_word_spans.append((
                            pre_alpha_word_span[0], 
                            i - 1
                        ))
                        pre_alpha_word_spans.append((
                            i, 
                            pre_alpha_word_span[1], 
                        ))
                        break
                
        else:
            alpha_word_spans.append(pre_alpha_word_span)
            continue
            
    alpha_word_spans.sort()
        
    alpha_word_spans = _offset_word_spans(alpha_word_spans, post_offset)

    return alpha_word_spans


def _offset_word_spans(word_spans, post_offset):
    if post_offset:
        return [
            (word_span[0] + post_offset, word_span[1] + post_offset)
                                                    for word_span in word_spans
        ]
    else:
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
        alpha_word_spans = get_alpha_word_spans_in_text(text,
                                                        post_offset=text_start)
        if not alpha_word_spans:
            return 
        fixed_alpha_word_spans = [
            (word_start, word_end + 1) for (word_start, word_end) in
            alpha_word_spans
        ]
        alpha_words_we_are_in = [
            (word_start, word_end) for (word_start, word_end) in
            fixed_alpha_word_spans
                                  if word_start <= nominal_position <= word_end
        ]
        app.ExecuteCommand('set-visit-history-anchor')
        if alpha_words_we_are_in:
            alpha_word_we_are_in = alpha_words_we_are_in[-1]
            editor.SetSelection(*alpha_word_we_are_in)
        else:
            closest_alpha_word_span = shared.argmin(
                fixed_alpha_word_spans,
                lambda (alpha_word_start, alpha_word_end):
                    min(abs(alpha_word_start - nominal_position),
                        abs(alpha_word_end - nominal_position),)
            )
            editor.SetSelection(*closest_alpha_word_span)            
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
        
    
    
    
    
    