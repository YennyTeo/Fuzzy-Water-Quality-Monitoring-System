import numpy as np
from skfuzzy import control as ctrl
from skfuzzy import membership as mf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def initialize_system():
    # INITIALIZE INPUTS AND OUTPUTS
    ph = ctrl.Antecedent(np.arange(0, 14, 0.1), 'ph')
    hardness = ctrl.Antecedent(np.arange(0, 1200, 0.1), 'hardness')
    quality = ctrl.Consequent(np.arange(0, 100, 0.1), 'quality')

    # DEFINE MEMBERSHIP FUNCTIONS FOR FUZZY SETS OF VARIABLES
    ph['low'] = mf.trimf(ph.universe, [0, 0, 6])
    ph['medium'] = mf.trimf(ph.universe, [5.5, 7, 8.5])
    ph['high'] = mf.trimf(ph.universe, [8, 14, 14])

    hardness['low'] = mf.trapmf(hardness.universe, [0, 0, 300, 500])
    hardness['medium'] = mf.trimf(hardness.universe, [100, 450, 900])
    hardness['high'] = mf.trimf(hardness.universe, [700, 1200, 1200])

    quality['poor'] = mf.trimf(quality.universe, [0, 0, 40])
    quality['fair'] = mf.trimf(quality.universe, [30, 50, 70])
    quality['excellent'] = mf.trimf(quality.universe, [60, 100, 100])
    return ph, hardness, quality

def define_rules(ph, hardness, quality):
    rule1 = ctrl.Rule(ph['low'] & hardness['low'], quality['fair'])
    rule2 = ctrl.Rule(ph['low'] & hardness['medium'], quality['fair'])
    rule3 = ctrl.Rule(ph['low'] & hardness['high'], quality['poor'])
    rule4 = ctrl.Rule(ph['medium'] & hardness['low'], quality['excellent'])
    rule5 = ctrl.Rule(ph['medium'] & hardness['medium'], quality['excellent'])
    rule6 = ctrl.Rule(ph['medium'] & hardness['high'], quality['poor'])
    rule7 = ctrl.Rule(ph['high'] & hardness['low'], quality['fair'])
    rule8 = ctrl.Rule(ph['high'] & hardness['medium'], quality['fair'])
    rule9 = ctrl.Rule(ph['high'] & hardness['high'], quality['poor'])
    
    rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]
    return rules

def construct_fuzzy_control_system(ph, hardness, quality, rules):
    water_ctrl = ctrl.ControlSystem(rules=rules)
    water = ctrl.ControlSystemSimulation(control_system=water_ctrl)
    return water

def get_user_input():
    while True:
        try:
            ph_value = float(input("Please enter the pH value (0-14): "))
            hardness_value = float(input("Please enter the hardness value (0-1200mg/L): "))
            
            if 0 <= ph_value <= 14 and 0 <= hardness_value <= 1200:
                return ph_value, hardness_value
            else:
                print("Please enter values within the specified limits!\n")
        except ValueError:
            print("Please enter valid numeric values!\n")
    
def compute_water_quality(ph_value, hardness_value, water):
    water.input['ph'] = ph_value
    water.input['hardness'] = hardness_value
    water.compute()
    
    quality_crisp = water.output['quality']
    print(f"Water Quality: {quality_crisp:.2f}%")
    if quality_crisp > 30:
        print("Drinkable Water!")
    else:
        print("Water Undrinkable!")
    quality.view(sim=water)
    plt.show()

def plot_membership_functions(ph, hardness, quality):
    print("Showing Fuzzy Sets..")
    ph.view()
    hardness.view()
    quality.view()
    plt.show()
    
def plot_3d_surface():
    print("Showing 3D Surface Plot..")
    x, y = np.meshgrid(np.linspace(ph.universe.min(), ph.universe.max(), 100),
                        np.linspace(hardness.universe.min(), hardness.universe.max(), 100))
    z_quality = np.zeros_like(x, dtype=float)

    for i, r in enumerate(x):
        for j, c in enumerate(r):
            water.input['ph'] = x[i, j]
            water.input['hardness'] = y[i, j]
            try:
                water.compute()
            except:
                z_quality[i, j] = float('inf')
            z_quality[i, j] = water.output['quality']
            
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z_quality, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)
    
    ax.contourf(x, y, z_quality, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
    ax.contourf(x, y, z_quality, zdir='x', offset=x.max()*1.5, cmap='viridis', alpha=0.5)
    ax.contourf(x, y, z_quality, zdir='y', offset=y.max()*1.5, cmap='viridis', alpha=0.5)
    ax.view_init(30, 200)
    plt.show()
    
if __name__ == "__main__":
    ph, hardness, quality = initialize_system()
    rules = define_rules(ph, hardness, quality)
    water = construct_fuzzy_control_system(ph, hardness, quality, rules)
    
    print("==========================================================================\n")
    print("          Welcome to Fuzzy Water Quality Monitoring System          ")
    print("\n==========================================================================\n")
    
    while True:
        ph_value, hardness_value = get_user_input()
        compute_water_quality(ph_value, hardness_value, water)
        
        check_again = input("\nDo you want to check the water quality again? (yes/no): ").lower()
        if check_again != 'yes':
            break
    plot_membership_functions(ph, hardness, quality)
    plot_3d_surface()