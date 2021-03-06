#######################################################################
# This file is part of steve.
#
# Copyright (C) 2012-2014 Will Kahn-Greene
# Licensed under the Simplified BSD License. See LICENSE for full
# license.
#######################################################################

import os
from unittest import TestCase

import pytest
from click.testing import CliRunner

from steve.util import (
    ConfigNotFound,
    create_project_config_file,
    get_project_config,
    get_video_id,
    html_to_markdown,
    IniConfig,
    is_youtube,
    NoOptionError,
    SteveException,
    verify_video_data,
    YamlConfig,
)


class VerifyVideoDataTestCase(TestCase):
    default = {
        'title': 'Foo',
        'category': 'Test Category',
        'language': 'English',
    }

    def test_default_minimum(self):
        """Verify that default verifies"""
        # Note: This is dependent on video_reqs.json data.

        data = dict(self.default)

        assert len(verify_video_data(data)) == 0

    def test_category(self):
        """Test category variations"""
        # category is none, no data['category']
        data = dict(self.default)
        del data['category']
        assert len(verify_video_data(data, None)) == 1

        # category is something, no data['category']
        assert len(verify_video_data(data, 'Test Category')) == 0

        # category is none, data['category'] = something
        data = dict(self.default)
        assert len(verify_video_data(data, None)) == 0

        # category is something, data['category'] = same something
        assert len(verify_video_data(data, data['category'])) == 0

        # category is something, data['category'] = different something
        assert len(verify_video_data(data, data['category'] + 'abc')) == 1

    def test_minimum_requirements(self):
        """Tests verifying required fields"""
        # Note: This is dependent on video_reqs.json data.

        data = dict(self.default)
        del data['title']
        assert len(verify_video_data(data)) == 1

        data = dict(self.default)
        del data['category']
        assert len(verify_video_data(data)) == 1

        data = dict(self.default)
        del data['language']
        assert len(verify_video_data(data)) == 1

        # Three errors if we pass in an empty dict
        assert len(verify_video_data({})) == 3

    def test_speakers(self):
        """Tests speakers which is a TextArrayField"""
        # Note: This is dependent on video_reqs.json data.

        data = dict(self.default)

        data['speakers'] = []
        assert len(verify_video_data(data)) == 0

        data['speakers'] = ['']
        assert len(verify_video_data(data)) == 1

        data['speakers'] = ['Jimmy Discotheque']
        assert len(verify_video_data(data)) == 0

    def test_state(self):
        """Test verifying state (IntegerField with choices)"""
        # Note: This is dependent on video_reqs.json data.

        data = dict(self.default)

        data['state'] = 0
        assert len(verify_video_data(data)) == 1

        data['state'] = 1
        assert len(verify_video_data(data)) == 0

        data['state'] = 2
        assert len(verify_video_data(data)) == 0

        data['state'] = 3
        assert len(verify_video_data(data)) == 1

    def test_video_ogv_download_only(self):
        """Test BooleanField"""
        # Note: This is dependent on video_reqs.json data.

        data = dict(self.default)

        data['video_ogv_download_only'] = True
        assert len(verify_video_data(data)) == 0

        data['video_ogv_download_only'] = False
        assert len(verify_video_data(data)) == 0

        data['video_ogv_download_only'] = 'True'
        assert len(verify_video_data(data)) == 1


def test_html_to_markdown():
    """Test html_to_markdown"""
    assert (
        html_to_markdown('<p>this is <b>html</b>!</p>') ==
        u'this is **html**!'
    )


def test_is_youtube():
    data = [
        ('http://www.youtube.com/watch?v=N29XAFjiKf4', True),
        ('http://youtu.be/N29XAFjiKf4', True),
    ]

    for url, expected in data:
        assert is_youtube(url) == expected


def test_get_video_id():
    # Test valid urls
    data = [
        # url, expected
        ('http://pyvideo.org/video/2822', 2822),
        ('http://pyvideo.org/video/2822/', 2822),
        ('http://pyvideo.org/video/2822/foo-bar-baz', 2822),
        ('https://pyvideo.org/video/2822/foo-bar-baz', 2822),
        ('https://richard.example.com/video/2822/foo-bar-baz', 2822),
    ]

    for url, expected in data:
        assert get_video_id(url) == expected

    # Test invalid urls
    data = [
        None,
        'foo',
        'http://pyvideo.org/',
        'http://pyvideo.org/video/foo'
    ]
    for url in data:
        try:
            get_video_id(url)
            assert False
        except SteveException:
            pass


# @pytest.mark.parametrize(("config", ), [IniConfig, YamlConfig, ])
@pytest.mark.parametrize(("config", ), [
    (IniConfig, ),
    (YamlConfig, ),
])
class TestConfig:
    def test_ini_config_creation(self, config):
        runner = CliRunner()
        with runner.isolated_filesystem():
            path = os.getcwd()

            with pytest.raises(ConfigNotFound):
                get_project_config()
            # Create the project directory
            create_project_config_file(path, config)
            cfg = get_project_config()

            assert os.path.exists(config.file_name)
            tmp_dir = 'tmp'
            os.mkdir(tmp_dir)
            os.chdir(tmp_dir)
            cfg2 = get_project_config()
            os.chdir(path)
            assert cfg.get('project', 'jsonpath') == cfg2.get('project', 'jsonpath')

            with pytest.raises(NoOptionError):
                cfg.get('project', 'xmlpath')
