import copy
from tqdm import tqdm

from lib.log import logger
from domain.const import SIMULATION_ENV
from domain.data.human import HumanFactory
from domain.data.cluster import ClusterFactory
from domain.policy.lockdown import lockdown
from domain.policy.pcr import distribute_pcr_kit


def simulate():
    # 試験用オブジェクトを作成
    human_dict = {}
    for i in tqdm(range(SIMULATION_ENV.population)):
        human_factory = HumanFactory()
        unique_id, human = human_factory.generate_instance()
        human_dict.update({unique_id: human})

    cluster_factory = ClusterFactory(human_dict=human_dict)
    cluster_dict, human_dict = cluster_factory.create()

    human_dict_1 = copy.deepcopy(human_dict)
    cluster_dict_1 = copy.deepcopy(cluster_dict)
    human_dict_2 = copy.deepcopy(human_dict)
    cluster_dict_2 = copy.deepcopy(cluster_dict)

    # ロックダウン時の人の接触感染シミュレート
    logger.info("start generate human list")
    simulation_result_when_lockdown = lockdown(human_dict=human_dict_1, cluster_dict=cluster_dict_1)

    # PCR検査キットを配布した場合の接触感染シミュレート
    logger.info("start generate human list")

    simulation_result_when_pcr = distribute_pcr_kit(human_dict=human_dict_2, cluster_dict=cluster_dict_2)

    return simulation_result_when_lockdown, simulation_result_when_pcr
