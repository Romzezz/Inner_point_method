#!/usr/bin/env python
# coding: utf-8

# In[5]:


from scipy.optimize import linprog
import re
import sympy


# In[6]:


def extract_coeffs(expr, symbols):
    return [float(expr.coeff(symbol)) for symbol in symbols]


# In[9]:


def solve():
    method = int(input(
        """
        Выберите метод решения:
        1 - Метод Ньютона
        2 - Метод логарифмических барьеров
        3 - прямо-двойственный метод внутренней точки
        Метод: 
        """
    ))
    func = input('Введите функцию в аналитическом виде: ')
    func = sympy.sympify(func)
    varnames = list(func.free_symbols)
    obj = extract_coeffs(func, varnames)
    constraint = input('Введите хотя-бы одно ограничение (оставьте пустым для остановки):')
    lhs_ineq, rhs_ineq = [], []
    lhs_eq, rhs_eq = [], []
    while constraint:
        sign = re.findall(r'(?:<=|>=|=|<|>)', constraint)[0]
        left, right = constraint.split(sign)
        left = sympy.sympify(left)
        right = float(right)
        coeffs = dict()
        for var in varnames:
            coeffs[var] = left.coeff(var)
        if sign == '=':
            lhs_eq.append(list(coeffs.values()))
            rhs_eq.append([right])
        else:
            if sign in ('>=', '>'):
                right *= -1
                for var in coeffs:
                    coeffs[var] = -coeffs[var]
            lhs_ineq.append(list(coeffs.values()))
            rhs_ineq.append(right)
        

        constraint = input('Введите ограничение (оставьте пустым для остановки):')
    initial_point = list(map(float, input('Ввдите начальную точку: ').split()))
    lhs_ineq = lhs_ineq or None
    rhs_ineq = rhs_ineq or None
    lhs_eq = lhs_eq or None
    rhs_eq = rhs_eq or None
    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
                  A_eq=lhs_eq, b_eq=rhs_eq, x0=initial_point,
                  method="revised simplex")
    return opt.x


# In[ ]:




