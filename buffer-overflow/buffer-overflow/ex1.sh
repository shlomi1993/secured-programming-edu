gcc -o ex1.out ex1.c -fno-stack-protector -z execstack -g -m32
# Consider: sudo chown root ex1.out && sudo chmod +s ex1.out