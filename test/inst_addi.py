#=========================================================================
# addi
#=========================================================================

import random

from pymtl                import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc, < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x3, x1, 0x0004
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

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
     gen_rimm_dest_dep_test( 5, "addi", 1, 0x0ff,  256 ),
     gen_rimm_dest_dep_test( 4, "addi", 2, 0xff0,  -14 ),
     gen_rimm_dest_dep_test( 3, "addi", 3, 0xf00, -253 ),
     gen_rimm_dest_dep_test( 2, "addi", 4, 0x00f,   19 ),
     gen_rimm_dest_dep_test( 1, "addi", 5, 0xfff,    4 ),
     gen_rimm_dest_dep_test( 0, "addi", 6, 0x0f0,  246 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return[
    gen_rimm_src_dep_test( 5, "addi", 0x00000f0f, 0x0ff, 0x0000100e ),
    gen_rimm_src_dep_test( 4, "addi", 0x0000f0f0, 0xff0, 0x0000f0e0 ),
    gen_rimm_src_dep_test( 3, "addi", 0x00000f0f, 0xf00, 0x00000e0f ),
    gen_rimm_src_dep_test( 2, "addi", 0x0000f0f0, 0xf0f, 0x0000efff ),
    gen_rimm_src_dep_test( 1, "addi", 0x00000f0f, 0xfff, 0x00000f0e ),
    gen_rimm_src_dep_test( 0, "addi", 0x0000f0f0, 0x0f0, 0x0000f1e0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test("addi", 4562,  0xFF1, 4547),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test("addi", 0x00000000, 0x000, 0x00000000),
    gen_rimm_value_test("addi", 0x00000001, 0x001, 0x00000002),
    gen_rimm_value_test("addi", 0x00000006, 0x009, 0x0000000F),

    gen_rimm_value_test("addi", 0x00000000, 0x0FF, 0x000000FF),
    gen_rimm_value_test("addi", 0xA0000000, 0x000, 0xA0000000),
    gen_rimm_value_test("addi", 0xA0000000, 0xF00, 0x9FFFFF00),

    gen_rimm_value_test("addi", 0xAAAA0000, 0xF00, 0xAAA9FF00),
    gen_rimm_value_test("addi", 0x00AAAA00, 0x0F0, 0x00AAAAF0),
    gen_rimm_value_test("addi", 0x0000AAAA, 0x00F, 0x0000AAB9),

    gen_rimm_value_test("addi", 0xA0000000, 0x000, 0xA0000000),
    gen_rimm_value_test("addi", 0xAFFFFFFF, 0xFFF, 0xAFFFFFFE),
    
    gen_rimm_value_test("addi", 0x00000000, 0xFFF, 0xFFFFFFFF),
    gen_rimm_value_test("addi", 0xFFFFFFFF, 0x001, 0x00000000),
    gen_rimm_value_test("addi", 0xFFFFFFFF, 0xFFF, 0xFFFFFFFE),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src  = Bits( 32, random.randint(0,0xffffffff) )
    imm  = Bits( 12, random.randint(0,0xfff) )
    dest = src + sext(imm,32)
    asm_code.append( gen_rimm_value_test( "addi", src.int(), imm.int(), dest.int() ) )
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
    addi x3, x1,  0x0004
    addi x4, x3,  0x0004
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x4 > 13
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x3, x1,  0x0004
    addi x3, x1,  0x0005
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
    addi x3, x2, 5
    addi x2, x1, 5
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
# Multiple
#-------------------------------------------------------------------------

def gen_multiple_test():
  return """
    csrr x1, mngr2proc < 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x2, x1,  0x0001
    addi x3, x2,  0x0001
    addi x4, x3,  0x0001
    addi x5, x4,  0x0001
    addi x6, x5,  0x0001
    addi x7, x6,  0x0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x7 > 7
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

