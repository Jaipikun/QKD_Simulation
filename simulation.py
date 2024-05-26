from human import Human
from scipy.stats import mode
import numpy as np

class Simulation():
    def __init__(self,
                alice : dict() = {"emitter_efficiency":100},
                bob : dict() = {"detector_efficiency":100},
                eve : dict() = {"exists":False}):
        required_keys = ["emitter_efficiency","detector_efficiency","exists"]
        alice_test = required_keys[0] not in alice.keys()
        bob_test = required_keys[1] not in bob.keys()
        eve_test_1 = required_keys[2] not in eve.keys()
        if alice_test or bob_test or eve_test_1:
            raise KeyError("Invalid configuration")
        else:
            eve_test_2 = required_keys[0] not in eve.keys()
            eve_test_3 = required_keys[1] not in eve.keys()
            if eve[required_keys[2]] and (eve_test_2 or eve_test_3):
                raise KeyError("Invalid configuration for Eve")
            self.alice_config = alice
            self.bob_config = bob
            self.eve_config = eve
    @staticmethod
    def create_configuration_dict(emitter_efficiency: int = 0,
                                detector_efficiency: int = 0,
                                exists: bool = False):
        """
        Helper function for creating a valid config
        """
        config = {"emitter_efficiency":emitter_efficiency,
                "detector_efficiency":detector_efficiency,
                "exists":exists}
        return config
    def simulate(self,sender_key_length : int, tactic : int = 0):
        """
        Performs the simulation for the given key length and with a given eve's tactic.
        Available tactics:
        0 - eve randomizes all bases once, when receiving then sends with same bases
        1 - eve randomizes all bases both when receiving and sending photons
        2 - eve uses 0 as a base for every measurement
        3 - eve uses 1 as a base for every measurement
        4 - eve uses a base of 1s and 0s where 1 is for odd indices and 0 for even

        Args:
            sender_key_length: int defining the initial key length
            tactic: int defining which tactic's to be used
        Returns:
            results_dict: a dict holding all the results
                     scheme:
                        {
                        "alice_initial_key" : str,
                        "alice_base" : str,
                        "bob_initial_key" : str,
                        "bob_base" : str,
                        "eve_stolen_key" : str || None,
                        "eve_base" : str || None,
                        "final_key" : str,
                        "error_rate" : float,
                        "alice_key_same_bases" : str,
                        "bob_key_same_bases" : str
                        }
        """
        alice = Human(sender_key_length,emitter_efficiency=self.alice_config["emitter_efficiency"])
        photon_beam = alice.send()
        bob = Human(detector_efficiency=self.bob_config["detector_efficiency"])
        if self.eve_config["exists"]:
            eve = Human(emitter_efficiency=self.eve_config["emitter_efficiency"],
                        detector_efficiency=self.eve_config["detector_efficiency"])
            if tactic in [2,3]:
                temp_base = ""
                for i in range(sender_key_length):
                    temp_base += '0' if tactic == 2 else '1'
                eve.base = temp_base
            if tactic == 4:
                temp_base = ""
                for i in range(sender_key_length):
                    if i%2:
                        temp_base += '0' # even numbers
                    else:
                        temp_base +='1'  # odd numbers
                eve.base = temp_base
            eve.receive(photon_beam)
            if tactic == 1:
                eve.base = None
            photon_beam = eve.send()
        bob.receive(photon_beam)
        results_dict = {
            "alice_initial_key" : alice.key,
            "alice_base" : alice.base,
            "bob_initial_key" : bob.key,
            "bob_base" : bob.base,
            "eve_stolen_key" : eve.key if self.eve_config["exists"] else None,
            "eve_base" : eve.base if self.eve_config["exists"] else None,
            "tactic" : tactic if self.eve_config["exists"] else None,
        }
        results_dict.update(self.qber(alice, bob))
        return results_dict
    def qber(self,
            alice : Human,
            bob : Human):
        """
        Function used for calculating the quantum bit error rate as well as creating final key by
        filtering out the incorrect bits

        Args:
            alice: Human instance equivalent to BB84 Alice
            bob: Human instance equivalent to BB84 Bob
        Returns:
            results_dict: a dict holding all the results from comparisons
                     scheme:
                        {
                        "final_key" : str,
                        "error_rate" : float,
                        "alice_key_same_bases" : str,
                        "bob_key_same_bases" : str
                        }
        """
        alice_key_filtered = ""
        bob_key_filtered = ""
        final_key = ""
        good_bits = 0
        for i in range(alice.key_length):
            if alice.base[i] == bob.base[i]:
                alice_key_filtered += alice.key[i]
                bob_key_filtered += bob.key[i]
                if alice.key[i] == bob.key[i]:
                    good_bits +=1
                    final_key += alice.key[i]
        if good_bits == 0:
            error_rate = 100
        else:
            error_rate = (1 - (good_bits / len(alice_key_filtered))) * 100.0
        results_dict = {
            "final_key" : final_key,
            "error_rate" : error_rate,
            "alice_key_same_bases" : alice_key_filtered,
            "bob_key_same_bases" : bob_key_filtered
        }
        return results_dict

def main():
    """
    Basic test
    """
    alice = Simulation.create_configuration_dict(100,100,True)
    bob = Simulation.create_configuration_dict(100,100,True)
    eve = Simulation.create_configuration_dict(100,100,True)
    sim = Simulation(alice,bob,eve)
    results_dict = sim.simulate(15)
    print (results_dict["error_rate"])

if __name__ == "__main__":
    main()
