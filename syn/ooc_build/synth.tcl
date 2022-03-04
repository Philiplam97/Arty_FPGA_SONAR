source ../sonar_prj.tcl
read_xdc ooc_timing.xdc -mode out_of_context
synth_design -mode out_of_context -flatten_hierarchy rebuilt -top chirp_gen -part XC7A35TICSG324-1L  -assert
write_checkpoint -force chirp_gen_build/chirp_gen_synth.dcp
report_timing_summary -file chirp_gen_build/synth_timing_summary.txt
