Here is a simple example. Assume that `assignment1.py` is a student's submission, and that `test_assignment1.py` contains unit tests for that submission.

Running
`pygrade grade -s students.tsv -t test_assignment1.py`

will generate `grades.json`.

Note that `students.tsv` lists the github repository used to fetch the student's assignment1.py. Here, we use the `pygrade` repository.
