firstletter="B C D E F G H I J"
secondletter="A B C D E F G H I J"

for value1 in $firstletter
do
     for value2 in $secondletter
     do
           directory="vsw-ortho-SP-$value1$value2"
           cd $directory/
           file2="vsw-ortho-SP-"$value1$value2"_pv.maegz"
           echo "$directory"
           if [ -f "$file2" ]; then
                 marker=1
           else
                 marker=0
           fi       
           cd ..
           echo "$value1$value2 $final_lig $marker" >> output_present1.log   
     done
done
    



