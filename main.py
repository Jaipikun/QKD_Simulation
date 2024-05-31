from simulation import Simulation
from scipy.stats import mode
from numpy import average
import matplotlib.pyplot as plt

CONFIG = {
    "key_lengths" : [10,15,20],
    "detector_efficiencies" : [i*5 for i in range(21)],
    "emitter_efficiencies" : [i*5 for i in range(21)],
    "eavesdropping" : [False,True],
    "eve_tactic" : [0,1,2,3,4],
    "generate_plots" : True,
    "number_of_iterations_per_simulation" : 200,
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

def detector_efficiency_tests():
    """
    This function performs simulations for all given detector efficiencies
    """
    no_iterations = CONFIG["number_of_iterations_per_simulation"]
    total_iter = no_iterations * len(CONFIG["emitter_efficiencies"])*len(CONFIG["eavesdropping"])*len(CONFIG["key_lengths"])
    print(f"Simulation for detector efficiency : total number of iterations = {total_iter}")
    iteration = 1
    for key_length in CONFIG["key_lengths"]:
        x_list = []
        y_lists = [[],[],[],[]]
        for eavesdropper in CONFIG["eavesdropping"]:
            for det_eff in CONFIG["detector_efficiencies"]:
                temp_result = [[],[]]
                for j in range(no_iterations):
                    print(f"Simulating {iteration} / {total_iter} with config {key_length,det_eff,eavesdropper}")
                    alice_config = Simulation.create_configuration_dict(emitter_efficiency=100)
                    bob_config = Simulation.create_configuration_dict(detector_efficiency=det_eff)
                    eve_config = Simulation.create_configuration_dict(100,100,eavesdropper)
                    sim = Simulation(alice_config,bob_config,eve_config)
                    results_dict = sim.simulate(key_length,0)
                    temp_result[0].append(results_dict["error_rate"])
                    temp_result[1].append(len(results_dict["final_key"]))
                    iteration+=1
                x_list.append(det_eff)
                y_lists[0].append(average(temp_result[0]))
                y_lists[1].append(mode(temp_result[0])[0])
                y_lists[2].append(average(temp_result[1]))
                y_lists[3].append(mode(temp_result[1])[0])
        fig,axes = plt.subplots(2,2,figsize=(20,20))
        for k in range(4):
            axes[k%2, int(k/2.0)].plot(x_list[0:len(CONFIG["detector_efficiencies"])],y_lists[k][0:len(CONFIG["detector_efficiencies"])],color = 'blue',label="without Eve")
            axes[k%2, int(k/2.0)].plot(x_list[len(CONFIG["detector_efficiencies"]):-1],y_lists[k][len(CONFIG["detector_efficiencies"]):-1],'--r',label="with Eve")
            axes[k%2, int(k/2.0)].legend(fontsize=12,loc='best')
            axes[k%2, int(k/2.0)].set_title(f"{'Mode' if k%2 else 'Average'} {'quantum bit error rate' if k in [0,1] else 'usable key length'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_ylabel(f"{'quantum bit error rate' if k in [0,1] else 'usable key length'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_xlabel('Detector efficiency [%]',fontsize=20)
        fig.savefig(f"test_detector_{key_length}.png")
        print("xddd")


def emitter_efficiency_tests():
    """
    This function performs simulations for all given emitter efficiencies
    """
    no_iterations = CONFIG["number_of_iterations_per_simulation"]
    total_iter = no_iterations * len(CONFIG["emitter_efficiencies"])*len(CONFIG["eavesdropping"])*len(CONFIG["key_lengths"])
    print(f"Simulation for emitter efficiency : total number of iterations = {total_iter}")
    iteration = 1
    for key_length in CONFIG["key_lengths"]:
        x_list = []
        y_lists = [[],[],[],[]]
        for eavesdropper in CONFIG["eavesdropping"]:
            for emi_eff in CONFIG["emitter_efficiencies"]:
                temp_result = [[],[]]
                for j in range(no_iterations):
                    print(f"Simulating {iteration} / {total_iter} with config {key_length,emi_eff,eavesdropper}")
                    alice_config = Simulation.create_configuration_dict(emitter_efficiency=emi_eff)
                    bob_config = Simulation.create_configuration_dict(detector_efficiency=100)
                    eve_config = Simulation.create_configuration_dict(100,100,eavesdropper)
                    sim = Simulation(alice_config,bob_config,eve_config)
                    results_dict = sim.simulate(key_length,0)
                    temp_result[0].append(results_dict["error_rate"])
                    temp_result[1].append(len(results_dict["final_key"]))
                    iteration+=1
                x_list.append(emi_eff)
                y_lists[0].append(average(temp_result[0]))
                y_lists[1].append(mode(temp_result[0])[0])
                y_lists[2].append(average(temp_result[1]))
                y_lists[3].append(mode(temp_result[1])[0])
        fig,axes = plt.subplots(2,2,figsize=(20,20))
        for k in range(4):
            axes[k%2, int(k/2.0)].plot(x_list[0:len(CONFIG["emitter_efficiencies"])],y_lists[k][0:len(CONFIG["emitter_efficiencies"])],color = 'blue',label="without Eve")
            axes[k%2, int(k/2.0)].plot(x_list[len(CONFIG["emitter_efficiencies"]):-1],y_lists[k][len(CONFIG["emitter_efficiencies"]):-1],'--r',label="with Eve")
            axes[k%2, int(k/2.0)].legend(fontsize=12,loc='best')
            axes[k%2, int(k/2.0)].set_title(f"{'Average' if k%2 else 'Mode'} {'quantum bit error rate' if k in [0,1] else 'usable key length'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_ylabel(f"{'quantum bit error rate' if k in [0,1] else 'usable key length'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_xlabel('Emitter efficiency [%]',fontsize=20)
        fig.savefig(f"test_emitter_{key_length}.png")


def eve_tactics_test():
    """
    This function performs simulations for all given detector efficiencies
    """
    no_iterations = CONFIG["number_of_iterations_per_simulation"]
    total_iter = no_iterations * len(CONFIG["tactic"])*len(CONFIG["eavesdropping"])*len(CONFIG["key_lengths"])
    print(f"Simulation for different eve tactics : total number of iterations = {total_iter}")
    iteration = 1
    # TBD

def main():
    detector_efficiency_tests()
    print("\n\nDETECTOR EFFICIENCY SIMULATIONS FINISHED\n\n")
    emitter_efficiency_tests()
    

if __name__ == "__main__":
    main()
