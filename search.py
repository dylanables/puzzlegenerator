from flask import render_template, request, make_response
import random, string, json
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from fpdf import FPDF
from __main__ import app
client = OpenAI()

def get_words(prompt_req):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output words in all uppercase for a word search puzzle in JSON. Create a valid json array of strings with a key name of 'words'"},
            {"role": "user", "content": prompt_req}
        ]
    )
    json_response = json.loads(response.choices[0].message.content)
    print(json_response)
    words = json_response['words']
    print(words)
    
    return words

def make_grid(words, backwards_allowed):
    grid_size = 20
    print(backwards_allowed)
    orientations = ['leftright', 'rightleft', 'up', 'down', 'rightup', 'rightdown', 'leftup', 'leftdown']
    if backwards_allowed == False:
        orientations = ['leftright', 'down', 'rightup', 'rightdown']
    print(orientations)

    # populate a grid_size x grid_size grid with underscores
    grid = [['_' for _ in range(grid_size)] for _ in range(grid_size)]

    for word in words:
        word_length = len(word)

        placed = False
        while not placed:
            orientation = random.choice(orientations)

            if orientation == 'leftright':
                step_x = 1
                step_y = 0
            if orientation == 'rightleft':
                step_x = -1
                step_y = 0
            if orientation == 'up':
                step_x = 0
                step_y = -1
            if orientation == 'down':
                step_x = 0
                step_y = 1
            if orientation == 'rightup':
                step_x = 1
                step_y = -1
            if orientation == 'rightdown':
                step_x = 1
                step_y = 1
            if orientation == 'leftup':
                step_x = -1
                step_y = -1
            if orientation == 'leftdown':
                step_x = -1
                step_y = 1

            # choosing random starting position for word
            x_pos = random.randint(0, grid_size-1)
            y_pos = random.randint(0, grid_size-1)

            # determine if word can fit in grid with it's starting position
            ending_x = x_pos + word_length*step_x
            ending_y = y_pos + word_length*step_y

            if ending_x < 0 or ending_x >= grid_size: continue
            if ending_y < 0 or ending_y >= grid_size: continue

            failed = False

            for i in range(word_length):
                character = word[i]

                curr_x = x_pos + i*step_x
                curr_y = y_pos + i*step_y

                character_curr_pos = grid[curr_x][curr_y]
                if character_curr_pos != '_':
                    if character_curr_pos == character:
                        continue
                    else:
                        failed = True
                        break
                
            if failed:
                continue
            else:
                # place word
                for i in range(word_length):
                    character = word[i]

                    curr_x = x_pos + i*step_x
                    curr_y = y_pos + i*step_y

                    grid[curr_x][curr_y] = character

                placed = True

    # fill rest of grid with random letters
    for x in range(grid_size):
        for y in range(grid_size):
            if (grid[x][y] == '_'):
                grid[x][y] = random.choice(string.ascii_uppercase)

    return grid

def save_pdf(prompt, grid, words):
    pdf = FPDF(orientation = 'P',unit = 'mm', format='A4')

    pdf.add_page()
    gridx = 200
    gridy = 8

    pdf.set_font("Arial", size = 25)
    title = prompt.upper()
    pdf.cell(gridx, 10, txt = title, ln = 1, align = 'C')

    pdf.set_font("Courier", size = 12)
    pdf.cell(gridx, gridy, txt = "", ln = 1) 
    # create a cell
    for i in grid:
        x = "  ".join(i)
        pdf.cell(gridx, gridy, txt = x, ln = 1, align = 'C')
    
    pdf.set_font("Courier", size = 12)
    pdf.cell(gridx, gridy, txt = "", ln = 1) 
    hints_per_row = 5
    split_lists = [words[x:x+hints_per_row] for x in range(0, len(words), hints_per_row)]
    for i in split_lists:
        wordx = ", ".join(i)
        pdf.cell(gridx, 10, txt = wordx, ln = 1, align = 'C')
    
    response = make_response(pdf.output("wordsearch.pdf"))
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route("/wordsearch", methods=['GET'])
def wordsearch():
    if request.method == 'GET':
        prompt = request.args.get('prompt')
        if prompt:
            backwards = request.args.get('backwards', type=int)
            backwards_allowed = True
            if backwards == 0:
                backwards_allowed = False
            print(backwards_allowed)
            prompt_req = "Provide 10 unique words (no spaces or hyphens) related to " + prompt + "?"
            words = get_words(prompt_req)
            grid = make_grid(words, backwards_allowed)
            return render_template("wordsearch.html", prompt=string.capwords(prompt), grid=grid, words=words)
        else:
            return render_template("wordsearch.html", prompt=prompt)
    else:
        prompt = ''
        return render_template("wordsearch.html", prompt=prompt)