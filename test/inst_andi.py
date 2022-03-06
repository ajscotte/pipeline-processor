#=========================================================================
# andi
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    andi x3, x1, 0x00ff
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 >0x0000000f
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
    gen_rimm_dest_dep_test( 5, "andi", 0x00000f0f, 0x0ff, 0x0000000f ),
    gen_rimm_dest_dep_test( 4, "andi", 0x0000f0f0, 0xff0, 0x0000f0f0 ),
    gen_rimm_dest_dep_test( 3, "andi", 0x00000f0f, 0xf00, 0x00000f00 ),
    gen_rimm_dest_dep_test( 2, "andi", 0x0000f0f0, 0x00f, 0x00000000 ),
    gen_rimm_dest_dep_test( 1, "andi", 0x00000f0f, 0xfff, 0x00000f0f ),
    gen_rimm_dest_dep_test( 0, "andi", 0x0000f0f0, 0x0f0, 0x000000f0 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "andi", 0x00000f0f, 0x0ff, 0x0000000f ),
    gen_rimm_src_dep_test( 4, "andi", 0x0000f0f0, 0xff0, 0x0000f0f0 ),
    gen_rimm_src_dep_test( 3, "andi", 0x00000f0f, 0xf00, 0x00000f00 ),
    gen_rimm_src_dep_test( 2, "andi", 0x0000f0f0, 0xf0f, 0x0000f000 ),
    gen_rimm_src_dep_test( 1, "andi", 0x00000f0f, 0xfff, 0x00000f0f ),
    gen_rimm_src_dep_test( 0, "andi", 0x0000f0f0, 0x0f0, 0x000000f0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "andi", 0x00000f0f, 0xff0, 0x00000f00 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "andi", 0xff00ff00, 0xf0f, 0xff00ff00 ),
    gen_rimm_value_test( "andi", 0x0ff00ff0, 0x0f0, 0x000000f0 ),
    gen_rimm_value_test( "andi", 0x00ff00ff, 0x00f, 0x0000000f ),
    gen_rimm_value_test( "andi", 0xf00ff00f, 0xff0, 0xf00ff000 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src  = Bits( 32, random.randint(0,0xffffffff) )
    imm  = Bits( 12, random.randint(0,0xfff) )
    dest = src & sext(imm,32)
    asm_code.append( gen_rimm_value_test( "andi", src.uint(), imm.uint(), dest.uint() ) )
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
    andi x3, x1, 0x0001
    andi x4, x3, 0x0005
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x4 > 1
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
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    andi x3, x1, 0x0001
    andi x3, x1, 0x0002
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0
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
    andi x3, x2, 0x0001
    andi x2, x1, 0x0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x2 > 1
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
# Multiple
#-------------------------------------------------------------------------

def gen_multiple_test():
  return """
    csrr x1, mngr2proc < 0b1111111
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    andi x2, x1,  0b1111110
    andi x3, x2,  0b1111100
    andi x4, x3,  0b1111000
    andi x5, x4,  0b1110000
    andi x6, x5,  0b1100000
    andi x7, x6,  0b1000000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x7 > 0b1000000
  """
