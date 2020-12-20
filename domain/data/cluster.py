import uuid
from dataclasses import dataclass, field
from typing import List, Dict

import numpy as np
from tqdm import tqdm

from domain.const import SIMULATION_ENV
from domain.data.human import Human
from lib.log import logger


@dataclass(frozen=False)
class Cluster:
    id: str  # クラスタのID
    people: List[Human]  # people instances belongs to this cluster(クラスターに所属する人)
    size: int  # size of this cluster(クラスタのサイズ)
    able_to_freeze: bool  # whether the cluster is suppress or not(凍結するクラスターかどうか)
    freeze: bool = field(default=False)  # suppress or not(凍結クラスタ)
    freeze_remaining: int = field(default=0)  # the number of days to action(凍結の場合の解凍日数)
    is_full: bool = field(default=False)  # is full(満員フラグ)

    def add(self, human: Human) -> bool:
        """
        add human to cluster, then return success to add or not.
        クラスタへ人間を追加し、成功可否を返却する
        """
        if len(self.people) == self.size:
            return False
        else:
            self.people.append(human)
            if len(self.people) == self.size:
                self.is_full = True
            return True

    def check_duplicate(self, human: Human) -> bool:
        """
        check duplicate or not.
        people属性の重複チェックを行う
        """
        human_id = human.id
        is_duplicated = False
        for _human in self.people:
            if human_id == _human.id:
                is_duplicated = True
                break

        return is_duplicated


class ClusterFactory:
    def __init__(self, human_dict: Dict[str, Human]):
        self.cluster_dict = {}
        self.human_dict = human_dict

    def generate_clusters(self):
        """
        クラスタのサイズをポワソン分布に基づいた値で計算し、クラスタを生成する
        """
        poisson_distribution = np.random.poisson(lam=SIMULATION_ENV.mean_of_cluster_size, size=10000)
        logger.info("generate empty cluster")
        for _ in tqdm(range(SIMULATION_ENV.number_of_cluster)):
            cluster_size = np.random.choice(a=poisson_distribution)
            freeze = np.random.choice(a=[True, False], p=[SIMULATION_ENV.probability_of_freeze_cluster,
                                                          1 - SIMULATION_ENV.probability_of_freeze_cluster])
            if cluster_size < 2:
                # 1名以下のクラスタは2人として扱う
                cluster_size = 2

            unique_id = str(uuid.uuid4())
            cluster = Cluster(
                id=unique_id,
                able_to_freeze=freeze,
                people=[],
                size=cluster_size
            )
            self.cluster_dict.update({unique_id: cluster})

    def distribute_human_to_cluster(self):
        """
        クラスタをHumanで満員にし、返却する
        """
        logger.info("distribute human to cluster")
        human_list = []
        for key in self.human_dict.keys():
            human_list.append(self.human_dict[key])

        for cluster_key in tqdm(self.cluster_dict.keys()):
            for i in range(self.cluster_dict[cluster_key].size):
                added = False
                while added is False:
                    selected_human = np.random.choice(a=human_list)
                    is_duplicated = self.cluster_dict[cluster_key].check_duplicate(human=selected_human)
                    if is_duplicated is False:
                        selected_human.join_to_cluster(self.cluster_dict[cluster_key].id)
                        self.cluster_dict[cluster_key].add(human=selected_human)
                        added = True

    def create(self):
        logger.info("start generate cluster list")
        self.generate_clusters()
        self.distribute_human_to_cluster()

        return self.cluster_dict, self.human_dict
