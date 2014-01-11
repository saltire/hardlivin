from collections import OrderedDict
import csv
import os


DATAPATH = os.path.join(os.path.dirname(__file__), 'data')
INFOCOLS = 'title', 'desc', 'painted'


class CSVData:
    def __init__(self):
        # get list of source files
        files = os.listdir(DATAPATH)
        self.sources = [f[:-4] for f in files if f[-4:] == '.csv' and f[:-4] + '.png' in files]

        # read info
        with open(os.path.join(DATAPATH, 'info.csv'), 'rb') as csvfile:
            info = {row[0]: tuple(row[1:]) for row in csv.reader(csvfile)}

        self.info = OrderedDict()
        for source in self.sources:
            with open(os.path.join(DATAPATH, source + '.csv'), 'rb') as csvfile:
                for y, row in enumerate(csv.reader(csvfile)):
                    for x, title in enumerate(row):
                        if title:
                            sqinfo = (title,) + info.get(title, ())
                            # pad sqinfo to the correct number of columns
                            sqinfo += ('',) * (len(INFOCOLS) - len(sqinfo))
                            self.info['{0}-{1}-{2}'.format(source, x, y)] = sqinfo

        # read board
        with open(os.path.join(DATAPATH, 'board.csv'), 'rb') as csvfile:
            self.board = [[filename if filename in self.info else None for filename in row]
                          for row in csv.reader(csvfile)]


    def write_info(self, newinfo):
        for filename, sqinfo in newinfo.iteritems():
            # replace stored square info with new info
            self.info[filename] = tuple(sqinfo.get(col, '') for col in INFOCOLS)

        # write NEW info file
        with open(os.path.join(DATAPATH, 'info.csv'), 'wb') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            for filename, fileinfo in self.info.iteritems():
                writer.writerow(list(fileinfo))

        # write NEW source files
        sourcemaps = {}
        for filename, fileinfo in self.info.iteritems():
            source, x, y = filename.rsplit('-', 2)
            sourcemaps.setdefault(source, {})[int(x), int(y)] = fileinfo[0]

        for source in self.sources:
            w = max(x for x, _ in sourcemaps[source]) + 1
            h = max(y for _, y in sourcemaps[source]) + 1
            with open(os.path.join(DATAPATH, source + '.csv'), 'wb') as csvfile:
                writer = csv.writer(csvfile, lineterminator='\n')
                for y in range(h):
                    writer.writerow([sourcemaps[source].get((x, y), '') for x in range(w)])


    def write_board(self, rows):
        with open(os.path.join(DATAPATH, 'board.csv'), 'wb') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            for row in rows:
                writer.writerow(row)
