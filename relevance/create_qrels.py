import csv
import os
from collections import Counter


class CreateQrels:

    def __init__(self):
        self.scorings = {}
        self.here = os.path.dirname(os.path.realpath(__file__))

    def __init_scorings(self, info_id, poi_id):
        if self.scorings.get(info_id) is None:
            self.scorings[info_id] = {}
        if self.scorings[info_id].get(poi_id) is None:
            self.scorings[info_id][poi_id] = []

    @staticmethod
    def gtruth_from_list(scores):
        counts = Counter(scores)
        diff = max(scores) - min(scores)
        if diff <= 1:  # Minimal disagreement: Take majority vote
            return counts.most_common()[0][0]
        elif diff == 2:  # Moderate disagreement: Take average and round to closest integer
            return round(sum(scores) / len(scores))
        else:  # Large disagreement (diff > 2)
            if len(scores) >= 5:
                popular_amount = counts.most_common()[0][1]
                popular_number = counts.most_common()[0][0]
                if len(scores) - popular_amount <= 1:
                    return popular_number
            return int(round(sum(scores) / len(scores)))

    def read_scorings(self, filename='assessments.tsv'):
        tsv_file = open(self.here + '/' + filename)
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        for line in read_tsv:
            self.__init_scorings(line[0], line[1])
            self.scorings[line[0]][line[1]] = [int(x) for x in line[2].split(' ')]

    def write_grels_to_file(self, filename='qrels.trec'):
        with open(self.here + '/' + filename, 'w', ) as outfile:
            for info_id, poi_list in self.scorings.items():
                if len(poi_list) > 0:
                    for poi_id, scores in poi_list.items():
                        gt = self.gtruth_from_list(scores)
                        outfile.write(info_id + " 0 " + str(poi_id) + " " + str(gt) + "\n")
        outfile.close()
        print('Saved csv to:\n' + str(self.here))


if __name__ == "__main__":
    cq = CreateQrels()
    cq.read_scorings()
    cq.write_grels_to_file()
