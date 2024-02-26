#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string name = get_string("what is your name? ");

    int n = 0;
    while (name[n] != '\0')
    {
        n++;
    }
    printf("%i\n", n);
}

// = int main(void)
{
    string name = get_string("what is your name? ");
    int n = strlen(name;)
    printf("%i\n", n)
}