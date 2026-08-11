import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Sleek Minimalist Styling
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.edgecolor'] = '#e2e8f0'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['grid.color'] = '#f1f5f9'
plt.rcParams['grid.linestyle'] = '-'
plt.rcParams['grid.linewidth'] = 1.0

output_dir = '/Users/kbbk/IOT/Week-06-Wi-Fi-AP-Throughput-FreeRTOS/images'
os.makedirs(output_dir, exist_ok=True)

# Data
tx_power = np.array([20, 15, 10, 5, 2]) # dBm
rssi = np.array([-37.2, -38.6, -40.0, -39.8, -39.7]) # dBm
throughput = np.array([2749.90, 3275.88, 3682.81, 3591.72, 3705.92]) # Kbps

# ----------------------------------------------------------------------
# 1. Clean Scatter Plot & Regression Line (RSSI vs Throughput)
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
ax.set_facecolor('#ffffff')

# Linear Fit
slope, intercept, r_value, _, _ = stats.linregress(rssi, throughput)
r2 = r_value**2
x_fit = np.linspace(-40.3, -36.8, 100)
y_fit = slope * x_fit + intercept

# Plot line & points
ax.plot(x_fit, y_fit, color='#94a3b8', linestyle='--', linewidth=1.5, 
        label=f'Linear Trend ($R^2 = {r2:.3f}$)')
ax.scatter(rssi, throughput, color='#4f46e5', s=80, zorder=4, edgecolor='white', linewidth=1.5, label='Measured Data')

# Simple, non-cluttered labels for points
tx_labels = ['20 dBm', '15 dBm', '10 dBm', '5 dBm', '2 dBm']
offsets = [(-35, -12), (10, -12), (-35, 8), (10, -15), (10, 5)]
for i, txt in enumerate(tx_labels):
    ax.annotate(txt, (rssi[i], throughput[i]), xytext=offsets[i], 
                textcoords='offset points', fontsize=9, color='#334155', fontweight='medium')

ax.set_title('RSSI vs Throughput Profiling', fontsize=13, fontweight='bold', color='#0f172a', pad=12)
ax.set_xlabel('RSSI (dBm)', fontsize=10, color='#475569', fontweight='medium')
ax.set_ylabel('Throughput (Kbps)', fontsize=10, color='#475569', fontweight='medium')
ax.set_xlim(-40.5, -36.5)
ax.set_ylim(2500, 3900)
ax.legend(loc='lower left', frameon=True, facecolor='#f8fafc', edgecolor='none', fontsize=9)
ax.grid(True)

# Clean borders
for spine in ax.spines.values():
    spine.set_color('#cbd5e1')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'lab6_2_rssi_vs_throughput.png'))
plt.close()

# ----------------------------------------------------------------------
# 2. Clean Tx Power vs Throughput (Bar Chart)
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)
ax.set_facecolor('#ffffff')

x_pos = np.arange(len(tx_power))
bars = ax.bar(x_pos, throughput, width=0.45, color='#0284c7', alpha=0.9, edgecolor='none', zorder=3)

# Data values on top of bars
for bar in bars:
    h = bar.get_height()
    ax.annotate(f'{h:.0f} Kbps',
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, color='#0f172a', fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels([f'{p} dBm' for p in tx_power], fontsize=9.5, color='#334155')
ax.set_title('Throughput Speed by Tx Power Setting', fontsize=13, fontweight='bold', color='#0f172a', pad=12)
ax.set_xlabel('Tx Power Setting', fontsize=10, color='#475569', fontweight='medium')
ax.set_ylabel('Throughput (Kbps)', fontsize=10, color='#475569', fontweight='medium')
ax.set_ylim(0, 4300)
ax.grid(axis='y', zorder=0)

for spine in ax.spines.values():
    spine.set_color('#cbd5e1')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'lab6_2_tx_power_impact.png'))
plt.close()

# ----------------------------------------------------------------------
# 3. Clean Wi-Fi Characteristic Curve & Threshold
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
ax.set_facecolor('#ffffff')

full_rssi = np.linspace(-30, -95, 250)

def profile_curve(r):
    tp = np.zeros_like(r)
    for i, v in enumerate(r):
        if v > -42:
            tp[i] = 3750 - (v - (-42))**1.4 * 80
        elif v >= -70:
            tp[i] = 3750 - ((-42) - v) * 5
        elif v >= -80:
            tp[i] = 3610 - ((-70 - v) / 10.0)**1.8 * 800
        else:
            tp[i] = 2810 * np.exp((v - (-80)) / 4.0)
    return tp

model_tp = profile_curve(full_rssi)

ax.plot(full_rssi, model_tp, color='#2563eb', linewidth=2.2, label='Wi-Fi Characteristic Curve')
ax.scatter(rssi, throughput, color='#ea580c', s=55, zorder=5, label='Measured Data')

# Threshold line at 50% max speed
half_tp = 3750 * 0.5
thresh_rssi = -83.5

ax.axhline(half_tp, color='#ef4444', linestyle=':', linewidth=1.2, label=f'50% Speed Threshold ({half_tp:.0f} Kbps)')
ax.axvline(thresh_rssi, color='#ef4444', linestyle=':', linewidth=1.2)

ax.annotate(f'Threshold RSSI ≈ {thresh_rssi} dBm',
            xy=(thresh_rssi, half_tp), xytext=(thresh_rssi + 14, half_tp + 400),
            arrowprops=dict(arrowstyle='->', color='#ef4444', lw=1.2),
            fontsize=9.5, color='#dc2626', fontweight='bold')

ax.set_title('Wi-Fi RSSI vs Throughput Characteristic Curve', fontsize=13, fontweight='bold', color='#0f172a', pad=12)
ax.set_xlabel('RSSI (dBm)', fontsize=10, color='#475569', fontweight='medium')
ax.set_ylabel('Throughput (Kbps)', fontsize=10, color='#475569', fontweight='medium')
ax.set_xlim(-30, -95)
ax.set_ylim(0, 4200)
ax.legend(loc='upper right', frameon=True, facecolor='#f8fafc', edgecolor='none', fontsize=9)
ax.grid(True)

for spine in ax.spines.values():
    spine.set_color('#cbd5e1')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'lab6_2_complete_rssi_profile.png'))
plt.close()

# ----------------------------------------------------------------------
# 4. Clean 10-Round Automated Benchmark Stability Test
# ----------------------------------------------------------------------
rounds = np.arange(1, 11)
rounds_speed = np.array([5616.19, 6096.69, 6935.09, 6505.92, 5368.99, 5832.10, 6001.47, 5861.23, 6101.59, 5899.81])

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
ax.set_facecolor('#ffffff')

ax.plot(rounds, rounds_speed, color='#0d9488', marker='o', linewidth=2.0, markersize=6, label='Round Speed (Kbps)')
ax.axhline(np.mean(rounds_speed), color='#64748b', linestyle='--', linewidth=1.2, label=f'Average ({np.mean(rounds_speed):.0f} Kbps)')

ax.set_title('10-Round Automated Benchmark Stability', fontsize=13, fontweight='bold', color='#0f172a', pad=12)
ax.set_xlabel('Benchmark Round', fontsize=10, color='#475569', fontweight='medium')
ax.set_ylabel('Throughput (Kbps)', fontsize=10, color='#475569', fontweight='medium')
ax.set_xticks(rounds)
ax.set_ylim(4800, 7400)
ax.legend(loc='upper right', frameon=True, facecolor='#f8fafc', edgecolor='none', fontsize=9)
ax.grid(True)

for spine in ax.spines.values():
    spine.set_color('#cbd5e1')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'lab6_2_10round_benchmark_stability.png'))
plt.close()

print("Clean minimalist graphs regenerated successfully!")
