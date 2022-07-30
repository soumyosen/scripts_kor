firstletter="B C D E F G H I J"
secondletter="A B C D E F G H I J"

sum1=0
for value1 in $firstletter
do
     for value2 in $secondletter
     do
           directory="vsw-ortho-SP-$value1$value2"
           cd $directory/
           file1="vsw-ortho-SP-"$value1$value2"_subjobs.log"
           file2="vsw-ortho-SP-"$value1$value2"_pv.maegz"
           echo "$file1"
           if [ -f "$file1" ]; then
                 grep "DOCKING RESULTS FOR LIGAND" $file1 > check_progress_output.log
                 awk '{ print $5 }' check_progress_output.log > check_progress_output1.log
                 final_lig=$( tail -n 1 check_progress_output1.log )
                 rm check_progress_output*
                 if [ -f "$file2" ]; then
                       marker=1
                 else
                       marker=0
                 fi
           fi       
           cd ..
           echo "$value1$value2 $final_lig $marker" >> output_progress_bylogfile1.log   
           sum1=$((sum1 + final_lig))
     done
done
    
echo "number of ligands docked $sum1" 
echo "number of ligands docked $sum1" >> output_progress_bylogfile1.log 



