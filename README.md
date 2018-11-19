# digitakt-song-mode
Song mode prototype for Elektron Digitakt.

Currently pattern change messages are sent on channel 0.

## Example sequence (JSON file)
```
{
    "tempo": 134,
    "sequence": [
        {
            "pattern": 9,
            "bank": "A",
            "length": 4,
            "repetitions": 2
        },
        {
            "pattern": 10,
            "bank": "A",
            "length": 4,
            "repetitions": 2
        }
    ]
}
```
