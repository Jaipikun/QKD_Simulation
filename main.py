"""
Main module which generates all the plots based on BB84 QKD concept
"""
from scipy.stats import mode
from numpy import average
import matplotlib.pyplot as plt
from simulation import Simulation

# CONFIG for changing the parameters of simulation, all of them should be given as a list - even
# for 1 element, with the exception of 'number of iterations' which should be given straight
# as an int
CONFIG = {                                              # possible value ranges / types
    "key_lengths" : [20,15,10],                         # [1, 26] : int <- AerSimulator limit
    "detector_efficiencies" : [i*5 for i in range(21)], # [0,100] : int
    "emitter_efficiencies" : [i*5 for i in range(21)],  # [0,100] : int
    "system_efficiencies" : [i*5 for i in range(21)],   # [0,100] : int
    "eavesdropping" : [False,True],                     # False or True : bool
    "eve_tactic" : [0,1,2,3,4],                         # [0,4] : int
    "number_of_iterations_per_simulation" : 200,        # [1,inf) : int
}

def detector_efficiency_tests():
    """
    This function performs simulations for all given detector efficiencies
    """
    no_iterations = CONFIG["number_of_iterations_per_simulation"]
    total_iter = no_iterations*len(CONFIG["detector_efficiencies"])*len(CONFIG["eavesdropping"])*len(CONFIG["key_lengths"])
    print(f"Simulation for detector efficiency : total number of iterations = {total_iter}")
    iteration = 1
    for key_length in CONFIG["key_lengths"]:
        x_list = []
        y_lists = [[],[],[],[]]
        for eavesdropper in CONFIG["eavesdropping"]:
            for det_eff in CONFIG["detector_efficiencies"]:
                temp_result = [[],[]]
                for j in range(no_iterations):
                    print(f"Simulating detector tests # {iteration} / {total_iter} with config {key_length,det_eff,eavesdropper}")
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
            axes[k%2, int(k/2.0)].set_ylabel(f"{'quantum bit error rate [%]' if k in [0,1] else 'usable key length [bit]'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_xlabel('Detector efficiency [%]',fontsize=20)
        fig.savefig(f"test_detector_{key_length}.png")


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
                    print(f"Simulating emitter test # {iteration} / {total_iter} with config {key_length,emi_eff,eavesdropper}")
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
            axes[k%2, int(k/2.0)].set_title(f"{'Mode' if k%2 else 'Average'} {'quantum bit error rate' if k in [0,1] else 'usable key length'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_ylabel(f"{'quantum bit error rate [%]' if k in [0,1] else 'usable key length [bit]'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_xlabel('Emitter efficiency [%]',fontsize=20)
        fig.savefig(f"test_emitter_{key_length}.png")

def system_efficiency_tests():
    """
    This function performs simulations for all given system efficiencies
    """
    no_iterations = CONFIG["number_of_iterations_per_simulation"]
    total_iter = no_iterations*len(CONFIG["system_efficiencies"])*len(CONFIG["eavesdropping"])*len(CONFIG["key_lengths"])
    print(f"Simulation for detector efficiency : total number of iterations = {total_iter}")
    iteration = 1
    for key_length in CONFIG["key_lengths"]:
        x_list = []
        y_lists = [[],[],[],[]]
        for eavesdropper in CONFIG["eavesdropping"]:
            for eff in CONFIG["system_efficiencies"]:
                temp_result = [[],[]]
                for j in range(no_iterations):
                    print(f"Simulating detector tests # {iteration} / {total_iter} with config {key_length,eff,eavesdropper}")
                    alice_config = Simulation.create_configuration_dict(emitter_efficiency=eff)
                    bob_config = Simulation.create_configuration_dict(detector_efficiency=eff)
                    eve_config = Simulation.create_configuration_dict(100,100,eavesdropper)
                    sim = Simulation(alice_config,bob_config,eve_config)
                    results_dict = sim.simulate(key_length,0)
                    temp_result[0].append(results_dict["error_rate"])
                    temp_result[1].append(len(results_dict["final_key"]))
                    iteration+=1
                x_list.append(eff)
                y_lists[0].append(average(temp_result[0]))
                y_lists[1].append(mode(temp_result[0])[0])
                y_lists[2].append(average(temp_result[1]))
                y_lists[3].append(mode(temp_result[1])[0])
        fig,axes = plt.subplots(2,2,figsize=(20,20))
        for k in range(4):
            axes[k%2, int(k/2.0)].plot(x_list[0:len(CONFIG["system_efficiencies"])],y_lists[k][0:len(CONFIG["system_efficiencies"])],color = 'blue',label="without Eve")
            axes[k%2, int(k/2.0)].plot(x_list[len(CONFIG["system_efficiencies"]):-1],y_lists[k][len(CONFIG["system_efficiencies"]):-1],'--r',label="with Eve")
            axes[k%2, int(k/2.0)].legend(fontsize=12,loc='best')
            axes[k%2, int(k/2.0)].set_title(f"{'Mode' if k%2 else 'Average'} {'quantum bit error rate' if k in [0,1] else 'usable key length'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_ylabel(f"{'quantum bit error rate [%]' if k in [0,1] else 'usable key length [bit]'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_xlabel('System efficiency [%]',fontsize=20)
        fig.savefig(f"test_system_{key_length}.png")

def eve_tactics_test():
    """
    This function performs simulations for all given eve tactics
    """
    no_iterations = CONFIG["number_of_iterations_per_simulation"]
    efficiencies = [i*10 for i in range(11)]
    total_iter = no_iterations*len(efficiencies)*len(CONFIG["key_lengths"])*(len(CONFIG["eve_tactic"]) + 1)
    print(f"Simulation for different eve tactics : total number of iterations = {total_iter}")
    iteration = 1
    for key_length in CONFIG["key_lengths"]:
        x_list = [[],[]]
        y_lists = [[],[],[],[]]
        y_lists_2 = [[],[],[],[]]
        label_list = []
        for tactic in CONFIG["eve_tactic"]:
            label_list.append("Tactic #" + str(tactic))
            for eff in efficiencies:
                temp_result = [[],[]]
                for j in range(no_iterations):
                    print(f"Simulating eve tactic test # {iteration} / {total_iter} with config {key_length,eff,tactic}")
                    alice_config = Simulation.create_configuration_dict(emitter_efficiency=eff)
                    bob_config = Simulation.create_configuration_dict(detector_efficiency=eff)
                    eve_config = Simulation.create_configuration_dict(100,100,True)
                    sim = Simulation(alice_config,bob_config,eve_config)
                    results_dict = sim.simulate(key_length,tactic)
                    temp_result[0].append(results_dict["error_rate"])
                    temp_result[1].append(len(results_dict["final_key"]))
                    iteration+=1
                x_list[0].append(eff)
                y_lists[0].append(average(temp_result[0]))
                y_lists[1].append(mode(temp_result[0])[0])
                y_lists[2].append(average(temp_result[1]))
                y_lists[3].append(mode(temp_result[1])[0])
        for eff in efficiencies:
            temp_result = [[],[]]
            for j in range(no_iterations):
                print(f"Simulating eve tactic test # {iteration} / {total_iter} with config {key_length,eff,'no Eve'}")
                alice_config = Simulation.create_configuration_dict(emitter_efficiency=eff)
                bob_config = Simulation.create_configuration_dict(detector_efficiency=eff)
                eve_config = Simulation.create_configuration_dict(100,100,False)
                sim = Simulation(alice_config,bob_config,eve_config)
                results_dict = sim.simulate(key_length,0)
                temp_result[0].append(results_dict["error_rate"])
                temp_result[1].append(len(results_dict["final_key"]))
                iteration+=1
            x_list[1].append(eff)
            y_lists_2[0].append(average(temp_result[0]))
            y_lists_2[1].append(mode(temp_result[0])[0])
            y_lists_2[2].append(average(temp_result[1]))
            y_lists_2[3].append(mode(temp_result[1])[0])
        fig,axes = plt.subplots(2,2,figsize=(20,20))
        for k in range(4):
            for l in range(len(CONFIG["eve_tactic"])):
                axes[k%2, int(k/2.0)].plot(x_list[0][l*len(efficiencies):(l+1)*len(efficiencies)],y_lists[k][l*len(efficiencies):(l+1)*len(efficiencies)],label=label_list[l])
                axes[k%2, int(k/2.0)].legend(fontsize=12,loc='best')
                axes[k%2, int(k/2.0)].set_title(f"{'Mode' if k%2 else 'Average'} {'quantum bit error rate' if k in [0,1] else 'usable key length'}",fontsize=20)
                axes[k%2, int(k/2.0)].set_ylabel(f"{'quantum bit error rate [%]' if k in [0,1] else 'usable key length [bit]'}",fontsize=20)
                axes[k%2, int(k/2.0)].set_xlabel('Emitter and detector efficiency [%]',fontsize=20)
        for k in range(4):
            axes[k%2, int(k/2.0)].plot(x_list[1],y_lists_2[k],label="Without Eve")
            axes[k%2, int(k/2.0)].legend(fontsize=12,loc='best')
            axes[k%2, int(k/2.0)].set_title(f"{'Mode' if k%2 else 'Average'} {'quantum bit error rate' if k in [0,1] else 'usable key length'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_ylabel(f"{'quantum bit error rate [%]' if k in [0,1] else 'usable key length [bit]'}",fontsize=20)
            axes[k%2, int(k/2.0)].set_xlabel('Emitter and detector efficiency [%]',fontsize=20)
        fig.savefig(f"test_eve_tactic_{key_length}.png")

def main():
    """
    Main which activates all the test functions
    """
    #detector_efficiency_tests()
    #print("\n\nDETECTOR EFFICIENCY SIMULATIONS FINISHED\n\n")
    #emitter_efficiency_tests()
    #eve_tactics_test()
    system_efficiency_tests()

if __name__ == "__main__":
    main()
