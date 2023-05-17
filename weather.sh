#!/bin/bash
user_ip=$(curl -s ifconfig.me)
states=(NY CA IL TX AZ PA FL)
if [ ! -f "tagsoup-1.2.1.jar" ]
    then 
    wget "https://repo1.maven.org/maven2/org/ccil/cowan/tagsoup/tagsoup/1.2.1/tagsoup-1.2.1.jar"
fi

while true 
do
    i=1
    rm *.html
    rm *.xhtml
    for state in ${states[@]}
    do
        curr_data=`date +"%Y-%m-%d-%H-%M-%S-$state".html`
        link=$(sed -n "$i"p sources.txt)    
        curl $link > $curr_data
        java -jar tagsoup-1.2.1.jar --files $curr_data
        python3 Parser.py *$state.xhtml $user_ip $state
       ((i++)) 

    done
    sudo cp UI.php /var/www/html
    # command to drop tables quick drop tables AZ_T,NY_T,IL_T,PA_T,TX_T,CA_T,FL_T;
    sleep 6h
done
