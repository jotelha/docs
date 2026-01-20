awk '
$1=="ITEM:" && $2=="ATOMS" {reading=1; next}
$1=="ITEM:" {reading=0}
reading {
  atom++
  printf "%d %.8f %.8f %.8f\n", atom, $1, $2, $3
}
END { }
' forces.lammpstrj > forces_lmp_raw.dat

awk '{
  printf "%d %.8f %.8f %.8f\n", $1, $2*41.84, $3*41.84, $4*41.84
}' forces_lmp_raw.dat > forces_lmp.dat
