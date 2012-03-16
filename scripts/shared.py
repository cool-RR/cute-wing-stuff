# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for use in Wing scripts.'''

from  __future__ import with_statement

import re

import wingapi


_ignore_scripts = True


class SelectionRestorer(object):
    '''
    Context manager for restoring selection to what it was before the suite.
    
    Example:
    
        with SelectionRestorer(my_editor):
            # Change the selection to whatever you want
        # The selection has been returned to what it was originally.
       
    This was intended only for suites that don't change the contents of the
    editor.
    '''
    
    def __init__(self, editor, line_wise=False, line_offset=0):
        assert isinstance(editor, wingapi.CAPIEditor)
        if not line_wise:
            assert not line_offset
        self.editor = editor
        self.document = editor.GetDocument()
        self.line_wise = line_wise
        self.line_offset = line_offset
        
        
    def __enter__(self):
        start, end = self.editor.GetSelection()
        if self.line_wise:
            self.start_line_wise = character_position_to_line_position(
                self.document,
                start,
                line_offset=self.line_offset
            )
            self.end_line_wise = character_position_to_line_position(
                self.document,
                end,
                line_offset=self.line_offset
            )
        else:
            self.start = start
            self.end = end

                
    def __exit__(self, *args, **kwargs):
        if self.line_wise:
            start = line_position_to_character_position(self.document,
                                                        *self.start_line_wise)
            end = line_position_to_character_position(self.document,
                                                      *self.end_line_wise)
        else:
            start = self.start
            end = self.end
        self.editor.SetSelection(start, end)

        
class UndoableAction(object):
    '''
    Context manager for marking an action that can be undone by the user.
    
    Example:
    
        with UndoableAction(my_document):
            # Do anything here, make any changes to the document
        # Now the user can do Ctrl-Z and have the above suite undone.
    
    '''
    def __init__(self, document):
        assert isinstance(document, wingapi.CAPIDocument)
        self.document = document
        
    def __enter__(self):
        self.document.BeginUndoAction()
        
    def __exit__(self, *args, **kwargs):
        self.document.EndUndoAction()
        

def get_cursor_position(editor):
    '''
    Get the cursor position in the given editor, assuming no text is selected.
    '''
    start, _ = editor.GetSelection()
    assert start == _
    return start        


def select_current_word(editor=wingapi.kArgEditor):
    '''Select the current word that the cursor is on.'''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    editor.ExecuteCommand('backward-word')
    start = get_cursor_position(editor)
    length = 0
    for length in range(1000): 
        if start + length == document.GetLength():
            break
        else:
            character = document.GetCharRange(start + length,
                                              start + length + 1)
            assert len(character) == 1
            if character.isalnum() or character == '_':
                continue
            else:
                break
    end = start + length
    editor.SetSelection(start, end)
    return start, end


def get_indent_size_in_pos(editor, pos):
    '''
    Get the size of the indent, in spaces, in position `pos` in `editor`.
    
    Returns an `int` like 4, 8, 12, etc.
    '''    
    # todo: figure out something like `indent-to-match` except it looks at the
    # lines *below* the current one.
    
    # blocktodo: I think that 'indent-to-match' actually modifies the document,
    # adding or removing spaces! This is bad, should find substitute that
    # doesn't modify the document.
    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    with SelectionRestorer(editor):
        line_number = document.GetLineNumberFromPosition(pos)
        line_start_pos = document.GetLineStart(line_number)
        editor.SetSelection(pos, pos)
        editor.ExecuteCommand('indent-to-match')
        line_text_start_pos = editor.GetSelection()[0]
        
        return line_text_start_pos - line_start_pos
    

def camel_case_to_lower_case(s):
    '''
    Convert a string from camel-case to lower-case.
    
    Example: 
    
        camel_case_to_lower_case('HelloWorld') == 'hello_world'
        
    '''
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).\
           lower().strip('_')


def lower_case_to_camel_case(s):
    '''
    Convert a string from lower-case to camel-case.
    
    Example: 
    
        camel_case_to_lower_case('hello_world') == 'HelloWorld'
        
    '''
    assert isinstance(s, basestring)
    s = s.capitalize()
    while '_' in s:
        head, tail = s.split('_', 1)
        s = head + tail.capitalize()
    return s


def get_n_identical_edge_characters(string, character=None, head=True):
    '''
    Get the number of identical characters at `string`'s head.
    
    For example, the result for 'qqqwe' would be `3`, while the result for
    'meow' will be `1`.
    
    Specify `character` to only consider that character; if a different
    character is found at the head, `0` will be returned.
    
    Specify `head=False` to search the tail instead of the head.
    '''
    if not string:
        return 0
    index = 0 if head is True else -1
    direction = 1 if head is True else -1
    if character is None:
        character = string[index]
    else:
        assert isinstance(character, basestring) and len(character) == 1
    for i, c in enumerate(string[::direction]):
        if c != character:
            return i
    else:
        return len(string)
    
    
def _clip_to_document_range(position, document):
    '''Correct `position` to be within the confines of the `document`.'''
    assert isinstance(document, wingapi.CAPIDocument)
    if position < 0:
        return 0
    elif position > document.GetLength():
        return length
    else:
        return position

    
def _move_half_page(direction, editor=wingapi.kArgEditor):
    '''
    Move half a page, either up or down.
    
    If `direction=-1`, moves up, and if `direction=1`, moves down.
    
    This is essentially one half of Page-Down or Page-Up.
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    
    lines_to_move = editor.GetNumberOfVisibleLines() // 2
    
    # Determining current location: ###########################################
    current_position, _ = editor.GetSelection()
    current_line = document.GetLineNumberFromPosition(current_position)
    column = current_position - document.GetLineStart(current_line)
    ###########################################################################
    
    # Determining new location to go to: ######################################
    new_line = current_line + (lines_to_move * direction)
    length_of_new_line = \
                document.GetLineEnd(new_line) - document.GetLineStart(new_line)
    new_column = min((column, length_of_new_line))
    new_position = _clip_to_document_range(
        document.GetLineStart(new_line) + new_column,
        document=document
    )
    ###########################################################################

    with UndoableAction(document):
        editor.SetSelection(new_position, new_position)
        

def character_position_to_line_position(document, character_position,
                                        line_offset=0):
    ''' '''
    assert isinstance(document, wingapi.CAPIDocument)
    line_number = document.GetLineNumberFromPosition(character_position)
    line_position = character_position - document.GetLineStart(line_number)
    return (line_number+line_offset, line_position)
    
    
def line_position_to_character_position(document, line_number, line_position):
    ''' '''
    assert isinstance(document, wingapi.CAPIDocument)
    return document.GetLineStart(line_number) + line_position
    