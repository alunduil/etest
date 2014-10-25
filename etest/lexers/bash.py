# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os
import ply.lex

logger = logging.getLogger(__name__)

reserved = (
    'CASE',
    'COPROC',
    'DO',
    'DONE',
    'ELIF',
    'ELSE',
    'ESAC',
    'FI',
    'FOR',
    'FUNCTION',
    'IF',
    'IN',
    'SELECT',
    'THEN',
    'TIME',
    'UNTIL',
    'WHILE',
)


class BashLexer(object):
    def __init__(self):
        self.lexer = None

    def build(self, *args, **kwargs):
        self.lexer = ply.lex.lex(
            module = self,
            outputdir = os.path.dirname(__file__),
            errorlog = logger,
            *args,
            **kwargs
        )

    states = (
        ( 'singlequote', 'exclusive', ),
        ( 'doublequote', 'exclusive', ),
    )

    tokens = (
        'AND_AND',
        'AND_GREATER',
        'AND_GREATER_GREATER',
        'ARITH_CMD',
        'ARITH_FOR_EXPRS',
        'BANG',
        'BAR_AND',
        'COMMENT',
        'COND_CMD',
        'COND_END',
        'COND_START',
        'DOUBLE_QUOTE',
        'GREATER_AND',
        'GREATER_BAR',
        'GREATER_GREATER',
        'LESS_AND',
        'LESS_GREATER',
        'LESS_LESS',
        'LESS_LESS_LESS',
        'LESS_LESS_MINUS',
        'NEWLINE',
        'NUMBER',
        'OR_OR',
        'REDIR_WORD',
        'SEMI_AND',
        'SEMI_SEMI',
        'SEMI_SEMI_AND',
        'SINGLE_QUOTE',
        'TIMEIGN',
        'TIMEOPT',
        'WORD',
    ) + reserved

    literals = (
        '<',
        '=',
        '>',
        '|',
        '-',
        ';',
        '(',
        ')',
        '{',
        '}',
        '&',
    )

    t_AND_AND = r'&&'
    t_AND_GREATER = r'&<'
    t_AND_GREATER_GREATER = r'&<<'

    def t_ARITH_CMD(self, t):
        r'arith cmd'
        return t

    def t_ARITH_FOR_EXPRS(self, t):
        r'arith for exprs'
        return t

    t_BANG = r'!'
    t_BAR_AND = r'\|&'

    t_ignore_COMMENT = r'\#[^\n]*'

    def t_COND_CMD(self, t):
        r'cond cmd'
        return t

    t_COND_END = r']]'
    t_COND_START = r'\[\['

    def t_DOUBLE_QUOTE(self, t):
        r'"'

        if t.lexer.lexstate == 'INITIAL':
            t.lexer.begin('doublequote')

        return t

    def t_doublequote_DOUBLE_QUOTE(self, t):
        r'"'

        t.lexer.begin('INITIAL')

        return t

    t_doublequote_WORD = r'([^"]|(\\\\)*\\")+'

    t_GREATER_AND = r'>&'
    t_GREATER_BAR = r'>\|'
    t_GREATER_GREATER = r'>>'
    t_LESS_AND = r'<&'
    t_LESS_GREATER = r'<>'
    t_LESS_LESS = r'<<'
    t_LESS_LESS_LESS = r'<<<'
    t_LESS_LESS_MINUS = r'<<-'

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.type = 'NEWLINE'
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_OR_OR = r'\|\|'

    def t_REDIR_WORD(self, t):
        r'stdin|stdout|stderr'
        return t

    t_SEMI_AND = r';&'
    t_SEMI_SEMI = r';;'
    t_SEMI_SEMI_AND = r';;&'

    def t_SINGLE_QUOTE(self, t):
        r'\''

        if t.lexer.lexstate == 'INITIAL':
            t.lexer.begin('singlequote')

        return t

    def t_singlequote_SINGLE_QUOTE(self, t):
        r'\''

        t.lexer.begin('INITIAL')

        return t

    t_singlequote_WORD = r'([^\']|(\\\\)*\\\')+'

    t_TIMEIGN = r'--'
    t_TIMEOPT = r'-p'

    def t_WORD(self, t):
        r'[a-zA-Z-][\da-zA-Z\./{},_-]*'

        if t.value.upper() in reserved:
            t.type = t.value.upper()

        return t

    t_ignore = ' \t'
    t_doublequote_ignore = ''
    t_singlequote_ignore = ''

    def t_error(self, t):
        line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos)

        if line_start < 0:
            line_start = 0

        column = (t.lexpos - line_start) + 1

        line_end = t.lexer.lexdata.find('\n', t.lexpos)

        if line_end < 0:
            line_end = t.lexpos

        error_message = '{t.lexer.lineno}: '.format(t = t)

        _ = len(error_message)

        error_message += t.lexer.lexdata[line_start:line_end].strip() + '\n'
        error_message += ' ' * ( column - 2 + _ ) + '^\n'
        error_message += 'unexpected token: {t.value}'.format(t = t)

        logger.error('\n' + error_message)

        raise BashSyntaxError(error_message, t)

    t_singlequote_error = t_error
    t_doublequote_error = t_error


class BashSyntaxError(RuntimeError):
    pass
