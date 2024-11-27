def filter_imf(random_probs, imf_probs):

    '''
    INPUT 

    random_probs: array of random uniform probabilities
    imf_probs: array of IMF probabilities calculated for each mass (Kroupa (2001))

    
    RETURNS 

    in_imf: an array of True or False depending on if random_probs (< or >) imf_probs
    
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

   
    in_imf  = (random_probs < imf_probs)
        
    return in_imf




def filter_evolved(random_ages,ms_lifetimes):

    '''
    INPUT 

    random_ages: array of random uniform ages
    ms_lifetimes: array of the Main Sequence lifetime calculated for each mass (CITE)


    RETURNS 

    is_evolved: an array of True or False depending on if random_ages (< or >) ms_lifetimes

    * if the age is bigger than the MS lifetime, the star has had enough time to evolve, and therefore is_evolved == True
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

           
    is_evolved = (ms_lifetimes <= random_ages)
    is_not_evolved = (ms_lifetimes > random_ages)

    
    print(
    f''' STATISTICS
        Stars in the MS: {sum(is_not_evolved==True)}
        Stars out of the MS: {sum(is_evolved==True)}''')

    
    return is_evolved
