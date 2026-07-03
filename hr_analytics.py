"""
HR Analytics Dashboard
Syntecxhub Data Analysis Internship - Task 3, Project 2
Author: Arya Mohood
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Styling ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#F0F4FF',
    'axes.facecolor':   '#F0F4FF',
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'font.family':      'DejaVu Sans',
})
PURPLE  = '#4B0082'
COLORS  = ['#2C0A5E','#6A1B9A','#AB47BC','#CE93D8','#48C9B0','#F39C12']
YES_NO  = ['#4B0082','#CE93D8']

# ═══════════════════════════════════════════════════════════════════════════
# 1. LOAD & CLEAN
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  HR ANALYTICS DASHBOARD")
print("  Syntecxhub Internship | Task 3 — Project 2")
print("=" * 60)

df = pd.read_csv('hr_data.csv')
df.dropna(inplace=True)
df['Attrition_Flag'] = (df['Attrition'] == 'Yes').astype(int)

print(f"\n📦 Dataset Shape     : {df.shape}")
print(f"👥 Total Employees   : {len(df)}")
print(f"🏢 Departments       : {df['Department'].nunique()}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. KEY KPIs
# ═══════════════════════════════════════════════════════════════════════════
total_emp      = len(df)
attrition_cnt  = df['Attrition_Flag'].sum()
attrition_rate = round(attrition_cnt / total_emp * 100, 2)
retention_rate = round(100 - attrition_rate, 2)
avg_salary     = round(df['MonthlyIncome'].mean(), 2)
avg_age        = round(df['Age'].mean(), 1)
avg_exp        = round(df['YearsAtCompany'].mean(), 1)
avg_sat        = round(df['JobSatisfaction'].mean(), 2)

print(f"\n{'='*60}")
print("  📈 KEY KPIs")
print(f"{'='*60}")
print(f"  Total Employees    : {total_emp:,}")
print(f"  Attrition Count    : {attrition_cnt}")
print(f"  Attrition Rate     : {attrition_rate}%")
print(f"  Retention Rate     : {retention_rate}%")
print(f"  Avg Monthly Income : ₹{avg_salary:,.0f}")
print(f"  Avg Age            : {avg_age} yrs")
print(f"  Avg Experience     : {avg_exp} yrs")
print(f"  Avg Job Satisfaction (1-4): {avg_sat}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. ATTRITION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
dept_attr  = df.groupby('Department')['Attrition_Flag'].agg(['sum','mean']).reset_index()
dept_attr.columns = ['Department','Attrition_Count','Attrition_Rate']
dept_attr['Attrition_Rate'] = (dept_attr['Attrition_Rate']*100).round(2)

role_attr  = df.groupby('JobRole')['Attrition_Flag'].mean().sort_values(ascending=False)*100
ot_attr    = df.groupby('OverTime')['Attrition_Flag'].mean()*100
sat_attr   = df.groupby('JobSatisfaction')['Attrition_Flag'].mean()*100
wlb_attr   = df.groupby('WorkLifeBalance')['Attrition_Flag'].mean()*100
marital_attr = df.groupby('MaritalStatus')['Attrition_Flag'].mean()*100

print(f"\n{'='*60}")
print("  🏢 ATTRITION BY DEPARTMENT")
print(f"{'='*60}")
print(dept_attr.to_string(index=False))

print(f"\n{'='*60}")
print("  💼 ATTRITION BY JOB ROLE (Top 5)")
print(f"{'='*60}")
print(role_attr.head().round(2).to_string())

print(f"\n{'='*60}")
print("  ⏰ OVERTIME IMPACT ON ATTRITION")
print(f"{'='*60}")
print(ot_attr.round(2).to_string())

# ═══════════════════════════════════════════════════════════════════════════
# 4. CORRELATION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
num_cols = ['Age','MonthlyIncome','YearsAtCompany','JobSatisfaction',
            'WorkLifeBalance','DistanceFromHome','Attrition_Flag']
corr = df[num_cols].corr()

print(f"\n{'='*60}")
print("  🔗 TOP CORRELATIONS WITH ATTRITION")
print(f"{'='*60}")
attr_corr = corr['Attrition_Flag'].drop('Attrition_Flag').sort_values(key=abs, ascending=False)
print(attr_corr.round(3).to_string())

# ═══════════════════════════════════════════════════════════════════════════
# 5. DASHBOARD — 6-panel
# ═══════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(22, 14))
fig.patch.set_facecolor('#F0F4FF')
fig.suptitle('HR Analytics Dashboard\nSyntecxhub Internship — Task 3 Project 2',
             fontsize=18, fontweight='bold', color='#2C0A5E', y=0.98)

# ── Panel 1: Attrition Rate by Department ───────────────────────────────
ax1 = fig.add_subplot(2, 3, 1)
bars1 = ax1.bar(dept_attr['Department'], dept_attr['Attrition_Rate'],
                color=COLORS[:len(dept_attr)], edgecolor='white', linewidth=1.5)
ax1.axhline(attrition_rate, color='red', linestyle='--', linewidth=1.2,
            label=f'Overall: {attrition_rate}%')
ax1.set_title('Attrition Rate by Department (%)', fontweight='bold', color='#2C0A5E')
ax1.set_ylabel('Attrition Rate (%)')
ax1.tick_params(axis='x', rotation=15)
ax1.legend(fontsize=8)
for bar, val in zip(bars1, dept_attr['Attrition_Rate']):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f'{val}%', ha='center', fontsize=9, fontweight='bold')

# ── Panel 2: KPI Summary ────────────────────────────────────────────────
ax2 = fig.add_subplot(2, 3, 2)
ax2.axis('off')
kpis = [
    ('Total Employees', f'{total_emp:,}', '#2C0A5E'),
    ('Attrition Rate',  f'{attrition_rate}%', '#C0392B'),
    ('Retention Rate',  f'{retention_rate}%', '#27AE60'),
    ('Avg Salary',      f'₹{avg_salary:,.0f}', '#6A1B9A'),
    ('Avg Age',         f'{avg_age} yrs', '#AB47BC'),
    ('Avg Satisfaction',f'{avg_sat}/4', '#48C9B0'),
]
for idx, (label, value, color) in enumerate(kpis):
    y = 0.85 - idx * 0.14
    ax2.add_patch(plt.Rectangle((0.05, y-0.06), 0.9, 0.11,
                                 facecolor=color, alpha=0.15, transform=ax2.transAxes))
    ax2.text(0.5, y, f'{label}: {value}', ha='center', va='center',
             fontsize=11, fontweight='bold', color=color, transform=ax2.transAxes)
ax2.set_title('Key HR KPIs', fontweight='bold', color='#2C0A5E')

# ── Panel 3: Overtime vs Attrition ──────────────────────────────────────
ax3 = fig.add_subplot(2, 3, 3)
bars3 = ax3.bar(ot_attr.index, ot_attr.values, color=YES_NO, edgecolor='white', linewidth=1.5)
ax3.set_title('Attrition Rate: Overtime vs No Overtime (%)', fontweight='bold', color='#2C0A5E')
ax3.set_ylabel('Attrition Rate (%)')
for bar, val in zip(bars3, ot_attr.values):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')

# ── Panel 4: Job Satisfaction vs Attrition ──────────────────────────────
ax4 = fig.add_subplot(2, 3, 4)
sat_labels = {1:'Low',2:'Medium',3:'High',4:'Very High'}
ax4.plot(sat_attr.index, sat_attr.values, color=PURPLE, marker='o',
         linewidth=2.5, markersize=8)
ax4.fill_between(sat_attr.index, sat_attr.values, alpha=0.2, color=PURPLE)
ax4.set_xticks(sat_attr.index)
ax4.set_xticklabels([sat_labels.get(i,'') for i in sat_attr.index])
ax4.set_title('Attrition Rate by Job Satisfaction', fontweight='bold', color='#2C0A5E')
ax4.set_xlabel('Job Satisfaction Level')
ax4.set_ylabel('Attrition Rate (%)')
for x, y in zip(sat_attr.index, sat_attr.values):
    ax4.text(x, y+0.5, f'{y:.1f}%', ha='center', fontsize=9, fontweight='bold')

# ── Panel 5: Salary Distribution by Attrition ───────────────────────────
ax5 = fig.add_subplot(2, 3, 5)
for attr, color, label in [('No','#CE93D8','Stayed'), ('Yes','#4B0082','Left')]:
    ax5.hist(df[df['Attrition']==attr]['MonthlyIncome'], bins=20,
             alpha=0.7, color=color, label=label, edgecolor='white')
ax5.set_title('Salary Distribution: Stayed vs Left', fontweight='bold', color='#2C0A5E')
ax5.set_xlabel('Monthly Income (₹)')
ax5.set_ylabel('Employee Count')
ax5.legend()

# ── Panel 6: Correlation Heatmap ────────────────────────────────────────
ax6 = fig.add_subplot(2, 3, 6)
sns.heatmap(corr, annot=True, fmt='.2f', cmap='BuPu', ax=ax6,
            linewidths=0.5, linecolor='white', cbar_kws={'shrink':0.8})
ax6.set_title('Correlation Heatmap', fontweight='bold', color='#2C0A5E')
ax6.tick_params(axis='x', rotation=30, labelsize=7)
ax6.tick_params(axis='y', labelsize=7)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('hr_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Dashboard saved → hr_dashboard.png")

# ═══════════════════════════════════════════════════════════════════════════
# 6. RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════
top_dept = dept_attr.loc[dept_attr['Attrition_Rate'].idxmax(), 'Department']
print(f"\n{'='*60}")
print("  💡 HR RECOMMENDATIONS")
print(f"{'='*60}")
print(f"""
1. OVERTIME POLICY → Employees working overtime have significantly
   higher attrition. Cap overtime hours and compensate fairly.

2. HIGH-RISK DEPT → {top_dept} has the highest attrition rate.
   Conduct stay interviews and improve conditions there first.

3. JOB SATISFACTION → Lower satisfaction strongly predicts attrition.
   Implement quarterly feedback cycles and career growth plans.

4. SALARY GAPS → Lower-income employees leave more often.
   Review pay bands and ensure market-competitive salaries.

5. WORK-LIFE BALANCE → Poor WLB is a key attrition driver.
   Introduce flexible work policies and wellness programs.

6. RETENTION TARGET → Aim to bring attrition below 15% from {attrition_rate}%.
""")

# Save outputs
dept_attr.to_csv('hr_attrition_by_dept.csv', index=False)
role_attr.to_csv('hr_attrition_by_role.csv')
df[num_cols].corr().to_csv('hr_correlation.csv')

print("✅ Files saved:")
print("   → hr_attrition_by_dept.csv")
print("   → hr_attrition_by_role.csv")
print("   → hr_correlation.csv")
print("   → hr_dashboard.png")
print("\n🎉 HR Analytics Complete!")
