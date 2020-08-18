#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

//Reads an audio file and plays it

#define MAX_WAV_SIZE 16184

typedef struct wav_struct {
    char magic[4];
    int32_t size; //The size of the entire file, minus 8 bytes
    char fmt[4];
}
wav_header;

typedef struct wav_body_struct {
    char magic[4];
    int32_t size;
    int16_t audio_format;
    int16_t channel_num;
    int32_t sample_size;
    int32_t byte_rate;
    int16_t block_align;
    int16_t bits_per_sample;
}
wav_body;

void play_wav(char * data) {
    // Decode the WAV and play it... but i don't want to do that
    // Probably some ALSA stuff here
    printf("Playing WAV!\n");
}

int main(int argc, char * argv[]) {
    wav_header header;
    wav_body body;

    //There's plenty of space on the stack...
    char data[MAX_WAV_SIZE];
    if (argc < 2) {
        fprintf(stderr, "Usage: ./wav input.wav\n");
        goto error;
    }

    FILE* file = fopen(argv[1], "r");
    if (file == 0) {
        fprintf(stderr, "Unable to open file\n");
        goto error;
    }

    // Read header of wav file
    fread(&header, 1, sizeof(wav_header), file);

    if (memcmp(header.magic, "RIFF", 4) == 0) {
        fprintf(stderr, "%s is a WAV file\n", argv[1]);
    } else {
        fprintf(stderr, "%s: Unknown format\n", argv[1]);
        goto error;
    }

    // Now read the body
    fread(&body, 1, sizeof(body), file);
    if (memcmp(body.magic, "fmt", 3) != 0) {
        fprintf(stderr, "%s: Unknown WAV format\n", argv[1]);
        goto error;
    } else {
        fprintf(stderr, "%s: Channels : %i\n", argv[1], body.channel_num);
        fprintf(stderr, "%s: Sample Size: %i\n", argv[1], body.sample_size);
    }

    // Max sure header.size is not bigger than our buffer size
    if (header.size + 8 > MAX_WAV_SIZE) {
        fprintf(stderr, "%s: File too large\n", argv[1]);
        goto error;
    }

    rewind(file);
    fread(data, 1, header.size + 8, file);
    play_wav(data);
    return 0;

error:
    fclose(file);
    return 1;
}
