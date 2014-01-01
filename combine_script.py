#!/usr/bin/env python
import ssw_combine as ssc
# import os

# #######
# Instructions:
#  - put list of surface source files in the list "filelist"
#  - put final output name in the variable "finalfilename"
#  - run the script, e.g.    ./combine_script.py
    
filelist = ["wssr",
            "wsss",
            "wsst",
            "wssu",
            "wssv"
            ]

finalfilename = "ssw_finalfile"

ssc.combine_multiple_ss_files(filelist,finalfilename)
