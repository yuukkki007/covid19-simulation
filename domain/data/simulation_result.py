from dataclasses import dataclass
from typing import List


@dataclass(frozen=False)
class SimulationResult:
    economic_losses_transition: List  # economic losses transition(経済損失推移)
    serious_cases_transition: List  # number of patients serious transition(重症化者数推移)
    cumulative_economic_losses_transition: List  # transition of cumulative economic losses(累積経済損失推移)
    cumulative_serious_cases_transition: List  # transition of cumulative number of patients serious(累積重症化者数推移)
