def kroupa_imf(m):
    '''
    INPUT

    m: array of mass values

    RETURNS
    
    imf: array of IMF probabilities for each mass according to Kroupa (2001)
    
    '''
    import numpy as np

    imf = np.where(m<=0.5, (m/0.08)**-1.3, (0.5/0.08)**-1.3 * (m/0.5)**-2.3)
    
    return imf
        
        
