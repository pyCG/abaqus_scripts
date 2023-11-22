import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# FUNCTIONS
# =============================================================================

def ARCHARD_wear_model(p_A: list,
                       s: list,
                       k: float,
                       H: float,
                       ) -> object:
    '''
    Verschleißberechnung nach Archard

    Args:
        p_A: (list) Liste der Festkörperkontaktdruckwerte per Knoten
        s: (list) Liste der Relativverschiebungswerte per Knoten
        k: (float) Verschleißkoeffizient
        H: (float) Härte

    Returns:
        h_V: (list) Liste der Verschleißvolumenwerte nach Archard per Knoten
    '''

    h_V_list = []
    for p_A_node, s_node in zip(p_A, s):
        h_V = p_A_node * s_node * k / H
        h_V_list.append(h_V)
    # print("Verschleißvolume nach Archard ist berechnet")

    return np.abs(h_V_list)


def FLEISCHER_wear_model(p_A: list,
                         s: list,
                         mu: float,
                         e_R: float
                         ):
    '''
    Verschleißberechnung nach Fleischer

    Args:
        p_A: (list) Liste der Festkörperkontaktdruckwerte pro Knoten
        s: (list) Liste der Relativverschiebungswerte pro Knoten
        mu: (float) Reibwert
        e_R: (float) Reibenergiedichte

    Returns:
        h_V: (list) Liste der Verschleißvolumenwerte nach Archard per Knoten
    '''
    h_V_list = []
    for p_A_node, s_node in zip(p_A, s):
        h_V = mu * p_A_node * s_node / e_R
        h_V_list.append(h_V)
    # print("Verschleißvolume nach Fleischer ist berechnet")

    return np.abs(h_V_list)


def plot_node_values(w: list,
                     x: list,
                     y: list,
                     z: list,
                     title: str,
                     save_path: str,
                     file_name: str,
                     show_plot: bool
                     ):
    '''
    Knotenplot

    Args:
        w: (list) Liste der Magnitudenwerten pro Knoten
        x: (list) x-Koordinate der Knoten
        y: (list) y-Koordinate der Knoten
        z: (list) z-Koordinate der Knoten
        title: (str) Plots Titel
        save_path: (str) Pfad zum Speichern der Datei

    Returns:
        (.jpg) eine 3-D .jpg Bild mit den eingegebenen Magnitudenwerte und Koordinaten
    '''
    # Create a 3D plot
    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x, y, z, c=w, cmap='jet')
    ax.set_aspect('equal', 'box')
    # Add colorbar and set label
    cbar = fig.colorbar(sc, pad=0.12)
    cbar.ax.tick_params(labelsize=15)
    cbar.set_label(title, fontsize=15)
    # Set axis labels
    ax.set_xlabel('x - Coordinates [mm]', fontsize=15)
    ax.set_ylabel('y - Coordinates [mm]', fontsize=15)
    ax.set_zlabel('z - Coordinates [mm]', fontsize=15)

    # plt.tight_layout()

    plt.savefig(save_path + '\\' + file_name + '_' + title + '.png', dpi=600)

    if show_plot == True:
        plt.show()

    return
