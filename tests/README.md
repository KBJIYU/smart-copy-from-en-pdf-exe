# Unit Test

![smartcopy-logo](/logo.png)

## Requirements
```bash
python3 -m pip install pytest
```

## Start Testing
we run testing before every release to make sure everything works right:

1. go to root directory (smart-copy-from-en-pdf-exe/)
2. simply enter `python3 -m pytest` to the command line

## Fixtures (Datasets)
Stored in `/tests/data`, inputs are `*.txt` and the corresponding expected outputs are `*_answer.txt`

1. **thesis_basic**: to test if the program splits basic delimiters
2. **thesis**: to test if the program splits the citations
3. **novel**: to test if the program splits `."`
4. **latex**: to test if the program splits special latex symbols 
