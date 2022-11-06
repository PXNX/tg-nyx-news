import dataclasses
from typing import Optional

import yaml


@dataclasses.dataclass
class Source:
    name: str
    bloat: Optional[list[str]]
    bias: str
    username: Optional[str]
    invite: Optional[str]

    @classmethod
    def from_yaml(cls, data):
        return cls(
            name=data['name'],
            bloat=data.get('bloat', None),
            bias=data.get('bias', ''),
            username=data.get('username', None),
            invite=data.get('invite', None)
        )

sources = dict()
source_ids = list()
def get_sources():
    with open('sources.yaml', 'rb') as stream:
        data_loaded = yaml.load(stream, Loader=yaml.Loader)
        print(data_loaded)

        for k, v in data_loaded.items():
            channel_id = int(str(-100) + str(k))
            source_ids.append(channel_id)
            sources[channel_id] = Source.from_yaml(v)