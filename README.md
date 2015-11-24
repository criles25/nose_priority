# nose_priority
Nose_priority prioritizes nose tests based on past failures and execution history. It is based on the proposed technique in [Elbaum et al] (http://cse.unl.edu/~elbaum/pre-prints/fse2014-prePrint.pdf).

Nose_priority modifies test files by adding/changing the priority attribute of tests. Tests that have failed recently are assigned a priority of `test.priority=1`. Also, tests that haven't been executed recently are assigned a priority of `test.priority=1`. All other tests are assigned a priority of `test.priority=2`.

Nose_priority is intended to be used in the continuous integration setting (but does not have to be). The expected sequence of tasks when using nose_priority is:

1. Write tests using node.
2. Run nose_priority with `prioritize`.
3. Do `nosetests -a priority=1 ; nosetests -a priority=2`.
4. Feed log of test execution into nose_priority.
5. Repeat.

Nose_priority currently requires previous execution histories be fed into it. Future updates will add support for automatic storage of previous executions. Once the log of a previous nosetests execution is manually fed, the results of test execution are permanently stored.

Nose_priority is still a prototype, and may eventually be implemented as a plugin for nose.    


*to install*

	pip install nose_priority


*to run*

	cd project_root
	prioritize


*to feed log*

Nose_priority requires the previous execution results of `nosetests` in order to update the priorities. Additionally, nose_priority needs to know the date and time of when the test execution occurred. Thus, the log file must include the lines

	date
	Tue Nov 24 15:58:49 EST 2015

appended to the end of the `nosetests` output. A typical workflow when running nosetests might be

	nosetests -a priority=1 >> log.txt 2>&1
	nosetests -a priority=2 >> log.txt 2>&1
	echo date >> log.txt
	date >> log.txt

Once the log file is produced, it can be fed

	prioritize -np --log log.txt

