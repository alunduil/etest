# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os
import ply.yacc
import re

from etest.lexers.bash import BashLexer, BashSyntaxError

logger = logging.getLogger(__name__)


def split_expansion(text):
    '''Properly split an expansion's items at commas.'''

    expansion = ''
    level = 0

    for character in text:
        if character == ',' and level == 0:
            yield expansion
            expansion = ''
            continue

        if character == '{':
            level += 1

        if character == '}':
            level -= 1

        expansion += character

    yield expansion


def expand_word(word):
    '''Expand any BASH expansions and return the resulting tuple of words.'''

    logger.debug('word: %s', word)

    if not re.search(r'(?:(?:\\\\)*\\)?(?<!\$){', word):
        logger.debug('words: %s', (word, ))

        return (word, )

    prefix, rest = re.split(r'(?:(?:\\\\)*\\)?(?<!\$){', word, 1)
    logger.debug('prefix: %s', prefix)

    logger.debug('rest: %s', rest)

    suffix = ''.join(re.split(r'(?:(?:\\\\)*\\)?}', word)[-max(prefix.count('${'), 1):])
    logger.debug('suffix: %s', suffix)

    rest = rest[:rest.rindex(suffix) - 1].lstrip('\\}')

    logger.debug('rest: %s', rest)

    words = []

    for expansion in split_expansion(rest):
        words.extend([ prefix + _ + suffix for _ in expand_word(expansion) ])

    logger.debug('words: %s', tuple(words))

    return tuple(words)


class BashParser(object):
    tokens = BashLexer.tokens

    start = 'inputunit_list'

    precedence = (
        ('left', '&', ';', 'NEWLINE', ),
        ('left', 'AND_AND', 'OR_OR', ),
        ('right', '|', 'BAR_AND', ),
    )

    def __init__(self):
        self.parser = None

        self.symbols = {}

    def build(self, *args, **kwargs):
        self.parser = ply.yacc.yacc(
            module = self,
            outputdir = os.path.dirname(__file__),
            errorlog = logger,
            picklefile = os.path.join(os.path.dirname(__file__), 'bash.p'),
            *args,
            **kwargs
        )

    #
    # Modified Productions from the BASH Grammar
    #

    def p_inputunit_list(self, p):
        '''inputunit_list : inputunit
                          | inputunit_list inputunit

        '''

        for _ in range(len(p)):
            logger.debug('inputunit_list: p[%d]: %s', _, p[_])

    def p_inputunit(self, p):
        '''inputunit : simple_list simple_list_terminator
                     | NEWLINE

        '''

        for _ in range(len(p)):
            logger.debug('inputunit: p[%d]: %s', _, p[_])

    def p_word_list_word(self, p):
        '''word_list : WORD'''

        p[0] = expand_word(p[1])

        for _ in range(len(p)):
            logger.debug('world_list: p[%d]: %s', _, p[_])

    def p_word_list_list(self, p):
        '''word_list : word_list newline_list WORD'''

        p[0] = p[1] + expand_word(p[3])

        for _ in range(len(p)):
            logger.debug('world_list: p[%d]: %s', _, p[_])

    def p_redirection(self, p):
        '''redirection : '>' WORD
                       | '<' WORD
                       | NUMBER '>' WORD
                       | NUMBER '<' WORD
                       | REDIR_WORD '>' WORD
                       | REDIR_WORD '<' WORD
                       | GREATER_GREATER WORD
                       | NUMBER GREATER_GREATER WORD
                       | REDIR_WORD GREATER_GREATER WORD
                       | GREATER_BAR WORD
                       | NUMBER GREATER_BAR WORD
                       | REDIR_WORD GREATER_BAR WORD
                       | LESS_GREATER WORD
                       | NUMBER LESS_GREATER WORD
                       | REDIR_WORD LESS_GREATER WORD
                       | LESS_LESS WORD
                       | NUMBER LESS_LESS WORD
                       | REDIR_WORD LESS_LESS WORD
                       | LESS_LESS_MINUS WORD
                       | NUMBER LESS_LESS_MINUS WORD
                       | REDIR_WORD LESS_LESS_MINUS WORD
                       | LESS_LESS_LESS WORD
                       | NUMBER LESS_LESS_LESS WORD
                       | REDIR_WORD LESS_LESS_LESS WORD
                       | LESS_AND NUMBER
                       | NUMBER LESS_AND NUMBER
                       | REDIR_WORD LESS_AND NUMBER
                       | GREATER_AND NUMBER
                       | NUMBER GREATER_AND NUMBER
                       | REDIR_WORD GREATER_AND NUMBER
                       | LESS_AND WORD
                       | NUMBER LESS_AND WORD
                       | REDIR_WORD LESS_AND WORD
                       | GREATER_AND WORD
                       | NUMBER GREATER_AND WORD
                       | REDIR_WORD GREATER_AND WORD
                       | GREATER_AND '-'
                       | NUMBER GREATER_AND '-'
                       | REDIR_WORD GREATER_AND '-'
                       | LESS_AND '-'
                       | NUMBER LESS_AND '-'
                       | REDIR_WORD LESS_AND '-'
                       | AND_GREATER WORD
                       | AND_GREATER_GREATER WORD

        '''

        for _ in range(len(p)):
            logger.debug('redirection: p[%d]: %s', _, p[_])

    def p_simple_command_element_word(self, p):
        '''simple_command_element : WORD'''

        p[0] = ('WORD', p[1])

        for _ in range(len(p)):
            logger.debug('simple_command_element: p[%d]: %s', _, p[_])

    def p_simple_command_element_assignment(self, p):
        '''simple_command_element : assignment_word'''

        p[0] = ('ASSIGNMENT', p[1])

        for _ in range(len(p)):
            logger.debug('simple_command_element: p[%d]: %s', _, p[_])

    def p_simple_command_element_redirection(self, p):
        '''simple_command_element : redirection'''

        p[0] = ('REDIRECTION',)

        for _ in range(len(p)):
            logger.debug('simple_command_element: p[%d]: %s', _, p[_])

    def p_redirection_list(self, p):
        '''redirection_list : redirection
                            | redirection_list redirection

        '''

        for _ in range(len(p)):
            logger.debug('redirection_list: p[%d]: %s', _, p[_])

    def p_simple_command(self, p):
        '''simple_command : simple_command_element
                          | simple_command curly_off simple_command_element

        '''

        for _ in range(len(p)):
            logger.debug('simple_command: p[%d]: %s', _, p[_])

    def p_command(self, p):
        '''command : simple_command curly_on
                   | shell_command
                   | shell_command redirection_list
                   | function_def
                   | coproc

        '''

        p[0] = (p[1], )

        for _ in range(len(p)):
            logger.debug('command: p[%d]: %s', _, p[_])

    def p_shell_commend(self, p):
        '''shell_command : for_command
                         | case_command
                         | WHILE compound_list DO compound_list DONE
                         | UNTIL compound_list DO compound_list DONE
                         | select_command
                         | if_command
                         | subshell
                         | group_command
                         | arith_command
                         | cond_command
                         | arith_for_command

        '''

        for _ in range(len(p)):
            logger.debug('shell_command: p[%d]: %s', _, p[_])

    def p_for_command(self, p):
        '''for_command : FOR WORD newline_list DO compound_list DONE
                       | FOR WORD newline_list LBRACE compound_list '}'
                       | FOR WORD ';' newline_list DO compound_list DONE
                       | FOR WORD ';' newline_list LBRACE compound_list '}'
                       | FOR WORD newline_list IN word_list list_terminator newline_list DO compound_list DONE
                       | FOR WORD newline_list IN word_list list_terminator newline_list LBRACE compound_list '}'
                       | FOR WORD newline_list IN number_list list_terminator newline_list DO compound_list DONE
                       | FOR WORD newline_list IN number_list list_terminator newline_list LBRACE compound_list '}'
                       | FOR WORD newline_list IN list_terminator newline_list DO compound_list DONE
                       | FOR WORD newline_list IN list_terminator newline_list LBRACE compound_list '}'

        '''

        for _ in range(len(p)):
            logger.debug('for_command: p[%d]: %s', _, p[_])

    def p_arith_for_command(self, p):
        '''arith_for_command : FOR ARITH_FOR_EXPRS list_terminator newline_list DO compound_list DONE
                             | FOR ARITH_FOR_EXPRS list_terminator newline_list LBRACE compound_list '}'
                             | FOR ARITH_FOR_EXPRS DO compound_list DONE
                             | FOR ARITH_FOR_EXPRS LBRACE compound_list '}'

        '''

        for _ in range(len(p)):
            logger.debug('arith_for_command: p[%d]: %s', _, p[_])

    def p_select_command(self, p):
        '''select_command : SELECT WORD newline_list DO list DONE
                          | SELECT WORD newline_list LBRACE list '}'
                          | SELECT WORD ';' newline_list DO list DONE
                          | SELECT WORD ';' newline_list LBRACE list '}'
                          | SELECT WORD newline_list IN word_list list_terminator newline_list DO list DONE
                          | SELECT WORD newline_list IN word_list list_terminator newline_list LBRACE list '}'

        '''

        for _ in range(len(p)):
            logger.debug('select_command: p[%d]: %s', _, p[_])

    def p_case_command(self, p):
        '''case_command : CASE WORD newline_list IN newline_list ESAC
                        | CASE WORD newline_list IN case_clause_sequence newline_list ESAC
                        | CASE WORD newline_list IN case_clause ESAC

        '''

        for _ in range(len(p)):
            logger.debug('case_command: p[%d]: %s', _, p[_])

    def p_function_def_without_keyword(self, p):
        '''function_def : WORD '(' ')' newline_list function_body'''

        p[0] = ('FUNCTION', p[1], p[5], )

        for _ in range(len(p)):
            logger.debug('function_def: p[%d]: %s', _, p[_])

    def p_function_def_with_keyword_and_parens(self, p):
        '''function_def : FUNCTION WORD '(' ')' newline_list function_body'''

        p[0] = (p[1], p[2], p[6], )

        for _ in range(len(p)):
            logger.debug('function_def: p[%d]: %s', _, p[_])

    def p_function_def(self, p):
        '''function_def : FUNCTION WORD newline_list function_body'''

        p[0] = (p[1], p[2], p[4], )

        for _ in range(len(p)):
            logger.debug('function_def: p[%d]: %s', _, p[_])

    def p_function_body(self, p):
        '''function_body : shell_command
                         | shell_command redirection_list

        '''

        for _ in range(len(p)):
            logger.debug('function_body: p[%d]: %s', _, p[_])

    def p_subshell(self, p):
        '''subshell : '(' compound_list ')' '''

        for _ in range(len(p)):
            logger.debug('subshell: p[%d]: %s', _, p[_])

    def p_coproc(self, p):
        '''coproc : COPROC shell_command
                  | COPROC shell_command redirection_list
                  | COPROC WORD shell_command
                  | COPROC WORD shell_command redirection_list
                  | COPROC simple_command

        '''

        for _ in range(len(p)):
            logger.debug('coproc: p[%d]: %s', _, p[_])

    def p_if_command(self, p):
        '''if_command : IF compound_list THEN compound_list FI
                      | IF compound_list THEN compound_list ELSE compound_list FI
                      | IF compound_list THEN compound_list elif_clause FI

        '''

        for _ in range(len(p)):
            logger.debug('subshell: p[%d]: %s', _, p[_])

    def p_group_command(self, p):
        '''group_command : LBRACE compound_list '}' '''

        for _ in range(len(p)):
            logger.debug('group_command: p[%d]: %s', _, p[_])

    def p_arith_command(self, p):
        '''arith_command : ARITH_CMD'''

        for _ in range(len(p)):
            logger.debug('arith_command: p[%d]: %s', _, p[_])

    def p_cond_command(self, p):
        '''cond_command : COND_START COND_CMD COND_END'''

        for _ in range(len(p)):
            logger.debug('cond_command: p[%d]: %s', _, p[_])

    def p_elif_clause(self, p):
        '''elif_clause : ELIF compound_list THEN compound_list
                       | ELIF compound_list THEN compound_list ELSE compound_list
                       | ELIF compound_list THEN compound_list elif_clause

        '''

        for _ in range(len(p)):
            logger.debug('elif_clause: p[%d]: %s', _, p[_])

    def p_case_clause(self, p):
        '''case_clause : pattern_list
                       | case_clause_sequence pattern_list

        '''

        for _ in range(len(p)):
            logger.debug('case_clause: p[%d]: %s', _, p[_])

    def p_pattern_list(self, p):
        '''pattern_list : newline_list pattern ')' compound_list
                        | newline_list pattern ')' newline_list
                        | newline_list '(' pattern ')' compound_list
                        | newline_list '(' pattern ')' newline_list

        '''

        for _ in range(len(p)):
            logger.debug('pattern_list: p[%d]: %s', _, p[_])

    def p_case_clause_sequence(self, p):
        '''case_clause_sequence : pattern_list SEMI_SEMI
                                | case_clause_sequence pattern_list SEMI_SEMI
                                | pattern_list SEMI_AND
                                | case_clause_sequence pattern_list SEMI_AND
                                | pattern_list SEMI_SEMI_AND
                                | case_clause_sequence pattern_list SEMI_SEMI_AND

        '''

        for _ in range(len(p)):
            logger.debug('case_clause_sequence: p[%d]: %s', _, p[_])

    def p_pattern(self, p):
        '''pattern : WORD
                   | pattern '|' WORD

        '''

        for _ in range(len(p)):
            logger.debug('pattern: p[%d]: %s', _, p[_])

    def p_list(self, p):
        '''list : newline_list list0'''

        for _ in range(len(p)):
            logger.debug('list: p[%d]: %s', _, p[_])

    def p_compound_list(self, p):
        '''compound_list : list
                         | newline_list list1

        '''

        for _ in range(len(p)):
            logger.debug('compound_list: p[%d]: %s', _, p[_])

    def p_list0(self, p):
        '''list0 : list1 NEWLINE newline_list
                 | list1 '&' newline_list
                 | list1 ';' newline_list

        '''

        for _ in range(len(p)):
            logger.debug('list0: p[%d]: %s', _, p[_])

    def p_list1(self, p):
        '''list1 : list1 AND_AND newline_list list1
                 | list1 OR_OR newline_list list1
                 | list1 '&' newline_list list1
                 | list1 ';' newline_list list1
                 | list1 NEWLINE newline_list list1
                 | pipeline_command

        '''

        for _ in range(len(p)):
            logger.debug('list2: p[%d]: %s', _, p[_])

    def p_simple_list_terminator(self, p):
        '''simple_list_terminator : NEWLINE'''

        for _ in range(len(p)):
            logger.debug('simple_list_terminator: p[%d]: %s', _, p[_])

    def p_list_terminator(self, p):
        '''list_terminator : NEWLINE
                           | ';'

        '''

        for _ in range(len(p)):
            logger.debug('list_terminator: p[%d]: %s', _, p[_])

    def p_newline_list(self, p):
        '''newline_list :
                        | newline_list NEWLINE

        '''

        for _ in range(len(p)):
            logger.debug('newline_list: p[%d]: %s', _, p[_])

    def p_simple_list(self, p):
        '''simple_list : simple_list1
                       | simple_list1 '&'
                       | simple_list1 ';'

        '''

        p[0] = p[1]

        for _ in range(len(p)):
            logger.debug('simple_list: p[%d]: %s', _, p[_])

    def p_simple_list1_list_with_newlines(self, p):
        '''simple_list1 : simple_list1 AND_AND newline_list simple_list1
                        | simple_list1 OR_OR newline_list simple_list1

        '''

        p[0] = (p[1], p[2], p[4], )

        for _ in range(len(p)):
            logger.debug('simple_list1: p[%d]: %s', _, p[_])

    def p_simple_list1_list(self, p):
        '''simple_list1 : simple_list1 '&' simple_list1
                        | simple_list1 ';' simple_list1

        '''

        p[0] = (p[1], p[2], p[3], )

        for _ in range(len(p)):
            logger.debug('simple_list1: p[%d]: %s', _, p[_])

    def p_simple_list1_command(self, p):
        '''simple_list1 : pipeline_command'''

        p[0] = (p[1], )

        for _ in range(len(p)):
            logger.debug('simple_list1: p[%d]: %s', _, p[_])

    def p_pipeline_command_unmodified(self, p):
        '''pipeline_command : pipeline'''

        p[0] = (p[1], )

        for _ in range(len(p)):
            logger.debug('pipeline_command: p[%d]: %s', _, p[_])

    def p_pipeline_command_modified(self, p):
        '''pipeline_command : BANG pipeline_command
                            | timespec pipeline_command
                            | timespec list_terminator
                            | BANG list_terminator

        '''

        p[0] = (p[1], p[2], )

        for _ in range(len(p)):
            logger.debug('pipeline_command: p[%d]: %s', _, p[_])

    def p_pipeline_with_pipe(self, p):
        '''pipeline : pipeline '|' newline_list pipeline
                    | pipeline BAR_AND newline_list pipeline

        '''

        p[0] = ('PIPE', p[1], p[3], )

        for _ in range(len(p)):
            logger.debug('pipeline: p[%d]: %s', _, p[_])

    def p_pipeline_with_command(self, p):
        '''pipeline : command'''

        p[0] = (p[1], )

        for _ in range(len(p)):
            logger.debug('pipeline: p[%d]: %s', _, p[_])

    def p_timespec(self, p):
        '''timespec : TIME
                    | TIME TIMEOPT
                    | TIME TIMEOPT TIMEIGN

        '''

        for _ in range(len(p)):
            logger.debug('timespec: p[%d]: %s', _, p[_])

    #
    # Additional Productions
    #

    def p_number_list_number(self, p):
        '''number_list : NUMBER'''

        p[0] = (p[1],)

        for _ in range(len(p)):
            logger.debug('world_list: p[%d]: %s', _, p[_])

    def p_number_list_list(self, p):
        '''number_list : number_list newline_list NUMBER'''

        p[0] = p[1] + (p[3],)

        for _ in range(len(p)):
            logger.debug('world_list: p[%d]: %s', _, p[_])

    def p_assignment_word_array(self, p):
        '''assignment_word : WORD '=' assignment_off '(' newline_list word_list newline_list ')' assignment_on'''

        if p[1] in self.symbols:
            logger.warn('re-assignment of %s', p[1])

        self.symbols[p[1]] = p[6]

        p[0] = p[1]

        for _ in range(len(p)):
            logger.debug('assignment_word: p[%d]: %s', _, p[_])

    def p_assignment_word_number(self, p):
        '''assignment_word : WORD '=' NUMBER'''

        if p[1] in self.symbols:
            logger.warn('re-assignment of %s', p[1])

        self.symbols[p[1]] = int(p[3])

        p[0] = p[1]

        for _ in range(len(p)):
            logger.debug('assignment_word: p[%d]: %s', _, p[_])

    def p_assignment_word_word(self, p):
        '''assignment_word : WORD '=' assignment_off WORD assignment_on'''

        if p[1] in self.symbols:
            logger.warn('re-assignment of %s', p[1])

        _ = expand_word(p[4])

        if len(_) == 1:
            _ = _[0]

        if not p[1].startswith('-'):
            self.symbols[p[1]] = _

        p[0] = p[1]

        for _ in range(len(p)):
            logger.debug('assignment_word: p[%d]: %s', _, p[_])

    def p_assignment_off(self, p):
        '''assignment_off : '''

        p.lexer.assignment = False

    def p_assignment_on(self, p):
        '''assignment_on : '''

        p.lexer.assignment = True

    def p_simple_command_element_number(self, p):
        '''simple_command_element : NUMBER'''

        p[0] = ('NUMBER', p[1])

        for _ in range(len(p)):
            logger.debug('simple_command_element: p[%d]: %s', _, p[_])

    def p_curly_off(self, p):
        '''curly_off : '''

        p.lexer.curly = False

    def p_curly_on(self, p):
        '''curly_on : '''

        p.lexer.curly = True

    def p_error(self, p):
        if p is None:
            raise BashSyntaxError('did not receive any input')

        logger.debug('p: %s', p)
        logger.debug('p.type: %s', p.type)
        logger.debug('p.value: %s', p.value)

        line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos)

        if line_start < 0:
            line_start = 0

        column = (p.lexpos - line_start) + 1

        line_end = p.lexer.lexdata.find('\n', p.lexpos)

        if line_end < 0:
            line_end = p.lexpos

        error_message = '{p.lexer.lineno}: '.format(p = p)

        _ = len(error_message)

        error_message += p.lexer.lexdata[line_start:line_end].strip() + '\n'
        error_message += ' ' * ( column - 2 + _ ) + '^\n'
        error_message += 'unexpected token ({p.type}): {p.value}'.format(p = p)

        logger.error('\n' + error_message)

        raise BashSyntaxError(error_message)
