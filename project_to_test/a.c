#include "a.h"

int a = 0;

void u(uint8 b)
{
	a += b;
	a++;
	return;	
}

char g(uint8 b)
{
	u(b);
	return !b;
}

int f(int a, char b)
{
	return a + 5 * g(b);
}

void h(int c)
{
	f(c,2);
}
