from rand_question_v4.data import questions
from rand_question_v4.data import name_list
from rand_question_v4.selector import rand_draw
#ces lignes permettent d'importer ces fonctions depuis les autres files

def main():
  while True:
    chosen_name, chosen_question = rand_draw(name_list,questions)
    print(f"{chosen_name}, please answer {chosen_question}")

    user_choice = input("Enter 'Y' to continue or any other key to quit:")

    #== signifie une comparaison
    if user_choice == 'Y':
       continue

    else:
        break
  

