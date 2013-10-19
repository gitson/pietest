#include "a.h"
#include <stdio.h>

int main(int argc, char *argv[])
{
	int a = 0, b = 11, c;

	// TEST: test1
	// CALLS: f(b-8,2)3;g(2)0;u(a+3)
	// CHECK: a == 0;b == a + 3;b
	a = f(3,2); 
	// END

	b = 6;

	// TEST: test2
	// CALLS: f(b-2,2)3;g(2)0;u(2)
	// CHECK: a == 0;b == a + 3;b
	a = f(4,a - 1); 
	// END

	// TEST: test3
	// CALLS: *;g(_)0;*
	b = 10;
	// CHECK: b - 5 == 5
	b = 0;
	// CHECK: a == 0;b == a + 3;!b
	b = 1;
	// CHECK: !b	
	a = f(4,2); 
	// END

	// TEST: test4
	// CALLS: *;f(3,_)_;*
	// CHECK: a == 3;b == 6 
	a = f(3,2); 
	// CHECK: b == a + 3
	// END

	a = a + b;
	a = f(4, 2);

	return 0;
}

