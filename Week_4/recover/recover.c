#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK_SIZE = 512;

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *raw_file = fopen(argv[1], "r");
    if (raw_file == NULL)
    {
        printf("Can not open");
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];
    FILE *jpg = NULL;
    int jpg_count = 0;

    while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
             if (jpg != NULL)
            {
                fclose(jpg);
            }

            char filename[8];
            sprintf(filename, "%03i.jpg", jpg_count);
            jpg = fopen(filename, "w");
            jpg_count++;

            if (jpg == NULL)
            {
                return 1;
            }
        }

        if (jpg != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, jpg);
        }

    }

    if (jpg != NULL)
    {
        fclose(jpg);
    }

    fclose(raw_file);
    return 0;
}