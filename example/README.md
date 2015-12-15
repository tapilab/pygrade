Here is a simple example. Assume that `assignment1.py` is a student's submission, and that `test_assignment1.py` contains unit tests for that submission.

Running
```sh
pygrade clone -s students.tsv -w students
```
will clone all repositories listed in `students.tsv` into the local directory `students`.

To grade the assignments, run:
```sh
pygrade grade -s students.tsv -t test_assignment1.py -w students
```
This will run the tests in `test_assignment1.py` against all student submissions and stores the output in `grades.json`. Please see `test_assignment1.py` for the "@" syntax, which specifies the file to run, as well as the point assignments for each test.

Finally, running
```sh
pygrade push -g grades.json
```
will generate a `grade.txt` file for each student and push it to their repository (this will only work if you have permission to write to this repo).

Note that `students.tsv` lists the github repository used to fetch the student's assignment1.py. Here, we use the `pygrade` repository.

You can shorten these commands using the default for filenames and directories (`students.tsv`, `students/`, `grades.json`):

```sh
pygrade clone
pygrade grade -t test_Assignment1.py
pygrade push
```
