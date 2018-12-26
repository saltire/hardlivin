from collections import OrderedDict
import csv
import os


DATAPATH = os.path.join(os.path.dirname(__file__), 'data')
INFOCOLS = ['title', 'desc', 'effect', 'difficulty', 'column', 'row', 'locked', 'sold', 'snakes',
            'scolumn', 'srow']


class CSVData:
    def __init__(self):
        # get list of source files
        files = os.listdir(DATAPATH)
        self.sources = [f[:-4] for f in files if f[-4:] == '.csv' and f[:-4] + '.png' in files]

        # read info
        with open(os.path.join(DATAPATH, 'info.csv'), 'rt', encoding='utf-8') as csvfile:
            info = {row[0]: tuple(str(s) for s in row[1:])
                    for row in csv.reader(csvfile)}

        self.info = OrderedDict()
        for source in self.sources:
            with open(os.path.join(DATAPATH, source + '.csv'), 'rt', encoding='utf-8') as csvfile:
                for y, row in enumerate(csv.reader(csvfile)):
                    for x, title in enumerate(row):
                        if title:
                            if title not in info:
                                print('No info found for', title)

                            filename = '{0}-{1}-{2}'.format(source, x, y)
                            sqinfo = dict(zip(INFOCOLS,
                                              (title,) + info.get(title, ()) # source csv info
                                              + (('',) * len(INFOCOLS)))) # pad to length
                            self.info[filename] = sqinfo


    def write_info(self, newinfo):
        for filename, sqinfo in newinfo.items():
            self.info[filename].update(sqinfo)

        # write NEW info file
        with open(os.path.join(DATAPATH, 'info.csv'), 'wb') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            for filename, sqinfo in self.info.items():
                writer.writerow([sqinfo[i].encode('utf-8') for i in INFOCOLS])

        # write NEW source files
        sourcemaps = {}
        for filename, fileinfo in self.info.items():
            source, x, y = filename.rsplit('-', 2)
            sourcemaps.setdefault(source, {})[int(x), int(y)] = fileinfo['title']

        for source in self.sources:
            w = max(x for x, _ in sourcemaps[source]) + 1
            h = max(y for _, y in sourcemaps[source]) + 1
            with open(os.path.join(DATAPATH, source + '.csv'), 'wb') as csvfile:
                writer = csv.writer(csvfile, lineterminator='\n')
                for y in range(h):
                    writer.writerow([sourcemaps[source].get((x, y), '') for x in range(w)])
