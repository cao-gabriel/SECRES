# generate alice directory and bob directory
mkdir alice bob
cd alice/
# alice generates a private key of size 1024 bits and write it in the file my_private_key.pem
openssl genrsa -out alice_private_key.pem 1024
# alice extracts public key from private key
openssl rsa -in alice_private_key.pem -pubout -out alice_public_key.pem
# alice send her public key to bob
cp alice_public_key.pem ../bob/
# bob creates a file
cd ../bob/
echo 'Travaux pratiques' > message.txt
# bob encrypts the file with the public key of alice
openssl rsautl -encrypt -inkey alice_public_key.pem -pubin -in message.txt -out encrypted_message.txt
# bob send the encrypted file to alice
cp encrypted_message.txt ../alice/
# alice decrypt the file
cd ../alice/
openssl rsautl -decrypt -inkey alice_private_key.pem -in encrypted_message.txt
# the text on the standard output should be the secret message that bob sent, here it should be 'Travaux pratiques'
