void towers(int,char,char,char);

void towers(int n, char frompeg, char topeg, char auxpeg)
{
	if(n==1)
	{ 
		printf("\nMove disk 1 from peg %c to peg %c",frompeg,topeg);
		return;
	}
	towers(n-1,frompeg,auxpeg,topeg);
	printf("\nMove disk %d from peg %c to peg %c",n,frompeg,topeg);
	towers(n-1,auxpeg,topeg,frompeg);
}

int main(int argc, char *argv[])
{ 
	int n;
	printf("Enter the number of disks : ");
	scanf("%d",&n);
	printf("The Tower of Hanoi involves the moves :\n\n");
	towers(n,'A','C','B');
	return 0;
 }
