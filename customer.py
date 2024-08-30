from config import MealFrequency, MealObjective, MealType, Allergen, Gender, bcolors
from datetime import date, timedelta, datetime
from questionnaire_utils import QuestionnaireUtils

class Customer:
    profile : dict
    starting_date : date
    ending_date : date
    type : MealType
    objective : MealObjective
    frequency : MealFrequency
    allergies : list[Allergen]
    
    def __init__(self, profile : dict) -> None:
        """
        Initializes a Customer object with the given profile.
        Parameters:
        - profile (dict): A dictionary containing the customer's profile information.
                          The dictionary must have the following keys: 'name', 'age', and 'gender'.
        Raises:
        - AssertionError: If the profile is not a dictionary or if it does not have the required keys; If the 'name' is not a string; If the 'age' is not an integer; If the 'gender' is not a string or not a valid gender value.
        Returns:
        - None
        """
        assert type(profile) == dict, "Profile must be a dictionary"
        assert list(profile.keys()) == ['name', 'age','gender' ]
        
        assert type(profile['name']) == str, "Name must be a string"
        assert type(profile['age']) == int, "Age must be an integer"
        assert type(profile['gender']) == str
        
        assert profile['gender'] in list(Gender.__members__)
        self.profile = profile
        
    def ask_duration(self):
        """
        Asks the user for the starting date and duration of subscription.
        Returns:
            None
        """
        self.starting_date = QuestionnaireUtils.ask_datetime_question("When would you like to start?", future_only=True)
        print(f"Starting date: {bcolors.OKGREEN}{self.starting_date.strftime('%B %-d, %Y')}{bcolors.ENDC}")

        durations = {
            "1 week": 7,
            "2 weeks": 14,
            "4 weeks": 28,
        }
        
        duration = QuestionnaireUtils.ask_multiple_choice_question("How long would you like to subscribe?", durations)
        
        self.ending_date = self.starting_date + timedelta(days=duration)
        assert self.ending_date > self.starting_date, "Ending date must be after starting date"
        print(f"Ending date: {bcolors.OKGREEN}{self.ending_date.strftime('%B %-d, %Y')}{bcolors.ENDC}")
    
    def ask_type(self):
        """
        Asks the user for the type of meal plan they would like.
        Returns:
            None
        """
        self.type = QuestionnaireUtils.ask_multiple_choice_question("What type of meal plan would you like?", MealType.to_dict())
        assert self.type in list(MealType.__dict__), f"Invalid meal type {self.type}"
    
    def ask_objective(self):
        """
        Asks the user for their weight objective.
        Returns:
            None
        """
        self.objective = QuestionnaireUtils.ask_multiple_choice_question("What is your weight objective?", MealObjective.to_dict())
        assert self.objective in list(MealObjective.__dict__), f"Invalid meal objective {self.objective}"

    def ask_frequency(self):
        """
        Asks the customer for their preferred meal frequency.
        Returns:
            None
        """
        self.frequency = QuestionnaireUtils.ask_multiple_choice_question("How many meals would you like to have per day?", MealFrequency.to_dict())
        assert self.frequency in list(MealFrequency.__dict__), f"Invalid meal frequency {self.frequency}"
        
    def ask_allergies(self):
        """
        Asks the customer about their allergies and stores the response in the 'allergies' attribute.

        Returns:
            None
        """
        self.allergies = QuestionnaireUtils.ask_list_question("Do you have any allergies?", Allergen.to_dict())
        assert all(allergy in list(Allergen.__dict__) for allergy in self.allergies), f"Invalid allergen {self.allergies}"
        
    def ask_add_ons(self):
        """
        (No Longer used) This method is used to ask the customer for any additional add-ons they would like to include with their purchase.
        """
        print(f"{bcolors.GRAY}Add ons is not yet available. Stay tuned for updates!{bcolors.ENDC}")
        pass
    
    def ask_all_questions(self):
        """
        Asks all the necessary questions to the customer.
        """
        
        self.ask_objective()
        self.ask_type()
        self.ask_duration()
        self.ask_frequency()
        self.ask_allergies()
        self.ask_add_ons()
        
    def confirm_preferences(self):
        """
        Displays the current preferences of the customer and allows them to modify their preferences if desired.

        Returns:
            None
        """
        self.print_preferences()
        confirmation = QuestionnaireUtils.ask_multiple_choice_question("Would you like to modify your preferences?", {"Yes": "Yes", "No": "No"})
        if confirmation == "Yes":
            options = {
                "Objective": self.ask_objective,
                "Meal Type": self.ask_type,
                "Duration": self.ask_duration,
                "Frequency": self.ask_frequency,
                "Allergies": self.ask_allergies,
                "Add-ons": self.ask_add_ons
            }
            question = "Which preference would you like to modify?"
            while confirmation == "Yes":
                choice = QuestionnaireUtils.ask_multiple_choice_question(question, options)
                choice()
                self.print_preferences()
                confirmation = QuestionnaireUtils.ask_multiple_choice_question("Would you like to modify another preference?", {"Yes": "Yes", "No": "No"})
        
    def print_preferences(self):
        """
        Print a summary of the customer's preferences.

        This method prints the starting date, ending date, meal type, objective, frequency, and allergies
        of the customer's preferences.
        """
        print("\n\n\n\tSUMMARY OF PREFERENCES")
        print(f"\tStarting date:\t{bcolors.OKGREEN}{self.starting_date.strftime('%B %-d, %Y')}{bcolors.ENDC}")
        print(f"\tEnding date:\t{bcolors.OKGREEN}{self.ending_date.strftime('%B %-d, %Y')}{bcolors.ENDC}")
        print(f"\tMeal type:\t{bcolors.OKGREEN}{MealType[self.type].value}{bcolors.ENDC}")
        print(f"\tObjective:\t{bcolors.OKGREEN}{MealObjective[self.objective].value}{bcolors.ENDC}")
        print(f"\tFrequency:\t{bcolors.OKGREEN}{MealFrequency[self.frequency].value}{bcolors.ENDC}")
        print(F"\tAllergies:\t{bcolors.OKGREEN}{', '.join([Allergen[allergy].value for allergy in self.allergies])}{bcolors.ENDC}")
        print("\n\n\n")

        