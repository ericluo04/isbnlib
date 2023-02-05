# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""tests for classifiers."""

from random import randint
from time import sleep

import pytest

from .._oclc import query_classify as query

pytestmark = pytest.mark.skip("OCLC doesn't allow so many tests for now!")

# this is a slow service
q1 = query('9781786330444') or {}
sleep(randint(10, 30))
q2 = query('9780425284629') or {}
sleep(randint(10, 30))


def test_query():
    """Test the query of classifiers (oclc.org) with 'low level' queries."""
    assert (len(repr(query('9782253112105'))) > 10) == True
    assert (len(repr(q1)) > 10) == True
    assert (len(repr(q2)) > 10) == True
    sleep(randint(10, 30))


def test_query_no_data():
    """Test the query of classifiers (oclc.org) with 'low level' queries (no data)."""
    assert (len(repr(query('9781849692341'))) == 2) == True
    sleep(randint(10, 30))
    assert (len(repr(query('9781849692343'))) == 2) == True


def test_query_exists_ddc():
    """Test exists 'DDC'."""
    assert (len(repr(q1['ddc'])) > 2) == True
    assert (len(repr(q2['ddc'])) > 2) == True


def test_query_exists_lcc():
    """Test exists 'LCC'."""
    assert (len(repr(q1['lcc'])) > 2) == True
    assert (len(repr(q2['lcc'])) > 2) == True


def test_query_fast():
    """Test exists 'fast' classifiers."""
    assert (len(repr(q1['fast'])) > 7) == True
    assert (len(repr(q2['fast'])) > 7) == True


def test_query_owi():
    """Test exists 'owi' classifiers."""
    assert (len(repr(q1['owi'])) > 5) == True
    assert (len(repr(q2['owi'])) > 5) == True


def test_query_oclc():
    """Test exists 'oclc' classifiers."""
    assert (len(repr(q1['oclc'])) > 7) == True
    assert (len(repr(q2['oclc'])) > 7) == True
