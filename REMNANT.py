def remnant(m):
    '''
    INPUT

    m: array of mass values 

    RETURNS

    r_list: list of remnant labels, ( 1 == WD, 2 == NS, 3 == BH )
    '''
    import random
    import numpy as np
    r_list = np.empty(len(m))


    wd_mask = m < 9

    r_list[wd_mask] = 1

    ns_mask = (m > 9) & (m < 15)
    
    r_list[ns_mask] = 2
    
    ns_bh_mask = (m > 15) & (m <= 27.5)

    random_ns_bh = np.random.uniform(0,1,sum(ns_bh_mask))

    ns_mask = random_ns_bh > 0.4
        
    r_list[ns_bh_mask][ns_mask] = 2
    
    bh_mask = random_ns_bh < 0.4
        
    r_list[ns_bh_mask][bh_mask] = 3
    

    bh_mask = m > 27.5

    r_list[bh_mask] = 3


    
    return r_list
    
    