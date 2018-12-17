# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from . import model_factories as mfactories

from ..serializers import DocumentSerializer

import mock
from django.core.files import File
from django.test.utils import override_settings


class DocumentSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mfactories.User()

    def test_contains_expected_fields(self):
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        # Mock with pdf since image files will trigger thumbnail generation
        file_mock.name = 'test1.pdf'

        document = mfactories.Document(file_name='Document1.pdf',
                                       file=file_mock)

        serializer = DocumentSerializer(instance=document)

        data = serializer.data

        keys = [
            'workflowlevel1_uuids',
            'file_type',
            'user_uuid',
            'workflowlevel2_uuids',
            'organization_uuid',
            'upload_date',
            'create_date',
            'contact_uuid',
            'uuid',
            'file_description',
            'id',
            'file',
            'file_name',
            'thumbnail'
        ]

        self.assertEqual(set(data.keys()), set(keys))

    @override_settings(AWS_ACCESS_KEY_ID='dummy')
    @override_settings(AWS_SECRET_ACCESS_KEY='ex123')
    @override_settings(BOTO_S3_BUCKET='example')
    @override_settings(BOTO_S3_HOST='example.com')
    def test_mock_s3(self):
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        # Mock with pdf since image files will trigger thumbnail generation
        file_mock.name = 'test1.pdf'

        self.document = mfactories.Document(file_name='Document1.pdf',
                                            file=file_mock)

        expected_file = "/file/{}".format(self.document.pk)

        serializer = DocumentSerializer(instance=self.document)
        self.assertEquals(serializer.data['file'], expected_file)

    def test_without_file(self):
        self.document = mfactories.Document(file_name='Document1.jpg',
                                            file=None)

        serializer = DocumentSerializer(instance=self.document)
        self.assertIsNone(serializer.data['file'])