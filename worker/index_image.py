import requests
import json
import os


BASEURL = "http://scanpix:5001/process_image"

def append_to_json(filepath, data):

    # if file is empty dump to eempty file and return
    if(os.stat(filepath).st_size == 0):
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump([data], f)
        return

    # construct JSON fragment as new file ending
    new_ending = ", " + json.dumps(data)[0:-1] + "}]"

    # edit the file in situ - first open it in read/write mode
    with open(filepath, 'r+') as f:

        f.seek(0, 2)        # move to end of file
        index = f.tell()    # find index of last byte

        # walking back from the end of file, find the index
        # of the original JSON List's closing ']'
        while not f.read().startswith(']'):
            index -= 1
            if index == 0:
                raise ValueError("can't find JSON object in {!r}".format(filepath))
            f.seek(index)

        # starting at the original ending ] position, write out
        # the new ending
        f.seek(index)
        f.write(new_ending)


class Indexer:

    def index(self, img_name, img_path):
        print(img_path)
        res = requests.get(url=BASEURL, params={'url': img_path }).json()
        res['file_name'] = img_name
        res['file_location'] = img_path
        return res

    def dump_to_json(self, json_index):
        append_to_json("/worker-app/index.json", json_index)
