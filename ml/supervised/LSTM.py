import numpy as np
from NonLinearityFunctions import sigmoid, tanh


def addition(x, y):
    for i in range(len(x)):
        x[i] += y[i]


class LSTMCell:
    def __init__(self,input_size, output_size, input_function=tanh, output_function=tanh):
        self.input_size = input_size
        self.output_size = output_size
        self.U_input = np.random.rand(input_size, output_size)-0.5
        self.V_input = np.random.rand(output_size, output_size)-0.5
        self.B_input = np.random.rand(output_size)-0.5
        self.U_input_gate = np.random.rand(input_size, output_size)-0.5
        self.V_input_gate = np.random.rand(output_size, output_size) - 0.5
        self.B_input_gate = np.random.rand(output_size) - 0.5
        self.U_forget_gate = np.random.rand(input_size, output_size) - 0.5
        self.V_forget_gate = np.random.rand(output_size, output_size) - 0.5
        self.B_forget_gate = np.random.rand(output_size) - 0.5
        self.U_output_gate = np.random.rand(input_size, output_size) - 0.5
        self.V_output_gate = np.random.rand(output_size, output_size) - 0.5
        self.B_output_gate = np.random.rand(output_size) - 0.5
        self.input_function = input_function
        self.output_function = output_function
        self.U_input_derivative = None
        self.V_input_derivative = None
        self.B_input_derivative = None
        self.U_input_gate_derivative = None
        self.V_input_gate_derivative = None
        self.B_input_gate_derivative = None
        self.U_forget_gate_derivative = None
        self.V_forget_gate_derivative = None
        self.B_forget_gate_derivative = None
        self.U_output_gate_derivative = None
        self.V_output_gate_derivative = None
        self.B_output_gate_derivative = None
        self.ret_deltas = []

    def hypot(self, inp):
        _, hypots, _, _, _, _, _ = self(inp)
        return hypots[1:]

    def __call__(self, inp):
        states = [np.zeros((1, self.output_size))]
        hypots = [np.zeros((1, self.output_size))]
        input_gates = []
        input_units = []
        forget_gates = []
        output_gates = []
        state_function = []
        for i in inp:
            prev_state = states[-1]
            prev_hypot = hypots[-1]
            i_unit = self.input_function(self.B_input +
                                         prev_hypot.dot(self.V_input) +
                                         i.dot(self.U_input))
            input_units.append(i_unit)
            i_gate = sigmoid(self.B_input_gate + prev_hypot.dot(self.V_input_gate) + i.dot(self.U_input_gate))
            input_gates.append(i_gate)
            f_gate = sigmoid(self.B_forget_gate + prev_hypot.dot(self.V_forget_gate) + i.dot(self.U_forget_gate))
            forget_gates.append(f_gate)
            o_gate = sigmoid(self.B_output_gate + prev_hypot.dot(self.V_output_gate) + i.dot(self.U_output_gate))
            output_gates.append(o_gate)
            state = prev_state*f_gate + i_unit*i_gate
            stf = self.output_function(state)
            state_function.append(stf)
            hypot = stf*o_gate
            states.append(state)
            hypots.append(hypot)
        return states, hypots, state_function, input_units, input_gates, forget_gates, output_gates

    def initialize_gradient(self):
        self.U_input_derivative = np.zeros_like(self.U_input)
        self.V_input_derivative = np.zeros_like(self.V_input)
        self.B_input_derivative = np.zeros_like(self.B_input)
        self.U_input_gate_derivative = np.zeros_like(self.U_input_gate)
        self.V_input_gate_derivative = np.zeros_like(self.V_input_gate)
        self.B_input_gate_derivative = np.zeros_like(self.B_input_gate)
        self.U_forget_gate_derivative = np.zeros_like(self.U_forget_gate)
        self.V_forget_gate_derivative = np.zeros_like(self.V_forget_gate)
        self.B_forget_gate_derivative = np.zeros_like(self.B_forget_gate)
        self.U_output_gate_derivative = np.zeros_like(self.U_output_gate)
        self.V_output_gate_derivative = np.zeros_like(self.V_output_gate)
        self.B_output_gate_derivative = np.zeros_like(self.B_output_gate)

    def unfold(self, i, inp, states, hypots, state_functions, delta, input_units, input_gates, forget_gates, output_gates, step=5):
        if step <= 0:
            return
        delta_output_gate = delta * state_functions[i] * sigmoid(output_gates[i], True)

        self.U_output_gate_derivative += inp[i].T.dot(delta_output_gate)
        self.V_output_gate_derivative += hypots[i].T.dot(delta_output_gate)
        self.B_output_gate_derivative += delta_output_gate.reshape(self.B_output_gate.shape)

        # self.unfold(i - 1, inp, states, hypots, state_functions,
        #             delta_output_gate.dot(self.V_output_gate.T),
        #             input_units, input_gates, forget_gates, output_gates, step=min(i, step - 1))

        delta_state = delta * output_gates[i] * self.output_function(states[i + 1], True)

        for j in range(i, max(i - step, -1), -1):
            delta_forget_gate = delta_state * states[j] * sigmoid(forget_gates[j])

            self.U_forget_gate_derivative += inp[j].T.dot(delta_forget_gate)
            self.V_forget_gate_derivative += hypots[j].T.dot(delta_forget_gate)
            self.B_forget_gate_derivative += delta_forget_gate.reshape(self.B_forget_gate.shape)

            #self.unfold(j - 1, inp, states, hypots, state_functions,
            #            delta_forget_gate.dot(self.V_forget_gate.T),
            #            input_units, input_gates, forget_gates, output_gates,
            #            step=min(step - i + j - 1, j))

            delta_input_gate = delta_state * input_units[j] * sigmoid(input_gates[j], True)

            self.U_input_gate_derivative += inp[j].T.dot(delta_input_gate)
            self.V_input_gate_derivative += hypots[j].T.dot(delta_input_gate)
            self.B_input_gate_derivative += delta_input_gate.reshape(self.B_input_gate.shape)

            #self.unfold(j - 1, inp, states, hypots, state_functions,
            #            delta_input_gate.dot(self.V_input_gate.T),
            #            input_units, input_gates, forget_gates, output_gates,
            #            step=min(step - i + j - 1, j))

            delta_input = delta_state * input_gates[j] * self.input_function(input_units[j], True)

            self.U_input_derivative += inp[j].T.dot(delta_input)
            self.V_input_derivative += hypots[j].T.dot(delta_input)
            self.B_input_derivative += delta_input.reshape(self.B_input.shape)

            #self.unfold(j - 1, inp, states, hypots, state_functions,
            #            delta_input.dot(self.V_input.T),
            #            input_units, input_gates, forget_gates, output_gates,
            #            step=min(step - i + j - 1, j))

            delta_state *= forget_gates[j]

    def get_gradient(self, inp, deltas, step=5):
        self.ret_deltas = []
        states, hypots, state_functions, input_units, input_gates, forget_gates, output_gates = self(inp)
        for i in range(len(deltas)):
            self.unfold(i=i, inp=inp, states=states, hypots=hypots, state_functions=state_functions, delta=deltas[i], input_units=input_units, input_gates=input_gates, forget_gates=forget_gates, output_gates=output_gates, step=step)
        return self.ret_deltas

    def get_gradient_by_output(self, inp, states, hypots, state_functions, input_units, input_gates, forget_gates, output_gates, deltas, step=5):
        self.ret_deltas = []
        for i in range(len(deltas)):
            self.unfold(i=i, inp=inp, states=states, hypots=hypots, state_functions=state_functions, delta=deltas[i], input_units=input_units, input_gates=input_gates, forget_gates=forget_gates, output_gates=output_gates, step=step)
        return self.ret_deltas

    def iteration(self, inp, deltas, alpha=0.001, step=5):
        pass


class LSTMNetwork:
    def __init__(self, *layers):
        assert len(layers) > 0
        self.layers = list(layers)

    def __call__(self, inp):
        inputs = [inp]
        states, hypots, state_functions, input_units, input_gates, forget_gates, output_gates = [], [], [], [], [], [], []
        for i in range(len(self.layers)):
            state, hypot, state_function, input_unit, input_gate, forget_gate, output_gate = self.layers[i](inp)
            inp = hypot[1:]
            inputs.append(inp)
            states.append(state)
            hypots.append(hypot)
            state_functions.append(state_function)
            input_units.append(input_unit)
            input_gates.append(input_gate)
            forget_gates.append(forget_gate)
            output_gates.append(output_gate)
        return inputs, states, hypots, state_functions, input_units, input_gates, forget_gates, output_gates

    def hypot(self, inp):
        return self(inp)[0][-1]

    def iteration(self, inp, labels, alpha=0.001, step=5):
        delta = None
        for cell in self.layers:
            cell.initialize_gradient()
        for i in range(len(inp)):
            inputs, states, hypots, state_functions, input_units, input_gates, forget_gates, output_gates = self(inp[i])
            label = np.array(labels[i])
            delta = np.array(inputs[-1]).reshape(label.shape) - label
            for j in range(len(self.layers)-1,-1,-1):
                delta = self.layers[j].get_gradient_by_output(deltas=delta, inp=inputs[j], states=states[j],
                        hypots=hypots[j], state_functions=state_functions[j], input_gates=input_gates[j], input_units=input_units[j],
                        forget_gates=forget_gates[j], output_gates=output_gates[j], step=step)

        for rnn in self.layers:
            rnn.U_input -= alpha * rnn.U_input_derivative
            rnn.V_input -= alpha * rnn.V_input_derivative
            rnn.B_input -= alpha * rnn.B_input_derivative
            rnn.U_output_gate -= alpha * rnn.U_input_gate_derivative
            rnn.V_input_gate -= alpha * rnn.V_input_gate_derivative
            rnn.B_input_gate -= alpha * rnn.B_input_gate_derivative
            rnn.U_forget_gate -= alpha * rnn.U_forget_gate_derivative
            rnn.V_forget_gate -= alpha * rnn.V_forget_gate_derivative
            rnn.B_forget_gate -= alpha * rnn.B_forget_gate_derivative
            rnn.U_output_gate -= alpha * rnn.U_output_gate_derivative
            rnn.V_output_gate -= alpha * rnn.V_output_gate_derivative
            rnn.B_output_gate -= alpha * rnn.B_output_gate_derivative

        return delta

    def cost(self, x, y):
        k = 0
        for j in range(len(x)):
            yt = np.array(y[j])
            errors = np.array(self.hypot(x[j])).reshape(yt.shape)
            errors -= yt
            k += np.sum(errors * errors)
        return k






def get_random_x():
    import random
    length = random.randint(20, 30)
    a = []
    b = []
    carry = 0
    for i in range(length):
        tmp = np.zeros((1, 2))
        v1 = random.randint(0, 1)
        v2 = random.randint(0, 1)
        tmp[0, 0] = v1
        tmp[0, 1] = v2
        a.append(tmp)
        b.append(np.array([[v1 ^ v2 ^ carry]]))
        carry = (v1 & v2) | (v1 & carry) | (v2 & carry)
    return a, b


def create_sequance():
    import random
    jump = random.choice([-1,1])
    x,y = [],[]
    index = random.randint(0,4)
    for i in range(20):
        x.append(np.zeros((1,5))-1.0)
        x[-1][0,index] = 1.0
        index += jump
        if index == 5:
            index = 0
        if index == -1:
            index = 4
        y.append(np.zeros((1,5))-1.0)
        y[-1][0,index] = 1.0
    return x,y
