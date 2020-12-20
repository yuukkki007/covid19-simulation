import uuid
from dataclasses import dataclass
from typing import List

import numpy as np

from domain.const import SIMULATION_ENV


@dataclass(frozen=False)
class Human:
    id: str  # random generated uuid(ランダムに採番されるuuid)
    age: int  # age(年齢)
    masked: bool  # wearing mask or not(マスク着用の有無)
    onset: bool  # onset or not(発症中かどうか)
    onset_delay_days: int  # number of days from infection to onset(感染から発症までの日数)
    onset_days: int  # number of days elapsed since onset(発症後経過日数)
    infected: bool  # infect or not(感染しているか)
    passed_day_after_infected: int  # number of days elapsed since infect(感染からの経過日数)
    know_infection: bool  # know that I am infected or not(感染していることを知っているか)
    has_antibodies: bool  # has antibodies or does not(抗体を持っているか)
    random_meet_per_day: int  # slight contact per day(1日あたりのすれ違いなどの接触人数)
    cluster_ids: List  # cluster id list of that belongs 所属しているクラスターのidリスト
    freeze: bool  # isolated or not(隔離中か)
    freeze_remaining: int  # remaining days be isolated(隔離残日数)
    pcr: bool  # take pcr in 10 days or not(直近10日間pcr実施有無)
    passed_day_after_pcr: int  # number of days elapsed since PCR test(PCR検査実施後経過日数)
    does_lock_down: bool  # follow at lockdown or not(lockdown時に従うか)

    def join_to_cluster(self, cluster_id: str):
        self.cluster_ids.append(cluster_id)


class HumanFactory:

    @staticmethod
    def generate_age() -> int:
        """
        return age based on distribution, you can implement other distribution if you want.
        人口の年齢分布に基づいて年齢を返却する、日本の分布に基づいているが必要であれば別の分布を実装しても良い
        # FIXME 時間がないため一様分布とした
        # FIXME uniform distribution, because of implementation time.
        """
        return np.random.randint(0, 90)

    @staticmethod
    def is_masked() -> bool:
        """
        return wearing mask or not based on environment variables
        マスクを着用するかどうかを環境変数に基づいて返却する
        """

        return bool(np.random.choice(a=[True, False], p=[SIMULATION_ENV.mask_rate, 1 - SIMULATION_ENV.mask_rate]))

    @staticmethod
    def is_infect() -> bool:
        """
        return this human is be infect or not based on environment variables
        現在感染しているかどうかを環境変数に基づいて返却する
        """
        return bool(np.random.choice(a=[True, False], p=[SIMULATION_ENV.percentage_of_infect_people,
                                                            1 - SIMULATION_ENV.percentage_of_infect_people]))

    def generate_instance(self):
        """
        Create Human instance based on SIMULATION_ENV instance
        シミュレーションの定数に基づいてHumanインスタンスを生成する
        """
        onset_delay_noise = np.random.normal(loc=0, scale=SIMULATION_ENV.mean_of_onset_delay_days / 3, size=None)
        if - onset_delay_noise > SIMULATION_ENV.mean_of_onset_delay_days:
            onset_delay_noise = - SIMULATION_ENV.mean_of_onset_delay_days
        random_meet_per_day_noise = np.random.normal(loc=0, scale=SIMULATION_ENV.mean_of_slight_contact / 3, size=None)
        if - random_meet_per_day_noise > SIMULATION_ENV.mean_of_slight_contact:
            random_meet_per_day_noise = - SIMULATION_ENV.mean_of_slight_contact
        unique_id = str(uuid.uuid4())
        is_initial_infected = self.is_infect()
        human = Human(
            id=unique_id,
            age=self.generate_age(),
            masked=self.is_masked(),
            onset_delay_days=int(SIMULATION_ENV.mean_of_onset_delay_days + onset_delay_noise),
            onset=False,
            onset_days=0,
            passed_day_after_infected=0,
            infected=is_initial_infected,
            know_infection=False,
            has_antibodies=False,
            random_meet_per_day=int(SIMULATION_ENV.mean_of_slight_contact + random_meet_per_day_noise),
            cluster_ids=[],
            freeze=False,
            freeze_remaining=0,
            pcr=False,
            passed_day_after_pcr=0,
            does_lock_down=bool(np.random.choice(a=[True, False], p=[1-SIMULATION_ENV.lockdown_suppression_rate,
                                                            SIMULATION_ENV.lockdown_suppression_rate]))
        )

        return unique_id, human
