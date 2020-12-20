from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SimulationEnvironment:
    """
    for storing variables to be assumed in the simulation.
    シミュレーションを行う上で仮定する変数を格納するクラス
    """
    simulation_days: int  # number of days for simulating(実験する日数)
    population: int  # population size of simulating(実験時の人口)
    aggravation_rate: Dict  # aggravation rate of each age layer(各年齢の罹患時重症化確率)
    aggravation_rate_when_medical_care_capacity_exceeded: Dict  # aggravation rate of each age layer when population exceeds capacity of medical care(病床超過時の各年齢の罹患時重症化確率)
    infection_rate: float  # infection rate when slight contact(すれ違いなど軽度接触での感染確率)
    clustered_infection_rate: float  # infection rate when concentrated contact(飲食などを伴う濃厚接触時の感染確率)
    utility_mask_to_someone: float  # utility to other people infection rate when wearing a mask(マスク着用時の周囲に対する感染率への影響)
    utility_mask_from_someone: float  # utility from other people infection rate when wearing a mask(マスク着用時の自身への感染率への影響)
    mask_rate: float  # wearing rate of mask(マスクの着用率の平均値)
    PCR_kit_price: int  # price of PCR inspection kit(PCRキット1つの値段)
    GDP_per_person: int  # annual gross domestic product per person(国民一人あたりの年間GDP)
    percentage_of_infect_people: float  # percentage of people infect at the start of simulation(実験開始時の発症者の割合)
    capacity_of_medical_care: float  # (人口に対する同時に医療を受けることができる割合)
    lockdown_threshold: float  # (ロックダウンの意思決定を行う感染者数の割合)
    lockdown_suppression_rate: float  # ロックダウン時の行動の抑制率、平常時から見て何割になるか
    mean_of_slight_contact: int  # 1日あたり通常の人が軽度接触する人数の平均
    number_of_cluster: int  # クラスタの生成トライアル数
    probability_of_freeze_cluster: float  # 感染者が出た場合の凍結されるクラスタの割合
    mean_of_cluster_size: int  # クラスタサイズの平均値
    mean_of_onset_delay_days: int  # 感染から発症までの平均日数


SIMULATION_ENV = SimulationEnvironment(
    simulation_days=365,
    population=1000,
    aggravation_rate={
        "0~9": 0.3,
        "10~19": 0.2,
        "20~29": 0.1,
        "30~39": 0.2,
        "40~49": 0.3,
        "50~59": 0.4,
        "60~69": 0.5,
        "70~79": 0.6,
        "80~89": 0.7
    },
    aggravation_rate_when_medical_care_capacity_exceeded={
        "0~9": 0.7,
        "10~19": 0.5,
        "20~29": 0.6,
        "30~39": 0.7,
        "40~49": 0.8,
        "50~59": 0.85,
        "60~69": 0.9,
        "70~79": 0.95,
        "80~89": 1
    },
    infection_rate=0.3,
    clustered_infection_rate=0.9,
    utility_mask_to_someone=0.3,
    utility_mask_from_someone=0.3,
    mask_rate=0.9,
    PCR_kit_price=15000,
    GDP_per_person=4200000,
    percentage_of_infect_people=0.03,
    capacity_of_medical_care=0.05,
    lockdown_threshold=0.01,
    lockdown_suppression_rate=0.3,
    mean_of_slight_contact=100,
    number_of_cluster=5000,
    probability_of_freeze_cluster=0.8,
    mean_of_cluster_size=6,
    mean_of_onset_delay_days=10
)
