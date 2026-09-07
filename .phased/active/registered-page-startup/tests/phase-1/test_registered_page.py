"""Registered-page behavioral contracts; bind to real integration in phase 1."""
import pytest


def test_html_identity_is_already_registered():
    # wf:contract: HTML contains the page_id generated with toolbox get_uuid and already registered under the request connection before the response is sent.
    pytest.fail("phase 1 pending")


def test_page_loads_have_distinct_identities():
    # wf:contract: Two valid page loads under one connection have distinct registered page IDs and preserve that connection's ownership.
    pytest.fail("phase 1 pending")


def test_unknown_page_does_not_register():
    # wf:contract: An unknown page returns not found without registering a page.
    pytest.fail("phase 1 pending")
