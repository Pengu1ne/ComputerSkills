'''
In this exercise, I try out a recursive function. I choose Fibonacci 
number series to try it out.

To be added:
    -- if the sequence starts from the middle/random number, two starting
       numbers have to be re-defined
'''

'''
I found it easier to describe F_0 and F_1 as a starting list. From here,
it was easy to define the rest of the numbers.
'''

fib = [0,1]

def fibonacci(start, iterations):
    if iterations == 1:
        print(fib)
        return fib
    else:
        iterations -=1
        start = fib[-1] + fib[-2]
        fib.append(start)
        return fibonacci(start, iterations)

fibonacci(1,20)
