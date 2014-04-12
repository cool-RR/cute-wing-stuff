# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `deep_to_var` script.

See its documentation for more information.
'''


from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import re

from python_toolbox import string_tools

import wingapi

import shared


get_verbs = ('get', 'calculate', 'identify', 'fetch', 'make', 'create',
             'grant', 'open', 'determine', 'download', 'obtain', 'measure',
             'choose')
get_verb_segment = '(?:%s)' % (
    '|'.join(
        '[%s%s]%s' % (verb[0], verb[0].upper(), verb[1:]) for verb in
        get_verbs
    )
)

###############################################################################
###############################################################################

attribute_pattern = re.compile(r'\.([a-zA-Z_][0-9a-zA-Z_]*)$')
getitem_pattern = re.compile(r'''\[['"]([a-zA-Z_][0-9a-zA-Z_]*)['"]\]$''')

### Defining `getter_pattern`: ################################################
#                                                                             #
getter_pattern = re.compile(r'%s_?([a-zA-Z_][0-9a-zA-Z_]*)\(.*\)$' %
                                                              get_verb_segment)
#                                                                             #
### Finished defining `getter_pattern`. #######################################

### Defining `mapping_get_pattern`: ###########################################
#                                                                             #
mapping_get_pattern = re.compile(
    r'''%s\(u?r?['"]{1,3}([a-zA-Z_][0-9a-zA-Z_]*)'''
    r'''['"]{1,3}.*\)$''' % get_verb_segment
)
#                                                                             #
### Finished defining `mapping_get_pattern`. ##################################

### Defining `iter_pattern`: ##################################################
#                                                                             #
iter_pattern = re.compile(
    r'''^iter\(.*\)$'''
)
#                                                                             #
### Finished defining `iter_pattern`. #########################################

### Defining `django_orm_get_pattern`: ########################################
#                                                                             #
django_orm_getter_verbs = ('get', 'get_or_create')

django_orm_getter_verb = '(?:%s)' % (
    '|'.join(
        '[%s%s]%s' % (verb[0], verb[0].upper(), verb[1:]) for verb in
        django_orm_getter_verbs
    )
)

django_orm_get_pattern = re.compile(
    r'([a-zA-Z_][0-9a-zA-Z_]*)\.objects\.%s\(.*\)$' % django_orm_getter_verb
)
#                                                                             #
### Finished defining `django_orm_get_pattern`. ###############################

### Defining `re_match_group_pattern`: ########################################
#                                                                             #
re_match_group_pattern = re.compile(
    r'''match\.group\(['"]([^'"]*?)['"]\)$'''
)
#                                                                             #
### Finished defining `re_match_group_pattern`. ###############################

instantiation_pattern = re.compile(
    r'''([A-Z]\w+)\(.*?\)$'''
)

### Defining datetime module patterns: ########################################
#                                                                             #
now_pattern = re.compile(r'''datetime(?:_module)?\.datetime\.(now)\(\)$''')
today_pattern = re.compile(r'''datetime(?:_module)?\.date\.(today)\(\)$''')
#                                                                             #
### Finished defining datetime module patterns. ###############################

patterns = [django_orm_get_pattern, getter_pattern, attribute_pattern,
            mapping_get_pattern, getitem_pattern, re_match_group_pattern,
            now_pattern, today_pattern, instantiation_pattern, iter_pattern]

variable_name_map = {
    iter_pattern: 'iterator',
}

def deep_to_var(editor=wingapi.kArgEditor):
    '''
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
    
    What this `deep-to-var` script will do for you is save you from having to
    write the `html_color = ` part, which is annoying to type because you don't
    have autocompletion for it.
    
    Just write your deep expression, like `self._style_handler.html_color`,
    invoke this `deep-to-var` script, and you'll get the full line and have the
    caret put on the next line.

    Suggested key combination: `Insert E`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    position, _ = editor.GetSelection()
    line_number = document.GetLineNumberFromPosition(position)
    line_start = document.GetLineStart(line_number)
    line_end = document.GetLineEnd(line_number)
    line = document.GetCharRange(line_start, line_end)
    line_stripped = line.strip()
    
    variable_name = None
    match = None
    for pattern in patterns:
        match = pattern.search(line_stripped)
        if match:
            if pattern in variable_name_map:
                variable_name = variable_name_map[pattern]
            else:
                (variable_name,) = match.groups()
            break
        
    if match:
        if variable_name != variable_name.lower():
            # `variable_name` has an uppercase letter, and thus is probably
            # camel-case. Let's flip it to underscore:
            variable_name = shared.camel_case_to_lower_case(variable_name)
        string_to_insert = '%s = ' % variable_name
        actual_line_start = line_start + \
              string_tools.get_n_identical_edge_characters(line, character=' ')
        
        with shared.UndoableAction(document):
            
            document.InsertChars(actual_line_start, string_to_insert)
            new_position = line_end + len(string_to_insert)
            editor.SetSelection(new_position, new_position)
            editor.ExecuteCommand('new-line')