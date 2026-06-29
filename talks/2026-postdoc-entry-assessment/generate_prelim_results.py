import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import os
import matplotlib

# Set matplotlib parameters for academic style
matplotlib.rcParams.update({
    'font.size': 12,
    'font.family': 'sans-serif',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'lines.linewidth': 2.0,
    'lines.markersize': 8,
})

# Create figures directory if not exists
fig_dir = 'figures'
os.makedirs(fig_dir, exist_ok=True)

def generate_mf_scaling():
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    # DOFs
    dofs = np.logspace(4, 7, 10)
    
    # Direct solver (O(N^1.5) to O(N^2) scaling approximately)
    time_direct = 1e-4 * dofs**1.6
    
    # Matrix-Free CG (O(N) scaling)
    time_mf = 2e-4 * dofs**1.1
    
    # Out of memory for direct solver above 2*10^6
    mask_direct = dofs < 3e6
    
    ax.plot(dofs[mask_direct], time_direct[mask_direct], 's-', color='#d62728', label='Assembly + Direct Solver', linewidth=2.5)
    ax.plot(dofs, time_mf, 'o-', color='#1f77b4', label='Matrix-Free + CG', linewidth=2.5)
    
    # Add out-of-memory annotation
    last_dof = dofs[mask_direct][-1]
    last_time = time_direct[mask_direct][-1]
    ax.annotate('OOM (Out of Memory)', xy=(last_dof, last_time), xytext=(last_dof*0.2, last_time*2),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
                fontsize=11)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Degrees of Freedom (DOFs)')
    ax.set_ylabel('Wall-clock Time (s)')
    ax.set_title('Matrix-Free vs. Explicit Assembly Scaling')
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'piml_mf_scaling.pdf'))
    plt.close()

def generate_piml_multiscale():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    
    # Draw macroscopic coarse mesh for half MBB beam
    nx, ny = 30, 15
    
    # Generate a dummy density field for half MBB
    X, Y = np.meshgrid(np.linspace(0, 1, nx), np.linspace(0, 1, ny))
    density = np.zeros((ny, nx))
    
    # Mock topology shape (arch)
    for i in range(ny):
        for j in range(nx):
            x = j / nx
            y = i / ny
            if (x - 0.5)**2 + (y - 0.0)**2 < 0.6**2 and (x - 0.5)**2 + (y - 0.0)**2 > 0.3**2:
                density[i, j] = 0.8 + 0.2*np.random.rand()
            elif x < 0.2 and y > 0.8:
                density[i, j] = 0.9
            else:
                density[i, j] = 0.1
                
    # Mirror for full MBB
    density_full = np.hstack((density[:, ::-1], density))
    nx_full = nx * 2
    
    # Plot macro density
    cmap = plt.cm.Greys
    im = ax.imshow(density_full, cmap=cmap, origin='lower', extent=[0, nx_full, 0, ny])
    
    # Draw coarse grid lines
    for i in range(nx_full+1):
        ax.axvline(x=i, color='gray', linewidth=0.2, alpha=0.5)
    for i in range(ny+1):
        ax.axhline(y=i, color='gray', linewidth=0.2, alpha=0.5)
        
    # Add an inset for micro-structure
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
    
    axins = inset_axes(ax, width="40%", height="40%", loc='upper right', borderpad=1)
    
    # Generate a micro-structure pattern
    mx, my = 20, 20
    micro_density = np.zeros((my, mx))
    # A cross-like structure inside
    for i in range(my):
        for j in range(mx):
            if abs(i - my/2) < 3 or abs(j - mx/2) < 3 or (i+j < 6) or (i+mx-j < 6):
                micro_density[i, j] = 1.0
            else:
                micro_density[i, j] = 0.0
                
    axins.imshow(micro_density, cmap='Blues', origin='lower', extent=[0, 1, 0, 1])
    axins.set_xticks([])
    axins.set_yticks([])
    
    # Add PIML text
    axins.text(0.5, -0.15, "PIML Predicted Micro-Stiffness", ha='center', va='top', transform=axins.transAxes, fontsize=10, color='#1f77b4', fontweight='bold')
    
    # Mark inset pointing to a solid block in macro mesh
    rect_x, rect_y = 15, 8
    ax.add_patch(patches.Rectangle((rect_x, rect_y), 1, 1, fill=False, edgecolor='#1f77b4', lw=2))
    mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="#1f77b4", lw=1.5, alpha=0.7)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('PIML Multi-scale Formulation (Macro-Micro mapping)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'piml_multiscale_mbb.pdf'))
    plt.close()

def generate_mmc_high_order():
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Background mesh (6x5)
    nx, ny = 6, 5
    for i in range(nx+1):
        ax.axvline(x=i, color='gray', linewidth=1.0, linestyle='--')
    for i in range(ny+1):
        ax.axhline(y=i, color='gray', linewidth=1.0, linestyle='--')
        
    # Draw MMC component (ellipse or thick line)
    # Let's draw an angled thick line/capsule
    x_c, y_c = 3.0, 2.5
    L = 5.0
    W = 1.2
    angle = 30 # degrees
    
    # Create transformation
    import matplotlib.transforms as transforms
    ts = ax.transData
    tr = transforms.Affine2D().rotate_deg_around(x_c, y_c, angle)
    t = tr + ts
    
    # Draw MMC component
    rect = patches.Rectangle((x_c - L/2, y_c - W/2), L, W, fill=True, color='#2ca02c', alpha=0.4, transform=t)
    ax.add_patch(rect)
    rect_edge = patches.Rectangle((x_c - L/2, y_c - W/2), L, W, fill=False, edgecolor='#2ca02c', lw=3, transform=t)
    ax.add_patch(rect_edge)
    
    # Add text for MMC component
    ax.text(x_c-1, y_c+1.5, 'MMC Explicit Component', color='#2ca02c', fontsize=12, fontweight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
            
    # Highlight a cut cell and its high order integration points
    cut_cell_x, cut_cell_y = 3, 2
    ax.add_patch(patches.Rectangle((cut_cell_x, cut_cell_y), 1, 1, fill=True, color='#ff7f0e', alpha=0.2))
    ax.add_patch(patches.Rectangle((cut_cell_x, cut_cell_y), 1, 1, fill=False, edgecolor='#ff7f0e', lw=2))
    
    # Draw Gauss points inside the cut cell
    # High-order integration (e.g. 4x4 or 3x3)
    gp = np.array([0.1127, 0.5, 0.8873])
    gp_points_x, gp_points_y = np.meshgrid(gp, gp)
    gp_points_x = gp_points_x.flatten() + cut_cell_x
    gp_points_y = gp_points_y.flatten() + cut_cell_y
    
    # To determine inside/outside, we just roughly color them
    # For a cell at (3,2) to (4,3), with center at 3.5, 2.5. The MMC passes right through it.
    for gx, gy in zip(gp_points_x, gp_points_y):
        # Rough check if inside the green region
        # Transform back
        pts = tr.inverted().transform((gx, gy))
        if abs(pts[0] - x_c) < L/2 and abs(pts[1] - y_c) < W/2:
            ax.plot(gx, gy, 'ko', markersize=5) # Material
        else:
            ax.plot(gx, gy, 'wo', markeredgecolor='k', markersize=5) # Void
            
    # Legend for integration points
    ax.plot([], [], 'ko', label='Gauss Point (Material)')
    ax.plot([], [], 'wo', markeredgecolor='k', label='Gauss Point (Void)')
    
    # Title and cleanup
    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('MMC Exact Geometry + High-Order Discretization')
    ax.legend(loc='lower left', framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'mmc_high_order_mesh.pdf'))
    plt.close()

if __name__ == '__main__':
    generate_mf_scaling()
    generate_piml_multiscale()
    generate_mmc_high_order()
    print("Successfully generated mock figures in 'figures' directory.")
