#!/usr/bin/env python

import mcnp
import binaryreader as br
import math

# Script includes method combine_multiple_ss_files to combine MCNP surface source entries
#  with a combined header.

def combine_multiple_ss_files(ssrnames,newssrname):
    """Method reads headers from ssr1name and ssr2name binary files
    and checks if the headers are "similar".  If not, it returns false.
    
    """
    ssrfiles = []
    for ssrname in ssrnames:
        ssrfiles += [mcnp.SurfSrc(ssrname,"rb")]
    
    
    # read first surface source file's header
    ssrfiles[0].read_header()
    # then compare it with the headers from other files.
    for cnt, ssrfile in enumerate(ssrfiles[1:]):
        ssrfile.read_header()
        # we quit if there is a mismatch.
        if ssrfiles[0].compare(ssrfile) != True:
            print "Headers do not match for all files.\nFile #", cnt+2, \
                "does not match 1st file."
            return False
        
    # calculate list of offsets for offsetting each track's nps value.
    trackoffsets = map(lambda x: sum(map(lambda y: ssrfiles[y].np1, range(len(ssrfiles[:x])))), range(len(ssrfiles)))
    # following line is not used, but useful if we condense so that np1 == nrss
    #histoffsets = map(lambda x: sum(map(lambda y: ssrfiles[y].nrss, range(len(ssrfiles[:x])))), range(len(ssrfiles)))
    
    newssr = mcnp.SurfSrc(newssrname,"wb")
    
    #header
    newssr.kod         = ssrfiles[0].kod   
    newssr.ver         = ssrfiles[0].ver   
    newssr.loddat      = ssrfiles[0].loddat
    newssr.idtm        = ssrfiles[0].idtm  
    newssr.probid      = ssrfiles[0].probid
    newssr.aid         = ssrfiles[0].aid   
    newssr.knod        = ssrfiles[0].knod
    newssr.put_header()
    
    #table 1
    newssr.np1         = sum(map(lambda x: x.orignp1, ssrfiles))
    newssr.nrss        = sum(map(lambda x: x.nrss, ssrfiles))
    newssr.ncrd        = ssrfiles[0].ncrd
    newssr.njsw        = ssrfiles[0].njsw
    newssr.niss        = ssrfiles[0].niss
    newssr.put_table_1()
    
    #table 2
    newssr.niwr        = ssrfiles[0].niwr
    newssr.mipts       = ssrfiles[0].mipts
    newssr.kjaq        = ssrfiles[0].kjaq
    newssr.table2extra = ssrfiles[0].table2extra
    newssr.put_table_2()
    
    # newssr.
    # newssr.
    
    
    # for rec in recordlist:
        # newssr.put_fortran_record(rec)
        
    # numparticles = ssrfiles[0].np1

    # adding lines for surfaces
    for cnt, s in enumerate(ssrfiles[0].surflist): # being suspicious here
        surf = br._FortranRecord("",0)
        
        
        surf.put_int(s.id)
        if ssrfiles[0].kjaq == 1:
            surf.put_int(s.facetId) # don't add a 'dummy facet ID'
        #else, no byte should be in the record.
        
        surf.put_int(s.type)
        surf.put_int(s.numParams)
        surf.put_double(s.surfParams)
        
        newssr.put_fortran_record(surf)
        
        if cnt > ssrfiles[0].njsw:
            print "Warning: njsw does not match number of entries in surfacelist!"
    
    #whatever the range from njsw to njsw+niwr is...
    for j in range(ssrfiles[0].njsw,ssrfiles[0].njsw+ssrfiles[0].niwr):
        print 'unsupported entries; needs mcnp.py additions'
    
    #summary info/table
    summaryrecord = br._FortranRecord("",0)
    summaryrecord.put_int(ssrfiles[0].summaryTable)
    summaryrecord.put_int(ssrfiles[0].summaryExtra)
    newssr.put_fortran_record(summaryrecord)
    
    # write each file's particle tracks in order of their listing.
    # nps is offset for each track by the entries in trackoffsets.
    # NOTE that first (0) entry in a track is it's nps value, which we are offsetting.
    for cnt, ssrfile in enumerate(ssrfiles):
        for k in range(ssrfile.nrss):
            trackinfo = ssrfile.get_fortran_record()
            
            if trackoffsets != 0:
                mod_ssr_record = br._FortranRecord("", 0)
                thisrecord = trackinfo.get_double(ssrfile.ncrd)
                # offsetting nps
                thisrecord[0] += math.copysign(trackoffsets[cnt], thisrecord[0])
                mod_ssr_record.put_double(thisrecord)
                newssr.put_fortran_record(mod_ssr_record)
            else:
                newssr.put_fortran_record(trackinfo)

    print "Finished writing to new surface source file '", newssrname,"'"
    newssr.close
    
    return True

