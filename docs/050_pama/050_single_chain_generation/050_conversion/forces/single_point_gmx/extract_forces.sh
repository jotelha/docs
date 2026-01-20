gmx traj -s singlepoint.tpr -f singlepoint.trr -of force.xvg
awk '
NR>17 {
  for (i=2;i<=NF;i++) {
    if (sqrt($i*$i) > max) max=sqrt($i*$i)
  }
}
END { print max }
' force.xvg


awk '
!/^[@#]/ {
  for (i=2; i<=NF; i+=3) {
    atom = (i-2)/3 + 1
    fx = $i
    fy = $(i+1)
    fz = $(i+2)
    printf "%d %.8f %.8f %.8f\n", atom, fx, fy, fz
  }
  exit
}
' force.xvg > forces_gmx.dat
