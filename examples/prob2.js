let fib1 = 1;
let fib2 = 2;
let sum = 0;
let fib3 = 0;
while (fib2 < 4000000) {
    sum = sum + fib2;
    fib3 = fib1 + fib2;
    fib1 = fib2 + fib3;
    fib2 = fib1 + fib3;
}
print(sum);