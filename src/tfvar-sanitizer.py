#!/usr/bin/env python3

import os
import re


def for_each(dirp):
    for filen in [a for a in os.listdir(dirp) if os.path.splitext(a)[-1] == '.tfvars']:
        filep = os.path.join(dirp, filen)
        do_each(filep)
    print('+ all good')


def do_each(filep):
    TfvarSanitizer.exec(filep)


class Reason(object):

    def __init__(self, text, lineno_and_issues):
        self._text = text
        self._lineno_and_issues = lineno_and_issues

    def to_str(self):
        texts = [self._text]
        for r in self._lineno_and_issues:
            texts.append('line {}: {}'.format(r[0], r[1]))
        return '\n'.join(texts)


class TfvarSanitizer(object):

    @classmethod
    def exec(cls, filename):
        lines = None
        with open(filename, 'r') as fp:
            lines = fp.readlines()
        ins = cls(lines)
        reason = ins.process()
        if reason:
            print(filename)
            print(reason.to_str())
            exit(1)

    def __init__(self, lines):
        self._lines = lines
        self._varnames = dict()
        self._dup_varnames = []
        self._new_lines = []

    def for_each(self):
        for idx, line in enumerate(self._lines):
            self._clean_dup_var(idx + 1, line)

    def _clean_dup_var(self, lineno, line):
        """
        
        billing_read_write_role_permissions = [ "none" ]
        cloudformation_read_role_permissions = [ "none" ]
        """
        found = re.findall('^([^=]+)\s+=\s+\[', line)
        if not found:
            return
        assert len(found) == 1
        varname = found[0]
        if varname not in self._varnames:
            self._varnames[varname] = lineno
            self._new_lines.append(line)
        else:
            prev_lineno = self._varnames[varname]
            self._dup_varnames.append(
                (lineno, '{}. Previous definition: line {}'.format(varname, prev_lineno)))

    def process(self):
        self.for_each()
        if self._dup_varnames:
            return Reason('Duplicated terraform variable', self._dup_varnames)
        return None


def main(dirp=None):
    if dirp is None:
        dirp = os.path.abspath('.')
    for_each(dirp)


main()
