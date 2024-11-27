def kalirai_ifmr(masses, remnants):

    '''
    INPUT

    masses: randomly generated masses
    remnants: classification assigned according to initial mass

    RETURNS

    final_masses: array containing the final mass for each star, according to Kalirai (2008) and Raithel (2018)*

    *We have added two linear interpolations to fill the gaps between 21.7 and 25.2 Msun for neutron stars, and 40 to 45 Msun for black holes


    
    '''
    import numpy as np 

    from scipy.interpolate import interp1d
    
    final_masses = np.zeros(len(masses))

    white_dwarfs = (remnants == 1)
        
    final_masses[white_dwarfs] = 0.109*masses[white_dwarfs] + 0.394


    neutron_stars = (remnants == 2)
    
    ns_1 = (9 <= masses) & (masses <= 13) & neutron_stars
    final_masses[ns_1] = (2.24 + 0.508 * (masses[ns_1] - 14.75) + 0.125 * (masses[ns_1] - 14.75) ** 2 + 0.011 * (masses[ns_1] - 14.75) ** 3)

    ns_2 = (13 < masses) & (masses < 15)& neutron_stars
    final_masses[ns_2] = 0.123 + 0.112 * masses[ns_2]

    ns_3 = (15 <= masses) & (masses < 17.8)& neutron_stars
    final_masses[ns_3] = 0.996 + 0.0384 * masses[ns_3]

    ns_4 = (17.8 <= masses) & (masses < 18.5)& neutron_stars
    final_masses[ns_4] = -0.020 + 0.10 * masses[ns_4]

    ns_5 = (18.5 <= masses) & (masses < 21.7)& neutron_stars
    final_masses[ns_5] = np.random.normal(1.6, 0.158, size=np.sum(ns_5))


    ns_extra = (masses >=  21.7) & (masses < 25.2) & neutron_stars

    up_lim = ( 3232.29 - 409.429*(25.2 - 2.619) + 17.2867*(25.2 - 2.619)**2 - 0.24315*(25.2 - 2.619)**3)

    interpolator = interp1d([21.7, 25.2], [ 1.6, up_lim])

    final_masses[ns_extra] = [interpolator(m_i) for m_i in masses[ns_extra]]

    ns_6 = (25.2 <= masses) & (masses < 27.5)& neutron_stars
    final_masses[ns_6] = ( 3232.29 - 409.429*(masses[ns_6] - 2.619) + 17.2867*(masses[ns_6] - 2.619)**2 - 0.24315*(masses[ns_6] - 2.619)**3 )



    
    black_holes = (remnants == 3)
    
    bh_1 = (15 <= masses) & (masses <= 40) & black_holes
    mcore = -2.049 + 0.4140*masses[bh_1]
    mall = (15.52 - 0.3294*(masses[bh_1] - 25.97) - 0.02121*(masses[bh_1] - 25.97)**2 + 0.003120*(masses[bh_1] - 25.97)**3)
    final_masses[bh_1] = 0.9*mcore + (1 - 0.9)*mall



    bh_extra = (masses >  40) & (masses < 45) & black_holes

    low_lim = 0.9*(-2.049 + 0.4140*40) + (1 - 0.9)*((15.52 - 0.3294*(40 - 25.97) - 0.02121*(40 - 25.97)**2 + 0.003120*(40 - 25.97)**3))

    up_lim = 5.697 + 7.8598 * 10**8 * (45)**-4.858

    interpolator = interp1d([40,45], [ low_lim, up_lim])

    final_masses[bh_extra] = [interpolator(m_i) for m_i in masses[bh_extra]]




    bh_2 = (45 <= masses) & (masses <= 100) & black_holes
    final_masses[bh_2] = 5.697 + 7.8598 * 10**8 * (masses[bh_2])**-4.858

    
    return final_masses
