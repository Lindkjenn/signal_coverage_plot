import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import griddata
from matplotlib.image import imread
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter

plot_type = 'layout'  # 'layout' or 'coverage'

radio_dots_online = 3 # 1 or 3
pipes = True

show_measure_points = True
show_radio_dots = False

# coverage plot type settings
test_type = 'signal' # 'signal', 'ping' or 'iperf'
test_type_target = 'rsrp' # 'signal': 'snr', 'rsrp' or 'rsrq', 'iperf': 'uplink' or 'downlink', 'ping': 'max_latency', 'avg_latency' or 'min_latency'

netperf_data_json = f'c:/Users/Andreas Lindkjenn Bø/Desktop/signal_coverage/netperf_signal_coverage_rev2__pipes_{str(pipes).lower()}__radio_dots_{radio_dots_online}_tcp_NR5G_SA.json'

background_image = imread('c:/Users/Andreas Lindkjenn Bø/Desktop/signal_coverage/lab_map_layout.png')
overlay_image = imread('c:/Users/Andreas Lindkjenn Bø/Desktop/signal_coverage/lab_map_overlay.png')

unit_of_measure = {'signal': 'dB',
                   'ping': 'ms',
                   'iperf':'Mbps'}


with open(netperf_data_json, 'r') as file:
    json_data = json.load(file)

# extract signal values and map them to ids
test_results = {str(result['id']): result[test_type][test_type_target] if test_type in result else np.nan for result in json_data['results']}

# find the worst value for the test type target
worst_value = np.nanmax(list(test_results.values())) if test_type in ['ping'] else np.nanmin(list(test_results.values()))


# create a 2D array of NaNs with dimensions 928 x 1717 (ratio of map)
array = np.full((928, 1717), np.nan)

radio_dots = {
    '0': {'coordinates': (184, 1552), 'operative': True if radio_dots_online == 3 else False},
    '1': {'coordinates': (380, 491), 'operative': False},
    '2': {'coordinates': (380, 434), 'operative': True},
    '3': {'coordinates': (655, 467), 'operative': True if radio_dots_online == 3 else False},
    '4': {'coordinates': (720, 467), 'operative': False}
}

# set measure points with ID
data_points_old = {
    '0': (560, 535),
    '1': (405, 533),
    '2': (347, 466),
    '3': (296, 464),
    '4': (251, 470),
    '5': (178, 478),
    '6': (139, 546),
    '7': (227, 375),
    '8': (227, 266),
    '9': (221, 153),
    '10': (223, 20),
    '11': (29, 24),
    '12': (124, 144),
    '13': (125, 263),
    '14': (22, 288),
    '15': (26, 141),
    '16': (22, 385),
    '17': (128, 350),
    '18': (353, 148),
    '19': (358, 270),
    '20': (364, 367),
    '21': (413, 470),
    '22': (476, 469),
    '23': (549, 470),
    '24': (516, 349),
    '25': (694, 469),
    '26': (635, 346),
    '27': (730, 337),
    '28': (813, 467),
    '29': (892, 472),
    '30': (799, 340),
    '31': (792, 221),
    '32': (800, 118),
    '33': (793, 35),
    '34': (892, 48)
}

data_points = {
    '28': (560, 535),
    '25': (405, 533),
    '1': (347, 466),
    '2': (296, 464),
    '3': (251, 470),
    '5': (178, 478),
    '6': (139, 546),
    '8': (227, 375),
    '9': (227, 266),
    '10': (221, 153),
    '11': (223, 20),
    '13': (29, 24),
    '15': (124, 144),
    '16': (125, 263),
    '17': (22, 288),
    '14': (26, 141),
    '18': (22, 385),
    '19': (128, 350),
    '21': (353, 148),
    '22': (358, 270),
    '23': (364, 367),
    '24': (413, 470),
    '26': (476, 469),
    '27': (549, 470),
    '43': (516, 349),
    '30': (694, 469),
    '42': (635, 346),
    '41': (730, 337),
    '32': (813, 467),
    '33': (892, 472),
    '40': (799, 340),
    '39': (792, 221),
    '38': (800, 118),
    '37': (793, 35),
    '36': (892, 48),
    '0': (349, 532),
    '4': (243, 535),
    '7': (73, 453),
    '12': (123, 24),
    '20': (387, 41),
    '29': (657, 543),
    '31': (759, 545),
    '34': (895, 280),
    '35': (895, 169),
    '44': (524, 223),
    '45': (693, 223),
    '46': (693, 58),
    '47': (524, 58),
    '48': (600, 154),
    '49': (393, 607),
    '50': (231, 613),
    '51': (110, 623),
    '52': (44, 623),
    '53': (44, 726),
    '54': (44, 822),
    '55': (158, 726),
    '56': (158, 829),
    '57': (301, 731),
    '58': (304, 824),
    '59': (382, 765),
    '60': (382, 864),
    '61': (464, 814),
    '62': (563, 815),
    '63': (563, 708),
    '64': (512, 618),
    '65': (464, 708),
    '66': (394, 966),
    '67': (411, 1078),
    '68': (531, 1054),
    '69': (493, 1000),
    '70': (493, 919),
    '71': (602, 913),
    '72': (672, 810),
    '73': (672, 709),
    '74': (637, 618),
    '75': (742, 897),
    '76': (760, 769),
    '77': (735, 619),
    '78': (867, 619),
    '79': (859, 755),
    '80': (868, 896),
    '81': (868, 1022),
    '82': (742, 1022),
    '83': (612, 1028),
    '84': (305, 918),
    '85': (194, 918),
    '86': (61, 923),
    '87': (61, 1027),
    '88': (70, 1120),
    '89': (194, 1024),
    '90': (218, 1115),
    '91': (303, 1028),
    '92': (338, 1114),
    '93': (510, 1115),
    '94': (416, 1185),
    '95': (416, 1297),
    '96': (416, 1438),
    '97': (268, 1195),
    '98': (269, 1286),
    '99': (257, 1381),
    '100': (168, 1195),
    '101': (36, 1259),
    '102': (42, 1386),
    '103': (135, 1386),
    '104': (95, 1323), 
    '105': (536, 1220),
    '106': (620, 1114),
    '107': (536, 1359),
    '108': (677, 1359),
    '109': (526, 1474),
    '110': (690, 1474),
    '111': (771, 1465),
    '112': (777, 1384),
    '113': (838, 1311),
    '114': (802, 1232),
    '115': (792, 1120),
    '116': (713, 1113),
    '117': (678, 1225),
    '118': (862, 1390),
    '119': (863, 1462),
    '120': (833, 1601),
    '121': (784, 1532),
    '122': (789, 1675),
    '123': (880, 1671),
    '124': (863, 1532),
    '125': (690, 1568),
    '126': (690, 1653),
    '127': (526, 1568),
    '128': (526, 1653),
    '129': (404, 1568),
    '130': (404, 1653),
    '131': (203, 1474),
    '132': (203, 1568),
    '133': (203, 1653),
    '134': (61, 1474),
    '135': (61, 1568),
    '136': (61, 1653)
}
    

legend_handles = []
if plot_type == 'layout':
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.imshow(background_image, aspect='auto', extent=[0, 1717, 928, 0], zorder=1)
    sns.heatmap(array, ax=ax, square=True, cbar=False, alpha=0.5, zorder=2, cmap='RdYlBu')
    #ax.set_title('Industrial Lab Layout')
    if show_measure_points:
        for id, (i, j) in data_points.items():
            ax.scatter(j + 0.5, i + 0.5, color='#C04040', s=20)
            ax.text(j + 0.5, i + 0.5, ' ' + id, color='#C04040', ha='left', va='top', fontsize=10)
        #legend_handles.append(Line2D([0], [0], marker='o', markeredgecolor='none', color='none', label='Measure Point', markersize=7, markerfacecolor='grey'))
elif plot_type == 'coverage':

    valid_points = []
    error_points_dict = {}
    for id, point in data_points.items():
        value = test_results.get(id)
        #point = data_points.get(id)
        if value is not None and not np.isnan(value): 
            array[point[0], point[1]] = value
            valid_points.append((point[0], point[1])) # not really used
        else:
            test_results[id] = worst_value
            array[point[0], point[1]] = worst_value
            error_points_dict[id] = (point[0], point[1])
            print(f'Missing {test_type} data for measure point: {id}')

    if valid_points:
        fig, ax = plt.subplots(figsize=(12, 9))

        x = np.arange(0, array.shape[1])
        y = np.arange(0, array.shape[0])
        xgrid, ygrid = np.meshgrid(x, y)
        points = np.column_stack((xgrid.ravel(), ygrid.ravel()))
        values = array.ravel()
        mask = ~np.isnan(values)

        grid_z0 = griddata(points[mask], values[mask], points, method='nearest')
        interpolated_array = grid_z0.reshape(array.shape)

        ax.imshow(overlay_image, aspect='auto', extent=[0, 1717, 928, 0], zorder=2)
        interpolated_array = gaussian_filter(interpolated_array, sigma=30)
        sns.heatmap(interpolated_array, ax=ax, square=True, alpha=0.6, zorder=1, cmap='RdYlBu_r' if test_type in ['ping'] else 'RdYlBu', cbar_kws={'fraction': 0.02, 'label': f'{test_type_target.upper()} ({unit_of_measure[test_type]})'})

        if show_measure_points:
            for id, (i, j) in data_points.items():
                ax.scatter(j + 0.5, i + 0.5, color='grey', s=20)
                #ax.text(j + 0.5, i + 0.5, ' ' + id, color='grey', ha='left', va='top', fontsize=10)
            for id, (i, j) in error_points_dict.items():
                ax.scatter(j + 0.5, i + 0.5, color='#C04040', s=20)
            legend_handles.append(Line2D([0], [0], marker='o', markeredgecolor='none', color='none', label='Measure Point', markersize=7, markerfacecolor='grey'))
            legend_handles.append(Line2D([0], [0], marker='o', markeredgecolor='none', color='none', label='Missing Measure Point', markersize=7, markerfacecolor='#C04040'))

        ax.set_title(f'Interpolated {test_type_target.upper()} Coverage from {test_type.capitalize()} Test\npipes={str(pipes).lower()}, radio_dots={radio_dots_online}', fontsize=16)
        legend_handles.append(Patch(facecolor='white', edgecolor='black', hatch='//////', label='Not Measured', alpha=0.6))
        ####legend_handles.append(Patch(facecolor='red', edgecolor='black', hatch='//////', label='To Be Measured', alpha=0.6))
        

if show_radio_dots:
    for id, data in radio_dots.items():
        (i, j) = data['coordinates']
        if data['operative']:   
            ax.scatter(j + 0.5, i + 0.5, color='white', s=100, edgecolor='green', linewidth=2.5)
        else:
            ax.scatter(j + 0.5, i + 0.5, color='white', s=100, edgecolor='#C04040', linewidth=2.5)
    legend_handles.append(Line2D([0], [0], marker='o', markeredgecolor='green', color='none', label='Online Radio Dot', markersize=10, markerfacecolor='w', markeredgewidth=2.5))
    legend_handles.append(Line2D([0], [0], marker='o', markeredgecolor='#C04040', color='none', label='Offline Radio Dot', markersize=10, markerfacecolor='w', markeredgewidth=2.5))

#ax.legend(handles=legend_handles, loc='upper left')
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()

plt.show()
