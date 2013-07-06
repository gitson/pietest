#include <stdio.h>
void towers(int, char, char, char);

void towers(int n, char frompeg, char topeg, char auxpeg)
{
  fprintf(stderr, "\n- call:\n    func: %s\n", "towers");
  fprintf(stderr, "    args: 0x%x 0x%x 0x%x 0x%x\n", n, frompeg, topeg, auxpeg);
  {
    if (n == 1)
    {
      printf("\nMove disk 1 from peg %c to peg %c", frompeg, topeg);
      fprintf(stderr, "\n- ret:\n    func: %s\n    val: None\n", "towers");
      return;
    }

    towers(n - 1, frompeg, auxpeg, topeg);
    printf("\nMove disk %d from peg %c to peg %c", n, frompeg, topeg);
    towers(n - 1, auxpeg, topeg, frompeg);
  }
  fprintf(stderr, "\n- ret:\n    func: %s\n    val: None\n", "towers");
  return;
}

int main(int argc, char *argv[])
{
  fprintf(stderr, "\n- call:\n    func: %s\n", "main");
  fprintf(stderr, "    args: 0x%x 0x%x\n", argc, argv);
  {
    int n;
    printf("Enter the number of disks : ");
    scanf("%d", &n);
    printf("The Tower of Hanoi involves the moves :\n\n");
    towers(n, 'A', 'C', 'B');
    {
      const int e5b9b38b = 0;
      fprintf(stderr, "\n- ret:\n    func: %s\n    val: 0x%x\n", "main", e5b9b38b);
      return e5b9b38b;
    }
  }
}

