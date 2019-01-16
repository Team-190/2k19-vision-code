from grip import GripPipeline
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import cv2

def mid_x(line):
    """
    Gets a GripPipeline.Line's midpoint's x coordinate
    :param line: GripPipeLine.Line line
    :return: midpoint x coordinate
    """
    return (line.x1 + line.x2) // 2

def is_left(line):
    """
    Finds if line is left line of pair
    :param line: GripPipeline.Line line
    :return: whether line is left line of pair
    """
    return line.angle() < 0

def merge_lines(lines):
    """
    Makes a list of merged lines

    :param lines: list of GripPipeline.Lines
    :return: list of GripPipeline.List
    """
    pairs = []
    for line in lines:
        if len(pairs) and is_left(pairs[-1][-1]) == is_left(line):
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

def find_ports(lines):
    """
    Finds point location of all visible cargo ports
    :param lines: list of GripPipeline.Line
    :return: list of points, representing port locations
    """
    ports = []
    left = None
    for line in lines:
        if left is None:
            if is_left(line):
                left = mid_x(line)
            else:
                # unpaired right
                pass
        else:
            if is_left(line):
                # unpaired left? should never happen
                pass
            else:
                ports.append((left+mid_x(line)) // 2)
    return ports


def graph(lines):
    """
    Graphs all detected lines
    :param lines: list of GripPipeline.Line objects
    :return: None
    """
    lines = [[[line.x1, line.y1], [line.x2, line.y2]] for line in lines]
    lc = mc.LineCollection(lines)
    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.set_xlim(320)
    ax.set_ylim(240)
    ax.invert_xaxis()
    plt.show()


def main():
    name = "2019VisionImages/CargoSideStraightDark36in.jpg"
    name = "2019VisionImages/CargoAngledDark48in.jpg"
    img = cv2.imread(name)
    print(name)
    pipeline = GripPipeline()
    pipeline.process(img)
    lines = pipeline.filter_lines_output
    lines.sort(key=mid_x)
    graph(lines)
    graph(merge_lines(lines))
    ports = find_ports(merge_lines(lines))
    for port in ports:
        plt.plot(port, 120, 'bo')
    plt.show()




if __name__ == "__main__":
    main()