user_input  = input("List of ascii code delimited by ,:" + "\n") #take user input into the user_input variable
to_list = user_input.split(",") # turn the user inputs from string into a list delimited by ,
convert_to_int = [int(k) for k in to_list] # turn each element of the list from string to integer
new =   []
for i in convert_to_int:#converts the arry of ascii code into letters
    result = chr(i)
    new.append(result)

print("".join(new))
