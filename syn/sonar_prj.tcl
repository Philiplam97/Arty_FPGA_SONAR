add_files -norecurse [file dirname [info script]]/../src/chirp_gen/scripts/chirp_rom_data.txt

read_vhdl -vhdl2008 [file dirname [info script]]/../src/sonar_pkg.vhd

read_vhdl -vhdl2008 [file dirname [info script]]/../src/chirp_gen/chirp_gen.vhd
read_vhdl -vhdl2008 [file dirname [info script]]/../src/chirp_gen/large_clk_div.vhd
read_vhdl -vhdl2008 [file dirname [info script]]/../src/I2S/I2S.vhd
												 
read_vhdl -vhdl2008 [file dirname [info script]]/../src/common/debouncer.vhd
read_vhdl -vhdl2008 [file dirname [info script]]/../src/common/sync_2FF.vhd
												 
read_vhdl -vhdl2008 [file dirname [info script]]/../src/arty_SONAR_top.vhd
