import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
import pandas as pd

class MicrostripAnalysis:
    def __init__(self, er=4.4, h=1.6e-3, tand=0.025, f_range=(1e9, 10e9, 1000)):
        self.er = er  # Relative permittivity
        self.h = h    # Substrate height (m)
        self.tand = tand  # Loss tangent
        self.f = np.linspace(f_range[0], f_range[1], f_range[2])
        self.c = constants.c
        
    def calc_microstrip_params(self, w):
        """Calculate microstrip line parameters"""
        # Effective permittivity
        if w/self.h >= 1:
            self.eff_er = (self.er + 1)/2 + (self.er - 1)/2 * (1 + 12*self.h/w)**(-0.5)
        else:
            self.eff_er = (self.er + 1)/2 + (self.er - 1)/2 * ((1 + 12*self.h/w)**(-0.5) + 0.04*(1 - w/self.h)**2)
        
        # Characteristic impedance
        if w/self.h >= 1:
            self.Z0 = 120*np.pi / (np.sqrt(self.eff_er) * (w/self.h + 1.393 + 0.667*np.log(w/self.h + 1.444)))
        else:
            self.Z0 = 60/np.sqrt(self.eff_er) * np.log(8*self.h/w + w/(4*self.h))
        
        return self.Z0, self.eff_er
    
    def calc_s_parameters(self, w, length):
        """Calculate S-parameters for microstrip line"""
        Z0, eff_er = self.calc_microstrip_params(w)
        
        # Propagation constant
        beta = 2*np.pi*self.f*np.sqrt(eff_er)/self.c
        
        # Attenuation (simplified)
        alpha_d = np.pi*self.f*np.sqrt(eff_er)*self.tand/self.c  # Dielectric loss
        alpha_c = 8.686 * 0.1 * np.sqrt(self.f)  # Conductor loss (simplified)
        alpha = alpha_d + alpha_c
        
        # Propagation constant with loss
        gamma = alpha + 1j*beta
        
        # S-parameters for transmission line
        Z_ref = 50  # Reference impedance
        
        # Reflection coefficient at input
        rho = (Z0 - Z_ref)/(Z0 + Z_ref)
        
        # Transmission line S-parameters
        exp_gl = np.exp(-gamma * length)
        
        S11 = rho * (1 - exp_gl**2) / (1 - rho**2 * exp_gl**2)
        S21 = exp_gl * (1 - rho**2) / (1 - rho**2 * exp_gl**2)
        S12 = S21  # Reciprocal network
        S22 = S11  # Symmetric network
        
        return S11, S21, S12, S22, Z0
    
    def plot_s_parameters(self, w_list, length=10e-3, title_suffix=""):
        """Plot S-parameters for different widths"""
        plt.figure(figsize=(12, 8))
        
        for i, w in enumerate(w_list):
            S11, S21, S12, S22, Z0 = self.calc_s_parameters(w, length)
            
            plt.subplot(2, 2, 1)
            plt.plot(self.f/1e9, 20*np.log10(np.abs(S11)), label=f'w={w*1000:.1f}mm')
            plt.ylabel('|S11| (dB)')
            plt.xlabel('Frequency (GHz)')
            plt.title('Return Loss')
            plt.grid(True)
            plt.legend()
            
            plt.subplot(2, 2, 2)
            plt.plot(self.f/1e9, 20*np.log10(np.abs(S21)), label=f'w={w*1000:.1f}mm')
            plt.ylabel('|S21| (dB)')
            plt.xlabel('Frequency (GHz)')
            plt.title('Insertion Loss')
            plt.grid(True)
            plt.legend()
            
            plt.subplot(2, 2, 3)
            plt.plot(self.f/1e9, np.angle(S11)*180/np.pi, label=f'w={w*1000:.1f}mm')
            plt.ylabel('Phase S11 (deg)')
            plt.xlabel('Frequency (GHz)')
            plt.title('S11 Phase')
            plt.grid(True)
            plt.legend()
            
            plt.subplot(2, 2, 4)
            plt.plot(self.f/1e9, np.angle(S21)*180/np.pi, label=f'w={w*1000:.1f}mm')
            plt.ylabel('Phase S21 (deg)')
            plt.xlabel('Frequency (GHz)')
            plt.title('S21 Phase')
            plt.grid(True)
            plt.legend()
        
        plt.suptitle(f'S-Parameters vs Frequency {title_suffix}')
        plt.tight_layout()
        plt.show()
    
    def analyze_lossless(self, w, length):
        """Check if network is lossless"""
        S11, S21, S12, S22, Z0 = self.calc_s_parameters(w, length)
        
        # For lossless network: |S11|^2 + |S21|^2 = 1
        power_sum = np.abs(S11)**2 + np.abs(S21)**2
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.f/1e9, power_sum, label='|S11|² + |S21|²')
        plt.axhline(y=1, color='r', linestyle='--', label='Lossless limit')
        plt.ylabel('Power Sum')
        plt.xlabel('Frequency (GHz)')
        plt.title('Lossless Network Check')
        plt.grid(True)
        plt.legend()
        plt.show()
        
        return power_sum

# Question 7 implementation
def question_7():
    """Microstrip line analysis with different widths and heights"""
    print("Question 7: Microstrip Line Analysis")
    
    # Base parameters
    analyzer = MicrostripAnalysis()
    
    # Part a: Different widths (2mm and 5mm)
    w_list = [2e-3, 5e-3]  # 2mm and 5mm
    analyzer.plot_s_parameters(w_list, title_suffix="- Width Comparison")
    
    # Part b: Different substrate heights
    for h in [0.5e-3, 1.5e-3]:
        analyzer_h = MicrostripAnalysis(h=h)
        analyzer_h.plot_s_parameters([2e-3], title_suffix=f"- h={h*1000:.1f}mm")
    
    # Lossless analysis
    analyzer.analyze_lossless(2e-3, 10e-3)

if __name__ == "__main__":
    question_7()