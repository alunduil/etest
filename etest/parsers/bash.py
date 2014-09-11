# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os
import ply.yacc

from etest.lexers.bash import BashLexer, BashSyntaxError

logger = logging.getLogger(__name__)


class BashParser(object):
    tokens = BashLexer.tokens

    def __init__(self):
        self.symbols = {}

        self.start = 'inputunit_list'

        self.parser = None

    def build(self, *args, **kwargs):
        self.parser = ply.yacc.yacc(
            module = self,
            tabmodule = 'bashtab',
            optimize = 1,
            outputdir = os.path.dirname(__file__),
            errorlog = logger,
            *args,
            **kwargs
        )

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

        for _ in range(len(p)):
            logger.debug('world_list: p[%d]: %s', _, p[_])

        p[0] = (p[1],)

        logger.debug('world_list: p[0]: %s', p[0])

    def p_word_list_list(self, p):
        '''word_list : word_list WORD'''

        for _ in range(len(p)):
            logger.debug('world_list: p[%d]: %s', _, p[_])

        p[0] = p[1] + (p[2],)

        logger.debug('word_list: p[0]: %s', p[0])

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

        for _ in range(len(p)):
            logger.debug('simple_command_element: p[%d]: %s', _, p[_])

        p[0] = ('WORD', p[1])

    def p_simple_command_element_assignment(self, p):
        '''simple_command_element : ASSIGNMENT_WORD'''

        for _ in range(len(p)):
            logger.debug('simple_command_element: p[%d]: %s', _, p[_])

        p[0] = ('ASSIGNMENT', p[1])

    def p_simple_command_element_redirection(self, p):
        '''simple_command_element : redirection'''

        for _ in range(len(p)):
            logger.debug('simple_command_element: p[%d]: %s', _, p[_])

        p[0] = ('REDIRECTION',)

    def p_redirection_list(self, p):
        '''redirection_list : redirection
                            | redirection_list redirection

        '''

        for _ in range(len(p)):
            logger.debug('redirection_list: p[%d]: %s', _, p[_])

    def p_simple_command(self, p):
        '''simple_command : simple_command_element
                          | simple_command simple_command_element

        '''

        for _ in range(len(p)):
            logger.debug('simple_command: p[%d]: %s', _, p[_])

    def p_command(self, p):
        '''command : simple_command
                   | shell_command
                   | shell_command redirection_list
                   | function_def
                   | coproc

        '''

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
                       | FOR WORD newline_list '{' compound_list '}'
                       | FOR WORD ';' newline_list DO compound_list DONE
                       | FOR WORD ';' newline_list '{' compound_list '}'
                       | FOR WORD newline_list IN word_list list_terminator newline_list DO compound_list DONE
                       | FOR WORD newline_list IN word_list list_terminator newline_list '{' compound_list '}'
                       | FOR WORD newline_list IN list_terminator newline_list DO compound_list DONE
                       | FOR WORD newline_list IN list_terminator newline_list '{' compound_list '}'

        '''

        for _ in range(len(p)):
            logger.debug('for_command: p[%d]: %s', _, p[_])

    def p_arith_for_command(self, p):
        '''arith_for_command : FOR ARITH_FOR_EXPRS list_terminator newline_list DO compound_list DONE
                             | FOR ARITH_FOR_EXPRS list_terminator newline_list '{' compound_list '}'
                             | FOR ARITH_FOR_EXPRS DO compound_list DONE
                             | FOR ARITH_FOR_EXPRS '{' compound_list '}'

        '''

        for _ in range(len(p)):
            logger.debug('arith_for_command: p[%d]: %s', _, p[_])

    def p_select_command(self, p):
        '''select_command : SELECT WORD newline_list DO list DONE
                          | SELECT WORD newline_list '{' list '}'
                          | SELECT WORD ';' newline_list DO list DONE
                          | SELECT WORD ';' newline_list '{' list '}'
                          | SELECT WORD newline_list IN word_list list_terminator newline_list DO list DONE
                          | SELECT WORD newline_list IN word_list list_terminator newline_list '{' list '}'

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

    def p_function_def(self, p):
        '''function_def : WORD '(' ')' newline_list function_body
                        | FUNCTION WORD '(' ')' newline_list function_body
                        | FUNCTION WORD newline_list function_body

        '''

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
        '''group_command : '{' compound_list '}' '''

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
            logger.debug('list1: p[%d]: %s', _, p[_])

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

        for _ in range(len(p)):
            logger.debug('simple_list: p[%d]: %s', _, p[_])

    def p_simple_list1(self, p):
        '''simple_list1 : simple_list1 AND_AND newline_list simple_list1
                        | simple_list1 OR_OR newline_list simple_list1
                        | simple_list1 '&' simple_list1
                        | simple_list1 ';' simple_list1
                        | pipeline_command

        '''

        for _ in range(len(p)):
            logger.debug('simple_list1: p[%d]: %s', _, p[_])

    def p_pipeline_command(self, p):
        '''pipeline_command : pipeline
                            | BANG pipeline_command
                            | timespec pipeline_command
                            | timespec list_terminator
                            | BANG list_terminator

        '''

        for _ in range(len(p)):
            logger.debug('pipeline_command: p[%d]: %s', _, p[_])

    def p_pipeline(self, p):
        '''pipeline : pipeline '|' newline_list pipeline
                    | pipeline BAR_AND newline_list pipeline
                    | command

        '''

        for _ in range(len(p)):
            logger.debug('pipeline: p[%d]: %s', _, p[_])

    def p_timespec(self, p):
        '''timespec : TIME
                    | TIME TIMEOPT
                    | TIME TIMEOPT TIMEIGN

        '''

        for _ in range(len(p)):
            logger.debug('timespec: p[%d]: %s', _, p[_])

    def p_error(self, p):
        _ = p.lexer.lexdata.rfind('\n', 0, p.lexpos)

        if _ < 0:
            _ = 0

        column = (p.lexpos - _) + 1

        raise BashSyntaxError('{p.lexer.lineno}: unexpected input: {p} at {0}'.format(column, p = p), p)
