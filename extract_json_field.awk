BEGIN{
    FS="\"" 
}
{ 
    for(i=1; i<=NF; i++) { 
        if($i == field) print $(i+2) 
    } 
}
