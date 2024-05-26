from simulation import Simulation
from scipy.stats import mode
from numpy import average
import matplotlib.pyplot as plt

CONFIG = {
    "key_lengths" : [15],
    "detector_efficiencies" : [i*5 for i in range(21)],
    "emitter_efficiencies" : [i*5 for i in range(21)],
    "eavesdropping" : [True,False],
    "tactic" : [0,1,2,3,4],
    "generate_plots" : True,
    "number_of_iterations_per_simulation" : 5,
    "change_eve_efficiency" : False # Not implemented
}

def set_of_simulations():
    results_list = []
    for key_length in CONFIG["key_lengths"]:
        for eavesdropper in CONFIG["eavesdropping"]:
            for tactic in CONFIG["tactic"]:
                for detector_efficiency in CONFIG["detector_efficiencies"]:
                    for emitter_efficiency in CONFIG["emitter_efficiencies"]:
                        temp = [[],[]]
                        for i in range(CONFIG["number_of_iterations_per_simulation"]): # TBD
                            alice_config = Simulation.create_configuration_dict(emitter_efficiency=emitter_efficiency)
                            bob_config = Simulation.create_configuration_dict(detector_efficiency=detector_efficiency)
                            eve_config = Simulation.create_configuration_dict(100,100,eavesdropper)
                            sim = Simulation(alice_config,bob_config,eve_config)
                            results_dict = sim.simulate(key_length,tactic)
                            temp[0].append(results_dict["error_rate"])
                            temp[1].append(len(results_dict["final_key"]))
                        results_dict.update({
                                "detector_efficiency" : detector_efficiency,
                                "emitter_efficiency" : emitter_efficiency,
                                "average_error_rate" : average(temp[0]),
                                "mode_error_rate" : mode(temp[0])[0],
                                "average_key_length" : average(temp[1]),
                                "mode_key_length" : mode(temp[1])[0],
                            })
                        results_list.append(results_dict)
                    break #TEMPORARY BREAKS
                break
            break
        break
    
    return results_list

def main():
    results = set_of_simulations()
    # TEMPORARY SOLUTION - TESTING PLOTS
    temp = [[],[],[],[],[],[]]
    for result in results:
        temp[0].append(result["detector_efficiency"])
        temp[1].append(result["emitter_efficiency"])
        temp[2].append(result["average_error_rate"])
        temp[3].append(result["mode_error_rate"])
        temp[4].append(result["average_key_length"])
        temp[5].append(result["mode_key_length"])
    
    fig = plt.figure(figsize=(12,8))
    plt.plot(temp[1],temp[2],color="blue",label = "average qber")
    plt.plot(temp[1],temp[3],color="red",label = "mode qber")
    plt.legend()
    fig.savefig("test_qber.png")
    fig = plt.figure(figsize=(12,8))
    plt.plot(temp[1],temp[4],color="blue",label = "average kl")
    plt.plot(temp[1],temp[5],color="red",label = "mode kl")
    plt.legend()
    fig.savefig("test_kl.png")
    

if __name__ == "__main__":
    main()
