"""
E-commerce Conversion Funnel Analysis
Syntecxhub Data Analysis Internship - Task 3, Project 1
Author: Arya Mohood
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Styling ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#F5F0FF',
    'axes.facecolor':   '#F5F0FF',
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'font.family':      'DejaVu Sans',
})
FUNNEL_COLORS = ['#2C0A5E', '#6A1B9A', '#AB47BC', '#CE93D8']
STAGE_NAMES   = ['Visited', 'Product Viewed', 'Added to Cart', 'Purchased']
COLS          = ['Visited', 'Product_Viewed', 'Added_to_Cart', 'Purchased']

# ═══════════════════════════════════════════════════════════════════════════
# 1. LOAD & CLEAN
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  E-COMMERCE CONVERSION FUNNEL ANALYSIS")
print("  Syntecxhub Internship | Task 3 — Project 1")
print("=" * 60)

df = pd.read_csv('ecommerce_funnel.csv')
df.dropna(inplace=True)
print(f"\n📦 Dataset Shape   : {df.shape}")
print(f"👥 Unique Users    : {df['UserID'].nunique()}")
print(f"📱 Devices         : {df['Device'].unique().tolist()}")
print(f"🔗 Traffic Sources : {df['Traffic_Source'].unique().tolist()}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. FUNNEL METRICS
# ═══════════════════════════════════════════════════════════════════════════
counts = [df[c].sum() for c in COLS]
drop_rates, conv_rates = [], []
for i in range(len(counts)):
    conv_rates.append(round(counts[i] / counts[0] * 100, 2))
    if i > 0:
        drop_rates.append(round((counts[i-1] - counts[i]) / counts[i-1] * 100, 2))
    else:
        drop_rates.append(0)

print(f"\n{'='*60}")
print("  📊 FUNNEL OVERVIEW")
print(f"{'='*60}")
for i, (stage, count, conv, drop) in enumerate(zip(STAGE_NAMES, counts, conv_rates, drop_rates)):
    drop_str = f"  (Drop-off from prev: {drop}%)" if i > 0 else ""
    print(f"  {stage:<20}: {count:>6,}  |  {conv:>6.1f}% of visitors{drop_str}")

overall_conv = round(counts[-1] / counts[0] * 100, 2)
biggest_drop_idx = drop_rates.index(max(drop_rates[1:]))
print(f"\n  🎯 Overall Conversion Rate : {overall_conv}%")
print(f"  ⚠️  Biggest Bottleneck     : {STAGE_NAMES[biggest_drop_idx]} → {STAGE_NAMES[biggest_drop_idx]} ({drop_rates[biggest_drop_idx]}% drop)")

# ═══════════════════════════════════════════════════════════════════════════
# 3. SEGMENT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
def funnel_by(col):
    result = df.groupby(col)[COLS].sum()
    result['Conv_Rate'] = (result['Purchased'] / result['Visited'] * 100).round(2)
    return result.sort_values('Conv_Rate', ascending=False)

device_funnel   = funnel_by('Device')
source_funnel   = funnel_by('Traffic_Source')
category_funnel = funnel_by('Category')

print(f"\n{'='*60}")
print("  📱 CONVERSION RATE BY DEVICE")
print(f"{'='*60}")
print(device_funnel[['Visited','Purchased','Conv_Rate']].to_string())

print(f"\n{'='*60}")
print("  🔗 CONVERSION RATE BY TRAFFIC SOURCE")
print(f"{'='*60}")
print(source_funnel[['Visited','Purchased','Conv_Rate']].to_string())

print(f"\n{'='*60}")
print("  🛍️  CONVERSION RATE BY CATEGORY")
print(f"{'='*60}")
print(category_funnel[['Visited','Purchased','Conv_Rate']].to_string())

# ═══════════════════════════════════════════════════════════════════════════
# 4. DASHBOARD — 6-panel
# ═══════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(22, 14))
fig.patch.set_facecolor('#F5F0FF')
fig.suptitle('E-commerce Conversion Funnel Analysis Dashboard\nSyntecxhub Internship — Task 3 Project 1',
             fontsize=18, fontweight='bold', color='#2C0A5E', y=0.98)

# ── Panel 1: Funnel Chart ────────────────────────────────────────────────
ax1 = fig.add_subplot(2, 3, 1)
bar_width = [0.9, 0.72, 0.52, 0.35]
for i, (stage, count, color, bw) in enumerate(zip(STAGE_NAMES, counts, FUNNEL_COLORS, bar_width)):
    ax1.barh(i, count, height=bw, color=color, edgecolor='white', linewidth=1.5)
    ax1.text(count + 50, i, f'{count:,} ({conv_rates[i]}%)',
             va='center', fontsize=9, fontweight='bold', color='#2C0A5E')
ax1.set_yticks(range(len(STAGE_NAMES)))
ax1.set_yticklabels(STAGE_NAMES, fontsize=10)
ax1.invert_yaxis()
ax1.set_title('Conversion Funnel', fontweight='bold', color='#2C0A5E')
ax1.set_xlabel('Number of Users')

# ── Panel 2: Drop-off Rate ───────────────────────────────────────────────
ax2 = fig.add_subplot(2, 3, 2)
transitions = [f'{STAGE_NAMES[i]}→{STAGE_NAMES[i+1]}' for i in range(len(STAGE_NAMES)-1)]
drops = drop_rates[1:]
bars2 = ax2.bar(transitions, drops, color=FUNNEL_COLORS[1:], edgecolor='white', linewidth=1.5)
ax2.set_title('Drop-off Rate Between Stages (%)', fontweight='bold', color='#2C0A5E')
ax2.set_ylabel('Drop-off Rate (%)')
ax2.tick_params(axis='x', rotation=20)
for bar, val in zip(bars2, drops):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f'{val}%', ha='center', fontsize=9, fontweight='bold')

# ── Panel 3: Conv Rate by Device ────────────────────────────────────────
ax3 = fig.add_subplot(2, 3, 3)
dev_colors = ['#2C0A5E','#AB47BC','#48C9B0']
bars3 = ax3.bar(device_funnel.index, device_funnel['Conv_Rate'],
                color=dev_colors, edgecolor='white', linewidth=1.5)
ax3.set_title('Conversion Rate by Device (%)', fontweight='bold', color='#2C0A5E')
ax3.set_ylabel('Conversion Rate (%)')
for bar, val in zip(bars3, device_funnel['Conv_Rate']):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
             f'{val}%', ha='center', fontsize=10, fontweight='bold')

# ── Panel 4: Conv Rate by Traffic Source ────────────────────────────────
ax4 = fig.add_subplot(2, 3, 4)
src_colors = ['#2C0A5E','#6A1B9A','#AB47BC','#CE93D8','#48C9B0']
bars4 = ax4.barh(source_funnel.index, source_funnel['Conv_Rate'],
                 color=src_colors, edgecolor='white', linewidth=1.5)
ax4.set_title('Conversion Rate by Traffic Source (%)', fontweight='bold', color='#2C0A5E')
ax4.set_xlabel('Conversion Rate (%)')
for bar, val in zip(bars4, source_funnel['Conv_Rate']):
    ax4.text(val+0.1, bar.get_y()+bar.get_height()/2,
             f'{val}%', va='center', fontsize=9, fontweight='bold')

# ── Panel 5: Conv Rate by Category ──────────────────────────────────────
ax5 = fig.add_subplot(2, 3, 5)
cat_colors = ['#2C0A5E','#6A1B9A','#AB47BC','#CE93D8','#E1BEE7']
bars5 = ax5.bar(category_funnel.index, category_funnel['Conv_Rate'],
                color=cat_colors, edgecolor='white', linewidth=1.5)
ax5.set_title('Conversion Rate by Category (%)', fontweight='bold', color='#2C0A5E')
ax5.set_ylabel('Conversion Rate (%)')
ax5.tick_params(axis='x', rotation=20)
for bar, val in zip(bars5, category_funnel['Conv_Rate']):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
             f'{val}%', ha='center', fontsize=9, fontweight='bold')

# ── Panel 6: Stage-wise stacked breakdown by device ─────────────────────
ax6 = fig.add_subplot(2, 3, 6)
device_stage = df.groupby('Device')[COLS].sum()
x = np.arange(len(device_stage))
width = 0.2
for i, (col, stage, color) in enumerate(zip(COLS, STAGE_NAMES, FUNNEL_COLORS)):
    ax6.bar(x + i*width, device_stage[col], width, label=stage, color=color, edgecolor='white')
ax6.set_xticks(x + width*1.5)
ax6.set_xticklabels(device_stage.index)
ax6.set_title('Funnel Stages by Device', fontweight='bold', color='#2C0A5E')
ax6.set_ylabel('Users')
ax6.legend(fontsize=7)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('funnel_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Dashboard saved → funnel_dashboard.png")

# ═══════════════════════════════════════════════════════════════════════════
# 5. RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("  💡 RECOMMENDATIONS TO IMPROVE CONVERSIONS")
print(f"{'='*60}")
print(f"""
1. BIGGEST BOTTLENECK → Visit to Product View ({drop_rates[1]}% drop-off)
   → Improve homepage UX, add trending products, better search.

2. CART ABANDONMENT → {drop_rates[2]}% drop from View to Cart
   → Add urgency (limited stock), clearer CTAs, wish-list option.

3. CHECKOUT DROP → {drop_rates[3]}% drop from Cart to Purchase
   → Simplify checkout, offer guest checkout, add trust badges.

4. BEST DEVICE → {device_funnel['Conv_Rate'].idxmax()} has highest conversion
   → Prioritize UI/UX optimizations for this device.

5. BEST SOURCE → {source_funnel['Conv_Rate'].idxmax()} converts best
   → Increase budget/focus on this channel.

6. BEST CATEGORY → {category_funnel['Conv_Rate'].idxmax()}
   → Feature this category prominently on homepage.
""")

# Save outputs
summary = pd.DataFrame({
    'Stage': STAGE_NAMES,
    'Users': counts,
    'Conv_Rate_from_Visit': conv_rates,
    'Drop_Rate_from_Prev': drop_rates
})
summary.to_csv('funnel_summary.csv', index=False)
device_funnel.to_csv('funnel_by_device.csv')
source_funnel.to_csv('funnel_by_source.csv')

print("✅ Files saved:")
print("   → funnel_summary.csv")
print("   → funnel_by_device.csv")
print("   → funnel_by_source.csv")
print("   → funnel_dashboard.png")
print("\n🎉 Funnel Analysis Complete!")
