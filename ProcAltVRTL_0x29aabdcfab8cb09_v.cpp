//======================================================================
// VProcAltVRTL_0x29aabdcfab8cb09_v.cpp
//======================================================================
// This wrapper exposes a C interface to CFFI so that a
// Verilator-generated C++ model can be driven from Python.
//

#include "obj_dir_ProcAltVRTL_0x29aabdcfab8cb09/VProcAltVRTL_0x29aabdcfab8cb09.h"
#include "stdio.h"
#include "stdint.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

// set to true when VCD tracing is enabled in Verilator
#define DUMP_VCD 1

// set to true when Verilog module has line tracing
#define VLINETRACE 1

#if VLINETRACE
#include "obj_dir_ProcAltVRTL_0x29aabdcfab8cb09/VProcAltVRTL_0x29aabdcfab8cb09__Syms.h"
#include "svdpi.h"
#endif

//----------------------------------------------------------------------
// CFFI Interface
//----------------------------------------------------------------------
// simulation methods and model interface ports exposed to CFFI

extern "C" {
  typedef struct {

    // Exposed port interface
    unsigned long * dmemresp_msg;
  unsigned char * dmemresp_val;
  unsigned char * dmemreq_rdy;
  unsigned long * imemresp_msg;
  unsigned char * imemresp_val;
  unsigned char * imemreq_rdy;
  unsigned char * proc2mngr_rdy;
  unsigned int * mngr2proc_msg;
  unsigned char * mngr2proc_val;
  unsigned int * core_id;
  unsigned char * reset;
  unsigned char * clk;
  unsigned char * stats_en;
  unsigned char * commit_inst;
  unsigned char * dmemresp_rdy;
  unsigned int * dmemreq_msg;
  unsigned char * dmemreq_val;
  unsigned char * imemresp_rdy;
  unsigned int * imemreq_msg;
  unsigned char * imemreq_val;
  unsigned int * proc2mngr_msg;
  unsigned char * proc2mngr_val;
  unsigned char * mngr2proc_rdy;

    // Verilator model
    void * model;

    // VCD state
    int _vcd_en;

    // VCD tracing helpers
    #if DUMP_VCD
    void *        tfp;
    unsigned int  trace_time;
    unsigned char prev_clk;
    #endif

  } VProcAltVRTL_0x29aabdcfab8cb09_t;

  // Exposed methods
  VProcAltVRTL_0x29aabdcfab8cb09_t * create_model( const char * );
  void destroy_model( VProcAltVRTL_0x29aabdcfab8cb09_t *);
  void eval( VProcAltVRTL_0x29aabdcfab8cb09_t * );

  #if VLINETRACE
  void trace( VProcAltVRTL_0x29aabdcfab8cb09_t *, char * );
  #endif
}

//----------------------------------------------------------------------
// sc_time_stamp
//----------------------------------------------------------------------
// Must be defined so the simulator knows the current time. Called by
// $time in Verilog. See:
// http://www.veripool.org/projects/verilator/wiki/Faq

vluint64_t g_main_time = 0;

double sc_time_stamp()
{
  return g_main_time;
}

//----------------------------------------------------------------------
// create_model()
//----------------------------------------------------------------------
// Construct a new verilator simulation, initialize interface signals
// exposed via CFFI, and setup VCD tracing if enabled.

VProcAltVRTL_0x29aabdcfab8cb09_t * create_model( const char *vcd_filename ) {

  VProcAltVRTL_0x29aabdcfab8cb09_t * m;
  VProcAltVRTL_0x29aabdcfab8cb09   * model;

  Verilated::randReset( 0 );

  m     = (VProcAltVRTL_0x29aabdcfab8cb09_t *) malloc( sizeof(VProcAltVRTL_0x29aabdcfab8cb09_t) );
  model = new VProcAltVRTL_0x29aabdcfab8cb09();

  m->model = (void *) model;

  // Enable tracing. We have added a feature where if the vcd_filename is
  // '' then we don't do any VCD dumping even if DUMP_VCD is true.

  m->_vcd_en = 0;
  #if DUMP_VCD
  if ( strlen( vcd_filename ) != 0 ) {
    m->_vcd_en = 1;
    Verilated::traceEverOn( true );
    VerilatedVcdC * tfp = new VerilatedVcdC();

    model->trace( tfp, 99 );
    tfp->spTrace()->set_time_resolution( "10ps" );
    tfp->open( vcd_filename );

    m->tfp        = (void *) tfp;
    m->trace_time = 0;
    m->prev_clk   = 0;
  }
  #endif

  // initialize exposed model interface pointers
  m->dmemresp_msg = &model->dmemresp_msg;
  m->dmemresp_val = &model->dmemresp_val;
  m->dmemreq_rdy = &model->dmemreq_rdy;
  m->imemresp_msg = &model->imemresp_msg;
  m->imemresp_val = &model->imemresp_val;
  m->imemreq_rdy = &model->imemreq_rdy;
  m->proc2mngr_rdy = &model->proc2mngr_rdy;
  m->mngr2proc_msg = &model->mngr2proc_msg;
  m->mngr2proc_val = &model->mngr2proc_val;
  m->core_id = &model->core_id;
  m->reset = &model->reset;
  m->clk = &model->clk;
  m->stats_en = &model->stats_en;
  m->commit_inst = &model->commit_inst;
  m->dmemresp_rdy = &model->dmemresp_rdy;
  m->dmemreq_msg = model->dmemreq_msg;
  m->dmemreq_val = &model->dmemreq_val;
  m->imemresp_rdy = &model->imemresp_rdy;
  m->imemreq_msg = model->imemreq_msg;
  m->imemreq_val = &model->imemreq_val;
  m->proc2mngr_msg = &model->proc2mngr_msg;
  m->proc2mngr_val = &model->proc2mngr_val;
  m->mngr2proc_rdy = &model->mngr2proc_rdy;

  return m;
}

//----------------------------------------------------------------------
// destroy_model()
//----------------------------------------------------------------------
// Finalize the Verilator simulation, close files, call destructors.

void destroy_model( VProcAltVRTL_0x29aabdcfab8cb09_t * m ) {

  VProcAltVRTL_0x29aabdcfab8cb09 * model = (VProcAltVRTL_0x29aabdcfab8cb09 *) m->model;

  // finalize verilator simulation
  model->final();

  #if DUMP_VCD
  if ( m->_vcd_en ) {
    printf("DESTROYING %d\n", m->trace_time );
    VerilatedVcdC * tfp = (VerilatedVcdC *) m->tfp;
    tfp->close();
  }
  #endif

  // TODO: this is probably a memory leak!
  //       But pypy segfaults if uncommented...
  //delete model;

}

//----------------------------------------------------------------------
// eval()
//----------------------------------------------------------------------
// Simulate one time-step in the Verilated model.

void eval( VProcAltVRTL_0x29aabdcfab8cb09_t * m ) {

  VProcAltVRTL_0x29aabdcfab8cb09 * model = (VProcAltVRTL_0x29aabdcfab8cb09 *) m->model;

  // evaluate one time step
  model->eval();

  #if DUMP_VCD
  if ( m->_vcd_en ) {

    // update simulation time only on clock toggle
    if (m->prev_clk != model->clk) {
      m->trace_time += 50;
      g_main_time += 50;
    }
    m->prev_clk = model->clk;

    // dump current signal values
    VerilatedVcdC * tfp = (VerilatedVcdC *) m->tfp;
    tfp->dump( m->trace_time );
    tfp->flush();

  }
  #endif

}

//----------------------------------------------------------------------
// trace()
//----------------------------------------------------------------------
// Note that we assume a trace string buffer of 512 characters. This is
// assumed in a couple of places, including the Python wrapper template
// and the Verilog vc/trace.v code. So if we change it, we need to change
// it everywhere.

#if VLINETRACE
void trace( VProcAltVRTL_0x29aabdcfab8cb09_t * m, char* str ) {

  VProcAltVRTL_0x29aabdcfab8cb09 * model = (VProcAltVRTL_0x29aabdcfab8cb09 *) m->model;

  const int nchars = 512;
  const int nwords = nchars/4;

  uint32_t words[nwords];
  words[0] = nchars-1;

  // Setup scope for accessing the line tracing function throug DPI.
  // Note, I tried using just this:
  //
  //  svSetScope( svGetScopeFromName("TOP.v.verilog_module") );
  //
  // but it did not seem to work. We would see correct line tracing for
  // the first test case but not any of the remaining tests cases. After
  // digging around a bit, it seemed like the line_trace task was still
  // associated with the very first model as opposed to the newly
  // instantiated models. Directly setting the scope seemed to fix
  // this issue.

  svSetScope( &model->__VlSymsp->__Vscope_v__verilog_module );
  model->line_trace( words );

  // Note that the way the line tracing works, the line tracing function
  // will store how the last character used in the line trace in the
  // first element of the word array. The line tracing functions store
  // the line trace starting from the most-signicant character due to the
  // way that Verilog handles strings.

  int nchar_last  = words[0];
  int nchars_used = ( nchars - 1 - nchar_last );

  // We subtract since one of the words (i.e., 4 characters) is for
  // storing the nchars_used.

  assert ( nchars_used < (nchars - 4) );

  // Now we need to iterate from the most-significant character to the
  // last character written by the line tracing functions and copy these
  // characters into the given character array. So we are kind of
  // flipping the order of the characters due to the different between
  // how Verilog and C handle strings.

  int j = 0;
  for ( int i = nchars-1; i > nchar_last; i-- ) {
    char c = static_cast<char>( words[i/4] >> (8*(i%4)) );
    str[j] = c;
    j++;
  }
  str[j] = '\0';

}
#endif

