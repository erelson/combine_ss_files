#!/usr/bin/env python

import mcnp
import binaryreader as br
import math

# Script includes method XXXXXXXXX to combine MCNP surface source entries
#  with a combined header.
    
def combine_header_records(myssr1, myssr2):

    mykod    = "{0:<8}".format( myssr1.kod         )
    myver    = "{0:<5}".format( myssr1.ver         )
    myloddat = "{0:<8}".format( myssr1.loddat      )
    myidtm   = "{0:<19}".format( myssr1.idtm )#"1"                )
    myprobid = "{0:<19}".format( myssr1.probid )#"1"                )
    myaid    = "{0:<80}".format( myssr1.aid         )
    rec = [mykod, myver, myloddat, myidtm, myprobid, myaid]
    newrecord = br._FortranRecord("".join(rec), len("".join(rec)))
    newrecord.put_int([myssr1.knod])
    
    return newrecord
       

def combine_table_1(myssr1, myssr2):
    
    newrecord = br._FortranRecord("", 0)
    
    newrecord.put_long( [-1* myssr1.np1 + 0*-1* myssr2.np1 ])
    newrecord.put_long( [myssr1.nrss + 0*myssr2.nrss])
    newrecord.put_int(  [myssr1.ncrd])
    newrecord.put_int(  [myssr1.njsw])
    newrecord.put_long( [myssr1.niss])
    
    return newrecord
    

def combine_table_2(myssr1, myssr2):
    
    newrecord = br._FortranRecord("", 0)
    newrecord.put_int( [myssr1.niwr ])
    newrecord.put_int( [myssr1.mipts])
    newrecord.put_int( [myssr1.kjaq ])
    newrecord.put_int(myssr1.table2extra) #, len(myssr1.table2extra))
    
    return newrecord
    
    
ssr = mcnp.SurfSrc("wssa","rb")
ssr2 = mcnp.SurfSrc("wssa","rb")

ssr.read_header()
ssr2.read_header()


if ssr.compare(ssr2):
    newheader = combine_header_records(ssr,ssr)
    newtable1 = combine_table_1(ssr,ssr2)
    newtable2 = combine_table_2(ssr,ssr2)

    recordlist = [newheader, newtable1, newtable2]
    
    newssr = mcnp.SurfSrc("rssa","wb") #newssr.w","wb")

    for rec in recordlist:
        newssr.put_fortran_record(rec)
        
    numparticles = ssr.np1

    # adding lines for surfaces
    for cnt, s in enumerate(ssr.surflist): # being suspicious here
        surf = br._FortranRecord("",0)
        
        
        surf.put_int(s.id)
        if ssr.kjaq == 1:
            surf.put_int(s.facetId) # don't add a 'dummy facet ID'
        #else, no byte should be in the record.
        surf.put_int(s.type)
        surf.put_int(s.numParams)
        surf.put_double(s.surfParams)
        
        newssr.put_fortran_record(surf)
        
        if cnt > ssr.njsw:
            print "Warning: njsw does not match number of entries in surfacelist!"
    
    #whatever the range from njsw to njsw+niwr is...
    for j in range(ssr.njsw,ssr.njsw+ssr.niwr):
        print 'minor problem here that needs mcnp.py additions'
    
    #summary info/table
    summaryrecord = br._FortranRecord("",0)
    summaryrecord.put_int(ssr.summaryTable)
    summaryrecord.put_int(ssr.summaryextra)
    newssr.put_fortran_record(summaryrecord)
    
    # write particle tracks
    for j in range(ssr.nrss):
        trackInfo = ssr.get_fortran_record()
        newssr.put_fortran_record(trackInfo)
    
    print "Finished writing to new surface source file 'rssa'"
    newssr.close
