from __future__ import print_function, nested_scopes, generators, division
from __future__ import absolute_import
import sys, math

def atomID(s):
  # Return the ID of the atom, which includes its chain, residue name,
  # residue number, atom name, and alternate separated by spaces
  w = s.split()
  return w[0]+" "+w[1]+" "+w[2]+" "+w[3]+" "+w[4]

def position(s):
  # Return a tuple that has the location of the atom.
  w = s.split()
  return ( float(w[5]), float(w[6]), float(w[7]) )

def radius(s):
  # Return the radius for the atom.
  w = s.split()
  return ( w[8] )

def flag(s,f):
  # Return a flag for the atom, indexed by 0-2.
  w = s.split()
  return ( w[9+f] )

def distance(a, b):
  # Return the distance between 3-space tuples a and b
  return math.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 )

def run_comparison(fileName1, fileName2, thresh, verbosity = 10):
  # Read the the data from each file.
  # Sort the lines from the file so that we'll get chain, residue, atom name sorting.

  if verbosity >= 1:
    print('Reading data from',fileName1)
  with open(fileName1) as f:
    m1 = f.readlines()
  m1.sort(key=lambda x:atomID(x))

  if verbosity >= 1:
    print('Reading model from',fileName2)
  with open(fileName2) as f:
    m2 = f.readlines()
  m2.sort(key=lambda x:atomID(x))

  # Compare the two and report on any differences.
  # Both lists are sorted, so we'll know which has a missing element compared
  # to the other.  We walk from the beginning to the end of each list.
  m1ID = 0
  m2ID = 0
  while m1ID < len(m1) and m2ID < len(m2):
    if verbosity >= 5:
      print('      Checking atoms',m1ID,'and',m2ID)

    # Atom names are unique within residues, so we can use that to
    # match atoms in one file from those in the other and print out
    # missing atoms and differences in positions.
    if atomID(m1[m1ID]) < atomID(m2[m2ID]):
      print('Only in first:',atomID(m1[m1ID]))
      m1ID += 1
      continue

    if atomID(m1[m1ID]) > atomID(m2[m2ID]):
      print('Only in second:',atomID(m2[m2ID]))
      m2ID += 1
      continue

    # Check the radius to see if they differ
    oldRadius = radius(m1[m1ID])
    newRadius = radius(m2[m2ID])
    if oldRadius != newRadius:
      print(atomID(m1[m1ID])+' radii differ: old is {}, new is {}'.format(oldRadius,newRadius))

    # Check the flag fields to see if any of them differ
    for f in range(3):
      oldFlag = flag(m1[m1ID], f)
      newFlag = flag(m2[m2ID], f)
      if oldFlag != newFlag:
        print(atomID(m1[m1ID])+' flags differ: old is {}, new is {}'.format(oldFlag,newFlag))

    # Check the distance between the atoms.
    dist = distance(position(m1[m1ID]),position(m2[m2ID]))
    if dist > thresh:
      print(atomID(m1[m1ID])+' Distance between runs: {:.2f}'.format(dist))

    # Go on to next line
    m1ID += 1
    m2ID += 1

  # Finish up either list that is not done
  while m1ID < len(m1):
    print('Only in first:',atomID(m1[m1ID]))
    m1ID += 1
  while m2ID < len(m2):
    print('Only in second:',atomID(m2[m2ID]))
    m2ID += 1

if __name__ == "__main__":

  threshold = 0.02
  verbosity = 0
  if len(sys.argv) < 3:
    print('Usage:',sys.argv[0],'FILE1 FILE2 [threshold [verbosity]]')
    print('  threshold: Distance atoms must be apart to be reported: default',threshold)
    print('  verbosity: Amount of extra information to print: default',verbosity)
    sys.exit(1)

  try:
    threshold = float(sys.argv[3])
  except:
    pass

  try:
    verbosity = int(sys.argv[4])
  except:
    pass

  run_comparison(sys.argv[1], sys.argv[2], threshold, verbosity)

  sys.exit(0)

