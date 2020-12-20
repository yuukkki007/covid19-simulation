import numpy as np
from scipy import stats
from lib.log import logger
from domain.simulation import simulate


if __name__ == '__main__':

    result_lockdown_serious_case_list = []
    result_lockdown_economy_loss_list = []

    result_pcr_serious_case_list = []
    result_pcr_economy_loss_list = []
    for i in range(5):
        logger.info(f"start simulation {i+1}")
        simulation_result_when_lockdown, simulation_result_when_pcr = simulate()

        print("lockdown", "serious case", sum(simulation_result_when_lockdown.serious_cases_transition))
        result_lockdown_serious_case_list.append(sum(simulation_result_when_lockdown.serious_cases_transition))
        print("lockdown", "economic losses", sum(simulation_result_when_lockdown.economic_losses_transition))
        result_lockdown_economy_loss_list.append(sum(simulation_result_when_lockdown.economic_losses_transition))

        print("pcr", "serious case", sum(simulation_result_when_pcr.serious_cases_transition))
        result_pcr_serious_case_list.append(sum(simulation_result_when_pcr.serious_cases_transition))
        print("pcr", "economic losses", sum(simulation_result_when_pcr.economic_losses_transition))
        result_pcr_economy_loss_list.append(sum(simulation_result_when_pcr.economic_losses_transition))

    print("lockdown serious case mean", np.mean(result_lockdown_serious_case_list))
    print("lockdown serious case std", np.sqrt(np.var(result_lockdown_serious_case_list)))
    print("lockdown serious case skew", stats.skew(np.array(result_lockdown_serious_case_list)))

    print("lockdown economic loss mean", np.mean(result_lockdown_economy_loss_list))
    print("lockdown economic loss std", np.sqrt(np.var(result_lockdown_economy_loss_list)))
    print("lockdown economic loss skew", stats.skew(np.array(result_lockdown_economy_loss_list)))

    print("pcr serious case mean", np.mean(result_pcr_serious_case_list))
    print("pcr serious case std", np.sqrt(np.var(result_pcr_serious_case_list)))
    print("pcr serious case skew", stats.skew(np.array(result_pcr_serious_case_list)))

    print("pcr economic loss mean", np.mean(result_pcr_economy_loss_list))
    print("pcr economic loss std", np.sqrt(np.var(result_pcr_economy_loss_list)))
    print("pcr economic loss skew", stats.skew(np.array(result_pcr_economy_loss_list)))
