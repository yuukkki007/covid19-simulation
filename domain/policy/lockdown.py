import copy
from random import choice
from typing import Dict

import numpy as np
from tqdm import tqdm

from domain.const import SIMULATION_ENV
from domain.data.cluster import Cluster
from domain.data.human import Human
from domain.data.simulation_result import SimulationResult
from lib.log import logger


def lockdown(human_dict: Dict[str, Human], cluster_dict: Dict[str, Cluster]) -> SimulationResult:
    """
    ロックダウンシナリオのシミュレーション
    """
    logger.info("start evaluation lockdown scenario")
    result = SimulationResult(
        economic_losses_transition=[], serious_cases_transition=[],
        cumulative_economic_losses_transition=[], cumulative_serious_cases_transition=[]
    )
    lockdown_flg = False
    lockdown_days = 0

    for _ in tqdm(range(SIMULATION_ENV.simulation_days)):
        if lockdown_flg is True:
            logger.info("lockdown")
            lockdown_days += 1
            if lockdown_days == 10:
                lockdown_flg = False
        onset_ids = []
        economic_loss = 0
        freeze_rate = 0.0
        freeze_count = 0
        # humanの状態更新
        for key in human_dict.keys():
            if human_dict[key].infected is True:
                human_dict[key].passed_day_after_infected += 1
                if human_dict[key].passed_day_after_infected == human_dict[key].onset_delay_days:
                    human_dict[key].onset = True
                    onset_ids.append(human_dict[key].id)

            # 凍結期間の更新
            if human_dict[key].freeze is True:
                human_dict[key].freeze_remaining -= 1
                if human_dict[key].freeze_remaining == 0:
                    human_dict[key].freeze = False
                freeze_count += 1
                # 凍結時に1日分の経済損失の計算(20 ~ 70歳の生産人口の場合に経済損失を計上する)
                if (human_dict[key].age <= 70) and (human_dict[key].age >= 20):
                    economic_loss += int(SIMULATION_ENV.GDP_per_person / 365)

        if freeze_count != 0:
            freeze_rate = freeze_count / SIMULATION_ENV.population

        # クラスタの凍結日数が0なら凍結解除
        for key in cluster_dict.keys():
            if cluster_dict[key].freeze_remaining == 0:
                cluster_dict[key].freeze = False

        # 凍結可能クラスタかつ、感染を知っている or 発症をしている人がいればクラスタを凍結する
        for key in cluster_dict.keys():
            for human in cluster_dict[key].people:
                if (human_dict[human.id].onset is True) or (human_dict[human.id].know_infection is True):
                    cluster_dict[key].freeze = True
                    cluster_dict[key].freeze_remaining = 10

        # 同日内に再帰的に評価元の配列が変わってしまわないために評価用配列と別オブジェクトにしておく
        evaluation_human_dict = copy.deepcopy(human_dict)
        evaluation_cluster_dict = copy.deepcopy(cluster_dict)

        human_list = []
        for key in human_dict.keys():
            human_list.append(human_dict[key])

        for human_key in human_dict.keys():
            # 感染中かつ発症3日前よりあとなら接触人数に基づいてランダム感染する
            if (human_dict[human_key].infected is True) and (
                    human_dict[human_key].onset_delay_days - human_dict[human_key].passed_day_after_infected >= 3) and (
                    human_dict[human_key].freeze is False):
                # 平均で人に合う人数に凍結レートをかけたものが接触人数となる
                if freeze_rate == 0.0:
                    meet_per_day = human_dict[human_key].random_meet_per_day
                else:
                    meet_per_day = int(human_dict[human_key].random_meet_per_day * freeze_rate)
                for _ in range(meet_per_day):
                    is_freeze_human = True
                    while is_freeze_human is True:
                        selected_human = choice(human_list)
                        if selected_human.freeze is False:
                            is_freeze_human = False
                    # 抗体なしなら確率で感染
                    if selected_human.has_antibodies is False:
                        # マスク着用有無により感染確率の判断
                        if human_dict[human_key].masked:
                            factor_1 = SIMULATION_ENV.utility_mask_to_someone
                        else:
                            factor_1 = 1

                        if selected_human.masked:
                            factor_2 = SIMULATION_ENV.utility_mask_from_someone
                        else:
                            factor_2 = 1

                        # 感染判断
                        probability_of_infect = SIMULATION_ENV.infection_rate * factor_1 * factor_2
                        is_infect = bool(np.random.choice([True, False],
                                                     p=[probability_of_infect, 1 - probability_of_infect]))
                        evaluation_human_dict[human_key].infected = is_infect
                        if is_infect is True:
                            evaluation_human_dict[human_key].passed_day_after_infected = 0
                            evaluation_human_dict[human_key].has_antibodies = True

                for cluster_id in human_dict[human_key].cluster_ids:
                    # クラスターのhumanを呼び出してクラスター内の人間の評価を行う
                    cluster = cluster_dict[cluster_id]
                    # クラスターが凍結状態であれば、そのクラスターの評価は行わない。クラスターの凍結日を1日下げる。
                    if cluster.freeze is True:
                        evaluation_cluster_dict[cluster_id].freeze_remaining -= 1
                        continue

                    cluster_human_list = cluster.people
                    for human in cluster_human_list:
                        if (human.infected is True) and (human.onset_delay_days - human.passed_day_after_infected >= 2):
                            for eval_human in evaluation_cluster_dict[cluster_id].people:
                                if eval_human.has_antibodies is False:
                                    if human.masked:
                                        factor_1 = SIMULATION_ENV.utility_mask_to_someone
                                    else:
                                        factor_1 = 1
                                    if eval_human.masked:
                                        factor_2 = SIMULATION_ENV.utility_mask_from_someone
                                    else:
                                        factor_2 = 1
                                    probability_of_infect = SIMULATION_ENV.infection_rate * factor_1 * factor_2
                                    is_infect = bool(np.random.choice(a=[True, False],
                                                                 p=[probability_of_infect, 1 - probability_of_infect]))
                                    evaluation_human_dict[eval_human.id].infected = is_infect
                                    if is_infect is True:
                                        evaluation_human_dict[eval_human.id].passed_day_after_infected = 0
                                        evaluation_human_dict[eval_human.id].has_antibodies = True

        # 評価後の配列を次の日の評価元配列として保存する
        human_dict = evaluation_human_dict
        cluster_dict = evaluation_cluster_dict

        # 発症している人間を凍結する
        for key in human_dict.keys():
            if human_dict[key].onset is True and human_dict[key].freeze is False:
                human_dict[key].freeze = True
                human_dict[key].freeze_remaining = 10

        # 感染中の人間の数をカウントし、しきい値を超えていたらロックダウン手続きを行う
        counts = 0
        for human_key in human_dict.keys():
            if human_dict[human_key].onset is True:
                counts += 1
        threshold = int(SIMULATION_ENV.population * SIMULATION_ENV.lockdown_threshold)
        print(counts)
        if (threshold < counts) and (lockdown_flg is False):
            lockdown_flg = True
            logger.info("lockdown triggered!")
            for human_key in human_dict.keys():
                if human_dict[human_key].does_lock_down is True:
                    human_dict[human_key].freeze = True
                    human_dict[human_key].freeze_remaining = 10

        for key in human_dict.keys():
            if human_dict[key].onset is True:
                human_dict[key].onset_days += 1
                # 10日経過時点で発症をFalse
                if human_dict[key].onset_days == 10:
                    human_dict[key].onset = False

        # 重症評価
        aggravated_count = 0
        for _id in onset_ids:
            human = human_dict[_id]
            if counts > SIMULATION_ENV.population * SIMULATION_ENV.capacity_of_medical_care:
                table = SIMULATION_ENV.aggravation_rate_when_medical_care_capacity_exceeded
            else:
                table = SIMULATION_ENV.aggravation_rate
            if (human.age >= 0) and (human.age < 10):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["0~9"], 1-table["0~9"]]))
            elif (human.age >= 10) and (human.age < 20):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["10~19"], 1 - table["10~19"]]))
            elif (human.age >= 20) and (human.age < 30):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["20~29"], 1 - table["20~29"]]))
            elif (human.age >= 30) and (human.age < 40):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["30~39"], 1 - table["30~39"]]))
            elif (human.age >= 40) and (human.age < 50):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["40~49"], 1 - table["40~49"]]))
            elif (human.age >= 50) and (human.age < 60):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["50~59"], 1 - table["50~59"]]))
            elif (human.age >= 60) and (human.age < 70):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["60~69"], 1 - table["60~69"]]))
            elif (human.age >= 70) and (human.age < 80):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["70~79"], 1 - table["70~79"]]))
            elif (human.age >= 80) and (human.age < 90):
                aggravated = bool(np.random.choice(a=[True, False], p=[table["80~89"], 1 - table["80~89"]]))
            if aggravated is True:
                aggravated_count += 1
        result.serious_cases_transition.append(aggravated_count)
        if len(result.cumulative_serious_cases_transition) == 0:
            result.cumulative_serious_cases_transition.append(aggravated_count)
        else:
            cumulative = result.cumulative_serious_cases_transition[-1] + aggravated_count
            result.cumulative_serious_cases_transition.append(cumulative)
            print(cumulative)

        # 経済損失の計上
        result.economic_losses_transition.append(economic_loss)
        if len(result.cumulative_economic_losses_transition) == 0:
            result.cumulative_economic_losses_transition.append(economic_loss)
        else:
            cumulative = result.cumulative_economic_losses_transition[-1] + economic_loss
            result.cumulative_economic_losses_transition.append(cumulative)
            print(cumulative)

    return result
