firstletter="B C D E F G H I J"
secondletter="A B C D E F G H I J"
for value in $firstletter
do
for value2 in $secondletter
do
directory="vsw-ortho-SP-$value$value2"
mkdir $directory
cd $directory
file1="vsw-ortho-SP-"$value$value2".in"
file2="vsw-ortho-SP-"$value$value2".sh"
cat << EOM >$file1
GRIDFILE    /sc/arion/projects/H_filizm02a/soumyo/kor_nam/structures/grid_mutation_change_loop_model_ortho_clsto_JDTic/glide-grid_1/glide-grid_1.zip
LIGANDFILE  /sc/arion/projects/H_filizm02a/ZINC20_3d/20210406_glide_ready_zinc/${value}${value2}_out.maegz
PRECISION   SP
EOM
cat << EOM >$file2
"\${SCHRODINGER}/glide" vsw-ortho-SP-$value$value2.in -OVERWRITE -adjust -HOST private-FEPdriver -SUBHOST Chimera-Long-lic03-VS -TMPDIR /sc/arion/scratch/sens05/.tmp_schrodinger/
EOM
cd ../
done
done
