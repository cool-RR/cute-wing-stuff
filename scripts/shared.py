# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for use in Wing scripts.'''

from  __future__ import with_statement

import collections
import re
import sys
import subprocess

from python_toolbox import context_management

try:
    import autopy.key
except ImportError:
    autopy_available = False
else:
    autopy_available = True

import wingapi

_ignore_scripts = True


class SelectionRestorer(context_management.ContextManager):
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

        if tuple(self.editor.GetSelection()) != (start, end):
            self.editor.SetSelection(start, end)
            # (Only conditionally setting selection, because if it's already
            # correct it's best to leave it as it is, because when we set it
            # ourselves some things (like `select-less`) stop working.)


class ClipboardRestorer(context_management.ContextManager):

    def __init__(self, app):
        assert isinstance(app, wingapi.CAPIApplication)
        self.app = app
        self.clipboard_data = None

    def __enter__(self):
        self.clipboard_data = self.app.GetClipboard()


    def __exit__(self, *args, **kwargs):
        self.app.SetClipboard(self.clipboard_data)



def scroll_to_line(editor, line_number):
    '''Scroll the `editor` to `line_number`.'''
    assert isinstance(editor, wingapi.CAPIEditor)
    file_path = editor.GetDocument().GetFilename()

    #print('Trying to reach line number %s...' % line_number)
    first_line_number_guess = line_number - \
                                          scroll_to_line.last_offset[file_path]
    #print("Last time there was an offset of %s, so we're gonna ask to scroll "
          #"to %s" % (scroll_to_line.last_offset[file_path],
                     #first_line_number_guess))
    editor.ScrollToLine(first_line_number_guess, pos='top')
    first_visible_line = editor.GetFirstVisibleLine()
    #print('We were scrolled to %s.' % first_visible_line)
    offset_to_target = first_visible_line - line_number
    offset_to_first_guess = \
                         first_visible_line - first_line_number_guess
    if offset_to_target:
        #print ('Got offset of %s, correcting...' % offset_to_target)
        editor.ScrollToLine(first_line_number_guess - offset_to_target,
                            pos='top')

    scroll_to_line.last_offset[file_path] = offset_to_first_guess

    #print('Function ended with us scrolled to %s' %
                                                 #editor.GetFirstVisibleLine())

scroll_to_line.last_offset = collections.defaultdict(lambda: 0)


class ScrollRestorer(context_management.ContextManager):
    '''
    Context manager for restoring scroll position to what it was before suite.
    '''
    def __init__(self, editor):
        assert isinstance(editor, wingapi.CAPIEditor)
        self.editor = editor

    def __enter__(self):
        self.first_line_number = self.editor.GetFirstVisibleLine()
        return self

    def __exit__(self, *args, **kwargs):
        scroll_to_line(self.editor, self.first_line_number)


def strip_selection_if_single_line(editor):
    '''
    If selection is on a single line, strip it, removing whitespace from edges.
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    start, end = editor.GetSelection()
    start_line_number = document.GetLineNumberFromPosition(start)
    end_line_number = document.GetLineNumberFromPosition(end - 1)
    if start_line_number == end_line_number:
        selection = document.GetCharRange(start, end)
        left_strip_size = len(selection) - len(selection.lstrip())
        right_strip_size = len(selection) - len(selection.rstrip())
        new_start = start + left_strip_size
        new_end = end - right_strip_size
        editor.SetSelection(new_start, new_end)


_whitespace_and_newlines_stripping_pattern = re.compile(
    r'''^(?P<leading>[ \r\n\t]*)(?P<content>.*?)(?P<trailing>[ \r\n\t]*)$''',
    flags=re.DOTALL
)
def strip_segment_from_whitespace_and_newlines(text, start, end):

    selection_text = text[start:end]
    match = _whitespace_and_newlines_stripping_pattern.match(selection_text)
    assert match
    new_start = start + len(match.group('leading'))
    new_end = end - len(match.group('trailing'))

    return new_start, new_end


class UndoableAction(context_management.ContextManager):
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


def select_current_word():
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
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    indent_size, indent_string = editor.fEditor._CalcNaturalIndent(
        document.GetLineNumberFromPosition(pos)
    )
    return indent_size


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


def _clip_to_document_range(position, document):
    '''Correct `position` to be within the confines of the `document`.'''
    assert isinstance(document, wingapi.CAPIDocument)
    if position < 0:
        return 0
    elif position > document.GetLength():
        return length
    else:
        return position


def _move_half_page(direction):
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


def plural_word_to_singular_word(plural_word):
    ''' '''
    assert isinstance(plural_word, (str, unicode))
    if plural_word.endswith('matrices'):
        return plural_word[:-3] + 'x'
    elif plural_word.endswith('ies'):
        return plural_word[:-3] + 'y'
    elif plural_word.endswith('sses'):
        return plural_word[:-2]
    elif plural_word.endswith('ches'):
        return plural_word[:-2]
    else:
        assert plural_word.endswith('s')
        return plural_word[:-1]


def clip_ahk():
    '''
    Cause AHK to think that a new word is being typed, for its auto-completion.
    '''
    import subprocess

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen(
        (r'c:\windows\py.exe',
         r'C:\Users\Administrator\Dropbox\Scripts and shortcuts\_type_f24.py'),
        startupinfo=startupinfo
    )
    # assert autopy_available
    # autopy.key.tap(135) # F24 for making AHK think it's a new word


def get_text(document):
    # Getting the text using `GetCharRange` instead of `GetText` because
    # `GetText` returns unicode.
    assert isinstance(document, wingapi.CAPIDocument)
    return document.GetCharRange(0, document.GetLength())

def argmin(sequence, key_function=None):
    if key_function is None:
        key_function = lambda x: x
        index
    indices = range(len(sequence))
    indices.sort(key=lambda index: key_function(sequence[index]))
    return sequence[indices[0]]

def reset_caret_blinking(editor):
    selection = editor.GetSelection()
    editor.ExecuteCommand('forward-char')
    editor.SetSelection(*selection)


def get_file_content(file_path):
    with open(file_path) as file:
        return file.read()

def open_path_in_explorer(path):
    if sys.platform == 'darwin':
        subprocess.call(['open', '--', path])
    elif sys.platform == 'linux2':
        subprocess.call(['gnome-open', '--', path])
    elif sys.platform == 'win32':
        subprocess.call(['explorer', path])

# def get_n_monitors():
    # import win32api
    # return len(win32api.EnumDisplayMonitors())

