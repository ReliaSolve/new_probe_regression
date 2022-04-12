#!/bin/bash
#############################################################################
# Run regression tests against the current CCTBX/Probe and a
# specified original to check for differences between the results.
#
#############################################################################

######################
# Parse the command line

orig="8c9ac5a1ffc372f4f83152a0ec33c0426bfdd413"
if [ "$1" != "" ] ; then orig="$1" ; fi

echo "Checking against $orig"

#####################
# Make sure the probe submodule is checked out

echo "Updating submodule"
git submodule update --init
(cd probe; git pull) &> /dev/null 

######################
# The original version is build using Make because older versions don't
# have CMakeLists.txt files.

echo "Building $orig"
(cd probe; git checkout $orig; make) &> /dev/null 

orig_exe="./probe/probe"
orig_args="-quiet -kin -mc -self "all" -count -sepworse"
new_exe="mmtbx.probe2"
new_args='source_selection="all" record_added_hydrogens=False approach=self count_dots=True output.separate_worse_clashes=True'

######################
# Generate two outputs for each test file, redirecting standard
# output and standard error to different files.  This also causes the atom
# dump files, which are what we actually compare.
# Test the dump files to see if any differences are other than we expect.

echo
mkdir -p outputs
files=`(cd fragments; ls *.pdb)`
failed=0
for f in $files; do
  # Full input-file name
  inf=fragments/$f

  # File base name
  base=`echo $f | cut -d \. -f 1`

  # We must extract to a file and then run with that file as a command-line argument
  # because the original version did not process all models in a file when run with
  # the model coming on standard input.
  tfile=outputs/temp_file.tmp
  cp $inf $tfile

  ##############################################

  echo "Testing structure $base"
  # Run old and new versions in parallel
  ($orig_exe $orig_args -DUMPATOMS outputs/$base.orig.dump $tfile > outputs/$base.orig.out 2> outputs/$base.orig.stderr) &
  ($new_exe $new_args output.file_name=outputs/$base.new.out output.dump_file_name=outputs/$base.new.dump $tfile > outputs/$base.new.stdout 2> outputs/$base.new.stderr) &
  wait

  # Test for unexpected differences in atom-dump files.  The script returns messages when there
  # are any differences.  Threshold for significant difference between atom
  # positions is set.
  THRESH=0.05
  d=`python compare_dump_files.py outputs/$base.orig.dump outputs/$base.new.dump $THRESH`
  echo "$d" > outputs/$base.compare
  s=`echo -n $d | wc -c`
  if [ $s -ne 0 ]; then echo " Dump comparison Failed!"; failed=$((failed + 1)); fi

  # Test for unexpected differences in total counts.
  grep tot outputs/$base.orig.out > outputs/$base.orig.tot
  grep tot outputs/$base.new.out > outputs/$base.new.tot
  d=`diff outputs/$base.orig.tot outputs/$base.new.tot`
  s=`echo -n $d | wc -c`
  if [ $s -ne 0 ]; then echo " Score comparison Failed!"; failed=$((failed + 1)); fi

  # Done with the input file.
  rm -f $tfile

done

echo
if [ $failed -eq 0 ]
then
  echo "Success!"
else
  echo "$failed comparisons failed"
fi

exit $failed

