# Pipeline-Simulator RV32I
logic used: check if stalls print stall else print the stage and the instruction. Only Load causes 2 stalls, if forwarding than no stalls.
so check for load instruction causing stall, no need to do anything for forwarding or bypassing. get the target address in the ID stage
and Compute branch taken in EX stage, so empty the instructions in the ID/IF registers if branch and fetch the new instructions in next cycle
(predict not taken branch prediction technique)
