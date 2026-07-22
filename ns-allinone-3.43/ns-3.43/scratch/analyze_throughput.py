import os
import subprocess
import sys
import re
import matplotlib.pyplot as plt

def get_packet_sizes(student_id):
    # Divide student ID into 2 halves
    mid = len(student_id) // 2
    h1 = student_id[:mid]
    h2 = student_id[mid:]
    
    # Reverse the digits
    h1_rev = h1[::-1]
    h2_rev = h2[::-1]
    
    # Convert to integers
    sizes = [int(h1), int(h2), int(h1_rev), int(h2_rev)]
    print(f"Student ID: {student_id}")
    print(f"Divided halves: {h1}, {h2}")
    print(f"Reversed halves: {h1_rev}, {h2_rev}")
    print(f"Packet sizes: {sizes}")
    return sizes

def run_simulation(packet_size):
    print(f"\n--- Running simulation for Packet Size: {packet_size} bytes ---")
    cmd = ["./ns3", "run", f"scratch/first.cc --packetSize={packet_size}"]
    
    # Run the command and capture output
    result = subprocess.run(cmd, capture_output=True, text=True)
    stdout = result.stdout
    stderr = result.stderr
    
    # Combine outputs since ns-3 logs/output might go to stdout or stderr
    full_output = stdout + "\n" + stderr
    
    # Find throughput
    # Look for: Throughput: <val> bps
    match = re.search(r"Throughput:\s*([\d\.]+)\s*bps", full_output)
    if match:
        throughput = float(match.group(1))
        print(f"Successfully extracted Throughput: {throughput} bps")
        return throughput
    else:
        print(f"Error: Throughput not found for packet size {packet_size}!")
        print("Simulator output:")
        print(full_output)
        return None

def main():
    student_id = "24252627" # default/example ID
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
        # Validate that the student ID has even number of digits
        if not student_id.isdigit() or len(student_id) % 2 != 0 or len(student_id) < 2:
            print("Error: Student ID must be an even-length digit string (e.g., 24252627)")
            sys.exit(1)
            
    sizes = get_packet_sizes(student_id)
    
    throughputs = []
    valid_sizes = []
    
    for size in sizes:
        tp = run_simulation(size)
        if tp is not None:
            throughputs.append(tp)
            valid_sizes.append(size)
            
    if not throughputs:
        print("Error: No throughput data collected.")
        sys.exit(1)
        
    # Sort by packet size for a proper line plot
    paired = sorted(zip(valid_sizes, throughputs))
    sorted_sizes, sorted_throughputs = zip(*paired)
    
    print("\n--- Summary Results ---")
    for s, t in zip(sorted_sizes, sorted_throughputs):
        print(f"Packet Size: {s} bytes | Throughput: {t} bps")
        
    # Plot results
    plt.figure(figsize=(8, 6))
    plt.plot(sorted_sizes, sorted_throughputs, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    
    # Add data labels
    for s, t in zip(sorted_sizes, sorted_throughputs):
        plt.annotate(f"{t:.1f} bps", (s, t), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
        
    plt.title(f"Throughput vs Packet Size (Student ID: {student_id})", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Packet Size (bytes)", fontsize=12, labelpad=10)
    plt.ylabel("Throughput (bps)", fontsize=12, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Save the plot
    plot_path = "throughput_plot.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot successfully saved to: {os.path.abspath(plot_path)}")

if __name__ == "__main__":
    main()
