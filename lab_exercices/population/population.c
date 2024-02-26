#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int a;
    do
    {
        a = get_int("start size: ");
    }
    while (a < 9);

    // TODO: Prompt for end size
    int b;
    do
    {
        b = get_int("end size: ");
    }
    while (b < a);

    // TODO: Calculate number of years until we reach threshold
    int years = 0;
    while (b > a)
    {
        a = a + (a / 3) - (a / 4);
        years++;
    }

    // TODO: Print number of years
    printf("Years: %i", years);
}

// n = n + ( n / 3 ) - ( n / 4 )
// printf ("Years : %1\n",n)