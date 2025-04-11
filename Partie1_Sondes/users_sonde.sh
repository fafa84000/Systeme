echo -e "sonde\t`hostname`\tusers\t`who | wc -l`"; nc -N $1 $2;

# $1 ex: "localhost"
# $2 ex: 5000