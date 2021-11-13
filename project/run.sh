for size_key in 49 #128 256 512 768 1024
do
    prime_size=$(($size_key / 2))
    prime1=$(openssl prime -generate -bits $prime_size)
    prime2=$(openssl prime -generate -bits $prime_size)
    echo '---RSA-'$size_key'---'
    python lenstra_factor.py $prime1 $prime2 $(($size_key*10)) #> logRSA$size_key.txt
done 
