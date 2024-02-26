#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    printf("%s\n", text);
    int num_letters = count_letters(text);
    int num_words = count_words(text);
    int num_sentences = count_sentences(text);
    float L = (float) num_letters / num_words * 100;
    float S = (float) num_sentences / num_words * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = (int) round(index);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    int n = 0;
    for (int i = 0; i < strlen(text); i++) // i用于遍历字符串，而n用于遍历文本中的字母。
    {
        if (isalpha(text[i]))
        {
            n++;
        }
    }
    return n;
}

int count_words(string text)
{
    int n = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            n++;
        }
    }
    return n + 1;
}

int count_sentences(string text)
{
    int n = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            n++;
        }
    }
    return n;
}