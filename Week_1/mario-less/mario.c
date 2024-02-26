#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height > 8 || height < 1);

    for (int i = 1; i <= height; i++)
    {
        for (int space = 1; space <= height - i; space++)
        {
            printf(" ");
        }

        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}