#!/usr/bin/env python3

f = open("/home/kali/test/projects/read.txt", "r") #open file at location as read -> will be made a backup after this
copy = open("/home/kali/test/projects/write.txt", "w") #note that the copy file location does not need to exist before running
for line in f: #reads each line in the file
    if line == "is\n": # this can also be written as [if "<text>" in line:]
        #insert user_input()
            #rewrite yes or no?
                #if user_input == yes:
        copy.write("isn't\n") #----->
                #else:
                    #copy.write(line)
    else:
        copy.write(line)
f.close()
copy.close()

if __name__ == "__main__":
    print("Complete")
