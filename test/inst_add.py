#=========================================================================
# add
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "add", 1, 1, 2 ),
    gen_rr_dest_dep_test( 4, "add", 2, 1, 3 ),
    gen_rr_dest_dep_test( 3, "add", 3, 1, 4 ),
    gen_rr_dest_dep_test( 2, "add", 4, 1, 5 ),
    gen_rr_dest_dep_test( 1, "add", 5, 1, 6 ),
    gen_rr_dest_dep_test( 0, "add", 6, 1, 7 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "add",  7, 1,  8 ),
    gen_rr_src0_dep_test( 4, "add",  8, 1,  9 ),
    gen_rr_src0_dep_test( 3, "add",  9, 1, 10 ),
    gen_rr_src0_dep_test( 2, "add", 10, 1, 11 ),
    gen_rr_src0_dep_test( 1, "add", 11, 1, 12 ),
    gen_rr_src0_dep_test( 0, "add", 12, 1, 13 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "add", 1, 13, 14 ),
    gen_rr_src1_dep_test( 4, "add", 1, 14, 15 ),
    gen_rr_src1_dep_test( 3, "add", 1, 15, 16 ),
    gen_rr_src1_dep_test( 2, "add", 1, 16, 17 ),
    gen_rr_src1_dep_test( 1, "add", 1, 17, 18 ),
    gen_rr_src1_dep_test( 0, "add", 1, 18, 19 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "add", 12, 2, 14 ),
    gen_rr_srcs_dep_test( 4, "add", 13, 3, 16 ),
    gen_rr_srcs_dep_test( 3, "add", 14, 4, 18 ),
    gen_rr_srcs_dep_test( 2, "add", 15, 5, 20 ),
    gen_rr_srcs_dep_test( 1, "add", 16, 6, 22 ),
    gen_rr_srcs_dep_test( 0, "add", 17, 7, 24 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "add", 25, 1, 26 ),
    gen_rr_src1_eq_dest_test( "add", 26, 1, 27 ),
    gen_rr_src0_eq_src1_test( "add", 27, 54 ),
    gen_rr_srcs_eq_dest_test( "add", 28, 56 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "add", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "add", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rr_value_test( "add", 0x00000003, 0x00000007, 0x0000000a ),

    gen_rr_value_test( "add", 0x00000000, 0xffff8000, 0xffff8000 ),
    gen_rr_value_test( "add", 0x80000000, 0x00000000, 0x80000000 ),
    gen_rr_value_test( "add", 0x80000000, 0xffff8000, 0x7fff8000 ),

    gen_rr_value_test( "add", 0x00000000, 0x00007fff, 0x00007fff ),
    gen_rr_value_test( "add", 0x7fffffff, 0x00000000, 0x7fffffff ),
    gen_rr_value_test( "add", 0x7fffffff, 0x00007fff, 0x80007ffe ),

    gen_rr_value_test( "add", 0x80000000, 0x00007fff, 0x80007fff ),
    gen_rr_value_test( "add", 0x7fffffff, 0xffff8000, 0x7fff7fff ),

    gen_rr_value_test( "add", 0x00000000, 0xffffffff, 0xffffffff ),
    gen_rr_value_test( "add", 0xffffffff, 0x00000001, 0x00000000 ),
    gen_rr_value_test( "add", 0xffffffff, 0xffffffff, 0xfffffffe ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = src0 + src1
    asm_code.append( gen_rr_value_test( "add", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code

#-------------------------------------------------------------------------
# RAW Hazards (Read After Write)
#-------------------------------------------------------------------------

def gen_raw_test():
  return """
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add x3, x1, x2
    add x4, x3, x1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x4 > 14
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """
#-------------------------------------------------------------------------
# WAW Hazards (Write After Write)
#-------------------------------------------------------------------------

def gen_waw_test():
  return """
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add x3, x1, x2
    add x3, x1, x1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 10
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# WAR Hazards (Write After Read)
#-------------------------------------------------------------------------

def gen_war_test():
  return """
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add x3, x1, x2
    add x2, x1, x1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x2 > 10
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# Multiple adds
#-------------------------------------------------------------------------

def gen_multiple_test():
  return """
    csrr x1, mngr2proc < 1
    csrr x2, mngr2proc < 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add x3, x1, x2
    add x4, x3, x1
    add x5, x4, x1
    add x6, x5, x1
    add x7, x6, x1
    add x8, x7, x1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x8 > 7

  """
