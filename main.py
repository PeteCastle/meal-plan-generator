import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

from config import MealType, MealFrequency, Allergen, MealObjective, bcolors, Gender
from customer import Customer
from document_generator import DocumentGenerator
from questionnaire_utils import QuestionnaireUtils

import subprocess

class MealPlan:
    customer : Customer
    dataset : pd.DataFrame
    meals : pd.DataFrame
    
    def __init__(self, customer : Customer) -> None:
        """
        Initializes an instance of the class and loads the meal dataset.

        Parameters:
        - customer (Customer): The customer object.

        Returns:
        - None
        """
        assert type(customer) == Customer, "Customer must be a Customer object"
        self.customer = customer
        self.dataset = pd.read_excel("datasets/meal_dataset.xlsx", sheet_name="Meals with SKUs")
        assert type(self.dataset) == pd.DataFrame, f"Expected DataFrame, got {type(self.dataset)}"
        assert len(self.dataset) > 0, "Raw dataset is empty"
        self.meals = pd.DataFrame()
        
    def generate_meal_plan(self):
        """
        Generates a meal plan based on the customer's preferences and dietary restrictions.  For the complete meal plan generation, please refer to the documentation.
        Returns:
            pandas.DataFrame: A DataFrame containing the generated meal plan.
        """
        dataset = self.dataset
        meals = dataset[dataset['Type'] == MealType[self.customer.type].value]
        for allergy in self.customer.allergies:
            ingredient = Allergen[allergy].value
            if ingredient == 'Meat':
                meals = meals[~meals['Main Ingredient'].isin('Chicken','Beef','Pork')]
            else:
                meals = meals[meals['Main Ingredient'] != ingredient]
        
        meal_schedule, meals_per_day, num_days = self._get_meal_schedule()
        
        try:
            meals_list = meals.sample(n=num_days*meals_per_day, replace=True)
        except ValueError:
            print(f"{bcolors.FAIL}ERROR: Not enough meals in the dataset to generate a meal plan.  Our fault!{bcolors.ENDC}")
            return None
        
        meals_list['Date'] = meal_schedule
        if len(meals_list['SKU']) != len(meals_list['SKU'].unique()):
            print(f"{bcolors.WARNING}WARNING: Some meals are repeated. {len(meals_list['SKU']) - len(meals_list['SKU'].unique())} total.{bcolors.ENDC}")
        
        meals_list = self._add_calories(meals_list)
        meals_list.reset_index(drop=True, inplace=True)
        
        if MealType[self.customer.type].name == 'VEGAN':
            cost_per_meal = 500
        elif MealType[self.customer.type].name == 'ORGANIC':
            cost_per_meal = 800
        elif MealType[self.customer.type].name == 'NON_ORGANIC':
            cost_per_meal = 600
        elif MealType[self.customer.type].name == 'KETO':
            cost_per_meal = 1000
            
        self.total_cost = len(meals_list) * cost_per_meal
        self.meals_list = meals_list

        assert type(meals_list) == pd.DataFrame, f"Expected DataFrame, got {type(meals_list)}"
        assert len(meals_list) > 0, "No meals generated"
        return meals_list
    
    def ask_to_generate_document(self):
        """
        Asks the user if they would like to generate a PDF document for their meal plan.
        Returns:
            bool: True if the user wants to generate the document, False otherwise.
        """
        generate = QuestionnaireUtils.ask_multiple_choice_question("Would you like to generate a PDF document for your meal plan?",{"Yes":True, "No":False})
        if generate:
            print("Generating PDF document...")
            doc = DocumentGenerator.generate_document_from_meal_plan(self)
            doc.generate_pdf(f'output/meal_plan', clean_tex=False)
            
            try:
                subprocess.run(['xdg-open', f'output/meal_plan.pdf'])
            except Exception as e:
                print(f"{bcolors.FAIL}An error has occurred when generating the document.  Make sure that  the Latex compiler is installed{bcolors.ENDC}")

    def print_meal_plan(self):
        """
        Print the meal plan for the customer.

        This method prints the customer's meal plan, including the meal type, objective, frequency,
        date covered, total costs, and the list of meals for each date.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        print("YOUR MEAL PLAN")
        print('Meal Type:', f"{bcolors.OKCYAN}{MealType[self.customer.type].value}{bcolors.ENDC}", sep='\t')
        print('Objective:', f"{bcolors.OKCYAN}{MealObjective[self.customer.objective].value}{bcolors.ENDC}", sep='\t')
        print('Frequency:', f"{bcolors.OKCYAN}{MealFrequency[self.customer.frequency].value}{bcolors.ENDC}", sep='\t')
        print('Date Covered:', f'{bcolors.OKCYAN}{self.customer.starting_date.strftime('%B %-d, %Y')} - {self.customer.ending_date.strftime('%B %-d, %Y')}{bcolors.ENDC}', sep='\t')
        print('Total Costs:', f'{bcolors.OKCYAN}Php {self.total_cost:.2f}{bcolors.ENDC}', sep='\t')
        print()
        for date, meals in self.meals_list.groupby(self.meals_list['Date'].dt.date):
            print(f"{bcolors.OKCYAN}{date.strftime('%B %-d, %Y')}{bcolors.ENDC}")
            for index, row in meals.iterrows():
                print(f"\t{bcolors.OKGREEN}{row['Meal']}{bcolors.ENDC} ({row['Main Ingredient']})")
                print(f"\t  {bcolors.GRAY}{row['Calories']:.1f} calories | {round(row['Carbohydrates (g)'],1)}g of cargs | {round(row['Protein (g)'],1)}g of protein | {round(row['Fat (g)'],1)}g of fat |{bcolors.ENDC}")
            
    def save_meal_plan(self):
        """
        Save the meal plan to a CSV file.
        """
        import os
        self.meals_list.to_csv('output/meal_plan.csv', index=False)
        print()
        print(f"{bcolors.OKGREEN}Meal plan saved to {os.getcwd()}/output/meal_plan.csv{bcolors.ENDC}")
        print()
    
    def _get_meal_schedule(self):
        """
        Generates a meal schedule based on the customer's frequency, starting date, and ending date.
        Returns:
            meal_schedule (list): A list of datetime objects representing the scheduled meal times.
            meals_per_day (int): The number of meals per day based on the customer's frequency.
            num_days (int): The total number of days in the meal schedule.
        """
        if MealFrequency[self.customer.frequency].name == 'OMAD':
            meals_per_day = 1
            meal_times = ["17:00"]
        elif MealFrequency[self.customer.frequency].name == 'TMAD':
            meals_per_day = 2
            meal_times = ["11:00", "18:00"]
        elif MealFrequency[self.customer.frequency].name == 'THMAD':
            meals_per_day = 3
            meal_times = ["08:00", "12:00", "19:00"]
    
        date_range = pd.date_range(self.customer.starting_date, 
                                   self.customer.ending_date, 
                                   freq='B')
        num_days = len(date_range)
        
        meal_schedule = []
        for date in date_range:
            for time in meal_times:
                meal_datetime = pd.to_datetime(f"{date.date()} {time}")
                meal_schedule.append(meal_datetime)
                
        assert len(meal_schedule) == meals_per_day * num_days, "Incorrect number of meals in the schedule"
        assert type(meal_schedule) == list, f"Expected list, got {type(meal_schedule)}"
        assert type(meals_per_day) == int, f"Expected int, got {type(meals_per_day)}"
        assert type(num_days) == int, f"Expected int, got {type(num_days)}"
        
        return meal_schedule, meals_per_day, num_days
    
    def _add_calories(self, df):
        """
        Adds calorie information to the given DataFrame based on the customer's objective.
        Parameters:
        - df: pandas DataFrame
            The DataFrame containing the data to be modified.
        Returns:
        - pandas DataFrame
            The modified DataFrame with added calorie information.
        Raises:
        - None
        """
        
     
        if MealObjective[self.customer.objective].name == 'WEIGHT_LOSS':
            min_calories_per_day = 1500
            max_calories_per_day = 1800
        elif MealObjective[self.customer.objective].name == 'MUSCLE_GAIN':
            min_calories_per_day = 2000
            max_calories_per_day = 2300
        else:
            min_calories_per_day = 1800
            max_calories_per_day = 2000
            
        df_grouped  = df.groupby(df['Date'].dt.date)
        
        _df_grouped = []
        for date, group in df_grouped:
            num_rows = group.shape[0]
            calories = np.random.randint(min_calories_per_day//3, max_calories_per_day//3, num_rows)
            group['Calories'] = calories
            group['Carbohydrates (g)'] = (group['Calories'] * (group['Carbohydrate (%)']/100)) * 0.129598
            group['Protein (g)'] = (group['Calories'] * (group['Protein (%)']/100)) * 0.129598
            group['Fat (g)'] = (group['Calories'] * (group['Fat (%)']/100)) * 0.129598
            _df_grouped.append(group)
        assert type(pd.concat(_df_grouped)) == pd.DataFrame, f"Expected DataFrame, got {type(pd.concat(_df_grouped))}"
        assert len(pd.concat(_df_grouped)) > 0, "No calories added to the DataFrame"
        return pd.concat(_df_grouped)
    
def main():
    print("Welcome to the Meal Plan Generator")
    name = QuestionnaireUtils.ask_question(question = "What is your name?", return_type = str)
    print(f"Hello, {bcolors.OKBLUE}{name}{bcolors.ENDC}!")
    age = QuestionnaireUtils.ask_question(question = "How old are you?", return_type = int)
    if age < 18:
        print(f"{bcolors.FAIL}Sorry, you must be 18 years or older to use this service.{bcolors.ENDC}")
        return
    gender = QuestionnaireUtils.ask_multiple_choice_question("What is your gender?", Gender.to_dict())
    profile = {
        "name": name,
        "age": age,
        "gender": gender,
    }

    customer = Customer(profile)
    customer.ask_all_questions()
    customer.confirm_preferences()
    
    meal_plan = MealPlan(customer)
    meal_plan.generate_meal_plan()
    meal_plan.print_meal_plan()
    meal_plan.save_meal_plan()
    meal_plan.ask_to_generate_document()
    
    print("Thank you for using the Meal Plan Generator")
    
if __name__ == "__main__":
    main()
    
