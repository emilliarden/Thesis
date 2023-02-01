from numpy import exp, array, random, dot
from random import uniform
import math

class NeuralNetwork:
    def __init__(self):
        self.input_layer = [Neuron() for _ in range(7)]
        self.hidden_layer = [Neuron() for _ in range(14)]
        # self.hidden_layer2 = [Neuron() for _ in range(6)]
        self.output_layer = [Neuron() for _ in range(2)]
    
    def get_output(self, input):
        input_outputs = []
        for i in range(len(input)):
            out = self.input_layer[i].get_intermediate_output(input[i])
            input_outputs.append(out)
        
        hidden_outputs = []
        for neuron in self.hidden_layer:
            out = neuron.get_output_wos(input_outputs)
            hidden_outputs.append(out)

        # hidden_outputs2 = []
        # for neuron in self.hidden_layer2:
        #     out = neuron.get_output_wos(hidden_outputs)
        #     hidden_outputs2.append(out)

        output = []
        for neuron in self.output_layer:
            out = neuron.get_output(hidden_outputs)
            output.append(out)

        return output


class Neuron:
    def __init__(self):
        self.weight = uniform(-4,4)
        self.bias = uniform(-1,1)

    def get_intermediate_output(self, input):
        return (input * self.weight) + self.bias

    def get_output_wos(self, input):
        sum = 0.0
        for i in input:
            sum += i * self.weight
        sum += self.bias 

        return sum

    def get_output(self, input):
        sum = 0.0
        for i in input:
            sum += i * self.weight
        sum += self.bias 

        return self.__sigmoid(sum)
        
        
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))
