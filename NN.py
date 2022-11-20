from numpy import exp, array, random, dot
from random import uniform

no_input_neurons = 8

class NeuralNetwork:
    def __init__(self):
        self.input_layer = [Neuron() for _ in range(4)]
        self.hidden_layer = [Neuron() for _ in range(4)]
        self.output_layer = [Neuron() for _ in range(4)]
    
    def get_output(self, input):
        input_outputs = []
        for i in range (len(input)):
            out = self.input_layer[i].get_intermediate_output(input[i])
            input_outputs.append(out)
        
        # hidden_outputs = []
        # for neuron in self.hidden_layer:
        #     out = neuron.get_output(input_outputs)
        #     hidden_outputs.append(out)
        output = []
        for neuron in self.output_layer:
            out = neuron.get_output(input_outputs)
            output.append(out)

        max_value = max(output)
        max_index = output.index(max_value)

        # moves = [(0,-10), (10,0), (0,10), (-10,0)]
        # return moves[round(normalised_sum * 3)]
        # #0 = up // (0,-10)
        # #1 = right // (10, 0)
        # #2 = down // (0,10)
        # #3 = left // (-10,0)

        if max_index == 0:
            return (10,0)
        elif max_index == 1:
            return (0,10)
        elif max_index == 2:
            return (0, -10)
        else:
            return (-10,0)

       
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

class Neuron:
    def __init__(self):
        self.weight = uniform(-1,1)
        self.bias = uniform(-1,1)

    def get_intermediate_output(self, input):
        return (input * self.weight) + self.bias


    def get_output(self, input):
        sum = 0.0
        for i in input:
            sum += i * self.weight
        sum += self.bias 

        return self.__sigmoid(sum)
        
        
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))