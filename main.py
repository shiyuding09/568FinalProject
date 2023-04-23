from flask import Flask, render_template, request, redirect, url_for
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = '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'
# Set up the GPT engine
engine = "gpt-3.5-turbo"
rules = (f"You are the Keeper for Call of Cthulhu. You should follow the Keeper Rulebook of COC and make sure the user follows the rule of the investigator handbook"
          f"1. Play the game in turns, starting with you.\n"
          f"2. The game output will always show 'Turn number', 'Time period of the day', 'Current day number', 'Weather', Location', 'Description', 'Abilities', and 'Possible Commands', 'Current Character setting','current item' of the roles.\n"
          f"3. Always wait for the player’s next command.\n"
          f"4. Stay in character as a keeper and respond to commands the way a keeper should.\n"
          f"5. Wrap all game output in code blocks.\n"
          f"6. The ‘Description’ must stay between 3 to 10 sentences.\n"
          f"7. Increase the value for ‘Turn number’ by +1 every time it’s your turn.\n"
          f"8. ‘Time period of day’ must progress naturally after a few turns.\n"
          f"9. Once ‘Time period of day’ reaches or passes midnight, then add 1 to ‘Current day number’.\n"
          f"10. Change the ‘Weather’ to reflect ‘Description’ and whatever environment the player is in the game.\n\n")
messages = [
    {"role":"system","content":rules},
    {"role":'user',"content":rules+f"Please remember this in the entire game.The game is not start yet, When I tell you Game Start, you can start the game"
}]

response = openai.ChatCompletion.create(model=engine,
                             messages= messages,
                             max_tokens=2048,
                             n=1,
                             stop=None,
                             temperature=0.2)

response = response['choices'][0]['message']['content']
print(response)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_character", methods=["POST"])
def game():
    if 'submit-btn' in request.form:
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        occupation = request.form["occupation"]
        nationality = request.form["nationality"]
        strength = request.form["strength"]
        dexterity = request.form["dexterity"]
        constitution = request.form["constitution"]
        intelligence = request.form["intelligence"]
        power = request.form["power"]
        education = request.form["education"]
        size = request.form["size"]
        appearance = request.form["appearance"]
        skills = request.form["skills"]
        equipment = request.form["equipment"]
        sanity = request.form["sanity"]
        magic = request.form["magic"]

        prompt = (f"\nName: {name}\n"
                  f"Age: {age}\n"
                  f"Gender: {gender}\n"
                  f"Occupation: {occupation}\n"
                  f"Nationality: {nationality}\n"
                  f"Strength: {strength}\n"
                  f"Dexterity: {dexterity}\n"
                  f"Constitution: {constitution}\n"
                  f"Intelligence: {intelligence}\n"
                  f"Power: {power}\n"
                  f"Education: {education}\n"
                  f"Size: {size}\n"
                  f"Appearance: {appearance}\n"
                  f"Skills: {skills}\n"
                  f"Equipment: {equipment}\n"
                  f"Sanity:{sanity}\n"
                  f"magic:{magic}\n"
                  f"sanity:{sanity}\n"
                  f"magic:{magic}\n")
        response = openai.ChatCompletion.create(model=engine,
                                            messages= [
                                                {"role":"system","content":rules},
                                                {'role':"assistant","content":rules},
                                                {"role":"user","content":rules+"The character of user is"+prompt+"Game Start"}],
                                            max_tokens=2048,
                                            n=1,
                                            stop=None,
                                            temperature=0.7,
                                            )
        print('submit successful')
    else:
        prompt = 'Generate a character sheet for user that under the rules of COC 7th keeper rule book and the investigator handbook, then start game'
        response = openai.ChatCompletion.create(model=engine,
                                            messages=[{"role":"system","content":rules,
                                                      "role":'assistant',"content":rules,
                                                       "role":'user',"content":prompt,
                                                       }],
                                            max_tokens=2048,
                                            n=1,
                                            stop=None,
                                            temperature=0.7,
                                            )
        user_character = response['choices'][0]['message']['content']
        response = openai.ChatCompletion.create(model=engine,
                                            messages= [
                                                {"role":"system","content":rules},
                                                {'role':"assistant","content":rules},
                                                {"role":"user","content":rules+"The character of user is"+user_character+"Game Start"}],
                                            max_tokens=2048,
                                            n=1,
                                            stop=None,
                                            temperature=0.7,
                                            )
        print('generate a character')
    response = response['choices'][0]['message']['content']
    response = response.replace('\n','<br>')
    print(response)
    return render_template('dialog.html', keeper_response = response)


@app.route('/dialog', methods=['GET', 'POST'])
def interact():
    if request.method == 'POST':
        user_input = request.form['user-input']
        keeper_response = generate_response(user_input)
    if request.method == 'GET':
        keeper_response = request.args.get('keeper_response')

    return render_template('dialog.html',keeper_response = keeper_response)




def generate_response(user_input):
    prompt = f"The user said: {user_input}\nThe Keeper said:"
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[
            {"role":'system',"content":rules},
            {"role":"assistant","content":rules},
            {"role":'user','content':rules+prompt}
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )
    response = response['choices'][0]['message']['content']
    response = response.replace('\n','<br>')
    return response


if __name__ == "__main__":
    app.run(debug=True)
