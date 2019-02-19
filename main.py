from grip import GripPipeline
import matplotlib.pyplot as plt
from matplotlib import collections as mc
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
        for line in lines:
            if left is None:
                if self.is_left(line):
                    left = self.mid(line)
                else:
                    # unpaired right
                    pass
            else:
                if self.is_left(line):
                    # unpaired left? should never happen
                    pass
                else:
                    ports.append(int(left[0] + self.mid(line)[0]) // 2)
                    left = None
        print(ports)
        return ports


    def graph(lines, name):
        """
        Graphs all detected lines
        :param lines: list of GripPipeline.Line objects
        :return: None
        """
        lines = [[[line.x1, line.y1], [line.x2, line.y2]] for line in lines]
        lc = mc.LineCollection(lines, linewidths=[7] * len(lines), colors=['b'] * len(lines))
        fig, ax = plt.subplots()
        ax.imshow(plt.imread(name))
        ax.add_collection(lc)
        ax.set_xlim([0, 320])
        ax.set_ylim([0, 240])
        ax.invert_yaxis()
        # ax.axis('off')
        plt.show()


    def process(self, img):
        # name = "2019VisionImages/CargoSideStraightDark36in.jpg"
        # name = "2019VisionImages/CargoAngledDark48in.jpg"
        # name = "2019VisionImages/RocketPanelAngleDark60in.jpg"
        # name = "2019VisionImages/CargoSideStraightDark72in.jpg"

        # load and process image
        # img = cv2.imread(name)
        # print(name)]
        self.pipeline.process(img)
        lines = self.pipeline.filter_lines_output
        lines.sort(key=lambda i:self.mid(i)[0])  # sort lines left to right

        # graph intermediate steps
        # graph(lines, name)
        # graph(merge_lines(lines), name)
        ports = self.find_ports(self.merge_lines(lines))

        # plot port points
        # plt.imshow(plt.imread(name))
        # plt.xlim([0, 320])
        # plt.ylim([0, 240])
        #
        # plt.gca().invert_yaxis()
        # x, y = zip(*ports)
        # plt.scatter(x=x, y=y, c='r', s=81)
        # plt.show()
        return ports


if __name__ == "__main__":
    Processor().process()
