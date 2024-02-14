from fpdf import FPDF
import sys
import os

def write_full_letter(letter, x, y, conf, pdf):
    pdf.set_font('Arial', 'B', conf["header_font"])
    square_size=conf["square_size"]
    y_plus = square_size/2 + conf["header_font"]/8
    x_plus = square_size/2 - conf["header_font"]/8
    pdf.text(x+x_plus,y+y_plus,letter)

def write_small_number(number, x, y, conf, pdf):
    fsize = conf["q_font"] - 4
    pdf.set_font('Arial', 'B', fsize)
    square_size=conf["square_size"]
    x_plus = 0.5
    y_plus = fsize/4 + 0.5
    pdf.text(x + x_plus,y+ y_plus,number)

def write_black_square(x, y, square_size,pdf):
    pdf.set_fill_color(0)
    pdf.rect(x=x, y=y, w=square_size, h=square_size, style="FD")
    pdf.set_fill_color(255)

def read_in_solution(filename):
    full_filename = "./puzzles/"+filename+"/grid.txt"
    with open(full_filename, "r") as input_file:
        lines = input_file.readlines()

    lines = [line.strip() for line in lines]
    return lines

def vline(i, j, grid, min_word_length):
    if i + min_word_length >= len(grid):
        return False
    for k in range(i+1, i+min_word_length):
        if grid[k][j] == "#":
            return False
    return True

def hline(i, j, grid, min_word_length):
    if j + min_word_length >= len(grid[i]):
        return False
    for k in range(j+1, j+min_word_length):
        if grid[i][k] == "#":
            return False
    return True

def gen_numbers(grid, min_word_length=2):
    vertical = []
    horizontal = []
    grid_to_num = {}
    counter = 1
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            hit=False
            if grid[i][j] == "#":
                continue
            if (i == 0 or grid[i-1][j] == "#") and vline(i,j,grid,min_word_length):
                vertical.append(counter)
                hit=True
            if (j == 0 or grid[i][j-1] == "#") and hline(i,j,grid,min_word_length):
                horizontal.append(counter)
                hit=True
            if hit:
                grid_to_num[(i,j)] = counter
                counter+=1
    return grid_to_num, vertical, horizontal

def print_column(pdf, conf, questions, index, col_num):
    # pdf.multi_cell(x,y+5, test_text)
    col_x=5
    col_y=7
    square_size=conf["square_size"]
    grid_size=conf["grid_size"]
    if col_num > 0:
        col_x=col_x+(conf["width"]*col_num)
        col_y=square_size*grid_size+10

    pdf.set_font('Arial', '', conf["q_font"])
    pdf.set_y(col_y)
    while pdf.get_y() < pdf.h-38 and index < len(questions):
        if questions[index] == "across":
            pdf.set_x(col_x)
            pdf.set_font('Arial', 'B', conf["header_font"])
            pdf.text(col_x+17,pdf.get_y(), "Across")
            pdf.set_y(pdf.get_y()+3)
            pdf.set_font('Arial', '', conf["q_font"])
            index=index+1
        if questions[index] == "down":
            pdf.set_x(col_x)
            pdf.set_font('Arial', 'B', conf["header_font"])
            pdf.text(col_x+30,pdf.get_y()+8, "Down")
            pdf.set_font('Arial', '', conf["q_font"])
            pdf.set_y(pdf.get_y()+10)
            index=index+1
        pdf.set_x(col_x)
        pdf.multi_cell(conf["width"]-2,conf["height"], questions[index], align="L")
        index+=1
    return index

def write_out_template_clues(filename, vertical, horizontal):
    full_filename = "./puzzles/"+filename+"/template.txt"
    with open(full_filename, "w") as output_file:
        output_file.write("across\n")
        for i in vertical:
            output_file.write(str(i)+":" + "\n")
        output_file.write("down\n")
        for i in horizontal:
            output_file.write(str(i)+":" + "\n")

def get_clues(filename):
    #first check if a file exists
    question_file = "./puzzles/"+filename+"/question.txt"
    template_file = "./puzzles/"+filename+"/template.txt"
    if os.path.isfile(question_file):
        print("found questions text file")
        with open(question_file, "r") as input_file:
            lines = input_file.readlines()
        return [line.strip() for line in lines]
    else:
        with open(template_file, "r") as input_file:
            lines = input_file.readlines()
        return [line.strip() for line in lines]

def write_puzzle(grid, grid_to_num, conf, pdf, solution=True):
    n=len(grid)
    square_size=conf[n]["square_size"]
    pdf.set_fill_color(255)
    x_required = square_size*len(grid[0])
    start_x = pdf.w - (x_required + 5)
    print("page width", pdf.w, "page height", pdf.h, "x_required", x_required)
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            x = start_x+square_size*j
            y = 5+square_size*i
            if c == "#":
                write_black_square(x, y, square_size,pdf)
            else:
                pdf.rect(x=x, y=y, w=square_size, h=square_size, style="FD")
                if solution:
                    write_full_letter(c, x, y, conf[n], pdf)
                if (i,j) in grid_to_num:
                    write_small_number(str(grid_to_num[(i,j)]), x, y, conf[n], pdf)

def write_clues(clues, grid, conf, pdf):
    # write out the clues
    n = len(grid)
    index = 0
    for col_num in range(conf[n]["cols"]):
        index = print_column(pdf, conf[n], clues, index, col_num)


conf = {}
conf[8] = {"width": 70, "height":7, "header_font": 20, "q_font": 16, "cols":3, "grid_size": 8, "square_size": 15}
conf[15] = {"width": 70, "height":5, "header_font": 16, "q_font": 12, "cols":3, "grid_size": 15, "square_size": 10}
conf[17] = {"width": 50, "height":4, "header_font": 16, "q_font": 10, "cols":4, "grid_size": 17, "square_size": 9}

input_filename = sys.argv[1]
grid = read_in_solution(input_filename)
filename = os.path.splitext(input_filename)[0]
grid_to_num, vertical, horizontal = gen_numbers(grid)
write_out_template_clues(filename, horizontal, vertical)
clues = get_clues(filename)
print (clues)
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
write_puzzle(grid, grid_to_num, conf, pdf, solution=False)
write_clues(clues, grid, conf, pdf)
pdf.add_page()
write_puzzle(grid, grid_to_num, conf, pdf, solution=True)
write_clues(clues,grid, conf, pdf)

full_filename = "./puzzles/"+filename+"/"+filename+".pdf"
pdf.output(full_filename)
