#include <stdio.h>
#include <cs50.h>

typedef struct
{
    string name;
    int votes;
} candidate;

candidate get_candidate(string prompt);

int main(void)
{
    candidate candidate_array[3];
    for(int i = 0; i < 3; i++)
    {
        candidate_array[i] = get_candidate("Enter a canidate: ");
    }

}

candidate get_candidate(string prompt)
{
    printf("%s\n", prompt);

    candidate c;
    c.name = get_string("Enter a name: ");
    c.votes = get_int("Enter a number of vote: ");
    return c;
}