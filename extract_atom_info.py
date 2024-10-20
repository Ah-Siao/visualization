import json
from pymatgen.core.periodic_table import Element
import random


atom_colors = {
    1:  [1.0, 1.0, 1.0],   # Hydrogen - White
    2:  [0.85, 1.0, 1.0],  # Helium - Pale Cyan
    3:  [0.8, 0.5, 1.0],   # Lithium - Violet
    4:  [0.76, 1.0, 0.0],  # Beryllium - Dark Green
    5:  [1.0, 0.71, 0.71], # Boron - Salmon
    6:  [0.2, 0.2, 0.2],   # Carbon - Grey/Black
    7:  [0.0, 0.0, 1.0],   # Nitrogen - Blue
    8:  [1.0, 0.0, 0.0],   # Oxygen - Red
    9:  [0.0, 1.0, 0.0],   # Fluorine - Green
    10: [0.7, 0.89, 0.96], # Neon - Light Blue
    11: [0.67, 0.36, 0.95],# Sodium - Purple
    12: [0.47, 1.0, 0.0],  # Magnesium - Green
    13: [0.75, 0.65, 0.65],# Aluminum - Light Grey
    14: [0.78, 0.78, 0.78],# Silicon - Grey
    15: [1.0, 0.5, 0.0],   # Phosphorus - Orange
    16: [1.0, 1.0, 0.0],   # Sulfur - Yellow
    17: [0.0, 1.0, 0.0],   # Chlorine - Green
    18: [0.5, 0.82, 0.89], # Argon - Cyan
    19: [0.56, 0.25, 0.83],# Potassium - Purple
    20: [0.24, 1.0, 0.0],  # Calcium - Green
    21: [0.9, 0.9, 0.9],   # Scandium - Grey
    22: [0.75, 0.76, 0.78],# Titanium - Silver
    23: [0.65, 0.65, 0.67],# Vanadium - Silver
    24: [0.54, 0.6, 0.78], # Chromium - Steel Blue
    25: [0.61, 0.48, 0.78],# Manganese - Light Purple
    26: [0.88, 0.4, 0.2],  # Iron - Brown/Orange
    27: [0.94, 0.56, 0.63],# Cobalt - Pink
    28: [0.31, 0.82, 0.31],# Nickel - Green
    29: [0.78, 0.5, 0.2],  # Copper - Orange
    30: [0.49, 0.5, 0.69], # Zinc - Blueish Grey
    31: [0.76, 0.56, 0.56],# Gallium - Grey
    32: [0.4, 0.56, 0.56], # Germanium - Grey
    33: [0.74, 0.5, 0.89], # Arsenic - Purple
    34: [1.0, 0.63, 0.0],  # Selenium - Orange
    35: [0.5, 0.18, 0.16], # Bromine - Dark Red/Brown
    36: [0.36, 0.72, 0.82],# Krypton - Cyan
    37: [0.44, 0.18, 0.69],# Rubidium - Purple
    38: [0.0, 1.0, 0.0],   # Strontium - Green
    39: [0.58, 1.0, 1.0],  # Yttrium - Pale Blue
    40: [0.58, 0.88, 0.88],# Zirconium - Pale Cyan
    41: [0.45, 0.76, 0.79],# Niobium - Pale Cyan
    42: [0.33, 0.71, 0.71],# Molybdenum - Cyan
    43: [0.23, 0.62, 0.62],# Technetium - Cyan
    44: [0.14, 0.56, 0.56],# Ruthenium - Cyan
    45: [0.04, 0.49, 0.55],# Rhodium - Dark Cyan
    46: [0.85, 0.85, 0.85],# Palladium - Light Grey
    47: [0.75, 0.75, 0.75],# Silver - Silver
    48: [1.0, 0.85, 0.56], # Cadmium - Yellow
    49: [0.65, 0.46, 0.45],# Indium - Grey
    50: [0.4, 0.5, 0.5],   # Tin - Grey
    51: [0.62, 0.39, 0.71],# Antimony - Purple
    52: [0.83, 0.48, 0.0], # Tellurium - Orange
    53: [0.58, 0.0, 0.58], # Iodine - Violet
    54: [0.26, 0.62, 0.69],# Xenon - Cyan
    55: [0.34, 0.09, 0.56],# Cesium - Purple
    56: [0.0, 0.79, 0.0],  # Barium - Green
    57: [0.44, 0.83, 1.0], # Lanthanum - Light Blue
    58: [1.0, 1.0, 0.78],  # Cerium - Light Yellow
    59: [0.85, 1.0, 0.78], # Praseodymium - Light Green
    60: [0.78, 1.0, 0.78], # Neodymium - Light Green
    61: [0.64, 1.0, 0.78], # Promethium - Light Green
    62: [0.56, 1.0, 0.78], # Samarium - Light Green
    63: [0.38, 1.0, 0.78], # Europium - Pale Green
    64: [0.27, 1.0, 0.78], # Gadolinium - Pale Green
    65: [0.19, 1.0, 0.78], # Terbium - Pale Green
    66: [0.12, 1.0, 0.78], # Dysprosium - Pale Green
    67: [0.0, 0.91, 0.73], # Holmium - Green
    68: [0.0, 0.83, 0.62], # Erbium - Green
    69: [0.0, 0.74, 0.53], # Thulium - Green
    70: [0.0, 0.67, 0.45], # Ytterbium - Green
    71: [0.0, 0.56, 0.39], # Lutetium - Green
    72: [0.74, 0.76, 0.78],# Hafnium - Silver
    73: [0.65, 0.76, 0.78],# Tantalum - Silver
    74: [0.55, 0.76, 0.78],# Tungsten - Silver
    75: [0.42, 0.76, 0.78],# Rhenium - Silver
    76: [0.33, 0.76, 0.78],# Osmium - Silver
    77: [0.23, 0.76, 0.78],# Iridium - Silver
    78: [0.13, 0.76, 0.78],# Platinum - Silver
    79: [1.0, 0.84, 0.0],  # Gold - Gold
    80: [0.72, 0.72, 0.81],# Mercury - Silver
    81: [0.65, 0.33, 0.3], # Thallium - Grey
    82: [0.34, 0.34, 0.38],# Lead - Dark Grey
    83: [0.62, 0.31, 0.71],# Bismuth - Purple
    84: [0.67, 0.36, 0.0], # Polonium - Brown
    85: [0.46, 0.31, 0.27],# Astatine - Brown
    86: [0.26, 0.51, 0.59],# Radon - Dark Cyan
    87: [0.26, 0.0, 0.4],  # Francium - Dark Violet
    88: [0.0, 0.49, 0.0],  # Radium - Green
    89: [0.44, 0.67, 0.98],# Actinium - Blue
    90: [0.0, 1.0, 0.0],   # Thorium - Green
    91: [0.0, 0.92, 0.0],  # Protactinium - Green
    92: [0.0, 0.82, 0.0],  # Uranium - Green
    93: [0.0, 0.72, 0.0],  # Neptunium - Green
    94: [0.0, 0.63, 0.0],  # Plutonium - Green
    95: [0.0, 0.56, 0.0],  # Americium - Green
    96: [0.0, 0.49, 0.0],  # Curium - Green
    97: [0.0, 0.42, 0.0],  # Berkelium - Green
    98: [0.0, 0.35, 0.0],  # Californium - Green
    99: [0.0, 0.31, 0.0],  # Einsteinium - Green
    100: [0.0, 0.27, 0.0], # Fermium - Green
    101: [0.0, 0.23, 0.0], # Mendelevium - Green
    102: [0.0, 0.19, 0.0], # Nobelium - Green
    103: [0.0, 0.16, 0.0], # Lawrencium - Green
    104: [0.74, 0.76, 0.78],# Rutherfordium - Silver
    105: [0.65, 0.76, 0.78],# Dubnium - Silver
    106: [0.55, 0.76, 0.78],# Seaborgium - Silver
    107: [0.42, 0.76, 0.78],# Bohrium - Silver
    108: [0.33, 0.76, 0.78],# Hassium - Silver
    109: [0.23, 0.76, 0.78],# Meitnerium - Silver
    110: [0.13, 0.76, 0.78],# Darmstadtium - Silver
    111: [0.0, 0.76, 0.78],# Roentgenium - Silver
    112: [0.0, 0.76, 0.78],# Copernicium - Silver
    113: [0.0, 0.76, 0.78],# Nihonium - Silver
    114: [0.0, 0.76, 0.78],# Flerovium - Silver
    115: [0.0, 0.76, 0.78],# Moscovium - Silver
    116: [0.0, 0.76, 0.78],# Livermorium - Silver
    117: [0.0, 0.76, 0.78],# Tennessine - Silver
    118: [0.0, 0.76, 0.78],# Oganesson - Silver
}




# Generate atomic data using pymatgen
atomic_data = {}

for el in Element:
    try:
        # Get a set of properties for each element
        # Fallback values or omissions for missing properties can be handled here
        atomic_data[el.symbol] = {
            'atomic_number':el.number,
            "atomic_mass": el.atomic_mass,
            "atomic_radius": el.atomic_radius if el.atomic_radius is not None else "unknown",
            "van_der_waals_radius": el.van_der_waals_radius if el.van_der_waals_radius is not None else "unknown",
            "electronic_structure": el.full_electronic_structure if el.full_electronic_structure is not None else "unknown",
            "color": atom_colors[int(el.number)], 
            "number_of_electrons": el.Z
        }
    except Exception as e:
        print(f"Could not process element {el.symbol}: {e}")

# Save the atomic data to a JSON file
with open('atomic_data.json', 'w') as f:
    json.dump(atomic_data, f, indent=4)

print("Atomic data JSON file has been created.")
