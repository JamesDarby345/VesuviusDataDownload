def convert_txt_to_csv(input_path, output_path):
    with open(input_path, "r") as input_file:
        lines = input_file.read().split(";")
        data = [line.strip().split() for line in lines if line.strip()]

    with open(output_path, "w") as output_file:
        output_file.write("jy,jx,jz\n")  # Writing the header
        for row in data:
            if len(row) == 3:  # Ensuring each row has exactly 3 elements
                output_file.write(",".join(row) + "\n")

input_file_path = 'temp.txt'
output_file_path = 'Scroll1_gp_grid_mask.csv'

# Perform the conversion
convert_txt_to_csv(input_file_path, output_file_path)