from fpdf import FPDF
import sys
import os

def write_full_letter(letter, x, y, pdf):
    pdf.set_font('Arial', 'B', 16)
    pdf.text(x+3,y+7,letter)

def write_small_number(number, x, y, pdf):
    pdf.set_font('Arial', 'B', 8)
    pdf.text(x+0.5,y+2.8,number)

def write_black_square(x, y, square_size,pdf):
    pdf.set_fill_color(0)
    pdf.rect(x=x, y=y, w=square_size, h=square_size, style="FD")
    pdf.set_fill_color(255)

def read_in_solution(filename):
    with open(filename, "r") as input_file:
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

def print_column(pdf, col_x,col_y,column_width, column_height, questions, index):
    # pdf.multi_cell(x,y+5, test_text)
    pdf.set_font('Arial', '', 12)
    pdf.set_y(col_y)
    while pdf.get_y() < pdf.h-40:
        print(len(questions), index, questions[index])
        if questions[index] == "across":
            pdf.set_x(col_x)
            pdf.set_font('Arial', 'B', 14)
            pdf.text(col_x+30,pdf.get_y(), "Across")
            pdf.set_font('Arial', '', 12)
            index=index+1
        if questions[index] == "down":
            pdf.set_x(col_x)
            pdf.set_font('Arial', 'B', 14)
            pdf.text(col_x+30,pdf.get_y()+8, "Down")
            pdf.set_font('Arial', '', 12)
            pdf.set_y(pdf.get_y()+10)
            index=index+1
        pdf.set_x(col_x)
        print(pdf.get_y())
        pdf.multi_cell(column_width,column_height, questions[index], align="L")
        index+=1
    return index

def write_puzzle(grid, grid_to_num, square_size, pdf, solution=True):
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
                    write_full_letter(c, x, y, pdf)
                if (i,j) in grid_to_num:
                    write_small_number(str(grid_to_num[(i,j)]), x, y, pdf)

    # write out the clues
    pdf.set_font('Arial', 'B', 16)
    column_width = 68
    first_colum_x = 5
    first_colum_y = 7
    second_colum_x = 70
    second_colum_y = square_size*len(grid)+10
    third_colum_x = 135
    third_colum_y = square_size*len(grid)+10
    x = first_colum_x
    y = first_colum_y

    text=[]
    scratch_text = "This is a longer clue that goes over multiple lines"
    text.append("across")
    qs=60
    for i in range(qs):
        text.append(str(i) + ": "+ scratch_text)
        if i == int(qs/2):
            text.append("down")

    index = print_column(pdf, first_colum_x, first_colum_y, column_width, 5, text, 0)
    index = print_column(pdf, second_colum_x, second_colum_y, column_width, 5, text, index)
    index = print_column(pdf, third_colum_x, third_colum_y, column_width, 5, text, index)

    




    # ## colum 2
    # pdf.set_y(second_colum_y)
    # pdf.set_x(second_colum_x)
    # while pdf.get_y() < pdf.h-50:
    #     pdf.set_x(second_colum_x)
    #     pdf.multi_cell(column_width,5, test_text, align="L")
    
    # for i in range(2):
    #     pdf.set_x(50)
    #     pdf.text(x+30,y, "Across")
    #     pdf.multi_cell(50,5, test_text, align="R")




input_filename = sys.argv[1]
grid = read_in_solution(input_filename)
filename = os.path.splitext(input_filename)[0]

grid_to_num, vertical, horizontal = gen_numbers(grid)
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
square_size=9
write_puzzle(grid, grid_to_num, square_size, pdf, solution=False)
pdf.add_page()
write_puzzle(grid, grid_to_num, square_size,pdf, solution=True)
pdf.output(filename+"_sol"+".pdf")
