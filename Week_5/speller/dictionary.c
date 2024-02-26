// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;
int countWord = 0;

// Hash table
node *table[N] = {NULL};

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hashnumber = hash(word);
    //creat cursor variable
    node *cursor = table[hashnumber];
    //loop until the end of the linked list
    while(cursor != NULL)
    {
        //check the words are the same
        if(strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        //or, move cursor to the next node
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //  Improve this hash function
    if(isalpha(word[0]))
    {
        return toupper(word[0]) - 'A';
    }
    return 0;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open the dictionary file and check it if returns null value
    FILE *DictionaryFile = fopen(dictionary, "r");

    if(DictionaryFile == NULL)
    {
        return false;
    }

    //read strings from file one at a time
    char str[LENGTH +1];
    while(fscanf(DictionaryFile, "%s", str) != EOF)
    {
        //Creat a new node for each word; use malloc (check if NULL)
        node *tem = malloc(sizeof(node));

        if(tem == NULL)
        {
            return false;
        }
        //copy word into node using strcpy
        strcpy(tem->word, str);

        //use the hush function
        int hashnum = hash(str);
        tem->next = table[hashnum];
        //point the header to temp
        table[hashnum] = tem;
        countWord += 1;
    }
    //close the file
    fclose(DictionaryFile);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return countWord;
}

void freenode(node *n)
{
    if(n->next != NULL)
    {
        freenode(n->next);
    }
    free(n);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for(int i = 0; i < N; i++)
    {
        if(table[i] != NULL)
        {
            freenode(table[i]);
        }
    }
    return true;
}
