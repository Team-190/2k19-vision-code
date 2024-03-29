from grip import GripPipeline
# import matplotlib.pyplot as plt
# from matplotlib import collections as mc
import cv2


class Processor:

    def __init__(self):
        self.pipeline = GripPipeline()

    def mid(self, line):
        """
        Gets a GripPipeline.Line's midpoint's x coordinate
        :param line: GripPipeLine.Line line
        :return: midpoint x coordinate
        """
        return [(line.x1 + line.x2) // 2, (line.y1 + line.y2) // 2]

    def is_left(self, line):
        """
        Finds if line is left line of pair
        :param line: GripPipeline.Line line
        :return: whether line is left line of pair
        """
        return line.angle() < 0

    def merge_lines(self, lines):
        """
        Makes a list of merged lines

        :param lines: list of GripPipeline.Lines
        :return: list of GripPipeline.List
        """
        pairs = []
        for line in lines:
            if len(pairs) and self.is_left(pairs[-1][-1]) == self.is_left(line):
                pairs[-1].append(line)
            else:
                pairs.append([line])

        lines = []
        for pair in pairs:
            if len(pair) == 1:
                lines.append(pair[0])
            else:
                x1 = sum([line.x1 for line in pair]) // len(pair)
                x2 = sum([line.x2 for line in pair]) // len(pair)
                y1 = sum([line.y1 for line in pair]) // len(pair)
                y2 = sum([line.y2 for line in pair]) // len(pair)
                lines.append(GripPipeline.Line(x1, y1, x2, y2))
        return lines

    def find_ports(self, lines):
        """
        Finds point location of all visible cargo ports
        :param lines: list of GripPipeline.Line
        :return: list of points, representing port locations
        """
        ports = []
        left = None
        self.dists = []
        for line in lines:
            if left is None:
                if self.is_left(line):
                    left = self.mid(line)
            else:
                if not self.is_left(line):
                    ports.append(int(left[0] + self.mid(line)[0]) // 2)
                    self.dists.append(left[0] - self.mid(line)[0])
                    left = None
        # print(ports)
        return ports

    def process(self, img):

        self.pipeline.process(img)
        lines = self.pipeline.filter_lines_output
        self.lines = lines
        # print(len(lines))
        lines.sort(key=lambda i: self.mid(i)[0])  # sort lines left to right

        ports = self.find_ports(self.merge_lines(lines))

        return ports if ports else []


if __name__ == "__main__":
    Processor().process()
