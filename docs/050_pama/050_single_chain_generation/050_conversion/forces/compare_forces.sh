paste single_point_gmx/forces_gmx.dat single_point_lmp/forces_lmp.dat | \
awk '{
  dx = $2 - $6
  dy = $3 - $7
  dz = $4 - $8
  diff = sqrt(dx*dx + dy*dy + dz*dz)
  fg   = sqrt($2*$2 + $3*$3 + $4*$4)
  fl   = sqrt($6*$6 + $7*$7 + $8*$8)
  printf "%d %.6f %.6f %.6f\n", $1, fg, fl, diff
}' > force_compare.dat


awk '{if ($4 > max) {max=$4; a=$1}} END {print "Max ΔF:",max,"atom",a}' force_compare.dat
