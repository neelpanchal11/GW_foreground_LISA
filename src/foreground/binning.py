import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from legwork import strain, psd

# --- Function to process a galaxy: clean, mask, bin, and plot ---
def bin_unresolved_galaxy(galaxy_df, galaxy_name="Galaxy", min_sources=4, plot=True):
    """
    Given a galaxy DataFrame and its distance array,
    mask unresolved binaries, bin the unresolved PSD,
    and optionally plot the result.

    Returns:
    - f_fit_unresolved: frequencies of valid bins [Hz]
    - psd_fit_unresolved: corresponding PSD [strain²/Hz]
    """

    # Step 1: Clean the galaxy (porb > 0 and finite)
    distance_array = np.sqrt(galaxy_df['x_kpc'].values**2 + galaxy_df['y_kpc'].values**2 + galaxy_df['z_kpc'].values**2) * u.kpc
    valid_mask = (galaxy_df['porb'] > 0) & (np.isfinite(galaxy_df['porb']))
    df_clean = galaxy_df[valid_mask]
    dist_clean = distance_array[valid_mask]

    porb_clean = df_clean['porb'].values * u.day
    f_orb_clean = (1 / porb_clean).to(u.Hz)
    f_gw_clean = 2 * f_orb_clean

    m1_clean = df_clean['mass_1'].values * u.Msun
    m2_clean = df_clean['mass_2'].values * u.Msun
    ecc_clean = df_clean['ecc'].values

    # Chirp mass
    def chirp_mass(m1, m2):
        return ((m1 * m2)**(3/5)) / ((m1 + m2)**(1/5))
    
    m_c_clean = chirp_mass(m1_clean, m2_clean)

    # Characteristic strain
    h_c_clean = strain.h_c_n(
        m_c=m_c_clean,
        f_orb=f_orb_clean,
        ecc=ecc_clean,
        n=2,
        dist=dist_clean
    ).flatten()

    # Step 2: SNR calculation
    S_n_clean = psd.power_spectral_density(f_gw_clean)
    snr_clean = np.sqrt(h_c_clean**2 / (f_gw_clean * S_n_clean))

    # Step 3: Mask unresolved (SNR < 7)
    unresolved_mask = (snr_clean < 7)
    f_gw_unresolved = f_gw_clean[unresolved_mask]
    h_c_unresolved = h_c_clean[unresolved_mask]

    # Step 4: Bin the unresolved binaries
    bins = np.logspace(np.log10(np.min(f_gw_unresolved.value)), np.log10(np.max(f_gw_unresolved.value)), 100)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])

    psd_est_unresolved = np.full_like(bin_centers, fill_value=np.nan)

    for i in range(len(bin_centers)):
        idx = (f_gw_unresolved.value >= bins[i]) & (f_gw_unresolved.value < bins[i+1])
        if np.sum(idx) >= min_sources:
            psd_est_unresolved[i] = np.mean((h_c_unresolved[idx])**2 / f_gw_unresolved[idx].to(u.Hz).value)

    valid = (~np.isnan(psd_est_unresolved)) & (psd_est_unresolved > 0)
    f_fit_unresolved = bin_centers[valid]
    psd_fit_unresolved = psd_est_unresolved[valid]

    # Step 5: Plot (optional)
    if plot:
        plt.figure(figsize=(12, 8))
        plt.loglog(f_fit_unresolved, psd_fit_unresolved, '.', color='black')
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("PSD [strain²/Hz]")
        plt.title(f"Binned PSD (Unresolved Sources) - {galaxy_name}")
        plt.grid(True, which="both", ls=":")
        plt.tight_layout()
        plt.show()

    return f_fit_unresolved, psd_fit_unresolved

'''
Example Use:
f_fit_unresolved, psd_fit_unresolved = bin_unresolved_galaxy(g1110_0021, galaxy_name = "G1110_0021")
'''
