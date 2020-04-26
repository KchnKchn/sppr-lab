import abc

class Method():
    def __init__(self):
        self.__left_bound = None
        self.__right_bound = None
        self.__f = None
        self.__r = None
        self.__eps = None
        self.__max_iter = None

    def set_r(self, r: float):
        self.__r = r

    def set_eps(self, eps: float):
        if eps <= 0:
            raise ValueError("Некорректное значение допустимой точности")
        self.__eps = eps

    def set_max_iter(self, max_iter: int):
        if max_iter <= 0:
            raise ValueError("Некорректное значение максимального числа итераций")
        self.__max_iter = max_iter

    def set_bounds(self, left_bound: float, right_bount: float):
        if left_bound >= right_bount:
            raise ValueError("Некорректный ввод границ поиска")
        self.__left_bound = left_bound
        self.__right_bound = right_bount

    def set_f(self, f):
        self.__f = f

    def calculate(self):
        curr_iter = 0
        x = [self.__left_bound, self.__right_bound]
        z = [self.__calculate_f(self.__left_bound), self.__calculate_f(self.__right_bound)]
        while True:
            m = self.__calculate_m(x, z)
            max_pair, R = self.__calculate_max_metric(m, x, z)
            if self.__is_not_max_iter(curr_iter) and self.__accuracy_not_achieved(x[max_pair-1], x[max_pair]):
                x_next = self._calculate_next_x(m, x[max_pair-1], z[max_pair-1], x[max_pair], z[max_pair])
                x.append(x_next)
                x.sort()
                z = [self.__calculate_f(elem) for elem in x]
                curr_iter += 1
            else:
                break
        min_index = z.index(min(z))
        return x, z, min_index, curr_iter

    @abc.abstractmethod
    def _calculate_metric(self, m: float, x1: float, z1: float, x2: float, z2: float):
        pass

    def __calculate_max_metric(self, m: float, x: list, z: list):
        max_pair = 1
        R_max = self._calculate_metric(m, x[max_pair-1], z[max_pair-1], x[max_pair], z[max_pair])
        t = len(x)
        for i in range(1, t):
            R_curr = self._calculate_metric(m, x[i-1], z[i-1], x[i], z[i])
            if R_max < R_curr:
                R_max = R_curr
                max_pair = i
        return max_pair, R_max

    @abc.abstractmethod
    def _calculate_next_x(self, m: float, x1: float, z1: float, x2: float, z2: float):
        pass

    def __calculate_M(self, x: list, z: list):
        t = len(x)
        M = 0.0
        for i in range(1, t):
            M = max(M, abs(z[i] - z[i-1]) / (x[i] - x[i-1]))
        return M
            
    def __calculate_m(self, x: list, z: list):
        M = self.__calculate_M(x, z)
        m = 1
        if M > 0:
            m = self.__r * M
        return m

    def __calculate_f(self, x: float):
        return self.__f(x)

    def __accuracy_not_achieved(self, x_prev: float, x_curr: float):
        return (abs(x_prev - x_curr) > self.__eps)

    def __is_not_max_iter(self, curr_iter: int):
        return curr_iter != self.__max_iter

class StronginMethod(Method):
    def _calculate_metric(self, m: float, x1: float, z1: float, x2: float, z2: float):
        return m * (x2 - x1) + (z2 - z1) ** 2 / (m * (x2 - x1)) - 2 * (z1 + z2)

    def _calculate_next_x(self, m: float, x1: float, z1: float, x2: float, z2: float):
        return 0.5 * (x1 + x2) - (z2 - z1) / (2 * m)

class PiyavskyMethod(Method):
    def _calculate_metric(self, m: float, x1: float, z1: float, x2: float, z2: float):
        return 0.5 * m * (x2 - x1) - (z1 + z2) / 2

    def _calculate_next_x(self, m: float, x1: float, z1: float, x2: float, z2: float):
        return 0.5 * (x1 + x2) - (z2 - z1) / (2 * m)

class BruteForceMethod(Method):
    def _calculate_metric(self, m: float, x1: float, z1: float, x2: float, z2: float):
        return x2 - x1

    def _calculate_next_x(self, m: float, x1: float, z1: float, x2: float, z2: float):
        return 0.5 * (x1 + x2)
    