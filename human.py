from qiskit import QuantumCircuit,transpile
from qiskit_aer import AerSimulator
from photon import Photon

class Human():
    def __init__(self,
                key_length: int = 1,
                emitter_efficiency: float = 100.0,
                detector_efficiency: float = 100.0):
        self.key_length = key_length
        self.emitter_efficiency = emitter_efficiency
        self.detector_efficiency = detector_efficiency
        self.base = None
        self.key = None
    def receive(self,photon_beam: list):
        """
        Simulation of the photon beam generation procedure.

        Args:
            photon_beam: a list containing Photon class elements
        """
        no_photons = len(photon_beam)
        # Generate base
        base_val = self.randomize_number(no_photons)
        # Convert base to binary str with preceding 0s
        self.base = self.convert_decimal_to_binary_str(base_val,no_photons)
        key = ''
        for i,photon in enumerate(photon_beam):
            # Simulate the possible malfunction of the detector
            detector_malfunction = self.device_malfunction(1 - self.detector_efficiency)
            if detector_malfunction:
                # Detector failed, randomize whether it changed the base or the value of the photon
                value_change = self.randomize_number(1)
                if value_change:
                    photon.change_value()
                else:
                    photon.switch_base()
            measurement = self.measure_photon(photon,int(self.base[i]))
            key = key + str(measurement)
        self.key = key
    def measure_photon(self,photon: Photon,measurement_base:int):
        """
        Measures the bit contained in the photon

        Args:
            photon: Photon class photon to be measured
            measurement_base: base in which the photon's measured
        """
        if photon.base != measurement_base:
            # If the bases are different, value is randomized
            photon.value = self.randomize_number(1)
        return photon.value
    def send(self):
        """
        Simulation of the photon beam generation procedure.

        Returns:
            photon_beam: a list containing Photon class elements
        """
        # Generate key
        key_val = self.randomize_number(self.key_length)
        # Convert key to binary str with preceding 0s
        self.key = self.convert_decimal_to_binary_str(key_val,self.key_length)
        # Generate base
        base_val = self.randomize_number(self.key_length)
        # Convert base to binary str with preceding 0s
        self.base = self.convert_decimal_to_binary_str(base_val,self.key_length)
        photon_beam = []
        for i in range(self.key_length):
            # Create a photon with each base and key bit value
            photon = Photon(int(self.base[i]),int(self.key[i]))
            # Simulate the possible malfunction of the emitter
            emitter_malfunction = self.device_malfunction(1 - self.emitter_efficiency)
            if emitter_malfunction:
                # Emitter failed, randomize whether it changed the base or the value of the photon
                value_change = self.randomize_number(1)
                if value_change:
                    photon.change_value()
                else:
                    photon.switch_base()
            photon_beam.append(photon)
        return photon_beam
    def convert_decimal_to_binary_str(self,decimal_number:int,number_of_bits:int):
        binary = str(bin(decimal_number))[2:]
        new_str = ''
        if len(binary) != number_of_bits:
            for i in range(number_of_bits - len(binary)):
                new_str = new_str + '0'
        return new_str + binary

    def randomize_number(self,number_of_bits:int = 1):
        """
        This function's going to return a fully random number
        Args:
            number_of_bits: int equal to the number of bits in the output number
        Returns:
            value: int in the range of (0,2^number_of_bits - 1)
        """
        simulator = AerSimulator()
        circuit = QuantumCircuit(number_of_bits)
        for i in range(number_of_bits):
            circuit.h(i)
        circuit.measure_all()
        compiled = transpile(circuit,simulator)
        result_of_circuit = simulator.run(compiled,shots=1).result().data()['counts']
        value = int(list(result_of_circuit.keys())[0],16)
        return value
    def device_malfunction(self,chance_of_malfunction: float = 0.0):
        """
        Function which decides whether the device malfunctioned, thus caused an error.
        It's purely undeterministic (assuming the qubits are real) with an accuracy of up to
        10th of a percent since we assume 1/1024 ~ 1/1000

        Args:
            chance_of_malfunction: float between 0-100 equal to the chance of device malfunctioning
        Returns:
            measurement: either True or False - where True means that the device malfunctioned

        """
        amount_of_error_states = int(round(chance_of_malfunction / 0.1,2))
        error_states = [
            i for i in range(amount_of_error_states)
        ]
        measurement = self.randomize_number(10)
        if measurement in error_states:
            return True
        return False


def main():
    key_length = 28
    Alice = Human(key_length,emitter_efficiency=0)
    Bob = Human()
    photon_beam = Alice.send()
    Bob.receive(photon_beam)
    print(f"Alice's key: {Alice.key}\nBob's key: {Bob.key}")
    cnt=0
    alice_key = Alice.key
    bob_key = Bob.key
    for i in range(key_length):
        if alice_key[i] == bob_key[i]:
            cnt+=1
    print(f'Similarity percentage: {round(cnt/key_length,2)*100}%')
    return 0

if __name__=='__main__':
    for i in range(20):
        main()
