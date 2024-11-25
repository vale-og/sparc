def main(initial_star_number = 100, seed = 1): 
    '''
    
    INPUT
    
    initial_star_number: stars to be randomly generated, default is 100


    STEPS

    1) Generate data
    random_probs: random values from 0 to 1
    random_masses: random values from 0.08 to 100 Msun
    random_ages: random values from 0 to 13.9 Gyr (MW age)

    2) Build a dataframe with all the stars, including the IMF probability (Kroupa (2001)), and the MS lifetime 

    3) Filter the dataframe to select stars in and out of the IMF limits, and in and out of the main sequence

    4) Assing remnant labels to stars that are out of the main sequence
    remnants: classification (1 == 'wd', 2 == 'ns', 3 == 'bh') according to the initial mass

    5) Obtain final mass for each star according to the remnant type
    final_mass: calculated according to Kalirai for stars that have evolved out of the main sequence

    RETURNS
    A file containing the masses, ages, remnant type and final mass for stars out of the MS
    '''
    
    import numpy as np

    import matplotlib.pyplot as plt
    from numpy.random import choice
    from scipy.integrate import quad
    
    import pandas as pd
    
    
    from IMF import kroupa_imf
    from IFMR import kalirai_ifmr
    from REMNANT import remnant
    from FILTER import filter_imf, filter_evolved

    import time 
 
    start_time = time.time() 


    np.random.seed(seed)
    print('Generating random probabilities...')
    
    random_probs = np.random.uniform(0,1,initial_star_number)
    
    print('Generating random masses...')


    
    random_masses = np.random.uniform(0.08,100,initial_star_number)

    print('Calculating IMF probabilities...')
    
    imf_probs = kroupa_imf(random_masses)
    
    print('Data ready! Now filtering stars below the IMF boundary...')


    in_imf = filter_imf(random_probs, imf_probs)

    masses_in_imf = random_masses[in_imf]
    

    print('Generating random ages...')

    random_ages = np.random.uniform(0,13.9,len(masses_in_imf))

    
    print('Calculating Main Sequence lifetimes...')


    ms_lifetimes =  10/(masses_in_imf**2.5)

    
    print('Now filtering stars that have left the Main Sequence...')

    is_evolved = filter_evolved(random_ages, ms_lifetimes)


    
    print('Classifying Remnant Types...')

    remnants = remnant(masses_in_imf[is_evolved])
    

    
    print('Calculating Final Masses...')

    final_masses = kalirai_ifmr(masses_in_imf[is_evolved], remnants)
    
    
    print(f'''REMNANTS
    WDs: {len(remnants[remnants == 1])}, {round(len(remnants[remnants == 1])/len(remnants)*100, 2)}%
    NSs: {len(remnants[remnants == 2])}, {round(len(remnants[remnants == 2])/len(remnants)*100, 2)}%
    BHs: {len(remnants[remnants == 3])}, {round(len(remnants[remnants == 3])/len(remnants)*100, 2)}%''')


    df = pd.DataFrame({'mass': masses_in_imf[is_evolved],
                       'age': random_ages[is_evolved],
                       'remnant': remnants,
                       'final_mass': final_masses})
    df.to_csv('evolved_stars.csv', index = False)
    

    df = pd.DataFrame({'mass': masses_in_imf[~is_evolved],
                       'age': random_ages[~is_evolved]})
    
    df.to_csv('ms_stars.csv', index = False)

    
    end_time = time.time() 
    execution_time = end_time - start_time 


    
    return  input("Would you like to plot results? (y/n): ")


def plots(plot_ms, plot_evolved, fig_path):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    
    evolved_stars = pd.read_csv('evolved_stars.csv')
    ms_stars = pd.read_csv('ms_stars.csv')

    
    if plot_ms == 'y':
        max_mass = ms_stars['mass'].max()
        
        fig, axs = plt.subplots(nrows = 1, ncols = 2,  figsize = (15,10))

        
        axs[0].hist(ms_stars['mass'], bins = 100, color = 'red', alpha = 0.4, density = False, range = (0, max_mass))
        axs[0].set_xlabel('M [M$_\\odot$]')
        axs[0].set_ylabel('Counts')


        axs[1].hist(ms_stars['age'], bins = 100, color = 'red', alpha = 0.4, density = False, range = (0, max_mass))
        axs[1].set_xlabel('M [M$_\\odot$]')
        axs[1].set_ylabel('Counts')

        fig.suptitle('Mass and Age distribution for MS stars')

        plt.savefig(fig_path + 'ms_mass_age_distribution.pdf', dpi = 300)

        plt.show()



        input('Click ENTER to go to next plot')

    
    if plot_evolved == 'y':

        fig, axs = plt.subplots(nrows = 2, ncols = 3, figsize = (15,15))

        max_mass = evolved_stars['final_mass'][evolved_stars['remnant'] == 1].max()
        
        axs[0][0].hist(evolved_stars['final_mass'][evolved_stars['remnant'] == 1] , bins = 100, color = 'gray', alpha = 0.4, density = False, label = 'WD', range = (0, max_mass))

        max_mass = evolved_stars['final_mass'][evolved_stars['remnant'] == 2].max()
        
        axs[0][1].hist(evolved_stars['final_mass'][evolved_stars['remnant'] == 2] , bins = 100, color = 'blue', alpha = 0.4, density = False, label = 'NS', range = (0, max_mass))

        max_mass = evolved_stars['final_mass'][evolved_stars['remnant'] == 3].max()
        
        axs[0][2].hist(evolved_stars['final_mass'][evolved_stars['remnant'] == 3] , bins = 100, color = 'black', alpha = 0.4, density = False, label = 'BH', range = (0, max_mass))




        
        max_age = evolved_stars['age'][evolved_stars['remnant'] == 1].max()
        
        axs[1][0].hist(evolved_stars['age'][evolved_stars['remnant'] == 1] , bins = 100, color = 'gray', alpha = 0.4, density = False, label = 'WD', range = (0, max_age))

        max_age = evolved_stars['age'][evolved_stars['remnant'] == 2].max()
        
        axs[1][1].hist(evolved_stars['age'][evolved_stars['remnant'] == 2] , bins = 100, color = 'blue', alpha = 0.4, density = False, label = 'NS', range = (0, max_age))

        max_age = evolved_stars['age'][evolved_stars['remnant'] == 3].max()
        
        axs[1][2].hist(evolved_stars['age'][evolved_stars['remnant'] == 3] , bins = 100, color = 'black', alpha = 0.4, density = False, label = 'BH', range = (0, max_age))




        
        axs[0][0].set_xlabel('M [M$_\\odot$]')
        axs[0][0].set_ylabel('Counts')
        axs[0][1].set_xlabel('M [M$_\\odot$]')
        axs[0][1].set_ylabel('Counts')
        axs[0][2].set_xlabel('M [M$_\\odot$]')
        axs[0][2].set_ylabel('Counts')
        axs[1][0].set_xlabel('Age [Gyr]')
        axs[1][0].set_ylabel('Counts')
        axs[1][1].set_xlabel('Age [Gyr]')
        axs[1][1].set_ylabel('Counts')
        axs[1][2].set_xlabel('Age [Gyr]')
        axs[1][2].set_ylabel('Counts')

        axs[1][0].legend()
        axs[1][1].legend()
        axs[1][2].legend()

        fig.suptitle('Mass and Age distribution for evolved stars')


        plt.savefig(fig_path + 'evolved_mass_age_distribution.pdf', dpi = 300)
        plt.show()

    return print(f'Check your plots at {fig_path}')






if __name__ == "__main__":

    initial_star_number = int(input("Number of stars to simulate: "))
    seed = int(input("Random Seed: "))

    plot_prompt = main(initial_star_number, seed)

    if plot_prompt == 'y':
        
        plot_ms = input('Would you like to plot the mass and age distribution of the main sequence stars? (y/n): ') 
        plot_evolved = input('Would you like to plot the mass and age distribution of the evolved stars? (y/n): ') 
        fig_path = input('Directory to save files: ') 

        plots(plot_ms, plot_evolved, fig_path)
        
    else:
        print('Done! :)')
    
