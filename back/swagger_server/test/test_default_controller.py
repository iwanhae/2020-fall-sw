# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.query import Query  # noqa: E501
from swagger_server.models.result import Result  # noqa: E501
from swagger_server.models.status import Status  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_new_query(self):
        """Test case for new_query

        Requset a new query
        """
        body = Query()
        response = self.client.open(
            '/api/request',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_progress(self):
        """Test case for show_progress

        
        """
        response = self.client.open(
            '/api/progress/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_result(self):
        """Test case for show_result

        
        """
        response = self.client.open(
            '/api/result/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
