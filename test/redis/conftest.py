# Copyright 2020-present ScyllaDB
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# This file contains "test fixtures", a pytest concept described in
# https://docs.pytest.org/en/latest/fixture.html.
# A "fixture" is some sort of setup which an invididual test requires to run.
# The fixture has setup code and teardown code, and if multiple tests
# require the same fixture, it can be set up only once - while still allowing
# the user to run individual tests and automatically set up the fixtures they need.

import pytest

from pytest_elk_reporter import ElkReporter
import logging
import os

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--redis-host", action="store", default="localhost",
        help="ip address")
    parser.addoption("--redis-port", action="store", type=int, default=6379,
        help="port number")
    parser.addoption('--publish-elk', action='store_true', default=False,
                     help="Publish test results to Elasticsearch")

def pytest_plugin_registered(plugin):
    if isinstance(plugin, ElkReporter):
        if plugin.config.getoption("--publish-elk"):
            try:
                plugin.es_address = os.getenv('SCYLLA_ELASTIC_URL')
                plugin.es_username = os.getenv('SCYLLA_ELASTIC_USER')
                plugin.es_password = os.getenv('SCYLLA_ELASTIC_PASS')
                plugin.es_index_name = os.getenv('SCYLLA_ELASTIC_INDEX_NAME')
            except Exception as e:
                logger.warning(f"Error while setting elasticsearch configuration: {e}")



@pytest.fixture
def redis_host(request):
    return request.config.getoption('--redis-host')

@pytest.fixture
def redis_port(request):
    return request.config.getoption('--redis-port')

