# Cute Wing stuff #

A collection of scripts for [Wing IDE 4](http://www.wingware.com/).

In order to use these scripts in your copy of Wing, download the repo to
someplace in your computer, fire up Wing, go to `Edit` -> `Preferences` -> `IDE
Extension Scripting` and add the path of the repo's `scripts` folder to your
`Search Path`. (Possibly you'll need to do `edit` -> `Reload All Scripts` to
get Wing to see them for the first time.)

After you do that, the commands will become available in Wing; For example you
could do `Ctrl-F12` and then type `flip-case` to activate the `flip_case`
script. But you probably want to bind these commands to some key combination;
do that in `Edit` -> `Preferences` -> `Keyboard` -> `Custom Key Bindings`.)


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
argument.) Then run this `arg_to_attr` script.

The final result is that you'll get a `self.crunchiness = crunchiness` line and
have the cursor ready in the next line.

Suggested key combination: `Ctrl-Insert A`.


## flip-case ##

Flip the case of the current word between undercase and camelcase.

For example, if the cursor is on `something_like_this` and you activate
this script, you'll get `SomethingLikeThis`. Do it again and you'll get
`something_like_this` again.

Suggested key combination: `Ctrl-Insert C`.


## comment-braces ##

Create "comment braces" with a title around a piece of code.

For example, if you have this code:

    do_something()
    do_something_else()
    meow = frr + 7
    do_something_again()
    
You can select it, then run the `comment_braces` script with a title of
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

Suggested key combination: `Ctrl-Insert B`.


## comment-hr ##

Enter a horizontal line of "#" characters going until character 79.

Example:

    #######################################################################
    
Suggested key combination: `Ctrl-Insert H`.
