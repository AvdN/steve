#######################################################################
# This file is part of steve.
#
# Copyright (C) 2015
# Licensed under the Simplified BSD License. See LICENSE for full
# license.
#######################################################################

from __future__ import print_function

import os
import datetime
import tempfile

from ruamel.yaml.convert import SyncJSON, datetime_to_time


class YAML_Data(SyncJSON):
    def __init__(self, cfg):
        self._cfg = cfg

    def sync(self):
        print('calling sync')
        json_path = self._cfg.get('project', 'jsonpath')
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        yaml_path = self._cfg.get('project', 'yamlpath')
        if not os.path.exists(yaml_path):
            os.makedirs(yaml_path)
        ts = self._cfg.status['yaml']['last_sync']
        last_synced = datetime_to_time(ts)
        super(YAML_Data, self).sync(json_path, yaml_path, last_synced=last_synced)
        self._cfg.status['yaml']['last_sync'] = datetime.datetime.now()
        self._cfg.save_status()
        # self.equal_all(json_path, yaml_path)

    def edit(self, combine_name=None):
        if combine_name is None:
            combine_name = tempfile.mktemp(suffix='.yaml')
            print(combine_name)
            _tmp_file = True
        else:
            _tmp_file = False
        yaml_path = self._cfg.get('project', 'yamlpath')
        assert os.path.isdir(yaml_path)
        super(YAML_Data, self).combine(combine_name, yaml_path)
        os.system('{0} {1}'.format(os.environ['EDITOR'], combine_name))
        if not os.path.exists(yaml_path):
            os.makedirs(yaml_path)
        super(YAML_Data, self).split(combine_name, yaml_path)
        if _tmp_file:
            os.remove(combine_name)

    def split(self, combine_name):
        yaml_path = self._cfg.get('project', 'yamlpath')
        assert os.path.isdir(yaml_path)
        super(YAML_Data, self).split(combine_name, yaml_path)

    def combine(self, combine_name):
        yaml_path = self._cfg.get('project', 'yamlpath')
        assert os.path.isdir(yaml_path)
        super(YAML_Data, self).combine(combine_name, yaml_path)

    def json_yaml_adapt(self, data):
        """adapt inviddual elements of the data"""
        data = super(YAML_Data, self).json_yaml_adapt(data)
        if isinstance(data, dict):
            for k in data:
                v = data[k]
                if isinstance(v, basestring):
                    if len(v) == 0:
                        data[k] = None
                    if len(v) == 10 and v[4] == '-' and v[7] == '-':
                        # date string of for 2015-10-05
                        try:
                            d = datetime.date(*map(int, v.split('-')))
                        except:
                            continue
                        data[k] = d
        return data

    def yaml_json(self, yfn, jfn):
        print('converting', os.path.basename(yfn))
        super(YAML_Data, self).yaml_json(yfn, jfn)

    def json_yaml(self, jfn, yfn):
        print('converting', os.path.basename(jfn))
        super(YAML_Data, self).json_yaml(jfn, yfn)

    def yaml_json_adapt(self, data):
        data = super(YAML_Data, self).yaml_json_adapt(data)
        if isinstance(data, dict):
            for k in data:
                v = data[k]
                if v is None:
                    data[k] = ''
        return data
