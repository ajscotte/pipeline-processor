#=========================================================================
# ProcDpathComponentsRTL_test.py
#=========================================================================

import pytest
import random

from pymtl      import *
from harness    import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import run_test_vector_sim

from lab2_proc.ProcDpathComponentsRTL import ImmGenRTL
from lab2_proc.ProcDpathComponentsRTL import AluRTL

#-------------------------------------------------------------------------
# ImmGenRTL
#-------------------------------------------------------------------------

def test_immgen( test_verilog, dump_vcd ):

  header_str = \
  ( "imm_type", "inst",
    "imm*" )
  
  run_test_vector_sim( ImmGenRTL(), [ header_str,
    # imm_type inst                                imm
    [ 0,       0b11111111111100000000000000000000, 0b11111111111111111111111111111111], # I-imm
    [ 0,       0b00000000000011111111111111111111, 0b00000000000000000000000000000000], # I-imm
    [ 0,       0b01111111111100000000000000000000, 0b00000000000000000000011111111111], # I-imm
    [ 0,       0b11111111111000000000000000000000, 0b11111111111111111111111111111110], # I-imm
    [ 1,       0b11111110000000000000111110000000, 0b11111111111111111111111111111111], # S-imm
    [ 1,       0b00000001111111111111000001111111, 0b00000000000000000000000000000000], # S-imm
    [ 1,       0b01111110000000000000111110000000, 0b00000000000000000000011111111111], # S-imm
    [ 1,       0b11111110000000000000111100000000, 0b11111111111111111111111111111110], # S-imm
    [ 2,       0b11111110000000000000111110000000, 0b11111111111111111111111111111110], # B-imm
    [ 2,       0b00000001111111111111000001111111, 0b00000000000000000000000000000000], # B-imm
    [ 2,       0b11000000000000000000111100000000, 0b11111111111111111111010000011110], # B-imm
    [ 3,       0b11111111111111111111000000000000, 0b11111111111111111111000000000000], # U-imm
    [ 3,       0b00000000000000000000111111111111, 0b00000000000000000000000000000000], # U-imm
    [ 4,       0b11111111111111111111000000000000, 0b11111111111111111111111111111110], # J-imm
    [ 4,       0b00000000000000000001111111111111, 0b00000000000000000001000000000000], # J-imm
    [ 4,       0b01000000000010011001000000000000, 0b00000000000010011001010000000000], # J-imm
  ], dump_vcd, test_verilog )

#-------------------------------------------------------------------------
# AluRTL
#-------------------------------------------------------------------------

def test_alu_add( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   0,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   0,  0x0ffbc964,   '?',      '?',       '?'      ],
    #pos-neg
    [ 0x00132050,   0xd6620040,   0,  0xd6752090,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   0,  0xfff0e890,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   0,  0xf353eaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

#''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Add more ALU function tests
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def test_alu_cp_op0( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  11,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  11,  0x0ffaa660,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  11,  0x00132050,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  11,  0xfff0a440,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  11,  0xfeeeeaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_op1( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  12,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  12,  0x00012304,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  12,  0xd6620040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  12,  0x00004450,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  12,  0xf4650000,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )


def test_alu_sub( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  1,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  1,  0x0ff9835c,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  1,  0xfff05ff0,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xfeeeeaa3,  1,  0x00000000,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )
  
def test_alu_and( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  2,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  2,  0x00002200,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  2,  0x00020040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  2,  0x00000440,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  2,  0xf4640000,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )  

def test_alu_or( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  3,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  3,  0x0ffba764,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  3,  0xd6732050,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  3,  0xfff0e450,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  3,  0xfeefeaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_xor( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  4,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  4,  0x0ffb8564,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  4,  0xd6712010,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  4,  0xfff0e010,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  4,  0x0a8beaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog)
  
def test_alu_slt( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  5,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0xf0012304,  5,  0x0,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  5,  0x0,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  5,  0x1,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  5,  0x0,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_sltu( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  6,  0x0,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  6,  0x0,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  6,  0x1,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  6,  0x0,   '?',      '?',       '?'      ],
    [ 0x0eeeeaa3,   0xf4650000,  6,  0x1,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )
  
  
def test_alu_sra( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  7,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  7,  0x00ffaa66,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  7,  0xfffffff0,   '?',      '?',       '?'      ],
    [ 0xf0eeeaa3,   0x0000,  7,  0xf0eeeaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )
  
def test_alu_srl( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  8,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  8,  0x00ffaa66,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620043,  8,  0x0002640a,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  8,  0x0000fff0,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  8,  0xfeeeeaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )
  
def test_alu_sll( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  9,  0xffaa6600,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620043,  9,  0x00990280,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  9,  0xa4400000,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  9,  0xfeeeeaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )
  
def test_alu_lui( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  10,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  10,  0x00012304,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  10,  0xd6620040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  10,  0x00004450,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  10,  0xf4650000,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )
  
def test_alu_jalr( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  14,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  14,  0x0ffbc964,   '?',      '?',       '?'      ],
    [ 0xf0132050,   0xd6620040,  14,  0xc6752090,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )
  
def test_alu_eq( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out* ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  0,  '?',   0x1,      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  0,  '?',   0x0,      '?',       '?'      ],
    [ 0xf0132050,   0xd6620040,  0,  '?',   0x0,      '?',       '?'      ],
    [ 0xf0132050,   0xf0132050,  0,  '?',   0x1,      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_lt( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out* ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  0,  '?',   '?',      0x0,       '?'      ],
    [ 0x0ffaa660,   0x00012304,  0,  '?',   '?',      0x0,       '?'      ],
    [ 0xf0132050,   0xd6620040,  0,  '?',   '?',      0x0,       '?'      ],
    [ 0xf4650000,   0xfeeeeaa3,  0,  '?',   '?',      0x1,       '?'      ],
    [ 0x04650000,   0x0eeeeaa3,  0,  '?',   '?',      0x1,       '?'      ],
  ], dump_vcd, test_verilog )
  
def test_alu_ltu( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*  ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  0,  '?',   '?',      '?',       0x0      ],
    [ 0x0ffaa660,   0x00012304,  0,  '?',   '?',      '?',       0x0      ],
    [ 0xf0132050,   0xd6620040,  0,  '?',   '?',      '?',       0x0      ],
    [ 0xf4650000,   0xfeeeeaa3,  0,  '?',   '?',      '?',       0x1      ],
  ], dump_vcd, test_verilog )
