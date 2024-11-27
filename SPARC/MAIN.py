def main(initial_star_number = 100, seed = 1): 
    '''
    
    INPUT
    
    initial_star_number: stars to be randomly generated, default is 100


    STEPS

    1) Generate data
    random_probs: random uniform probabilities with values from 0 to 1
    random_masses: random uniform masses from 0.08 to 100 Msun

    2) Calculate the IMF probability for each mass, and eliminate those with random probability larger than IMF probability

    3) Generate random ages from a uniform distribution for all stars below the IMF boundary, and calculate Main Sequence (MS) lifetimes using the mass values

    4) Classify the star as MS or evolved, as follows:
    age < t_MS: not evolved, still in MS
    age > t_MS: evolved

    5) Assing the respective remnant labels to the evolved stars, based on their initial masses

    7) Calculate final masses for the stars according to the remnant type and their mass

    8) Create two dataframes:

    ms_stars: All stars in the MS, that are below the IMF limit; includes only mass and ages

    evolved_stars: Stars that have evolved out of the MS; includes mass, age, remnant type and final mass

    Both of these dataframes are saved in separate .csv files once the program finishes

    9) OPTIONAL: plot the distribution of masses and ages for MS and evolved stars


    RETURNS
    A file containing the masses, ages, remnant type and final mass for stars out of the MS
    '''
    
    import numpy as np
    import matplotlib.pyplot as plt
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
                       'is_evolved': is_evolved[is_evolved],
                       'final_mass': final_masses})
    df.to_csv('evolved_stars.csv', index = False)
    

    df = pd.DataFrame({'mass': masses_in_imf[~is_evolved],
                       'age': random_ages[~is_evolved]})
    
    df.to_csv('ms_stars.csv', index = False)

    
    end_time = time.time() 
    execution_time = end_time - start_time 

    print(f'This took {execution_time} seconds')

    
    return  input("Would you like to plot results? (y/n): ")


def plots(plot_ms, plot_evolved):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    
    evolved_stars = pd.read_csv('evolved_stars.csv')
    ms_stars = pd.read_csv('ms_stars.csv')

    
    if plot_ms == 'y':
        max_mass = ms_stars['mass'].max()
        
        fig, axs = plt.subplots(nrows = 1, ncols = 2,  figsize = (15,10))

        weights = np.ones(len(ms_stars))/float(len(ms_stars))
        
        axs[0].hist(ms_stars['mass'], bins = 100, color = 'red', alpha = 0.4, weights = weights, range = (0, max_mass))
        axs[0].set_xlabel('M [M$_\\odot$]')
        axs[0].set_ylabel('Density')


        axs[1].hist(ms_stars['age'], bins = 100, color = 'red', alpha = 0.4, weights = weights, range = (0, max_mass))
        axs[1].set_xlabel('Age [Gyr]')
        axs[1].set_ylabel('Density')

        fig.suptitle('Mass and Age distribution for MS stars')

        plt.tight_layout()
        plt.savefig('ms_mass_age_distribution.pdf', dpi = 300)

        plt.show()


        if plot_evolved == 'y':
            input('Click ENTER to go to next plot')

    
    if plot_evolved == 'y':

        fig, axs = plt.subplots(nrows = 2, ncols = 3, figsize = (15,15))

        max_mass = evolved_stars['final_mass'][evolved_stars['remnant'] == 1].max()
        weights = np.ones(len(evolved_stars[evolved_stars['remnant'] == 1]))/float(len(evolved_stars[evolved_stars['remnant'] == 1]))

        axs[0][0].hist(evolved_stars['final_mass'][evolved_stars['remnant'] == 1] , bins = 100, color = 'gray', alpha = 0.4, weights = weights, label = 'WD', range = (0, max_mass))




        max_mass = evolved_stars['final_mass'][evolved_stars['remnant'] == 2].max()
        weights = np.ones(len(evolved_stars[evolved_stars['remnant'] == 2]))/float(len(evolved_stars[evolved_stars['remnant'] == 2]))

        axs[0][1].hist(evolved_stars['final_mass'][evolved_stars['remnant'] == 2] , bins = 100, color = 'blue', alpha = 0.4, weights = weights, label = 'NS', range = (0, max_mass))




        max_mass = evolved_stars['final_mass'][evolved_stars['remnant'] == 3].max()
        weights = np.ones(len(evolved_stars[evolved_stars['remnant'] == 3]))/float(len(evolved_stars[evolved_stars['remnant'] == 3]))

        axs[0][2].hist(evolved_stars['final_mass'][evolved_stars['remnant'] == 3] , bins = 100, color = 'black', alpha = 0.4, weights = weights, label = 'BH', range = (0, max_mass))




        
        max_age = evolved_stars['age'][evolved_stars['remnant'] == 1].max()
        weights = np.ones(len(evolved_stars[evolved_stars['remnant'] == 1]))/float(len(evolved_stars[evolved_stars['remnant'] == 1]))

        axs[1][0].hist(evolved_stars['age'][evolved_stars['remnant'] == 1] , bins = 100, color = 'gray', alpha = 0.4, weights = weights, label = 'WD', range = (0, max_age))



        max_age = evolved_stars['age'][evolved_stars['remnant'] == 2].max()
        weights = np.ones(len(evolved_stars[evolved_stars['remnant'] == 2]))/float(len(evolved_stars[evolved_stars['remnant'] == 2]))

        axs[1][1].hist(evolved_stars['age'][evolved_stars['remnant'] == 2] , bins = 100, color = 'blue', alpha = 0.4, weights = weights, label = 'NS', range = (0, max_age))



        max_age = evolved_stars['age'][evolved_stars['remnant'] == 3].max()
        weights = np.ones(len(evolved_stars[evolved_stars['remnant'] == 3]))/float(len(evolved_stars[evolved_stars['remnant'] == 3]))

        axs[1][2].hist(evolved_stars['age'][evolved_stars['remnant'] == 3] , bins = 100, color = 'black', alpha = 0.4, weights = weights, label = 'BH', range = (0, max_age))




        
        axs[0][0].set_xlabel('M [M$_\\odot$]')
        axs[0][0].set_ylabel('Density')
        axs[0][1].set_xlabel('M [M$_\\odot$]')
        axs[0][1].set_ylabel('Density')
        axs[0][2].set_xlabel('M [M$_\\odot$]')
        axs[0][2].set_ylabel('Density')
        axs[1][0].set_xlabel('Age [Gyr]')
        axs[1][0].set_ylabel('Density')
        axs[1][1].set_xlabel('Age [Gyr]')
        axs[1][1].set_ylabel('Density')
        axs[1][2].set_xlabel('Age [Gyr]')
        axs[1][2].set_ylabel('Density')

        axs[1][0].legend()
        axs[1][1].legend()
        axs[1][2].legend()

        fig.suptitle('Final Mass and Age distribution for evolved stars')

        plt.tight_layout()

        plt.savefig('evolved_mass_age_distribution.pdf', dpi = 300)
        plt.show()

    return print('Done! :)')






if __name__ == "__main__":

    initial_star_number = int(input("Number of stars to simulate: "))
    seed = int(input("Random Seed: "))

    plot_prompt = main(initial_star_number, seed)

    if plot_prompt == 'y':
        
        plot_ms = input('Would you like to plot the mass and age distribution of the main sequence stars? (y/n): ') 
        plot_evolved = input('Would you like to plot the mass and age distribution of the evolved stars? (y/n): ') 

        plots(plot_ms, plot_evolved)
        
    else:
        print('Done! :)')
    
