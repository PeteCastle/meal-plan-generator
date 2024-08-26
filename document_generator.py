from pylatex import Document, Section, Subsection, Command, Package, Table, Tabular
from pylatex.utils import NoEscape, italic, bold
from pylatex.basic import NewLine
from config import MealType, MealObjective, MealFrequency

class DocumentGenerator:
    @classmethod
    def generate_document_from_meal_plan(cls, meal_plan) -> Document:
        """
        Generate a document from a meal plan using Pylatex libarary.
        Parameters:
        - meal_plan: The meal plan object to generate the document from.
        Returns:
        - doc: The generated document.
        Raises:
        - ModuleNotFoundError: If the pylatex program is not installed.
        """
        doc = Document()
        
        doc.packages.append(Package('graphicx'))
        doc.packages.append(Package('float'))
        doc.packages.append(Package('paracol'))
        
        doc.preamble.append(Command('title', 'Meal Plan'))
        doc.preamble.append(Command('author', meal_plan.customer.profile['name']))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.preamble.append( NoEscape(r'\setlength{\columnseprule}{0.1pt}'))
        doc.append(NoEscape(r'\maketitle'))
        
        DocumentGenerator._generate_plan_info(doc, meal_plan)
        DocumentGenerator._generate_meal_schedule(doc, meal_plan)
        
        return doc
    
    @classmethod
    def _generate_plan_info(cls, doc : Document, meal_plan):
        """
        Saves the plan information to the given document.
        Parameters:
        - doc (Document): The document object to add the table to.
        - meal_plan (MealPlan): The meal plan object containing meal information.
        Returns:
        None
        """
        with doc.create(Table(position='H')) as table:
            # table.add_caption('Meal Plan Information')
            with table.create(Tabular('rl')) as tabular:
                tabular.add_row(('Meal Type:', MealType[meal_plan.customer.type].value))
                tabular.add_row(('Objective:', MealObjective[meal_plan.customer.objective].value))
                tabular.add_row(('Frequency:', MealFrequency[meal_plan.customer.frequency].value))
                tabular.add_row(('Date Covered:', f'{meal_plan.customer.starting_date.strftime('%B %-d, %Y')} - {meal_plan.customer.ending_date.strftime('%B %-d, %Y')}'))
                tabular.add_row(('Total Costs:', f'Php {meal_plan.total_cost:.2f}'))
                
    @classmethod
    def _generate_meal_schedule(cls, doc : Document, meal_plan):
        """
        Saves the meal schedules in the document.
        Parameters:
        - doc (Document): The document object to generate the meal schedule in.
        - meal_plan: The meal plan object containing the meals to be scheduled.
        Returns:
        None
        """
        meals  = meal_plan.meals_list
        
        for date, meals in meals.groupby(meals['Date'].dt.date):
            with doc.create(Section(NoEscape(date.strftime('%B %-d, %Y')), numbering=False)):
                doc.append(NoEscape(rf'\begin{{paracol}}[{len(meals)}]{{{len(meals)}}}'))
                doc.append(NoEscape(r"\sloppy"))
                for index, row in meals.iterrows():
                    
                    with doc.create(Subsection(row['Meal'], numbering=False)):
                        doc.append(italic(row['Main Ingredient']))
                        doc.append(NewLine())
                        doc.append(NewLine())
                        doc.append(NoEscape(f"{bold(round(row['Calories'],1))} calories"))
                        doc.append(NewLine())
                        doc.append(NoEscape(f"{bold(round(row['Carbohydrates (g)'],1))}g of carbs"))
                        doc.append(NewLine())
                        doc.append(NoEscape(f"{bold(round(row['Protein (g)'],1))}g of protein"))
                        doc.append(NewLine())
                        doc.append(NoEscape(f"{bold(round(row['Fat (g)'],1))}g of fats"))
                        doc.append(NewLine())
                        doc.append(NoEscape(r'\switchcolumn'))
             
                doc.append(NoEscape(r'\end{paracol}'))
            