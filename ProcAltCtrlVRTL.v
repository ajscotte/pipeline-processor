//=========================================================================
// 5-Stage Stalling Pipelined Processor Control
//=========================================================================

`ifndef LAB2_PROC_PIPELINED_PROC_ALT_CTRL_V
`define LAB2_PROC_PIPELINED_PROC_ALT_CTRL_V

`include "vc/trace.v"

`include "lab2_proc/TinyRV2InstVRTL.v"

module lab2_proc_ProcAltCtrlVRTL
(
  input  logic        clk,
  input  logic        reset,

  // Instruction Memory Port

  output logic        imemreq_val,
  input  logic        imemreq_rdy,

  input  logic        imemresp_val,
  output logic        imemresp_rdy,

  output logic        imemresp_drop,

  // Data Memory Port

  output logic        dmemreq_val,
  input  logic        dmemreq_rdy,

  input  logic        dmemresp_val,
  output logic        dmemresp_rdy,

  // mngr communication port

  input  logic        mngr2proc_val,
  output logic        mngr2proc_rdy,

  output logic        proc2mngr_val,
  input  logic        proc2mngr_rdy,

  // control signals (ctrl->dpath)

  output logic        reg_en_F,
  output logic [1:0]  pc_sel_F,

  output logic        reg_en_D,
  output logic        op1_sel_D,
  output logic [1:0]  op1_bypass_sel,
  output logic [1:0]  op2_sel_D,
  output logic [1:0]  op2_bypass_sel,
  output logic [1:0]  csrr_sel_D,
  output logic [2:0]  imm_type_D,
  output logic        imul_req_val_D,

  output logic        reg_en_X,
  output logic [3:0]  alu_fn_X,
  output logic [1:0]  ex_result_sel_X,
  output logic        imul_resp_rdy_X,
  output logic [2:0]  mem_type,
  
  output logic        reg_en_M,
  output logic        wb_result_sel_M,

  output logic        reg_en_W,
  output logic [4:0]  rf_waddr_W,
  output logic        rf_wen_W,

  // status signals (dpath->ctrl)

  input  logic [31:0] inst_D,
  input  logic        imul_req_rdy_D,
  input  logic        br_cond_eq_X,
  input  logic        br_cond_lt_x,
  input  logic        br_cond_ltu_x,
  input  logic        imul_resp_val_X,

  output logic        stats_en_wen_W,

  output logic        commit_inst

);

  //----------------------------------------------------------------------
  // Notes
  //----------------------------------------------------------------------
  // We follow this principle to organize code for each pipeline stage in
  // the control unit.  Register enable logics should always at the
  // beginning. It followed by pipeline registers. Then logic that is not
  // dependent on stall or squash signals. Then logic that is dependent
  // on stall or squash signals. At the end there should be signals meant
  // to be passed to the next stage in the pipeline.

  //----------------------------------------------------------------------
  // Valid, stall, and squash signals
  // ----------------------------------------------------------------------
  // We use valid signal to indicate if the instruction is valid.  An
  // instruction can become invalid because of being squashed or
  // stalled. Notice that invalid instructions are microarchitectural
  // events, they are different from archtectural no-ops. We must be
  // careful about control signals that might change the state of the
  // processor. We should always AND outgoing control signals with valid
  // signal.

  logic val_F;
  logic val_D;
  logic val_X;
  logic val_M;
  logic val_W;

  // Managing the stall and squash signals is one of the most important,
  // yet also one of the most complex, aspects of designing a pipelined
  // processor. We will carefully use four signals per stage to manage
  // stalling and squashing: ostall_A, osquash_A, stall_A, and squash_A.
  //
  // We denote the stall signals _originating_ from stage A as
  // ostall_A. For example, if stage A can stall due to a pipeline
  // harzard, then ostall_A would need to factor in the stalling
  // condition for this pipeline harzard.

  logic ostall_F;  // can ostall due to imemresp_val
  logic ostall_D;  // can ostall due to mngr2proc_val or other hazards
  logic ostall_X;  // can ostall due to dmemreq_rdy
  logic ostall_M;  // can ostall due to dmemresp_val
  logic ostall_W;  // can ostall due to proc2mngr_rdy

  // The stall_A signal should be used to indicate when stage A is indeed
  // stalling. stall_A will be a function of ostall_A and all the ostall
  // signals of stages in front of it in the pipeline.

  logic stall_F;
  logic stall_D;
  logic stall_X;
  logic stall_M;
  logic stall_W;

  // We denote the squash signals _originating_ from stage A as
  // osquash_A. For example, if stage A needs to squash the stages behind
  // A in the pipeline, then osquash_A would need to factor in this
  // squash condition.

  logic osquash_D; // can osquash due to unconditional jumps
  logic osquash_X; // can osquash due to taken branches

  // The squash_A signal should be used to indicate when stage A is being
  // squashed. squash_A will _not_ be a function of osquash_A, since
  // osquash_A means to squash the stages _behind_ A in the pipeline, but
  // not to squash A itself.

  logic squash_F;
  logic squash_D;

  //----------------------------------------------------------------------
  // F stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_F = !stall_F || squash_F;

  // Pipeline registers

  always_ff @( posedge clk ) begin
    if ( reset )
      val_F <= 1'b0;
    else if ( reg_en_F )
      val_F <= 1'b1;
  end

  // forward declaration for PC sel

  logic       pc_redirect_X;
  logic       pc_redirect_D;
  logic [1:0] pc_sel_D;
  logic [1:0] pc_sel_X;

  // PC select logic where branch is prioritized

  always_comb begin
    if ( pc_redirect_X )       // If a branch is taken in X stage
      pc_sel_F = pc_sel_X;     //Use pc from X
    else if ( pc_redirect_D )  // If a jump is taken in D stage
      pc_sel_F = pc_sel_D;     // Use pc from D
    else
      pc_sel_F = 2'b0;         // Use pc+4
  end

  // ostall due to the imem response not valid.

  assign ostall_F = val_F && !imemresp_val;

  // stall and squash in F

  assign stall_F  = val_F && ( ostall_F  || ostall_D || ostall_X || ostall_M || ostall_W );
  assign squash_F = val_F && ( osquash_D || osquash_X );

  // We drop the mem response when we are getting squashed

  assign imemresp_drop = squash_F;

  // imem is very special. Actually imem requests are sent before the F
  // stage. Note that we need to factor in reset to the imemreq_val
  // signal because we don't want to send out imem request when we are
  // resetting.

  assign imemreq_val  = ( !stall_F || squash_F ) && !reset;
  assign imemresp_rdy = !stall_F || squash_F;

  // Valid signal for the next stage (stage D)

  logic  next_val_F;
  assign next_val_F = val_F && !stall_F && !squash_F;

  //----------------------------------------------------------------------
  // D stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_D = !stall_D || squash_D;

  // Pipline registers

  always_ff @( posedge clk ) begin
    if ( reset )
      val_D <= 1'b0;
    else if ( reg_en_D )
      val_D <= next_val_F;
  end

  // Parse instruction fields

  logic   [4:0] inst_rd_D;
  logic   [4:0] inst_rs1_D;
  logic   [4:0] inst_rs2_D;
  logic   [11:0] inst_csr_D;

  rv2isa_InstUnpack inst_unpack
  (
    .inst     (inst_D),
    .opcode   (),
    .rd       (inst_rd_D),
    .rs1      (inst_rs1_D),
    .rs2      (inst_rs2_D),
    .funct3   (),
    .funct7   (),
    .csr      (inst_csr_D)
  );

  // Generic Parameters -- yes or no

  localparam n = 1'd0;
  localparam y = 1'd1;

  //jump type specifiers
  localparam jalx = 5'bx;
  localparam jal = 5'b111;
  localparam jalr = 5'b1000;
  // Register specifiers

  localparam rx = 5'bx;   // don't care
  localparam r0 = 5'd0;   // zero
  localparam rL = 5'd31;  // for jal

  // Branch type

  localparam br_x     = 3'bx; // Don't care
  localparam br_na    = 3'b0; // No branch
  localparam br_bne   = 3'b1; // bne
  localparam br_beq   = 3'b010;
  localparam br_blt   = 3'b011;
  localparam br_bltu  = 3'b100;
  localparam br_bge   = 3'b101;
  localparam br_bgeu  = 3'b110;
  

  //Operand 1 Mux Select
  localparam bm1_x      = 1'bx;
  localparam bm1_rf     = 1'b0;
  localparam bm1_pc     = 1'b1;

  // Operand 2 Mux Select

  localparam bm_x     = 2'bx; // Don't care
  localparam bm_rf    = 2'd0; // Use data from register file
  localparam bm_imm   = 2'd1; // Use sign-extended immediate
  localparam bm_csr   = 2'd2; // Use from mngr data

  // ALU Function

  localparam alu_x    = 4'bx;
  localparam alu_add  = 4'd0;
  localparam alu_sub  = 4'd1;
  localparam alu_and  = 4'd2;
  localparam alu_or  = 4'd3;
  localparam alu_xor  = 4'd4;
  localparam alu_slt  = 4'd5;
  localparam alu_sltu  = 4'd6;
  localparam alu_sra  = 4'd7;
  localparam alu_srl  = 4'd8;
  localparam alu_sll  = 4'd9;

  localparam alu_lui  = 4'd10;
  localparam alu_cp0  = 4'd11;
  localparam alu_cp1  = 4'd12;
  localparam alu_test  = 4'd13;
  localparam alu_jalr = 4'd14;

  // Immediate Type
  localparam imm_x    = 3'bx;
  localparam imm_i    = 3'd0;
  localparam imm_s    = 3'd1;
  localparam imm_b    = 3'd2;
  localparam imm_u    = 3'd3;
  localparam imm_j    = 3'd4;
  
  //req values multiplier
   localparam reqx    = 1'bx;
   localparam reqno    = 1'b0;
   localparam reqyes    = 1'b1;
  
  //resp values multiplier
   localparam respx    = 1'bx;
   localparam respno    = 1'b0;
   localparam respyes    = 1'b1;
   
  //ex_result mux select
  localparam exmux_x    = 2'bx;
  localparam exmux_pc   = 2'b01;
  localparam exmux_alu  = 2'b00;
  localparam exmux_mul = 2'b10;

  // Memory Request Type

  localparam nr       = 2'd0; // No request
  localparam ld       = 2'd1; // Load
  localparam st       = 2'd2; // Store

  // Writeback Mux Select

  localparam wm_x     = 1'bx; // Don't care
  localparam wm_a     = 1'b0; // Use ALU output
  localparam wm_m     = 1'b1; // Use data memory response

  // Instruction Decode

  logic       inst_val_D;
  logic [2:0] br_type_D;
  logic [4:0]  jump_type_D;
  logic       rs1_en_D;
  logic       rs2_en_D;
  logic [3:0] alu_fn_D;
  logic [1:0] dmemreq_type_D;
  logic       wb_result_sel_D;
  logic       rf_wen_pending_D;
  logic       csrr_D;
  logic       csrw_D;
  logic       proc2mngr_val_D;
  logic       mngr2proc_rdy_D;
  logic       stats_en_wen_D;
  logic [1:0] ex_result_sel_D;
  logic       req_val_D;//imul_req_val_D helper
  logic       resp_rdy_D;//make an x

  task cs
  (
    input logic       cs_inst_val,
    input logic [2:0] cs_br_type,
    input logic [4:0] cs_jump_type,
    input logic [2:0] cs_imm_type,
    input logic       cs_op1_sel,
    input logic       cs_rs1_en,
    input logic [1:0] cs_op2_sel,
    input logic       cs_rs2_en,
    input logic [3:0] cs_alu_fn,
    input logic [1:0] cs_ex_result_sel,
    input logic [1:0] cs_dmemreq_type,
    input logic       cs_wb_result_sel,
    input logic       cs_rf_wen_pending,
    input logic       cs_csrr,
    input logic       cs_csrw,
    input logic       cs_req_val
   // input logic       cs_resp_rdy
  );
  begin
    inst_val_D            = cs_inst_val;
    br_type_D             = cs_br_type;
    jump_type_D           = cs_jump_type;
    imm_type_D            = cs_imm_type;
    op1_sel_D             = cs_op1_sel;
    rs1_en_D              = cs_rs1_en;
    op2_sel_D             = cs_op2_sel;
    rs2_en_D              = cs_rs2_en;
    alu_fn_D              = cs_alu_fn;
    ex_result_sel_D       = cs_ex_result_sel;
    dmemreq_type_D        = cs_dmemreq_type;
    wb_result_sel_D       = cs_wb_result_sel;
    rf_wen_pending_D      = cs_rf_wen_pending;
    csrr_D                = cs_csrr;
    csrw_D                = cs_csrw;
    req_val_D             =cs_req_val;
   
  end
  endtask

  // Control signals table

  always_comb begin

    casez ( inst_D )

      //                           br      jal   imm    op1    rs1  op2    rs2 alu      ex        dmm wbmux rf
      //                       val type    type  type  muxsel   en  muxsel  en fn       muxsel    typ sel   wen csrr csrw req  resp
      `RV2ISA_INST_NOP     :cs( y, br_na, jalx,  imm_x, bm1_rf, n, bm_x,   n, alu_x,   exmux_alu, nr, wm_a, n,  n,   n,   reqx);
      `RV2ISA_INST_ADD     :cs( y, br_na, jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_add, exmux_alu, nr, wm_a, y,  n,   n,   reqx);
      `RV2ISA_INST_LW      :cs( y, br_na, jalx,  imm_i, bm1_rf, y, bm_imm, n, alu_add, exmux_alu, ld, wm_m, y,  n,   n,   reqx);
      `RV2ISA_INST_BNE     :cs( y, br_bne, jalx,  imm_b, bm1_rf, y, bm_rf,  y, alu_x,   exmux_alu, nr, wm_a, n,  n,   n,   reqx);
      `RV2ISA_INST_CSRR    :cs( y, br_na, jalx,  imm_i, bm1_rf, n, bm_csr, n, alu_cp1, exmux_alu, nr, wm_a, y,  y,   n,   reqx);
      `RV2ISA_INST_CSRW    :cs( y, br_na, jalx,  imm_i, bm1_rf, y, bm_rf,  n, alu_cp0, exmux_alu, nr, wm_a, n,  n,   y,   reqx);

      //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''
      // Add more instructions to the control signal table
      //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
      //make a new slot called jump_inst_d that only
      //register - register instructions 
      `RV2ISA_INST_SUB    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_sub, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_AND    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_and, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_OR     :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_or, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_XOR    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_xor, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SLT    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_slt, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SLTU   :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_sltu, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SRA    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_sra, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SRL    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_srl, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SLL    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_sll, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_MUL    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_rf,  y, alu_x, exmux_mul, nr, wm_a, y,  n,   n,   reqyes    );
      //register - immediate instructions 
      `RV2ISA_INST_ADDI    :cs( y, br_na,  jalx,  imm_i, bm1_rf, y, bm_imm,  y, alu_add, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_ORI     :cs( y, br_na,  jalx,  imm_i, bm1_rf, y, bm_imm,  y, alu_or, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_ANDI    :cs( y, br_na,  jalx,  imm_i, bm1_rf, y, bm_imm,  y, alu_and, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_XORI    :cs( y, br_na,  jalx,  imm_i, bm1_rf, y, bm_imm,  y, alu_xor, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SLTI    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_imm,  y, alu_slt, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SLTIU   :cs( y, br_na,  jalx,  imm_i, bm1_rf, y, bm_imm,  y, alu_sltu, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SRAI    :cs( y, br_na,  jalx,  imm_x, bm1_rf, y, bm_imm,  y, alu_sra, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SRLI    :cs( y, br_na,  jalx,  imm_i, bm1_rf, y, bm_imm,  y, alu_srl, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_SLLI    :cs( y, br_na,  jalx,  imm_i, bm1_rf, y, bm_imm,  y, alu_sll, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_LUI     :cs( y, br_na,  jalx,  imm_u, bm1_x, n, bm_imm,  y, alu_lui, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_AUIPC   :cs( y, br_na,  jalx,  imm_u, bm1_pc, y, bm_imm,  y, alu_add, exmux_alu, nr, wm_a, y,  n,   n,   reqno    );
    
      //memeory instructions 
      `RV2ISA_INST_SW   :cs( y, br_na,  jalx,  imm_s, bm1_rf, y, bm_imm,  y, alu_add, exmux_x, st, wm_x, n,  n,   n,   reqno    );
      
      //Jump intructions
      `RV2ISA_INST_JAL     :cs( y, br_na,  jal,  imm_j, bm1_rf, y, bm_rf,  y, alu_test, exmux_pc, nr, wm_a, y,  n,   n,   reqno    );
      `RV2ISA_INST_JALR    :cs( y, br_na, jalr, imm_i, bm1_rf, y, bm_imm,  y, alu_jalr, exmux_pc, nr, wm_a, y,  n,   n,   reqno    );
      
      //branching instructions
      `RV2ISA_INST_BEQ     :cs( y, br_beq, jalx,  imm_b, bm1_rf, y, bm_rf,  y, alu_x,   exmux_alu, nr, wm_a, n,  n,   n,   reqno    );
      `RV2ISA_INST_BLT     :cs( y, br_blt, jalx,  imm_b, bm1_rf, y, bm_rf,  y, alu_x,   exmux_alu, nr, wm_a, n,  n,   n,   reqno    );
      `RV2ISA_INST_BLTU    :cs( y, br_bltu, jalx,  imm_b, bm1_rf, y, bm_rf,  y, alu_x,   exmux_alu, nr, wm_a, n,  n,   n,   reqno    );
      `RV2ISA_INST_BGE     :cs( y, br_bge, jalx,  imm_b, bm1_rf, y, bm_rf,  y, alu_x,   exmux_alu, nr, wm_a, n,  n,   n,   reqno    );
      `RV2ISA_INST_BGEU    :cs( y, br_bgeu, jalx,  imm_b, bm1_rf, y, bm_rf,  y, alu_x,   exmux_alu, nr, wm_a, n,  n,   n,   reqno    );
      default              :cs( n, br_x,  jalx,  imm_x, bm1_x, n, bm_x,   n, alu_x,   exmux_alu, nr, wm_x, n,  n,   n,   reqno    );

    endcase
  end // always_comb

  logic [4:0] rf_waddr_D;
  assign rf_waddr_D = inst_rd_D;
  
  //multiply logic D stage
  
  assign imul_req_val_D = val_D && !stall_D && req_val_D;
  // csrr and csrw logic

  always_comb begin
    proc2mngr_val_D  = 1'b0;
    mngr2proc_rdy_D  = 1'b0;
    csrr_sel_D       = 2'h0;
    stats_en_wen_D   = 1'b0;

    if ( csrw_D && inst_csr_D == `RV2ISA_CPR_PROC2MNGR )
      proc2mngr_val_D    = 1'b1;
    if ( csrr_D && inst_csr_D == `RV2ISA_CPR_MNGR2PROC )
      mngr2proc_rdy_D  = 1'b1;
    if ( csrw_D && inst_csr_D == `RV2ISA_CPR_STATS_EN )
      stats_en_wen_D  = 1'b1;
    if ( csrr_D && inst_csr_D == `RV2ISA_CPR_NUMCORES )
      csrr_sel_D       = 2'h1;
    if ( csrr_D && inst_csr_D == `RV2ISA_CPR_COREID )
      csrr_sel_D       = 2'h2;
  end
//bypass logic

//logic for register 1 bypass
logic  bypass_waddr_X_rs1_D;
logic  bypass_waddr_X_rs2_D;
logic  bypass_waddr_M_rs1_D;
logic  bypass_waddr_M_rs2_D;
logic  bypass_waddr_W_rs1_D;
logic  bypass_waddr_W_rs2_D;
always_comb begin
  if(bypass_waddr_X_rs1_D) begin
    op1_bypass_sel = 2'b01;
  end else if(bypass_waddr_M_rs1_D) begin
    op1_bypass_sel = 2'b10;
  end else if(bypass_waddr_W_rs1_D) begin
    op1_bypass_sel = 2'b11;  
  end else begin
    op1_bypass_sel = 2'b00;
    end
  end
  
//logic for register 2 bypass  
always_comb begin
  if(bypass_waddr_X_rs2_D) begin
    op2_bypass_sel = 2'b01;
  end else if(bypass_waddr_M_rs2_D) begin
    op2_bypass_sel = 2'b10;
  end else if(bypass_waddr_W_rs2_D) begin
    op2_bypass_sel = 2'b11;
  end else begin
    op2_bypass_sel = 2'b00;
    end
  end

  // mngr2proc_rdy signal for csrr instruction

  assign mngr2proc_rdy  = val_D && !stall_D && mngr2proc_rdy_D;

  logic  ostall_mngr2proc_D;
  assign ostall_mngr2proc_D = val_D && mngr2proc_rdy_D && !mngr2proc_val;

  // bypassing for each stage:
  // bypass if address in X matches rs1 in D
  
  assign bypass_waddr_X_rs1_D 
    = val_D && rs1_en_D && val_X && rf_wen_pending_X 
    && (inst_rs1_D == rf_waddr_X) && (rf_waddr_X != 0) && (dmemreq_type_X != ld);

  // bypass if address in X matches rs2 in D
 
  assign bypass_waddr_X_rs2_D 
    = val_D && rs2_en_D && val_X && rf_wen_pending_X 
    && (inst_rs2_D == rf_waddr_X) && (rf_waddr_X != 0) && (dmemreq_type_X != ld);

  // bypass if address in X matches rs1 in M

  assign bypass_waddr_M_rs1_D 
    = val_D && rs1_en_D && val_M && rf_wen_pending_M && 
      (inst_rs1_D == rf_waddr_M) && (rf_waddr_M != 0);

// bypass if address in X matches rs2 in M
  assign bypass_waddr_M_rs2_D 
    = val_D && rs2_en_D && val_M && rf_wen_pending_M && 
      (inst_rs2_D == rf_waddr_M) && (rf_waddr_M != 0); //&& (dmemreq_type_X  != ld);

// bypass if address in W matches rs1 in D

  assign bypass_waddr_W_rs1_D 
    = val_D && rs1_en_D && val_W && rf_wen_pending_W && 
      (inst_rs1_D == rf_waddr_W) && (rf_waddr_W != 0);

  // bypass if address in X matches rs2 in W
  assign bypass_waddr_W_rs2_D 
    = val_D && rs2_en_D && val_W && rf_wen_pending_W && 
      (inst_rs2_D == rf_waddr_W) && (rf_waddr_W != 0);
      
  // ostall if write address in X matches rs1 in D

  logic  ostall_waddr_X_rs1_D;
  assign ostall_waddr_X_rs1_D
    = rs1_en_D && val_X && rf_wen_pending_X
      && ( inst_rs1_D == rf_waddr_X ) && ( rf_waddr_X != 5'd0 ) && (dmemreq_type_X == ld);

  // ostall if write address in X matches rs2 in D

  logic  ostall_waddr_X_rs2_D;
  assign ostall_waddr_X_rs2_D
    = rs2_en_D && val_X && rf_wen_pending_X
      && ( inst_rs2_D == rf_waddr_X ) && ( rf_waddr_X != 5'd0 ) && (dmemreq_type_X == ld);

    
  // Put together ostall signal due to hazards

  logic  ostall_hazard_D;
  assign ostall_hazard_D =
      ostall_waddr_X_rs1_D || ostall_waddr_X_rs2_D;

  // Final ostall signal

  assign ostall_D = val_D && ( ostall_mngr2proc_D || ostall_hazard_D || !imul_req_rdy_D);

  // osquash due to jump instruction in D stage 
  logic osquash_j_D;
  always_comb begin
    if (val_D && (jump_type_D == jal)) begin
      pc_redirect_D = 1'b1;
      pc_sel_D = 2'b10;
    end else begin
      pc_redirect_D = 1'b0;
      pc_sel_D = 2'b0;
      end
    end
    
    
  assign osquash_D = val_D && !stall_D && pc_redirect_D;

  // stall and squash in D

  assign stall_D  = val_D && ( ostall_D || ostall_X || ostall_M || ostall_W );
  assign squash_D = val_D && osquash_X;

  // Valid signal for the next stage

  logic  next_val_D;
  assign next_val_D = val_D && !stall_D && !squash_D;

  //----------------------------------------------------------------------
  // X stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_X = !stall_X;

  logic [31:0] inst_X;
  logic [1:0]  dmemreq_type_X;
  logic        wb_result_sel_X;
  logic        rf_wen_pending_X;
  logic [4:0]  rf_waddr_X;
  logic        proc2mngr_val_X;
  logic        stats_en_wen_X;
  logic [2:0]  br_type_X;
  logic [4:0]  jump_type_X;
  logic        mul_X;

  // Pipeline registers

  always_ff @( posedge clk )
    if (reset) begin
      val_X           <= 1'b0;
      stats_en_wen_X  <= 1'b0;
    end else if (reg_en_X) begin
      val_X           <= next_val_D;
      rf_wen_pending_X<= rf_wen_pending_D;
      inst_X          <= inst_D;
      alu_fn_X        <= alu_fn_D;
      rf_waddr_X      <= rf_waddr_D;
      proc2mngr_val_X <= proc2mngr_val_D;
      dmemreq_type_X  <= dmemreq_type_D;
      wb_result_sel_X <= wb_result_sel_D;
      stats_en_wen_X  <= stats_en_wen_D;
      br_type_X       <= br_type_D;
      ex_result_sel_X <= ex_result_sel_D;
      jump_type_X     <= jump_type_D;
      mul_X           <= req_val_D;
    end

  // branch logic, redirect PC in F if branch is taken

  always_comb begin
    if ( val_X && ( br_type_X == br_bne ) ) begin
      pc_redirect_X = !br_cond_eq_X;
      pc_sel_X      = 2'b1;          // use branch target
    end else if ( val_X && ( br_type_X == br_beq ) ) begin
      pc_redirect_X = br_cond_eq_X;
      pc_sel_X      = 2'b1;         // use branch target
    end else if ( val_X && ( br_type_X == br_blt ) ) begin
      pc_redirect_X = br_cond_lt_x;
      pc_sel_X      = 2'b1;         // use branch target
    end else if ( val_X && ( br_type_X == br_bltu ) ) begin
      pc_redirect_X = br_cond_ltu_x;
      pc_sel_X      = 2'b1;        // use branch target
    end else if ( val_X && ( br_type_X == br_bge ) ) begin
      pc_redirect_X = !br_cond_lt_x;
      pc_sel_X      = 2'b1;        // use branch target
    end else if ( val_X && ( br_type_X == br_bgeu ) ) begin
      pc_redirect_X = !br_cond_ltu_x;
      pc_sel_X      = 2'b1;        // use branch target
    end else if (val_X && (jump_type_X == jalr)) begin
      pc_redirect_X = 1'b1;
      pc_sel_X = 2'b11;           // use jump target
    end else begin
      pc_redirect_X = 1'b0;
      pc_sel_X      = 2'b0;          // use pc+4
    end
  end

//x stage is ready for a value
  assign imul_resp_rdy_X = val_X && !stall_X && mul_X;

//memory load and store word logic
  assign mem_type = (val_X && !stall_X && dmemreq_type_X == st)? 3'd1 : 3'd0; 
  // ostall due to dmemreq not ready.

  assign ostall_X = val_X && ((( dmemreq_type_X != nr ) && !dmemreq_rdy) || (!imul_resp_val_X && mul_X));

  // osquash due to taken branch, notice we can't osquash if current
  // stage stalls, otherwise we will send osquash twice.

  assign osquash_X = val_X && !stall_X && pc_redirect_X;

  // stall and squash used in X stage

  assign stall_X = val_X && ( ostall_X || ostall_M || ostall_W );

  // set dmemreq_val only if not stalling

  assign dmemreq_val = val_X && !stall_X && ( dmemreq_type_X != nr );

  // Valid signal for the next stage

  logic  next_val_X;
  assign next_val_X = val_X && !stall_X;

  //----------------------------------------------------------------------
  // M stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_M  = !stall_M;

  logic [31:0] inst_M;
  logic [1:0]  dmemreq_type_M;
  logic        rf_wen_pending_M;
  logic [4:0]  rf_waddr_M;
  logic        proc2mngr_val_M;
  logic        stats_en_wen_M;

  // Pipeline register

  always_ff @( posedge clk )
    if (reset) begin
      val_M            <= 1'b0;
      stats_en_wen_X   <= 1'b0;
    end else if (reg_en_M) begin
      val_M            <= next_val_X;
      rf_wen_pending_M <= rf_wen_pending_X;
      inst_M           <= inst_X;
      rf_waddr_M       <= rf_waddr_X;
      proc2mngr_val_M  <= proc2mngr_val_X;
      dmemreq_type_M   <= dmemreq_type_X;
      wb_result_sel_M  <= wb_result_sel_X;
      stats_en_wen_M   <= stats_en_wen_X;
    end

  // ostall due to dmemresp not valid

  assign ostall_M = val_M && ( dmemreq_type_M != nr ) && !dmemresp_val;

  // stall M

  assign stall_M = val_M && ( ostall_M || ostall_W );

  // Set dmemresp_rdy if valid and not stalling and this is a lw/sw

  assign dmemresp_rdy = val_M && !stall_M && ( dmemreq_type_M != nr );

  // Valid signal for the next stage

  logic  next_val_M;
  assign next_val_M = val_M && !stall_M;

  //----------------------------------------------------------------------
  // W stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_W = !stall_W;

  logic [31:0] inst_W;
  logic        proc2mngr_val_W;
  logic        rf_wen_pending_W;
  logic        stats_en_wen_pending_W;

  // Pipeline registers

  always_ff @( posedge clk ) begin
    if (reset) begin
      val_W            <= 1'b0;
      stats_en_wen_pending_W   <= 1'b0;
    end else if (reg_en_W) begin
      val_W            <= next_val_M;
      rf_wen_pending_W <= rf_wen_pending_M;
      inst_W           <= inst_M;
      rf_waddr_W       <= rf_waddr_M;
      proc2mngr_val_W  <= proc2mngr_val_M;
      stats_en_wen_pending_W   <= stats_en_wen_M;
    end
  end

  // write enable

  assign rf_wen_W       = val_W && rf_wen_pending_W;
  assign stats_en_wen_W = val_W && stats_en_wen_pending_W;

  // ostall due to proc2mngr

  assign ostall_W = val_W && proc2mngr_val_W && !proc2mngr_rdy;

  // stall and squash signal used in W stage

  assign stall_W = val_W && ostall_W;

  // proc2mngr port

  assign proc2mngr_val = val_W && !stall_W && proc2mngr_val_W;

  assign commit_inst = val_W && !stall_W;

endmodule

`endif

