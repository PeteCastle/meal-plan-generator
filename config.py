from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def to_dict(cls):
        """
        Converts the Enum to a dictionary.
        Returns:
            _type_: _description_
        """
        return {member.value : member.name  for member in cls}
    
class MealType(BaseEnum):
    KETO = "Keto"
    ORGANIC = "Organic"
    NON_ORGANIC = "Non-Organic"
    VEGAN = "Vegetarian"

class MealObjective(BaseEnum):
    WEIGHT_LOSS = "Weight Loss"
    MUSCLE_GAIN = "Muscle Gain"
    MAINTAIN = "Maintain"
    
class MealFrequency(BaseEnum):
    OMAD = "One Meal A Day"
    TMAD = "Two Meals A Day"
    THMAD = "Three Meals A Day"
    
class Gender(BaseEnum):
    MALE = "Male"
    FEMALE = "Female"

class Allergen(BaseEnum):
    CHICKEN = "Chicken"
    BEEF = "Beef"
    PORK = "Pork"
    SEAFOOD = "Seafood"
    MEAT = "Meat"
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'