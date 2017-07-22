import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

def prob_1():
    x = np.linspace(0, 10, 1000)
    
    plt.plot(x, x + 1, linestyle='-')
    plt.plot(x, np.sin(x), linestyle='--')
    plt.plot(x, -x, linestyle=':')
    
    plt.show()

def prob_2():
    x = np.random.uniform(0, 10, size=10)
    y = np.random.uniform(0, 10, size=10)
    
    rng = np.random.RandomState()
    colors = rng.rand(10); print(colors)
    sizes = 1000 * rng.rand(10)
    
    plt.scatter(x, y, c=colors, s=sizes)

def prob_3():
    plt.subplot(2, 1, 1)
    x = np.linspace(0, 10, 1000)
    
    plt.plot(x, x + 1, linestyle='-')
    plt.plot(x, np.sin(x), linestyle='--')
    plt.plot(x, -x, linestyle=':')
    
    plt.subplot(2, 1, 2)
    x = np.random.uniform(0, 10, size=10)
    y = np.random.uniform(0, 10, size=10)
    
    rng = np.random.RandomState()
    colors = rng.rand(10); print(colors)
    sizes = 1000 * rng.rand(10)
    
    plt.scatter(x, y, c=colors, s=sizes)
    
    plt.show()

def main():
    #prob_1()
    #prob_2()
    prob_3()
    
main()