import numpy as np
import matplotlib.pyplot as plt

class ADSSimulationGuide:
    """Guide for ADS simulation procedures"""
    
    def __init__(self):
        self.substrate_params = {
            'er': 4.4,
            'h': 1.6e-3,
            'tand': 0.025,
            'material': 'FR4'
        }
    
    def circuit_simulation_procedure(self):
        """Question 10a: Circuit model simulation procedure"""
        procedure = """
        ADS Circuit Model Simulation Procedure:
        
        1. Create New Project:
           - File → New → Project
           - Name: LPF_Circuit_Model
        
        2. Create Schematic:
           - Insert → Schematic
           - Add components from palette:
             * MLIN (Microstrip Line) for each section
             * Term (50Ω terminations) at ports
        
        3. Set Microstrip Parameters:
           - Double-click each MLIN component
           - Set W (width) and L (length) from design
           - Reference substrate: MSUB
        
        4. Add Substrate Definition:
           - Insert → Template → MSUB
           - Set: Er=4.4, H=1.6mm, TanD=0.025, T=35μm
        
        5. Add S-Parameter Simulation:
           - Insert → Simulation → S_Param
           - Set frequency range: 0.1 to 6 GHz, 1000 points
        
        6. Run Simulation:
           - Simulate → Simulate
        
        7. Plot Results:
           - Data Display → Rectangular Plot
           - Add S21 (dB) and S11 (dB) vs frequency
        """
        print(procedure)
        return procedure
    
    def layout_simulation_procedure(self):
        """Question 10b: EM simulation procedure"""
        procedure = """
        ADS Layout/EM Simulation Procedure:
        
        1. Create Layout:
           - Layout → Generate/Update Layout
           - Or manually: Insert → Layout
        
        2. Draw Microstrip Structures:
           - Use MLIN_LAYOUT or draw rectangles
           - Set layer: cond (conductor)
           - Set dimensions from circuit design
        
        3. Add Ports:
           - Insert → Port → Internal Port
           - Place at input/output of filter
           - Set reference plane and impedance (50Ω)
        
        4. Define Substrate:
           - Substrate → Stackup
           - Add layers: Ground plane, Dielectric (FR4), Metal
           - Set thickness and material properties
        
        5. Set Mesh:
           - EM → Mesh → View Mesh
           - Ensure adequate mesh density
           - Cells per wavelength > 20
        
        6. EM Simulation Setup:
           - EM → Simulation → Momentum
           - Set frequency range: 0.1 to 6 GHz
           - Set adaptive frequency sampling
        
        7. Run EM Simulation:
           - EM → Simulate
        
        8. View Results:
           - Data Display → Plot S-parameters
           - Compare with circuit model
        """
        print(procedure)
        return procedure
    
    def generate_comparison_plot(self):
        """Generate sample comparison plot for Question 11"""
        # Simulated data (example)
        f = np.linspace(0.1e9, 6e9, 1000)
        
        # Circuit model (ideal)
        fc = 3e9
        n = 5
        S21_circuit = 1 / (1 + (f/fc)**(2*n))
        S21_circuit_db = 20 * np.log10(np.abs(S21_circuit))
        
        # EM simulation (with parasitics)
        S21_em = S21_circuit * (1 - 0.1 * (f/fc)**2)  # Add some realistic effects
        S21_em_db = 20 * np.log10(np.abs(S21_em))
        
        # Layout with discontinuities
        S21_layout = S21_em * (1 - 0.05 * np.sin(2*np.pi*f/fc))
        S21_layout_db = 20 * np.log10(np.abs(S21_layout))
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(f/1e9, S21_circuit_db, 'b-', linewidth=2, label='Circuit Model')
        plt.plot(f/1e9, S21_em_db, 'r--', linewidth=2, label='EM Simulation')
        plt.plot(f/1e9, S21_layout_db, 'g:', linewidth=2, label='Layout (with discontinuities)')
        plt.ylabel('|S21| (dB)')
        plt.xlabel('Frequency (GHz)')
        plt.title('LPF Response Comparison')
        plt.grid(True)
        plt.legend()
        plt.axvline(x=3, color='k', linestyle='--', alpha=0.5, label='Cutoff')
        
        plt.subplot(1, 2, 2)
        # Return loss comparison
        S11_circuit = 1 - S21_circuit
        S11_em = 1 - S21_em
        S11_layout = 1 - S21_layout
        
        plt.plot(f/1e9, 20*np.log10(np.abs(S11_circuit)), 'b-', linewidth=2, label='Circuit Model')
        plt.plot(f/1e9, 20*np.log10(np.abs(S11_em)), 'r--', linewidth=2, label='EM Simulation')
        plt.plot(f/1e9, 20*np.log10(np.abs(S11_layout)), 'g:', linewidth=2, label='Layout')
        plt.ylabel('|S11| (dB)')
        plt.xlabel('Frequency (GHz)')
        plt.title('Return Loss Comparison')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
        # Analysis
        analysis = """
        Comparison Analysis:
        
        1. Circuit Model:
           - Ideal lumped element behavior
           - Smooth frequency response
           - No parasitic effects
        
        2. EM Simulation:
           - Includes distributed effects
           - Frequency dispersion
           - Substrate losses
           - More realistic performance
        
        3. Layout Simulation:
           - Includes discontinuities
           - Coupling effects
           - Manufacturing tolerances
           - Most accurate prediction
        
        Key Differences:
        - EM simulation shows higher insertion loss due to losses
        - Layout includes spurious resonances from discontinuities
        - Stopband rejection may differ due to parasitic coupling
        """
        print(analysis)

# Questions 10-11 implementation
def questions_10_11():
    """ADS simulation procedures and comparison"""
    print("Questions 10-11: ADS Simulation and Comparison")
    
    guide = ADSSimulationGuide()
    
    print("="*60)
    print("QUESTION 10a: Circuit Model Simulation")
    print("="*60)
    guide.circuit_simulation_procedure()
    
    print("\n" + "="*60)
    print("QUESTION 10b: Layout/EM Simulation")
    print("="*60)
    guide.layout_simulation_procedure()
    
    print("\n" + "="*60)
    print("QUESTION 11: Results Comparison")
    print("="*60)
    guide.generate_comparison_plot()

if __name__ == "__main__":
    questions_10_11()