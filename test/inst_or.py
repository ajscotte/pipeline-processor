#=========================================================================
# or
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x0f0f0f0f
    csrr x2, mngr2proc < 0x00ff00ff
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    or x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x0fff0fff
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
    gen_rr_dest_dep_test( 5, "or", 0x0000000f, 0x0000000f, 0x0000000f ),
    gen_rr_dest_dep_test( 4, "or", 0x000000f0, 0x0000000f, 0x000000ff ),
    gen_rr_dest_dep_test( 3, "or", 0x00000f00, 0x0000000f, 0x00000f0f ),
    gen_rr_dest_dep_test( 2, "or", 0x0000f000, 0x0000000f, 0x0000f00f ),
    gen_rr_dest_dep_test( 1, "or", 0x000f0000, 0x0000000f, 0x000f000f ),
    gen_rr_dest_dep_test( 0, "or", 0x00f00000, 0x0000000f, 0x00f0000f ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "or", 0x0000000f, 0x0000000f, 0x0000000f ),
    gen_rr_src0_dep_test( 4, "or", 0x000000f0, 0x0000000f, 0x000000ff ),
    gen_rr_src0_dep_test( 3, "or", 0x00000f00, 0x0000000f, 0x00000f0f ),
    gen_rr_src0_dep_test( 2, "or", 0x0000f000, 0x0000000f, 0x0000f00f ),
    gen_rr_src0_dep_test( 1, "or", 0x000f0000, 0x0000000f, 0x000f000f ),
    gen_rr_src0_dep_test( 0, "or", 0x00f00000, 0x0000000f, 0x00f0000f ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "or", 0x0000000f, 0x0000000f, 0x0000000f ),
    gen_rr_src1_dep_test( 4, "or", 0x0000000f, 0x000000f0, 0x000000ff ),
    gen_rr_src1_dep_test( 3, "or", 0x0000000f, 0x00000f00, 0x00000f0f ),
    gen_rr_src1_dep_test( 2, "or", 0x0000000f, 0x0000f000, 0x0000f00f ),
    gen_rr_src1_dep_test( 1, "or", 0x0000000f, 0x000f0000, 0x000f000f ),
    gen_rr_src1_dep_test( 0, "or", 0x0000000f, 0x00f00000, 0x00f0000f ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "or", 0x000f0f00, 0x0000ff00, 0x000fff00 ),
    gen_rr_srcs_dep_test( 4, "or", 0x00f0f000, 0x000ff000, 0x00fff000 ),
    gen_rr_srcs_dep_test( 3, "or", 0x0f0f0000, 0x00ff0000, 0x0fff0000 ),
    gen_rr_srcs_dep_test( 2, "or", 0xf0f00000, 0x0ff00000, 0xfff00000 ),
    gen_rr_srcs_dep_test( 1, "or", 0x0f00000f, 0xff000000, 0xff00000f ),
    gen_rr_srcs_dep_test( 0, "or", 0xf00000f0, 0xf000000f, 0xf00000ff ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "or", 0x00000f0f, 0x000000ff, 0x00000fff ),
    gen_rr_src1_eq_dest_test( "or", 0x0000f0f0, 0x00000ff0, 0x0000fff0 ),
    gen_rr_src0_eq_src1_test( "or", 0x000f0f00, 0x000f0f00 ),
    gen_rr_srcs_eq_dest_test( "or", 0x000f0f00, 0x000f0f00 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "or", 0xff00ff00, 0x0f0f0f0f, 0xff0fff0f ),
    gen_rr_value_test( "or", 0x0ff00ff0, 0xf0f0f0f0, 0xfff0fff0 ),
    gen_rr_value_test( "or", 0x00ff00ff, 0x0f0f0f0f, 0x0fff0fff ),
    gen_rr_value_test( "or", 0xf00ff00f, 0xf0f0f0f0, 0xf0fff0ff ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = src0 | src1
    asm_code.append( gen_rr_value_test( "or", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code

#-------------------------------------------------------------------------
# RAW Hazards (Read After Write)
#-------------------------------------------------------------------------

def gen_raw_test():
  return """
    csrr x1, mngr2proc < 1
    csrr x2, mngr2proc < 2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    or x3, x1, x2
    or x4, x3, x0
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x4 > 3
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
    csrr x1, mngr2proc < 1
    csrr x2, mngr2proc < 2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    or x3, x1, x2
    or x3, x1, x1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 1
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
    csrr x1, mngr2proc < 1
    csrr x2, mngr2proc < 2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    or x3, x1, x2
    or x2, x3, x0
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x2 > 3
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
# Multiple ors
#-------------------------------------------------------------------------

def gen_multiple_test():
  return """
    csrr x1, mngr2proc < 0b010101
    csrr x2, mngr2proc < 0b010011
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    or x3, x2, x1
    or x4, x3, x1
    or x5, x4, x1
    or x6, x5, x1
    or x7, x6, x1
    or x8, x7, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x8 > 0b010111
  """

#-------------------------------------------------------------------------
# Control Hazard
#-------------------------------------------------------------------------

def gen_control_test():
  return """
  """

#-------------------------------------------------------------------------
# Structural Hazard
#-------------------------------------------------------------------------

def gen_structural_test():
  return """
  """