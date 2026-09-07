"""Registered startup contracts; bind to real integration in phase 2."""
import pytest


def test_registered_startup_order():
    # wf:contract: genro exists before source acquisition; the registered page channel opens before the source request and the received source builds the live page.
    pytest.fail("phase 2 pending")


def test_page_identity_does_not_authorize_another_connection():
    # wf:contract: A different connection cannot acquire the registered page's source using its page_id.
    pytest.fail("phase 2 pending")


def test_disposed_startup_cannot_mount_late_results():
    # wf:contract: Disposing genro during startup releases its channel resources and late source responses cannot mount UI or revive the disposed runtime.
    pytest.fail("phase 2 pending")
