import numpy as np

# you must use python 3.6, 3.7, 3.8, 3.9 for sourcedefender
import sourcedefender
from HomeworkFramework import Function
from cmaes import CMA

class RS_optimizer(Function):  # need to inherit this class "Function"
    def __init__(self, target_func):
        super().__init__(target_func)  # must have this init to work normally

        self.dimension = self.f.dimension(target_func)
        self.upper = self.f.upper(target_func)
        self.lower = self.f.lower(target_func)
        print('upper:', self.upper, 'lower: ', self.lower)
        self.target_func = target_func

        self.eval_times = 0
        self.optimal_value = float("inf")
        self.optimal_solution = np.empty(self.dimension)

    def get_optimal(self):
        return self.optimal_solution, self.optimal_value
    def eval(self, solution):
        return self.f.evaluate(self.target_func, solution)

        print('upper: %d, lower: %d, dim: %d' % (self.upper, self.lower, self.dimension))
    def run(self, FES):  # main part for your implementation
        population_size = int(4+(3*np.log(self.dimension))); bounds = np.array([[self.lower, self.upper]]*self.dimension)

        optimizer = CMA(mean=np.zeros(self.dimension), sigma=0.5, bounds=bounds, population_size=population_size)
        while self.eval_times < FES:
            print('=====================FE=====================')
            # use other Function work because CMA need ask many times
            function = Function(self.target_func)
            solutions = []
            for generation in range(optimizer.population_size):
                solution = optimizer.ask()
                value = self.f.evaluate(func_num, solution)
                #print('generate: ', solution, 'loss: ', value)
                solutions.append((solution, value))
                self.eval_times += 1

                if value == "ReachFunctionLimit":
                    print("ReachFunctionLimit")
                    break
                if float(value) < self.optimal_value:
                    self.optimal_solution[:] = solution
                    self.optimal_value = float(value)
            optimizer.tell(solutions)

            print('eval times: ', self.eval_times)
            print("optimal: {}\n".format(self.get_optimal()[1]))


if __name__ == '__main__':
    func_num = 1
    fes = 0
    op = RS_optimizer(func_num)
    # op.test()
    op.run(1000)
    # function1: 1000, function2: 1500, function3: 2000, function4: 2500
    '''while func_num < 5:
        if func_num == 1:
            fes = 1000
        elif func_num == 2:
            fes = 1500
        elif func_num == 3:
            fes = 2000
        else:
            fes = 2500

        # you should implement your optimizer
        op = RS_optimizer(func_num)
        op.test()
        #op.run(fes)

        best_input, best_value = op.get_optimal()
        print('best', best_input, best_value)

        # change the name of this file to your student_ID and it will output properlly
        with open("{}_function{}.txt".format(__file__.split('_')[0], func_num), 'w+') as f:
            for i in range(op.dimension):
                f.write("{}\n".format(best_input[i]))
            f.write("{}\n".format(best_value))
        func_num += 1'''

