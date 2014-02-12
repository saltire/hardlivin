from collections import OrderedDict
import csv
import os


DATAPATH = os.path.join(os.path.dirname(__file__), 'data')
INFOCOLS = 'title', 'desc', 'effect', 'difficulty', 'column', 'row', 'locked'


class CSVData:
    def __init__(self):
        # get list of source files
        files = os.listdir(DATAPATH)
        self.sources = [f[:-4] for f in files if f[-4:] == '.csv' and f[:-4] + '.png' in files]

        # read info
        with open(os.path.join(DATAPATH, 'info.csv'), 'rb') as csvfile:
            info = {row[0]: tuple(row[1:]) for row in csv.reader(csvfile)}

        colcount = 0
        self.info = OrderedDict()
        for source in self.sources:
            with open(os.path.join(DATAPATH, source + '.csv'), 'rb') as csvfile:
                for y, row in enumerate(csv.reader(csvfile)):
                    for x, title in enumerate(row):
                        if title:
                            filename = '{0}-{1}-{2}'.format(source, x, y)
                            sqinfo = dict(zip(INFOCOLS,
                                              (title,) + info.get(title, ()) # source csv info
                                              + (('',) * len(INFOCOLS)))) # pad to length
                            self.info[filename] = sqinfo

                            if sqinfo['column'] != '' and sqinfo['row'] != '':
                                colcount = max(int(sqinfo['column']) + 1, colcount)

        self.columns = [[''] * 5 for _ in range(colcount)]
        for filename, sqinfo in self.info.iteritems():
            if sqinfo['column'] != '' and sqinfo['row'] != '':
                self.columns[colcount - int(sqinfo['column']) - 1][int(sqinfo['row'])] = filename


    def write_info(self, newinfo):
        for filename, sqinfo in newinfo.iteritems():
            self.info[filename].update(sqinfo)

        # write NEW info file
        with open(os.path.join(DATAPATH, 'info.csv'), 'wb') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            for filename, sqinfo in self.info.iteritems():
                writer.writerow([sqinfo[i] for i in INFOCOLS])

        # write NEW source files
        sourcemaps = {}
        for filename, fileinfo in self.info.iteritems():
            source, x, y = filename.rsplit('-', 2)
            sourcemaps.setdefault(source, {})[int(x), int(y)] = fileinfo['title']

        for source in self.sources:
            w = max(x for x, _ in sourcemaps[source]) + 1
            h = max(y for _, y in sourcemaps[source]) + 1
            with open(os.path.join(DATAPATH, source + '.csv'), 'wb') as csvfile:
                writer = csv.writer(csvfile, lineterminator='\n')
                for y in range(h):
                    writer.writerow([sourcemaps[source].get((x, y), '') for x in range(w)])
