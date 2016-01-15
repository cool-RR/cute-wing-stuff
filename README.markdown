# Cute Wing stuff #

A collection of scripts for [Wing IDE 5.0](http://www.wingware.com/).

In order to use these scripts in your copy of Wing, download the repo to
someplace in your computer, fire up Wing, go to `Edit` -> `Preferences` -> `IDE
Extension Scripting` and add the path of the repo's `scripts` folder to your
`Search Path`. (Possibly you'll need to do `edit` -> `Reload All Scripts` to
get Wing to see them for the first time.)

After you do that, the commands will become available in Wing; For example you
could do `Ctrl-F12` and then type `flip-case` to activate the `flip-case`
script. But you probably want to bind these commands to some key combination;
do that in `Edit` -> `Preferences` -> `Keyboard` -> `Custom Key Bindings`.

Tip: Many of the commands have a suggested binding starting with the `Insert`
key. In order for that to work, you need to bind `Insert` to nothing in Wing.
(i.e. just leave the command text input box empty.) If you're one of the rare
people who still like using the `Insert` key by itself, you can bind
`Ctrl-Insert` to `toggle-overtype`.

All the scripts are copyright Ram Rachum and released under the MIT open-source
license. Some code is by Raymond Hettinger, and licensed to use under the MIT
license. (License given by Hettinger in private email on May 25th, 2013.)

I provide `Development services in Python and Django <https://chipmunkdev.com>`_.


# What do the scripts do? #


## arg-to-attr ##

Turn an argument to `__init__` into an instance attribute.
    
For example, you have just typed this:

    class MyObject(object):
        def __init__(self, crunchiness):
            <Cursor is here>
            
(Of course, you can substitute `crunchiness` for whatever your argument's name
is.)

Now, you might want to put a `self.crunchiness = crunchiness` line in that
`__init__` method. But that would take so much typing, because
`self.crunchiness` doesn't exist yet, and won't be autocompleted. That would
require you to make around 20 keystrokes. I don't know about you, but I'm just
not ready for that kind of a commitment.

Instead, type `crunchiness`. (You'll get autocompletion because it exists as an
argument.) Then run this `arg-to-attr` script.

The final result is that you'll get a `self.crunchiness = crunchiness` line and
have the cursor ready in the next line.

Suggested key combination: `Insert A`


## backward-half-page ##
    
Move half a page up.
    
This is essentially one half of Page-Up.

Suggested key combination: `Alt-Page_up` (As long as you don't use Wing's folding.)


## brace-match-inner ##

Select the inside of the current/next pair of braces.

Similar to Wing's built-in `brace-match`, except it selects only the inside
of the braces, not including the braces themselves.

Known limitations: Misses some pairs of braces. Doesn't know to ignore
braces found in strings.

Suggested key combination: `Alt-Bracketright`


## comment-braces ##

Create "comment braces" with a title around a piece of code.

For example, if you have this code:

    do_something()
    do_something_else()
    meow = frr + 7
    do_something_again()
    
You can select it, then run the `comment-braces` script with a title of
"doing inane stuff", to get this:
    
    ### Doing inane stuff: ####################################################
    #                                                                         #
    do_something()
    do_something_else()
    meow = frr + 7
    do_something_again()
    #                                                                         #
    ### Finished doing inane stuff. ###########################################
    
(Don't try this inside a docstring, it works only in real code.)

The title usually has a first word ending with "ing". Don't bother capitalizing
the first letter or ending the sentence with any punctuation mark. You may also
use an empty title to get a title-less comment line.

Suggested key combination: `Insert B`


## comment-hr ##

Enter a horizontal line of "#" characters going until character 79.

Example:

    #######################################################################
    
Suggested key combination: `Insert H`


## cute-evaluate-sel-in-debug-probe ##

Evaluate selection in debug probe, doing `select-more` if nothing selected.
    
Suggested key combination: `Ctrl-Alt-D`

    
## cute-goto-line ##

Go to a specified line number in editor, temporarily showing line numbers.

This script is intended for people who don't like Wing to always show line
numbers in the editors, but who *do* want to see them temporarily when using
Wing's `goto-line` command, usually invoked by Ctrl-L, to go to a specific
line.

Using this script you can see exactly which line you're going to before issuing
the command; and if usually keep line numbers hidden, then they will be hidden
automatically after Wing has moved to the specified line.
    
Also, the caret will go to the beginning of the text on the line instead of
Wing's default of going to column 0.

Suggested key combination: `Ctrl-L`


## cute-open-line ##

Open a new line. (i.e. enter a newline character.)

If `line_offset` is set to `-1`, it will open a line at the line above. If
`line_offset` is set to `1`, it will open a line at the line below.

If `stand_ground=True`, it will make the caret not move when doing the
newline.

(The advantage of this over Wing's built-in `open-line` is that
`cute-open-line` doesn't just insert a newline character like `open-line`
does; it runs Wing's `new-line` command, which does various intelligent
things like auto-indenting your code to the right level, opening your
parentheses *just so* if you're doing function invocation, and a bunch of
other goodies.)

Suggested key combinations:

    `Alt-Return` for `stand_ground=True`
    `Shift-Return` for `line_offset=-1`
    `Ctrl-Return` for `line_offset=1`
    `Alt-Shift-Return` for `line_offset=-1, stand_ground=True`
    `Ctrl-Alt-Return` for `line_offset=1, stand_ground=True`
    
(The `Alt-Return` combination requires a AHK shim, at least on Windows.)


## cute-query-replace ##

Improved version of `query-replace` for finding and replacing in document.

BUGGY: If text is selected, it will be used as the text to search for, and the
contents of the clipboard will be offered as the replace value.

Implemented on Windows only.

Suggested key combination: `Alt-Comma`


## cute-replace-string ##

Improved version of `replace-string` for finding and replacing in document.

BUGGY: If text is selected, it will be used as the text to search for, and the
contents of the clipboard will be offered as the replace value.

Implemented on Windows only.

Suggested key combination: `Alt-Period`


## cute-start-select-line ##

Start selecting by visual lines instead of by character.

What this adds over `start-select-line` is that it takes the current
selection when this command is invoked and expands it to cover all of its
lines as the initial selection.

Suggested key combination: `Ctrl-F8`


## cute-word ##

Move, select or delete words.

This is a swiss-army knife command for handling "words". Unlike Wing's default
word-handling logic, this command separates using underscores and case. For
example, `foo_bar_baz` will be split to 3 words, and so will `FooBarBaz` and
`FOO_BAR_BAZ`.

When used with no arguments, this command will move a word forward or backward,
depending on `direction`, similarly to Wing's built-in `forward-word` and
`backward-word` commands.

When used with `extend=True`, this command will extend the existing selection a
word forward or backward, depending on `direction`, similarly to Wing's
built-in `forward-word-extend` and `backward-word-extend` commands.

When used with `delete=True`, this command will delete a word forward or
backward, depending on `direction`, similarly to Wing's built-in
`forward-delete-word` and `backward-delete-word` commands.

When used with `traverse=True`, this command will select the next alphanumeric
word or the previous alphanumeric word, depending on `direction`.

Suggested key combinations:

    `Ctrl-Alt-Right` for direction=1
    `Ctrl-Alt-Left` for direction=-1
    `Ctrl-Alt-Shift-Right` for direction=1, extend=True
    `Ctrl-Alt-Shift-Left` for direction=-1, extend=True
    `Ctrl-Alt-Shift-Down` for direction=1, traverse=True
    `Ctrl-Alt-Shift-Up` for direction=-1, traverse=True
    `Alt-Delete` for direction=1, delete=True
    `Alt-Backspace` for direction=-1, delete=True
    
(Tip: If you do bind to `Ctrl-Alt-Right` and `Ctrl-Alt-Left` as I suggest, then
I also suggest you bind `Ctrl-Right-Up` and `Ctrl-Right-Down` to
`goto-previous-bookmark` and `goto-next-bookmark` respectively, so you'll still
have bookmark-traversing commands available.)


## deep-to-var ##
    
Create a variable from a deep expression.

When you're programming, you're often writing lines like these:

    html_color = self._style_handler.html_color
    
Or:

    location = context_data['location']
    
Or:
    
    event_handler = super(Foobsnicator, self).get_event_handler()

Or:
        
    user_profile = models.UserProfile.objects.get(pk=pk)
        
What's common to all these lines is that you're accessing some expression,
sometimes a deep one, and then getting an object, and making a variable for
that object with the same name that it has in the deep expression.

What this `deep-to-var` script will do for you is save you from having to write
the `html_color = ` part, which is annoying to type because you don't have
autocompletion for it.

Just write your deep expression, like `self._style_handler.html_color`, invoke
this `deep-to-var` script, and you'll get the full line and have the caret put
on the next line.

Suggested key combination: `Insert E`


## delete-line-and-home ##

Delete the current line and send caret to beginning of text in next line.
    
When you use Wing's default `delete-line` command to delete a line, it
sends the caret to column 0, which is annoying. This script fixes that by
first deleting a line, then sending the caret to the beginning of the text
on the next line.

Suggested key combination: `Ctrl-Shift-C`


## dict-direct-to-get ##

Turn `foo[bar]` into `foo.get(bar, None)`.

Suggested key combination: `Insert Ctrl-G`


## django-toggle-between-view-and-template ##

Toggle between a view file in Django and the corresponding template file.

If you're currently viewing a template file, this'll open the corresponding
view file. If you're currently viewing a view file, this'll open the
corresponding template file.

This assumes that the view file has the word `view` in it and has a
definition for the class attribute `template_name`.

Suggested key combination: `Insert Quoteleft` (i.e. backtick)


## duplicate-file ##

Create a copy of the current file (in the same folder) and open it.

If a filename with no extension will be entered, the same extension used
for the original file will be used for the new file.

Suggested key combination: `Insert Ctrl-D`


## edit-string ##

Open a dialog for editing a string.

If the caret is standing on a string, it'll edit the current string.
Otherwise you can enter a new string and it'll be inserted into the
document. The dialog has lots of checkboxes for toggling things about the
string: Whether it's unicode, raw, bytes, type of quote, etc.

When is this better than editing a string in the editor?

- When you have a mess of escape character. The dialog automatically
    translates the escape characters for you so you don't have to think
    about them. (Very useful when entering Windows paths that have
    backslashes in them.)

- When you're editing a multiline string of this style:
    raise Exception("There's some long text here that takes up more than "
        "one line, and it's broken in a nice way that doesn't "
        "exceed 79 characters, and every time you edit it you "
        "see it as one block of text, while the cutting "
        "points will be automatically determined by the "
        "dialog.")

Note: Currently doesn't work on docstrings, and other triple-quote
multiline strings.

Suggested key combination: `Ctrl-Alt-S`


## flip ##

Flip between `True` and `False`.

Suggested key combination: `Insert P`


## flip-case ##

Flip the case of the current word between undercase and camelcase.

For example, if the cursor is on `something_like_this` and you activate
this script, you'll get `SomethingLikeThis`. Do it again and you'll get
`something_like_this` again.

Suggested key combination: `Insert C`


## for-thing-in-things ##

Turn `things` into `for thing in things:`.

Type any pluarl word, like `bananas` or `directories`. Then run this
script, and you get `for directory in directories`.

This also works for making `range(number)` into `for i in range(number):`.

Note: The `:` part is added only on Windows.

Suggested key combination: `Insert Ctrl-F`


## forward-half-page ##
    
Move half a page down.
    
This is essentially one half of Page-Down.

Suggested key combination: `Alt-Page_down` (As long as you don't use Wing's
folding.)


## frame-show-and-home ##

Go to the line of the current frame and send caret to beginning of text.

When you use Wing's default `frame-show` command to go to the line of the
current frame, it sends the caret to column 0, which is annoying. This script
fixes that by first doing `frame-show`, then sending the caret to the beginning
of the text.

Suggested key combination: `Shift-F11`


## go-down-to-project-frame ##

Go down one frame in the debugger, skipping any non-project frames.

Did you ever have Wing stop on an exception, and then drop you in code that
belongs to an external module? This is often annoying, because you want to
figure out what you did wrong on *your* code, and the external module is
usually not to blame.

`go-down-to-project-frame` to the rescue! Invoke this script while
debugging in order to be taken to the closest lower stack frame that's on a
project file rather than an external module.

Suggested key combination: `Alt-F12`


## go-up-to-project-frame ##

Go up one frame in the debugger, skipping any non-project frames.

Did you ever have Wing stop on an exception, and then drop you in code that
belongs to an external module? This is often annoying, because you want to
figure out what you did wrong on *your* code, and the external module is
usually not to blame.

`go-up-to-project-frame` to the rescue! Invoke this script while debugging
in order to be taken to the closest higher stack frame that's on a project
file rather than an external module.
    
Suggested key combination: `Alt-F11`


## guess-class-name ##

Guess the class name based on file name, and replace class name.

Imagine you had a file `foo_manager.py` with a class `FooManager` defined
in it, and you duplicated it, calling the new file `bar_grokker.py`. If you
run `guess-class-name`, it'll replace all instances of `FooManager` in your
new file to `BarGrokker`.

(It finds the original class name by taking the first class defined in the
file. If the file defined multiple classes, you might get the wrong
results.)

Suggested key combination: `Insert Ctrl-C`


## implicit-getattr-to-explicit ##

Convert something like `foo.bar` into `getattr(foo, 'bar', None)`.

Also selects the `None` so it could be easily modified.

Suggested key combination: `Insert Shift-G`


## instantiate ##
    
Write `my_class_name = MyClassName()`.
    
This is used to quickly instantiate a class. Write your class name, like
`CatNip`. It will usually be autocompleted. Then execute this script, and
you'll have `cat_nip = CatNip()`, with the cursor positioned between the brackes.

This saves a lot of typing, because normally you don't have autocompletion for
the new instance name `cat_nip` because it doesn't exist yet.

Note: The `()` part is added only on Windows.

Suggested key combination: `Insert I`


## previous-brace-match ##

Select the previous pair of braces.

Similar to Wing's built-in `brace-match`, except it goes backwards instead
of going forwards. Goes to the nearest pair of braces, whether it's (), [],
or {} that's before the current caret position, and selects those braces
including all their content.

Known limitations: Misses some pairs of braces. Doesn't know to ignore
braces found in strings.

Suggested key combination: `Ctrl-Bracketleft`


## previous-brace-match-inner ##

Select the inside of the previous pair of braces.

Similar to Wing's built-in `brace-match`, except it goes backwards instead
of going forwards. Goes to the nearest pair of braces, whether it's (), [],
or {} that's before the current caret position, and selects the content of
those braces, not including the braces themselves.

Known limitations: Misses some pairs of braces. Doesn't know to ignore
braces found in strings.

Suggested key combination: `Alt-Bracketleft`


## push-line-to-end ##

Push the current line to the end, aligning it to right border of editor.
    
This inserts or deletes as many spaces as necessary from the beginning of the
line to make the end of the line exactly coincide with the right border of the
editor. (Whose width can be configured in the `TARGET_LINE_LENGTH` constant in
the script's module.)

This is useful for creating lines of this style:
    
    if first_long_condition(foo, foobar) and \
                                          second_long_condition(fubaz, bazbar):

Also deletes trailing spaces.                                          


## remove-invocation ##

Remove the last invocation, turning `whatever.function(value)` to `value`.

Suggested key combinations: `Insert 8`


## remove-rectangles ##

Remove all rectangles that Wing drew on the editor.

Wing sometimes draws rectangles on the editor, either for search results or
for highlighting appearances of the currently selected word. This command
clears all of those squares.

Suggested key combination: `Insert Ctrl-R`


## reverse-selection ##

Reverse the selection, putting the caret on the opposite side.

If the caret was at the beginning of the selection, it'll be put at the
end, and if it was in the end, it'll be put in the beginning.

Suggested key combination: `Insert Shift-R`


## run-command-idempotent ##

Run a command, first terminating any running instances of it.


## select-dotted-name ##

Select the dotted name that the cursor is currently on, like `foo.bar.baz`.

This does `select-more` until the biggest possible dotted name is selected.

Suggested key combination: `Alt-Plus`


## select-expression ##

Select the Python expression that the cursor is currently on.

This does `select-more` until the biggest possible legal Python expression is
selected.
    
Suggested key combination: `Ctrl-Alt-Plus`


## select-next-argument ##

Select the next argument to a callable.

Set `limit_to_keywords=True` to go only to a keyword argument.

Suggested key combinations: `Ctrl-R`
                            `Ctrl-Alt-R` for `limit_to_keywords=True`


## select-next-assignment ##

Select the next (or current) assignment in the document.

This includes:

    = += -= *= /= **= //= %= |= &= ^= <<= >>=

Suggested key combination: `Ctrl-Alt-Backslash`


## select-next-camelcase ##

Select the next (or current) camelcase in the document.

Camelcase means a variable name that has a combination of lowercase and
uppercase letters.

Suggested key combination: `Ctrl-Alt-C`


## select-next-constant ##

Select the next (or current) constant in the document.

Constant means a name in all caps, like DEBUG or LOGIN_REDIRECT_URL.

Suggested key combination: `Ctrl-Alt-O`


## select-next-dotted ##

Select the next (or current) dotted name in the document, like `foo.bar`.

Suggested key combination: `Ctrl-D`


## select-next-invocation ##

Select the next invocation of a callable, e.g `foo.bar(baz)`.

Suggested key combination: `Ctrl-Alt-8`
    
    
## select-next-lhs ##

Select the next left-hand-side of an assignment.

Suggested key combination: `Ctrl-Alt-9`


## select-next-number ##

Select the next (or current) number in the document.

Suggested key combination: `Ctrl-0`


## select-next-operator ##

Select the next (or current) operator in the document.

Operators are:

    + - * / ** // % | & ^ << >> == != < <= > >=

Suggested key combination: `Alt-Backslash`


## select-next-rhs ##

Select the next right-hand-side of an assignment.

Suggested key combination: `Ctrl-Alt-0`


## select-next-scope-name ##

Select the next scope name like `def thing():` or `class Thing():`.

(Selects just the name.)

Suggested key combination: `Alt-Semicolon`


## select-next-string ##

Select the next (or current) string, starting from caret location.

Provide `inner=True` to select only the contents of the string.

Suggested key combinations: `Ctrl-Apostrophe`
                            `Alt-Apostrophe` for `inner=True`


## select-prev-argument ##

Select the previous argument to a callable.

Set `limit_to_keywords=True` to go only to a keyword argument.

Suggested key combinations: `Ctrl-Shift-R`
                            `Ctrl-Shift-Alt-R` for `limit_to_keywords=True`
                            
                            
## select-prev-assignment ##

Select the previous assignment in the document.

This includes:

    = += -= *= /= **= //= %= |= &= ^= <<= >>=

Suggested key combination: `Ctrl-Alt-Bar`


## select-prev-camelcase ##

Select the previous camelcase in the document.

Camelcase means a variable name that has a combination of lowercase and
uppercase letters.

Suggested key combination: `Ctrl-Alt-Shift-C`


## select-prev-constant ##

Select the previous constant in the document.

Constant means a name in all caps, like DEBUG or LOGIN_REDIRECT_URL.

Suggested key combination: `Ctrl-Alt-Shift-O`


## select-prev-dotted ##

Select the previous dotted name in the document, like `foo.bar`.

Suggested key combination: `Ctrl-Shift-D`


## select-prev-invocation ##

Select the previous invocation of a callable, e.g `foo.bar(baz)`.

Suggested key combination: `Ctrl-Alt-Asterisk`
    
    
## select-prev-lhs ##

Select the previous left-hand-side of an assignment.

Suggested key combination: `Ctrl-Alt-Parenleft`


## select-prev-number ##

Select the previous number in the document.

Suggested key combination: `Ctrl-9`


## select-prev-operator ##

Select the previous operator in the document.

Operators are:

    + - * / ** // % | & ^ << >> == != < <= > >=

Suggested key combination: `Alt-Bar`


## select-prev-rhs ##

Select the previous right-hand-side of an assignment.

Suggested key combination: `Ctrl-Alt-Parenright`


## select-prev-scope-name ##

Select the previous scope name like `def thing():` or `class Thing():`.

(Selects just the name.)

Suggested key combination: `Alt-Colon`


## select-prev-string ##

Select the previous string, starting from caret location.

Provide `inner=True` to select only the contents of the string.

Suggested key combinations: `Ctrl-Quotedbl`
                            `Alt-Quotedbl` for `inner=True`


# select-scope-name #

Select the name of the function or class that the cursor is currently on.

Suggested key combination: `Alt-Colon`


## select-whitespaceless-name ##

Select the whitespace-less name that the cursor is currently on.

Example: `foo.bar.baz(e=3)`.

This does `select-more` until the biggest possible whitespace-less name is selected.

Suggested key combination: `Ctrl-Alt-Equal`

    
## slash-line ##

Slash a long line into 2 lines, putting a `\` character as a separator.
    
This is good for automatically formatting long lines into this style:

    has_corresponding_source_file = \
                               os.path.exists(corresponding_python_source_file)
    nose.selector.Selector.wantFile = \
                       types.MethodType(wantFile, None, nose.selector.Selector)
    
Specify `line_offset` to slash a line different from the one that the caret
is on. For example, `line_offset=-1` would slash the previous line.

Specify `at_caret=True` to use the current caret position as the slashing
point, rather than finding one automatically.

Suggested key combination: `Insert L` for default arguments, `Insert Shift-L` for `line_offset=-1`, and `Insert Ctrl-L` for `at_caret=True`.


## smartgit ##

Start SmartGit for the current project.

Suggested key combination: `Insert G`    


## smartgit-blame ##

Start SmartGit blame on the currently selected line.
    
Suggested key combination: `Insert Ctrl-B`    


## type-super ##

Type `super(MyClass, self).my_method()`

`MyClass` and `my_method` will be copied with the current class and method
of the active scope.

Suggested key combination: `Insert Ctrl-S`


## unpack-tuple-to-one ##

Turn `things` into `(thing,)`.

Useful for writing things like:

    (thing,) == things
    
See this blog post for more context: http://blog.ram.rachum.com/post/1198230058/python-idiom-for-taking-the-single-item-from-a-list

Suggested key combination: `Insert U`


## wrap-lines-toggle ##

Toggle whether Wing wraps lines or not.
