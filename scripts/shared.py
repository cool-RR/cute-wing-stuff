# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for use in Wing scripts.'''

from  __future__ import with_statement

import collections
import functools
import re
import sys
import subprocess
from typing import Optional

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


from python_toolbox import context_management

try:
    import autopy.key
except ImportError:
    autopy_available = False
else:
    autopy_available = True

import wingapi
from pysource import strutils

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
        start, end = get_selection_unicode(self.editor)
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

        if tuple(get_selection_unicode(self.editor)) != (start, end):
            set_selection_unicode(self.editor, start, end)
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
    start, end = get_selection_unicode(editor)
    start_line_number = document.GetLineNumberFromPosition(start)
    end_line_number = document.GetLineNumberFromPosition(end - 1)
    if start_line_number == end_line_number:
        selection = document.GetText()[start : end]
        left_strip_size = len(selection) - len(selection.lstrip())
        right_strip_size = len(selection) - len(selection.rstrip())
        new_start = start + left_strip_size
        new_end = end - right_strip_size
        set_selection_unicode(editor, new_start, new_end)


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
    start, _ = get_selection_unicode(editor)
    assert start == _
    return start


def select_current_word(editor):
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
            character = document.GetText()[start + length : start + length + 1]
            assert len(character) == 1
            if character.isalnum() or character == '_':
                continue
            else:
                break
    end = start + length
    set_selection_unicode(editor, start, end)
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


def _move_half_page(direction, editor):
    '''
    Move half a page, either up or down.

    If `direction=-1`, moves up, and if `direction=1`, moves down.

    This is essentially one half of Page-Down or Page-Up.
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    lines_to_move = editor.GetNumberOfVisibleLines() // 2

    # Determining current location: ###########################################
    current_position, _ = get_selection_unicode(editor)
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
        set_selection_unicode(editor, new_position, new_position)


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
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        subprocess.Popen(
            (os.environ['PYTHONW_EXE'],
             r'C:\Users\Administrator\Dropbox\bin\Windows\_type_f13.py'),
            startupinfo=startupinfo
        )
    except FileNotFoundError:
        pass


def get_text(document):
    # todo: this might not be needed anymore
    return document.GetText()

def argmin(sequence, key_function=None):
    if key_function is None:
        key_function = lambda x: x
    indices = range(len(sequence))
    indices.sort(key=lambda index: key_function(sequence[index]))
    return sequence[indices[0]]

def reset_caret_blinking(editor):
    selection = get_selection_unicode(editor)
    editor.ExecuteCommand('forward-char')
    set_selection_unicode(editor, *selection)


def get_file_content(file_path):
    with open(file_path) as file:
        return file.read()

def open_folder_in_explorer(path):
    if sys.platform == 'darwin':
        subprocess.call(['open', '--', path])
    elif sys.platform in ('linux', 'linux2'):
        subprocess.call(['open', path])
    elif sys.platform == 'win32':
        subprocess.call(['explorer', path])

def show_file_in_explorer(path):
    path = os.path.normpath(path)
    if os.name == 'nt':  # For Windows
        subprocess.run(['explorer', '/select,', path])
    elif os.name == 'posix':  # For macOS and Linux
        if os.uname().sysname == 'Darwin':  # macOS
            subprocess.run(['open', '-R', path])
        else:  # Linux
            subprocess.run(['xdg-open', os.path.dirname(path)])
    else:
        print("Unsupported operating system")

# def get_n_monitors():
    # import win32api
    # return len(win32api.EnumDisplayMonitors())

class GeneratorContextManager(object):
    """Helper for @contextmanager decorator."""

    def __init__(self, gen):
        self.gen = gen

    def __enter__(self):
        try:
            return next(self.gen)
        except StopIteration:
            raise RuntimeError("generator didn't yield")

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                next(self.gen)
            except StopIteration:
                return
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = type()
            try:
                self.gen.throw(type, value, traceback)
                raise RuntimeError("generator didn't stop after throw()")
            except StopIteration as exc:
                # Suppress the exception *unless* it's the same exception that
                # was passed to throw().  This prevents a StopIteration
                # raised inside the "with" statement from being suppressed
                return exc is not value
            except:
                # only re-raise if it's *not* the exception that was
                # passed to throw(), because __exit__() must not raise
                # an exception unless __exit__() itself failed.  But throw()
                # has to raise the exception to signal propagation, so this
                # fixes the impedance mismatch between the throw() protocol
                # and the __exit__() protocol.
                #
                if sys.exc_info()[1] is not value:
                    raise

def contextmanager(func):
    """@contextmanager decorator.
    Typical usage:
        @contextmanager
        def some_generator(<arguments>):
            <setup>
            try:
                yield <value>
            finally:
                <cleanup>
    This makes this:
        with some_generator(<arguments>) as <variable>:
            <body>
    equivalent to this:
        <setup>
        try:
            <variable> = <value>
            <body>
        finally:
            <cleanup>
    """
    @functools.wraps(func)
    def helper(*args, **kwds):
        return GeneratorContextManager(func(*args, **kwds))
    return helper

@contextmanager
def nested(*managers):
    """Combine multiple context managers into a single nested context manager.
   This function has been deprecated in favour of the multiple manager form
   of the with statement.
   The one advantage of this function over the multiple manager form of the
   with statement is that argument unpacking allows it to be
   used with a variable number of context managers as follows:
      with nested(*managers):
          do_something()
    """
    exits = []
    vars = []
    exc = (None, None, None)
    try:
        for mgr in managers:
            exit = mgr.__exit__
            enter = mgr.__enter__
            vars.append(enter())
            exits.append(exit)
        yield vars
    except:
        exc = sys.exc_info()
    finally:
        while exits:
            exit = exits.pop()
            try:
                if exit(*exc):
                    exc = (None, None, None)
            except:
                exc = sys.exc_info()
        if exc != (None, None, None):
            # Don't rely on sys.exc_info() still containing
            # the right information. Another exception may
            # have been raised and caught by an exit method
            raise exc[0]


def get_selection_unicode(editor: wingapi.CAPIEditor) -> tuple[int, int]:
    """Get selection from editor as unicode character offsets rather than utf-8 byte offsets.

    Returns:
        Tuple of (start, end) positions as unicode character offsets (0-based)
    """
    doc = editor.GetDocument()
    text = doc.GetText()
    utf8_start, utf8_end = editor.GetSelection()

    start = len(text.encode('utf-8')[:utf8_start].decode('utf-8'))
    end = len(text.encode('utf-8')[:utf8_end].decode('utf-8'))

    return (start, end)

def set_selection_unicode(editor: wingapi.CAPIEditor, start: int, end: int) -> None:
    """Set selection in editor using unicode character offsets rather than utf-8 byte offsets.

    Args:
        editor: The editor to modify
        start: Start position as unicode character offset (0-based)
        end: End position as unicode character offset (0-based)
    """
    doc = editor.GetDocument()
    text = doc.GetText()

    utf8_start = len(text[:start].encode('utf-8'))
    utf8_end = len(text[:end].encode('utf-8'))

    editor.SetSelection(utf8_start, utf8_end)

def get_char_type_unicode(editor: wingapi.CAPIEditor, position: int, *,
                          text: Optional[str] = None) -> str:
    """Get the type of the character at the given position."""
    document = editor.GetDocument()
    if text is None:
        text = document.GetText()
    fixed_position = strutils.Utf8Len(text, 0, position)
    return editor.fEditor.GetCharType(fixed_position)
