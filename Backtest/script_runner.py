import subprocess

scripts = [
    "./Backtest/CCI.py",
    "./Backtest/RSI.py",
    "./Backtest/MACD.py",
    "./Backtest/Stochastic.py",
    "./Backtest/Double_SMA.py"
]

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(["python3", script], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(f"Error in {script}:\n{result.stderr}")
