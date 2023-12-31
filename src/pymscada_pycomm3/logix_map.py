"""Map between modbus table and Tag."""
import logging
from time import time
from pymscada.tag import Tag


# data types for PLCs
DTYPES = {
    'int32': [int, -2147483648, 2147483647],
    'float32': [float, -3.40282346639e+38, 3.40282346639e+38]
}


class LogixMap:
    """Do value updates for each tag."""

    def __init__(self, tagname: str, src_type: str, plc_tag: str):
        """Initialise modbus map and Tag."""
        dtype, dmin, dmax = DTYPES[src_type][0:3]
        self.tag = Tag(tagname, dtype)
        self.map_bus = id(self)
        self.plc_tag = plc_tag
        self.callback = None
        if dmin is not None:
            self.tag.value_min = dmin
        if dmax is not None:
            self.tag.value_max = dmax
        self.write_cb = None

    def set_callback(self, callback):
        """Add tag callback interface."""
        self.callback = callback
        self.tag.add_callback(self.tag_value_changed, bus_id=self.map_bus)

    def set_tag_value(self, value, time_us):
        """Pass update from IO driver to tag value."""
        if self.tag.value != value:
            self.tag.value = value, time_us, self.map_bus
        pass

    def tag_value_changed(self, tag: Tag):
        """Pass update from tag value to IO driver."""
        e = self.plc_tag.split(':')
        if len(e) == 3:
            self.callback(f'{e[1]}[{e[2]}]', tag.value)
        else:
            self.callback(e[1], tag.value)

class LogixMaps():
    """Link tags with protocol connector."""

    def __init__(self, tags: dict):
        """Collect maps based on a tag dictionary."""
        self.maps: dict[str, LogixMap] = {}
        self.reverse_map: dict[str, LogixMap] = {}
        for tagname, v in tags.items():
            addr = v['addr']
            map = LogixMap(tagname, v['type'], addr)
            self.maps[addr] = map
            self.reverse_map[map.tag.name] = map

    def add_write_callback(self, plc_name, writeok, callback):
        """Connection advises device links."""
        for w in writeok:
            for i in range(w['start'], w['end'] + 1):
                tag_name = f"{plc_name}:{w['addr']}:{i}"
                if tag_name not in self.maps:
                    continue
                self.maps[tag_name].set_callback(callback)

    def polled_data(self, plc_name, polls):
        """Pass updates read from the PLC to the tags."""
        time_us = int(time() * 1e6)
        for poll in polls:
            if poll.error is not None:
                logging.warning
            if '[' in poll.tag:
                stem, rhs = poll.tag.split('[')
                idx, _ = rhs.split(']')
                for i in range(int(idx) + int(idx) + len(poll.value)):
                    plc_tag = f'{plc_name}:{stem}:{i}'
                    if plc_tag not in self.maps:
                        continue
                    self.maps[plc_tag].set_tag_value(poll.value[i], time_us)
            else:
                self.maps[poll.tag].set_tag_value(poll.value, time_us)
