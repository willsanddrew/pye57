import numpy as np
from pyquaternion import Quaternion

from pye57 import libe57
from pye57.utils import get_fields, get_node


class ScanHeader:
    def __init__(self, scan_node):
        self.node = scan_node
        points = libe57.CompressedVectorNode(self.node.get("points"))
        self.point_fields = get_fields(libe57.StructureNode(points.prototype()))
        self.scan_fields = get_fields(self.node)

    @classmethod
    def from_data3d(cls, data3d):
        return [cls(scan) for scan in data3d]

    def _assert_pose(self):
        if not self.node.isDefined("pose"):
            raise ValueError("Scan header doesn't contain a pose")

    @property
    def points(self):
        return self.node["points"]

    @property
    def point_count(self):
        return self.points.childCount()

    @property
    def rotation(self) -> np.array:
        self._assert_pose()
        q = Quaternion([e.value() for e in self.node["pose"]["rotation"]])
        return q.rotation_matrix

    @property
    def translation(self):
        self._assert_pose()
        return np.array([e.value() for e in self.node["pose"]["translation"]])

    def pretty_print(self, node=None, indent=""):
        if node is None:
            node = self.node
        lines = []
        for field in get_fields(node):
            child_node = node[field]
            value = ""
            if hasattr(child_node, "value"):
                value = ": %s" % child_node.value()
            lines.append(indent + str(child_node) + value)
            if isinstance(child_node, libe57.StructureNode):
                lines += self.pretty_print(child_node, indent + "    ")
        return lines

    # print(get_node(self.node, "guid").value())
    # print(get_node(self.node, "temperature").value())
    # print(get_node(self.node, "relativeHumidity").value())
    # print(get_node(self.node, "atmosphericPressure").value())
    # print(get_fields(get_node(self.node, "indexBounds")))
    # print(get_node(self.node, "intensityLimits").value())
    # print(get_node(self.node, "cartesianBounds").value())
    # print(get_node(self.node, "pose").value())
    # print(get_node(self.node, "acquisitionStart").value())
    # print(get_node(self.node, "acquisitionEnd").value())
    # print(get_node(self.node, "pointGroupingSchemes").value())