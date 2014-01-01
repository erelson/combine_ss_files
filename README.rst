Notes 1-1-2014
--------------
Files written in Nov 2011, using binaryreader.py and mcnp.py from the PyNE project.

Instead of creating a "put_track" method, I naively was calling the internal _put_fortran_record() method.


Old Readme contents
-------------------
To setup this script, first open combine_script.py and see instructions at the top.
To run this script, Python 2.6 is required.  We have this in the CNERG space, so run

/filespace/groups/cnerg/opt/Python-2.6.6/bin/python2.6 combine_script.py

There are four files that are needed, if you copy these to another location:
binaryreader.py
mcnp.py
ssw_combine.py
combine_script.py
