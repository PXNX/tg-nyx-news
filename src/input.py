import dataclasses
from typing import Optional

import yaml

from src.db import insert_source, SourceDAO
from src.util import format_channel_id


@dataclasses.dataclass
class Source:
    name: str
    bloat: Optional[list[str]]
    bias: Optional[str]
    username: Optional[str]
    display: Optional[str]
    invite: Optional[str]

    @classmethod
    def from_yaml(cls, data):
        return cls(
            name=data['name'],
            bloat=data.get('bloat', None),
            bias=data.get('bias', None),
            username=data.get('username', None),
            display=data.get('display', None),
            invite=data.get('invite', None)
        )


sources = dict()
sources_full = dict()
source_ids = list()


def get_active_sources():
    with open('res/sources.yaml', 'rb') as stream:
        data_loaded = yaml.load(stream, Loader=yaml.Loader)
        print(data_loaded)

        for k, v in data_loaded.items():
            channel_id = format_channel_id(k)
            source_ids.append(channel_id)
            sources[channel_id] = Source.from_yaml(v)

def get_all_sources():
    with open('res/sources.yaml', 'rb') as stream:
        data_loaded = yaml.load(stream, Loader=yaml.Loader)
        print(data_loaded)

        for k, v in data_loaded.items():
            channel_id = format_channel_id(k)
            sources_full[channel_id] = Source.from_yaml(v)

def insert_sources():
    with open('res/sources.yaml', 'rb') as stream:
        data_loaded = yaml.load(stream, Loader=yaml.Loader)
        print(data_loaded)

        for k, v in data_loaded.items():
            insert_source(SourceDAO(
                int(str(-100) + str(k)),
                0,
                0,
                v["bias"] if "bias" in v else None,
                None,
                v["name"],
                v["display"] if "display" in v else None,
                v["invite"] if "invite" in v else None,
                v["username"] if "username" in v else None
            ))

##insert_sources()
