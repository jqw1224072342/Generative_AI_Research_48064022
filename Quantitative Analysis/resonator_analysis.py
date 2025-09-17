import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from scipy.optimize import fsolve

class ResonatorAnalysis:
    def __init__(self, er=4.4, h=1.6e-3, tand=0.025):
        self.er = er
        self.h = h
        self.tand = tand
        self.c = constants.c
        
    def calc_resonator_length(self, f_res, w=1e-3):
        """Calculate resonator length for given frequency"""
        # Effective permittivity (simplified)
        eff_er = (self.er + 1)/2 + (self.er - 1)/2 * (1 + 12*self.h/w)**(-0.5)
        
        # Quarter wavelength resonator
        lambda_g = self.c / (f_res * np.sqrt(eff_er))
        length = lambda_g / 4
        
        return length, eff_er
    
    def calc_resonator_s_params(self, d, g, w=1e-3, f_range=(1e9, 10e9, 1000)):
        """Calculate S-parameters for coupled resonator"""
        f = np.linspace(f_range[0], f_range[1], f_range[2])
        
        # Coupling coefficients (simplified model)
        k = 0.1 * np.exp(-g/self.h)  # Gap coupling
        
        # Quality factor
        Q_ext = 100  # External Q
        Q_int = 1000  # Internal Q (loss)
        Q_total = 1/(1/Q_ext + 1/Q_int)
        
        # Resonant frequency (approximate)
        length, eff_er = self.calc_resonator_length(5e9, w)  # 5 GHz nominal
        f_res = self.c / (4 * length * np.sqrt(eff_er))
        
        # S-parameters for coupled resonator
        delta = (f - f_res) / f_res
        
        S11 = (1j * Q_total * delta) / (1 + 1j * Q_total * delta)
        S21 = k / (1 + 1j * Q_total * delta)
        
        return f, S11, S21, f_res, length
    
    def plot_resonator_response(self, d_list, g_list):
        """Plot resonator S-parameters for different d and g values"""
        plt.figure(figsize=(12, 8))
        
        for d in d_list:
            for g in g_list:
                f, S11, S21, f_res, length = self.calc_resonator_s_params(d, g)
                
                plt.subplot(2, 2, 1)
                plt.plot(f/1e9, 20*np.log10(np.abs(S11)), 
                        label=f'd={d*1000:.1f}mm, g={g*1000:.2f}mm')
                plt.ylabel('|S11| (dB)')
                plt.xlabel('Frequency (GHz)')
                plt.title('Return Loss')
                plt.grid(True)
                plt.legend()
                
                plt.subplot(2, 2, 2)
                plt.plot(f/1e9, 20*np.log10(np.abs(S21)), 
                        label=f'd={d*1000:.1f}mm, g={g*1000:.2f}mm')
                plt.ylabel('|S21| (dB)')
                plt.xlabel('Frequency (GHz)')
                plt.title('Transmission')
                plt.grid(True)
                plt.legend()
                
                plt.subplot(2, 2, 3)
                plt.plot(f/1e9, np.angle(S11)*180/np.pi, 
                        label=f'd={d*1000:.1f}mm, g={g*1000:.2f}mm')
                plt.ylabel('Phase S11 (deg)')
                plt.xlabel('Frequency (GHz)')
                plt.title('S11 Phase')
                plt.grid(True)
                plt.legend()
                
                plt.subplot(2, 2, 4)
                plt.plot(f/1e9, np.angle(S21)*180/np.pi, 
                        label=f'd={d*1000:.1f}mm, g={g*1000:.2f}mm')
                plt.ylabel('Phase S21 (deg)')
                plt.xlabel('Frequency (GHz)')
                plt.title('S21 Phase')
                plt.grid(True)
                plt.legend()
        
        plt.suptitle('Resonator S-Parameters')
        plt.tight_layout()
        plt.show()
    
    def find_resonator_dimensions_8ghz(self):
        """Find d and g for 8 GHz resonance"""
        target_freq = 8e9
        
        # Calculate required length for 8 GHz
        length, eff_er = self.calc_resonator_length(target_freq)
        
        # Optimize d and g (simplified approach)
        d_opt = length  # Resonator length
        g_opt = 0.1e-3  # Small gap for tight coupling
        
        print(f"For 8 GHz resonance:")
        print(f"Required d = {d_opt*1000:.2f} mm")
        print(f"Required g = {g_opt*1000:.2f} mm")
        print(f"Resonator length = {length*1000:.2f} mm")
        
        return d_opt, g_opt, length

# Question 8 implementation
def question_8():
    """Resonator analysis"""
    print("Question 8: Resonator Analysis")
    
    analyzer = ResonatorAnalysis()
    
    # Base analysis
    d_base = 6e-3  # 6 mm
    g_base = 0.05e-3  # 0.05 mm
    
    f, S11, S21, f_res, length = analyzer.calc_resonator_s_params(d_base, g_base)
    
    print(f"Resonant frequency: {f_res/1e9:.2f} GHz")
    print(f"Resonator length at resonance: {length*1000:.2f} mm")
    
    # Compare different d and g values
    analyzer.plot_resonator_response([6e-3], [0.05e-3, 0.1e-3])
    
    # Find dimensions for 8 GHz
    analyzer.find_resonator_dimensions_8ghz()

if __name__ == "__main__":
    question_8()