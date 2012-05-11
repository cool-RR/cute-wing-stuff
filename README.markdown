# Cute Wing stuff #

A collection of scripts for [Wing IDE 4.1](http://www.wingware.com/).

In order to use these scripts in your copy of Wing, download the repo to
someplace in your computer, fire up Wing, go to `Edit` -> `Preferences` -> `IDE
Extension Scripting` and add the path of the repo's `scripts` folder to your
`Search Path`. (Possibly you'll need to do `edit` -> `Reload All Scripts` to
get Wing to see them for the first time.)

After you do that, the commands will become available in Wing; For example you
could do `Ctrl-F12` and then type `flip-case` to activate the `flip_case`
script. But you probably want to bind these commands to some key combination;
do that in `Edit` -> `Preferences` -> `Keyboard` -> `Custom Key Bindings`.


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

Suggested key combination: `Alt-Insert A`


## backward-half-page ##
    
Move half a page up.
    
This is essentially one half of Page-Up.

Suggested key combination: `Alt-Page_up` (As long as you don't use Wing's folding.)


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

Suggested key combination: `Alt-Insert B`


## comment-hr ##

Enter a horizontal line of "#" characters going until character 79.

Example:

    #######################################################################
    
Suggested key combination: `Alt-Insert H`


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

Open a new line, but don't move the caret down to the new line.
    
Running this command is like pressing Enter, except your caret doesn't move into the
new line that was created, but stays exactly where it was.

The advantage of this over Wing's built-in `open-line` is that `cute-open-line`
doesn't just insert a newline character like `open-line` does; it runs Wing's
`new-line` command, which does various intelligent things like auto-indenting
your code to the right level, opening your parentheses *just so* if you're
doing function invocation, and a bunch of other goodies.

Suggested key combination: `Ctrl-Return`


## deep-to-var ##
    
Create a variable from a deep expression.

When you're programming, you're often writing lines like these:

    html_color = self._style_handler.html_color
    
Or:

    location = context_data['location']
    
Or:
    
    event_handler = super(Foobsnicator, self).get_event_handler()
    
What's common to all these lines is that you're accessing some expression,
sometimes a deep one, and then getting an object, and making a variable for
that object with the same name that it has in the deep expression.

What this `deep-to-var` script will do for you is save you from having to write
the `html_color = ` part, which is annoying to type because you don't have
autocompletion for it.

Just write your deep expression, like `self._style_handler.html_color`, invoke
this `deep-to-var` script, and you'll get the full line and have the caret put
on the next line.

Suggested key combination: `Alt-Insert E`


## delete-line-and-home ##

Delete the current line and send caret to beginning of text in next line.
    
When you use Wing's default `delete-line` command to delete a line, it
sends the caret to column 0, which is annoying. This script fixes that by
first deleting a line, then sending the caret to the beginning of the text
on the next line.

Suggested key combination: `Ctrl-Shift-C`


## flip ##

Flip between `True` and `False`.

Suggested key combination: `Alt-Insert P`


## flip-case ##

Flip the case of the current word between undercase and camelcase.

For example, if the cursor is on `something_like_this` and you activate
this script, you'll get `SomethingLikeThis`. Do it again and you'll get
`something_like_this` again.

Suggested key combination: `Alt-Insert C`


## for-thing-in-things ##

Turn `things` into `for thing in things`.

Type any pluarl word, like `bananas` or `directories`. Then run this
script, and you get `for directory in directories`.

Suggested key combination: `Alt-Insert Ctrl-F`


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


## go-to-lowest-project-frame ##

Go to the lowest frame that's on project file rather than external module.

Did you ever have Wing stop on an exception, and then drop you in code that
belongs to an external module? This is often annoying, because you want to
figure out what you did wrong on *your* code, and the external module is
usually not to blame.

`go-to-lowest-project-frame` to the rescue! Invoke this script while debugging
in order to be taken to the lowest stack frame that's on a project file rather
than an external module.
    
Suggested key combination: `Alt-F11`
    

## instantiate ##
    
Write `my_class_name = MyClassName`.
    
This is used to quickly instantiate a class. Write your class name, like
`CatNip`. It will usually be autocompleted. Then execute this script, and
you'll have `cat_nip = CatNip`, with the cursor positioned at the end. Then
just press `(`, type in the arguments, and you're set.

This saves a lot of typing, because normally you don't have autocompletion for
the new instance name `cat_nip` because it doesn't exist yet.

Suggested key combination: `Alt-Insert I`


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

Suggested key combination: `Alt-Insert End`


## show-file-in-explorer ##

Open the currently-edited file's folder in Explorer.

Implementd only for Windows.

Suggested key combination: `Alt-Insert Ctrl-J`


## select-expression ##

Select the Python expression that the cursor is currently on.

This does `select-more` until the biggest possible legal Python expression is
selected.
    
Suggested key combination: `Ctrl-Alt Plus`

    
## slash-line ##

Slash a long line into 2 lines, putting a `\` character as a separator.
    
This is good for automatically formatting long lines into this style:

    has_corresponding_source_file = \
                               os.path.exists(corresponding_python_source_file)
    nose.selector.Selector.wantFile = \
                       types.MethodType(wantFile, None, nose.selector.Selector)
    
Suggested key combination: `Alt-Insert L`


## start-debug-with-preset-args ##

Start debugging with preset arguments.

You need to have a git-ignored file `cute_wing_stuff_local_settings.py`
right in this `scripts` folder, which defines a `dict` like this:

    all_debug_argument_presets = {
        'my_django_app.wpr': ['runserver --noreload', 'test']
        'other_django_app.wpr': ['runserver 80 --noreload', 'test',
                                 'syncdb']
        None: ['runserver 80 --noreload', 'test'], 
    }
   
What does this file mean? For each of your projects, you define the
different presets for debug arguments that will be used for your main debug
file. `None` is used as the default for any Wing projects that are not
listed.

Then you call this `start-debug-with-preset-args` with the `i_preset`
argument equal to the preset index number, and debug will start with those
arguments.

Suggested key combinations: `Alt-Insert F5` for preset 0, `Alt-Insert Shift-F5` for preset 1, `Alt-Insert Ctrl-F5` for preset 2, `Alt-Insert Ctrl-Shift-F5` for preset 3
