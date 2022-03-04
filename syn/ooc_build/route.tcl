open_checkpoint chirp_gen_build/chirp_gen_synth.dcp
opt_design
place_design
phys_opt_design
route_design
write_checkpoint -force chirp_gen_build/chirp_gen_route.dcp
report_timing_summary -file chirp_gen_build/route_timing_summary.txt
report_timing -sort_by group -max_paths 100 -path_type summary -file chirp_gen_build/route_timing.txt
report_utilization -file chirp_gen_build/route_util.txt
