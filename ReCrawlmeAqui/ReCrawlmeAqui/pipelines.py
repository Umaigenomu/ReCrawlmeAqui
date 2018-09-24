# -*- coding: utf-8 -*-

# The item pipeline responsible for persisting the returned dictionary is defined here.

from .gimei import Gimei
from .romkan import common as romakana
import os
import pickle


BASE_MISAKA_FOLDER = "CidadaoData"

class MisakaPipeline(object):
    def __init__(self):
        if not os.path.exists(BASE_MISAKA_FOLDER + '/' + 'waifu_ids.set'):
            waifu_set = set()
            with open(BASE_MISAKA_FOLDER + '/' + 'waifu_ids.set', 'wb') as f:
                pickle.dump(waifu_set, f)
        with open(BASE_MISAKA_FOLDER + '/' + 'waifu_ids.set', 'rb') as f:
            self.waifu_ids_seen = pickle.load(f)

    def close_spider(self, spider):
        with open(BASE_MISAKA_FOLDER + '/' + 'waifu_ids.set', 'wb') as f:
            pickle.dump(self.waifu_ids_seen, f)

    def process_item(self, item, spider):
        # Save item as a pickled file with a MOE name.chan
        date = item['data'].split()
        year = date[5]
        month = date[3]
        item_id = item['titulo'].strip() + item['data'].strip()
        if item_id in self.waifu_ids_seen:
            return {"Status": "Duplicate", }
        self.waifu_ids_seen.add(item_id)
        file_loc_prefix = BASE_MISAKA_FOLDER + '/' + year + '/' + month + '/'
        ''' 
            The chances of the same exact japanese female name being picked twice in the same folder
            are very low.
        '''
        waifu_dir = file_loc_prefix + romakana.to_roma(Gimei('female').name.hiragana)+".chan"
        if not os.path.exists(file_loc_prefix):
            os.makedirs(file_loc_prefix)
        with open(waifu_dir, 'wb') as waifu:
            pickle.dump(item, waifu)
        return {"Status": "Successful~", }

