import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

class LPFDesign:
    def __init__(self, er=4.4, h=1.6e-3, tand=0.025):
        self.er = er
        self.h = h
        self.tand = tand
        self.c = constants.c
        self.Z0 = 50  # System impedance
        
    def calc_microstrip_width(self, Z_target):
        """Calculate microstrip width for target impedance"""
        # Simplified formula for microstrip width
        if Z_target < 44:
            w_h = 2/np.pi * (self.er - 1) * np.log(np.pi/2) + (1/np.pi) * np.log(4/np.pi)
        else:
            A = Z_target * np.sqrt((self.er + 1)/2) / 60 + (self.er - 1)/(self.er + 1) * (0.23 + 0.11/self.er)
            w_h = 8 * np.exp(A) / (np.exp(2*A) - 2)
        
        return w_h * self.h
    
    def design_stepped_lpf(self, fc=3e9, n=5):
        """Design stepped impedance LPF"""
        # Chebyshev prototype values for n=5, 0.1dB ripple
        g = [1.0, 0.6180, 1.6180, 2.0000, 1.6180, 0.6180, 1.0]
        
        # Calculate impedances
        Z_high = []
        Z_low = []
        
        for i in range(1, n+1):
            if i % 2 == 1:  # Odd sections (series inductors -> high Z)
                Z_h = self.Z0 * np.sqrt(1 + g[i] * (np.pi/2) * (self.Z0/50))
                Z_high.append(Z_h)
            else:  # Even sections (shunt capacitors -> low Z)
                Z_l = self.Z0 / np.sqrt(1 + g[i] * (np.pi/2) * (50/self.Z0))
                Z_low.append(Z_l)
        
        # Calculate physical dimensions
        lambda_g = self.c / (fc * np.sqrt(self.er))
        section_length = lambda_g / 8  # Quarter wavelength sections
        
        # Calculate widths
        widths_high = [self.calc_microstrip_width(Z) for Z in Z_high]
        widths_low = [self.calc_microstrip_width(Z) for Z in Z_low]
        
        return {
            'Z_high': Z_high,
            'Z_low': Z_low,
            'widths_high': widths_high,
            'widths_low': widths_low,
            'section_length': section_length,
            'lambda_g': lambda_g
        }
    
    def calc_lpf_response(self, design_params, f_range=(0.1e9, 6e9, 1000)):
        """Calculate LPF frequency response"""
        f = np.linspace(f_range[0], f_range[1], f_range[2])
        
        # Simplified transmission line model
        # This is a basic approximation - actual EM simulation needed for accuracy
        
        S21_total = np.ones(len(f), dtype=complex)
        
        # High impedance sections (series inductors)
        for Z_h in design_params['Z_high']:
            # Inductive reactance approximation
            XL = 2 * np.pi * f * 1e-9  # Simplified inductance
            Z_series = Z_h + 1j * XL
            S21_section = 2 * self.Z0 / (Z_series + 2 * self.Z0)
            S21_total *= S21_section
        
        # Low impedance sections (shunt capacitors)
        for Z_l in design_params['Z_low']:
            # Capacitive reactance approximation
            XC = -1 / (2 * np.pi * f * 1e-12)  # Simplified capacitance
            Y_shunt = 1/Z_l + 1j/XC
            S21_section = 1 / (1 + Y_shunt * self.Z0 / 2)
            S21_total *= S21_section
        
        S11 = 1 - S21_total  # Simplified reflection
        
        return f, S11, S21_total
    
    def plot_lpf_response(self, design_params):
        """Plot LPF frequency response"""
        f, S11, S21 = self.calc_lpf_response(design_params)
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(f/1e9, 20*np.log10(np.abs(S21)), 'b-', linewidth=2)
        plt.ylabel('|S21| (dB)')
        plt.xlabel('Frequency (GHz)')
        plt.title('LPF Insertion Loss')
        plt.grid(True)
        plt.axvline(x=3, color='r', linestyle='--', label='Cutoff (3 GHz)')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(f/1e9, 20*np.log10(np.abs(S11)), 'r-', linewidth=2)
        plt.ylabel('|S11| (dB)')
        plt.xlabel('Frequency (GHz)')
        plt.title('LPF Return Loss')
        plt.grid(True)
        plt.axvline(x=3, color='r', linestyle='--', label='Cutoff (3 GHz)')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    def print_design_summary(self, design_params):
        """Print design summary"""
        print("LPF Design Summary (FR4 substrate):")
        print(f"Substrate: εr = {self.er}, h = {self.h*1000:.1f} mm, tan δ = {self.tand}")
        print(f"Section length: {design_params['section_length']*1000:.2f} mm")
        print("\nHigh impedance sections:")
        for i, (Z, w) in enumerate(zip(design_params['Z_high'], design_params['widths_high'])):
            print(f"  Section {i+1}: Z = {Z:.1f} Ω, w = {w*1000:.2f} mm")
        print("\nLow impedance sections:")
        for i, (Z, w) in enumerate(zip(design_params['Z_low'], design_params['widths_low'])):
            print(f"  Section {i+1}: Z = {Z:.1f} Ω, w = {w*1000:.2f} mm")

# Question 9 implementation
def question_9():
    """LPF design"""
    print("Question 9: Low-Pass Filter Design")
    
    designer = LPFDesign()
    design_params = designer.design_stepped_lpf(fc=3e9, n=5)
    
    designer.print_design_summary(design_params)
    designer.plot_lpf_response(design_params)
    
    return design_params

if __name__ == "__main__":
    question_9()