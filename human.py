from qiskit import QuantumCircuit,transpile
from qiskit_aer import AerSimulator

class Human():
    def __init__(self,
                input_bases: list = None,
                output_bases: list = None,
                key: list = None,
                emitter_efficiency: float = 0,
                detector_efficiency: float = 0):
        self.input_bases = input_bases
        self.output_bases = output_bases
        self.key = key
        self.emitter_efficiency = emitter_efficiency
        self.detector_efficiency = detector_efficiency
    def receive(self,photons):
        return 0
    def send(self):
        return 
    def device_malfunction(self,chance_of_malfunction: float = 0.0):
        simulator = AerSimulator()
        amount_of_error_states = int(round(chance_of_malfunction / 0.1,2))
        error_states = [
            i for i in range(amount_of_error_states)
        ]
        circuit = QuantumCircuit(10)
        for i in range(10):
            circuit.h(i)
        circuit.measure_all()
        compiled = transpile(circuit,simulator)
        result_of_circuit = simulator.run(compiled,shots=1).result().data()['counts']
        measurement = int(list(result_of_circuit.keys())[0],16)
        if measurement in error_states:
            return True
        return False


def main():
    human_test = Human()
    cnt=0
    for i in range(100):
        test = human_test.device_malfunction(20)
        if test:
            cnt+=1
    print(cnt)
    return 0

if __name__=='__main__':
    main()