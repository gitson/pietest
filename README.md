pietest
=======

Python-based C tester

Usage:
Instrument the function you want to test with comments like this:

```
// TEST: test1
// CALLS: f(b-8,2)3;g(2)0;u(a+3)
// CHECK: a == 0;b == a + 3;b
a = f(3, 2)
// END

```
Run: 

```
make

```
