import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
def _extract_delta(file):
    uncertaties = False
    data = {"delta_x": [], "err": []}
    with open(file, mode='r', encoding='utf-8') as file:
        for line in file.readlines():
            line = line.replace("\t", " ")
            line = line.split(sep=" ")
            while "" in line:
                line.remove("")
            while "\n" in line:
                line.remove("\n")
            for num in range(len(line)):
                if uncertaties == False:
                    data["delta_x"].append(float(line[num])/100.)
                else:
                    data["err"].append(float(line[num])/100.)
            uncertaties = not uncertaties
    return(data)
def extract(file):                                                          # funzione che abbiamo usato per estrarre i dati da tutti i txt 
    data = {"Temp_0": [], "Temp_1": [], "Time_0": [], "Time_1": []}
    with open(file, mode='r', encoding='utf-8') as file:
        for line in file.readlines():
            line = line.replace("\t", " ")
            line = line.split(sep=" ")
            while "" in line:
                line.remove("")
            for num in range(len(line)):
                if "\n" in line[num]:
                    line[num].replace("\n", " ")
                if num == 0:
                    data["Time_0"].append(float(line[num]))
                elif num == 1:
                    data["Temp_0"].append(float(line[num]))
                elif num == 2:
                    data["Time_1"].append(float(line[num]))
                else:
                    data["Temp_1"].append(float(line[num]))
    return(data)
def safe_extraction(lst, arr1, arr2):
    acc = 0
    _dev = 0
    m = 0
    n = 20
    #_max = 0
    #_min = 0
    first_cicle = True
    for files in sorted(os.listdir(lst)):
        acc = 0
        data = extract(lst+files)
        #_max = data["Temp_0"][len(data["Temp_0"])-n] - data["Temp_1"][len(data["Temp_1"])-n]
        #_min = data["Temp_0"][len(data["Temp_0"])-n] - data["Temp_1"][len(data["Temp_1"])-n]
        for num in range(len(data["Temp_0"])-n, len(data["Temp_0"])):
            acc = acc + float(data["Temp_0"][num] - data["Temp_1"][num])
        m = acc/float(n)
        #for num in range(len(data["Temp_0"])-n, len(data["Temp_0"])):
        #    _max = max(_max, data["Temp_0"][num] - data["Temp_1"][num])
        #    _min = min(_min, data["Temp_0"][num] - data["Temp_1"][num])
        for num in range(len(data["Temp_0"])-n, len(data["Temp_0"])):
            _dev = _dev + ((float(data["Temp_0"][num]) - float(data["Temp_1"][num])) - m)**2
        _dev = np.sqrt((1/(n*(n-1))) * _dev) 
        arr2.append(_dev)
        arr1.append(acc/float(n))
        #arr2.append(abs(_max)/2.)
        #arr1.append(acc/float(n))
        acc = 0.
data_x = []
sigma_x = []
safe_extraction("./misurazione_T2_221/misurazioni_rame/misurazioni/", data_x, sigma_x)
safe_extraction("./misurazione_T2_221/misurazioni_rame/misurazioni_10/", data_x, sigma_x)
def modello(x, m):
    return (m*x)
#for files in os.listdir("./misurazioni_rame/"):
#   data = extract(f"./misurazioni_rame/{files}")
#    acc = 0
#    for num in range(len(data["Temp_0"])-6, len(data["Temp_0"])):
#        print(data["Temp_0"][num])
#        acc = acc +  float(data["Temp_0"][num])
#    data_T_rame_T0.append(acc/6.)
#    acc = 0
#    for num in range(len(data["Temp_1"])-6, len(data["Temp_1"])):
#        acc = acc +  float(data["Temp_1"][num])
#    data_T_rame_T1.append(acc/6.)
data_delta_x = _extract_delta("dati_delta_x.txt")
delta_x_star = {"delta_x": [], "err": []}
for num in range(len(data_delta_x["delta_x"])):
    if num != 0:
        delta_x_star["delta_x"].append(data_delta_x["delta_x"][num] - data_delta_x["delta_x"][0])
        delta_x_star["err"].append(data_delta_x["err"][num] + data_delta_x["err"][0])
    else: 
        delta_x_star["delta_x"].append(data_delta_x["delta_x"][0])
        delta_x_star["err"].append(data_delta_x["err"][0])
del(data_delta_x)
plt.figure("Dati rame")
popt, pconv = curve_fit(modello, delta_x_star["delta_x"], data_x, absolute_sigma=True)
m_hat = popt
sigma_m = np.sqrt(pconv.diagonal())
x = np.linspace(0, 0.50)
plt.errorbar(delta_x_star["delta_x"], data_x, fmt='o', color="black", yerr=sigma_x)
plt.plot(x, modello(x, m_hat))
plt.xlabel(r"$\Delta x$ [m]")
plt.ylabel(r"$T_i [C]$")
plt.savefig("Grafico_differenza_temperatura_rame_dev.pdf")
plt.show() # 8 e 12
plt.figure("Grafico residui")
# Inizializza res["err"] come un array vuoto
delta_x_star["delta_x"] = np.array(delta_x_star["delta_x"])
res = {"value": [], "err": []}
res["err"] = []
for el in range(len(delta_x_star["delta_x"])):
    res["value"].append(data_x[el] - modello(delta_x_star["delta_x"][el], m_hat))
    res["err"].append(sigma_x[el])

# Converti res["err"] in un array NumPy
res["value"] = np.array(res["value"])
res["err"] = np.array(res["err"])
res["value"] = np.squeeze(np.array(res["value"]))
plt.errorbar(delta_x_star["delta_x"], res["value"], yerr=res["err"], fmt='o', color="green")
plt.axhline(0, xmin=0, xmax=1, color="orange")
plt.savefig("Grafico_residui_rame_dev.pdf")
plt.show()
S = np.pi * (2.5 * 10 ** (-2)) ** 2
V = 10.2
sigma_V = 0.1
I = 1.65
sigma_i = 0.01
sigma_r = 0.05 * 10 ** (-3)
r = 25 * 10 ** (-3)
print(f"m è pari a {m_hat}")
print(f"L'errore su m è: {sigma_m}")
_lambda = -(V * I)/(2 * m_hat[0] * S)
print(f"Il valore della conducibilità risulta pari {_lambda}")
print(f"L'errore su lambda è: {_lambda * np.sqrt((sigma_i/I) ** 2 + (sigma_V/V) ** 2 + (sigma_m/m_hat) ** 2 + 4*(sigma_r/r) ** 2)}")
chi_quadro = 0
for el in range(len(res["value"])):
    chi_quadro = chi_quadro + (res["value"][el]/sigma_x[el])**2
print(f"Il chi quadro risulta essere: {chi_quadro}")
#file = np.loadtxt("dati_delta_x.txt")
#for x in file[0]:
#    x_1["val"].append(x)
#for x in file[1]:
#     x_1["sigma"].append(x)
# for x in os.listdir("./misurazioni_rame"):
#     file = open("./misurazioni_rame/"+str(x), "r")
#     for el in file.read():
#         print(el)

