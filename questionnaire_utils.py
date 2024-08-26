from config import bcolors
from datetime import datetime

class QuestionnaireUtils:
    """
    A utility class for asking questions in the terminal. Contains various methods for asking questions and validating inputs.
    """
    
    @staticmethod
    def ask_question(question, return_type : type):
        """
        Asks a question and waits for user input.
        Args:
            question (str): The question to be displayed.
            return_type (type): The expected data type of the user's input.
        Returns:
            The user's input converted to the specified data type.
        Raises:
            None
        Example:
            >>> ask_question("Enter your age:", int)
            Enter your age:
            25
        """

        print(question)
        answer = None
        while answer is None:
            _answer = str(input())
            try:
                answer = return_type(_answer)
            except:
                print(f"{bcolors.FAIL}Invalid input.  Please try again.{bcolors.ENDC}")
        return answer
    
    @staticmethod
    def ask_multiple_choice_question(question, choices):
        """
        Ask a multiple choice question and wait for user input.  The intended input is the number corresponding to the choice. 
        Args:
            question (str): The question to ask
            choices (dict): List of choices  (key: id, value: Human readable choice)
        Returns:
            id (str): Key of choices
        """
        print(question)
        if len(choices) <= 4:
            for i, display_str in enumerate(choices):
                print(f"{bcolors.OKGREEN}[{i+1}]{bcolors.ENDC} {str(display_str)}", end="\t")
        else:
                num_rows = (len(choices) + 1) // 2
                for i in range(num_rows):
                    choices_list = list(choices.keys())
                    left_choice = choices_list[i]
                    right_choice = choices_list[i + num_rows] if i + num_rows < len(choices_list) else ""
                    print(f"{bcolors.OKGREEN}[{i+1}]{bcolors.ENDC} {left_choice:<20} {bcolors.OKGREEN}[{i+1+num_rows}]{bcolors.ENDC} {right_choice}")

        choice = None
        
        while choice is None:
            print(f"\n{bcolors.GRAY}Type the number of your choice: {bcolors.ENDC}", end="")
        
            _choice = str(input())
            if _choice in [str(i+1) for i in range(len(choices))]:
                choice = int(_choice)
            else:
                print(f"\r{bcolors.FAIL}Invalid input.  Please try again.{bcolors.ENDC}", end="")
            
            if _choice in [str(i+1) for i in range(len(choices))]:
                choice = int(_choice)
            else:
                print(f"\r{bcolors.FAIL}Invalid input.  Please try again.{bcolors.ENDC}", end="")
                

        print(f"{bcolors.OKGREEN}{list(choices.keys())[choice-1]}{bcolors.ENDC}")
        return choices[list(choices.keys())[choice-1]]
    
    @staticmethod
    def ask_datetime_question(question, future_only=False):
        """
        Asks the user a datetime question.
        Parameters:
        - question (str): The question to be displayed to the user.
        - future_only (bool): If True, only allows future dates to be entered.
        Returns:
        - date (datetime): The datetime object representing the user's input.
        Raises:
        - ValueError: If an invalid date is entered or if the date is not in the future (when future_only is True).
        """
        print(question)
        months = {month:i  for i, month in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])}
        month = QuestionnaireUtils.ask_multiple_choice_question("Enter the month",months)
        day = QuestionnaireUtils.ask_question("Enter the day", int)
        year = datetime.now().year
        
        try:
            date = datetime(year, month, day)
            if future_only and date < datetime.now():
                raise ValueError
        except ValueError:
            print(f"{bcolors.FAIL}Invalid date or date must be in the future.  Please try again.{bcolors.ENDC}")
            date = QuestionnaireUtils.ask_datetime_question(question)
        return date
        
    @staticmethod
    def ask_list_question(question, choices):
        """
        Similar to multiple choice question, but allows multiple choices to be selected.
        Args:
            question (str): The question to ask
            choices (dict): List of choices (key: id, value: Human readable choice)
        Returns:
            list: List of selected choices
        """
        print(question)
        for i, display_str in enumerate(choices):
            print(f"{bcolors.OKGREEN}[{i+1}]{bcolors.ENDC} {str(display_str)}", end="\t")
        print(f"\n{bcolors.GRAY}Type the numbers of your choices, separated by commas: {bcolors.ENDC}", end="")

        selected_choices = []
        while not selected_choices:
            _choices = list(set(str(input()).split(',')))
            if _choices == ['']:
                selected_choices = []
                break
            
            try:
                selected_choices = tuple([choices[list(choices.keys())[int(choice.strip()) - 1]] for choice in _choices])
            except (ValueError, IndexError):
                print(f"{bcolors.FAIL}Invalid input. Please try again.{bcolors.ENDC}")
                selected_choices = []

        print(f"{bcolors.OKGREEN}Selected choices: {', '.join(selected_choices)}{bcolors.ENDC}")
        return selected_choices