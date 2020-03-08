# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 15:42:09 2016

@author: Particular
"""


import numpy as np
import matplotlib.pyplot as plt



pi = np.pi

def Calculo(har, harvent, diametro, comp, alt, aletas, larg, esp, k, vent, Toleo, Tamb):
    if (vent == 0):
        h = har
    else:
        h = harvent
    
    cons_aletas = 2 * aletas # Dobro de aletas para consideração
    cons_alt = alt / 2  # Dobro de aletas com metade da altura    
    
    #Areas
    Asem = (diametro * pi * ((2*comp)+alt)) - cons_aletas * (esp)
    
    Aaleta = aletas*(larg*cons_alt) + 2*aletas*(esp*cons_alt)
    

    alfa = np.sqrt((2*h)/(k*esp))
    n = (np.tanh(alfa*cons_alt))/(alfa*cons_alt)


    #Transferencia de Calor por convecção
    Qsem = h * Asem * (Toleo - Tamb)
    Qaleta = h * Aaleta * n * (Toleo - Tamb)
    Qtotal = Qsem + Qaleta
    
    return (n,Qsem,Qaleta,Qtotal,Asem,Aaleta)


#fig = plt.figure(figsize=(8, 8), facecolor='black')


#Parametros
aletas = 30
alt = 3 # altura das aletas
larg = 0.52 #profundiade aleta
esp = 0.0085 #espessura aleta
gap = 0.05 #gap entre aletas
diametro = 0.07
har = 50    #Coeficiente de transf. do ar normal
k = 52 # Condutividade térmica (Aço)
comp = aletas*(esp + gap) #Comprimento do tubo
vent = 0
Toleo = 80
Tamb = 25

#Parametros Velocidade
kar = 0.03
diametro_vent = 1 #Diametro do ventilador
rpm = 860 #Velocidade do ventilador
velocidade = rpm * pi * (diametro_vent/60)
visc = 2.097 * 10**(-5) #viscosidade cinematica
Pr = 0.7202 #Numero de Prandtl
Re = (velocidade * alt)/(visc) #Numero de Reynolds
Nu = (0.037* Re**(0.8) - 871)*Pr**(1/3)
harvent = (kar/alt)*Nu # Coeficiente de trans do ar com ventilaçao

n, Qsem, Qaleta, Qtotal,Asem, Aaleta = Calculo(har, harvent, diametro, comp, alt, aletas, larg, esp, k, vent, Toleo, Tamb)

print('Transferência de Calor Total com Ventilação Desligada: %f W' %Qtotal)
print(Re)
#PLOT -SIMULAÇÃO

fig = plt.figure(figsize = (14,11), facecolor = 'white')
fig2 = plt.figure(facecolor = 'white')
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,1,2)


#Altura da aleta variando de 0 a 3m
tsteps_a = np.linspace(0,3.5,1000)
qsimulado_1 = np.array([])
nsimulado_1 = np.array([])
for altura in tsteps_a:
    n_sim, Qsem_sim, Qaleta_sim, Qtotal_sim, Asem_sim, Aaleta_sim = Calculo(har, harvent, diametro, comp, altura, aletas, larg, esp, k, vent, Toleo, Tamb)
    qsimulado_1 = np.append(qsimulado_1, [Qtotal_sim])       
    nsimulado_1 = np.append(nsimulado_1, [n_sim*100])
#PLOT CURVA TRANSFERENCIA DE CALOR VARIANDO ALTURA
ax1.plot(tsteps_a, qsimulado_1, label = 'Transferência de Calor')
ax1.scatter(alt, Qtotal)
ax1.grid()
ax1.legend(loc=2)
ax1.set_title('Gráfico variação da altura da aleta (Vent OFF)')
ax1.set_xlabel('Altura ( m )')
ax1.set_ylabel('Dissipação do Calor ( W )')
ax3.plot(tsteps_a, nsimulado_1,'r', label = 'Eficiência da Aleta')
ax3.grid()
ax3.legend()
ax3.set_title('Eficiência de aleta com variação da altura (Vent OFF)')
ax3.set_xlabel('Altura em "m"')
ax3.set_ylabel('Eficiência ( % )')
plt.show()
   
   
        
#Largura da aleta variando de 0 a 1m
tsteps_l = np.linspace(0,1,100)
qsimulado_2 = np.array([])
nsimulado_2 = np.array([])
for largura in tsteps_l:
     n_sim2, Qsem_sim, Qaleta_sim, Qtotal_sim2, Asem_sim, Aaleta_sim = Calculo(har, harvent, diametro, comp, alt, aletas, largura, esp, k, vent, Toleo, Tamb)
     qsimulado_2 = np.append(qsimulado_2, [Qtotal_sim2])
     nsimulado_2 = np.append(nsimulado_2, [n_sim2])
#PLOT CURVA TRANSFERENCIA DE CALOR VARIANDO ALTURA
ax2.plot(tsteps_l, qsimulado_2, label = 'Transferência de Calor')
ax2.scatter(larg, Qtotal)
ax2.grid()
ax2.legend(loc=2)
ax2.set_title('Gráfico variação da largura da aleta (Vent OFF)')
ax2.set_xlabel('Largura ( m )')
ax2.set_ylabel('Dissipação do Calor ( W )')
plt.show()


#Largura da aleta variando de 0 a 1m
tsteps_amb = np.linspace(0,35,500)
qsimulado_3 = np.array([])
for temperatura in tsteps_amb:
     n_sim, Qsem_sim, Qaleta_sim, Qtotal_sim, Asem_sim, Aaleta_sim = Calculo(har, harvent, diametro, comp, alt, aletas, larg, esp, k, vent, Toleo, temperatura)
     qsimulado_3 = np.append(qsimulado_3, [Qtotal_sim])
#PLOT CURVA TRANSFERENCIA DE CALOR VARIANDO ALTURA
plt.plot(tsteps_amb, qsimulado_3, label = 'Transferência de Calor')
plt.scatter(Tamb, Qtotal)
plt.grid()
plt.legend(loc=2)
plt.title('Variação da Temperatura do Ambiente (Ventilação Desligada)')
plt.xlabel('Temperatura ( ºC )')
plt.ylabel('Dissipação do Calor ( W )')
plt.show()







##### VENTILAÇÃO LIGADA ######



vent = 1


n, Qsem, Qaleta, Qtotal,Asem, Aaleta = Calculo(har, harvent, diametro, comp, alt, aletas, larg, esp, k, vent, Toleo, Tamb)

print('Transferência de Calor Total com ventilação ligada: %f W' %Qtotal)

#PLOT -SIMULAÇÃO

fig3 = plt.figure(figsize = (14,11), facecolor = 'white')
fig4 = plt.figure(facecolor = 'white')
ax4 = fig3.add_subplot(2,2,1)
ax5 = fig3.add_subplot(2,2,2)
ax6 = fig3.add_subplot(2,1,2)


#Altura da aleta variando de 0 a 3m
tsteps_a = np.linspace(0,3.5,1000)
qsimulado_1 = np.array([])
nsimulado_1 = np.array([])
for altura in tsteps_a:
    n_sim, Qsem_sim, Qaleta_sim, Qtotal_sim, Asem_sim, Aaleta_sim = Calculo(har, harvent, diametro, comp, altura, aletas, larg, esp, k, vent, Toleo, Tamb)
    qsimulado_1 = np.append(qsimulado_1, [Qtotal_sim])       
    nsimulado_1 = np.append(nsimulado_1, [n_sim*100])
#PLOT CURVA TRANSFERENCIA DE CALOR VARIANDO ALTURA
ax4.plot(tsteps_a, qsimulado_1, label = 'Transferência de Calor')
ax4.scatter(alt, Qtotal)
ax4.grid()
ax4.legend(loc=2)
ax4.set_title('Gráfico variação da altura da aleta (Vent ON)')
ax4.set_xlabel('Altura ( m )')
ax4.set_ylabel('Dissipação do Calor ( W )')
ax6.plot(tsteps_a, nsimulado_1,'r', label = 'Eficiência da Aleta')
ax6.grid()
ax6.legend()
ax6.set_title('Eficiência de aleta com variação da altura (Vent ON)')
ax6.set_xlabel('Altura ( m )')
ax6.set_ylabel('Eficiência ( % )')
plt.show()
   
   
        
#Largura da aleta variando de 0 a 1m
tsteps_l = np.linspace(0,1,100)
qsimulado_2 = np.array([])
nsimulado_2 = np.array([])
for largura in tsteps_l:
     n_sim2, Qsem_sim, Qaleta_sim, Qtotal_sim2, Asem_sim, Aaleta_sim = Calculo(har, harvent, diametro, comp, alt, aletas, largura, esp, k, vent, Toleo, Tamb)
     qsimulado_2 = np.append(qsimulado_2, [Qtotal_sim2])
     nsimulado_2 = np.append(nsimulado_2, [n_sim2])
#PLOT CURVA TRANSFERENCIA DE CALOR VARIANDO ALTURA
ax5.plot(tsteps_l, qsimulado_2, label = 'Transferência de Calor')
ax5.scatter(larg, Qtotal)
ax5.grid()
ax5.legend(loc=2)
ax5.set_title('Gráfico variação da largura da aleta (Vent ON)')
ax5.set_xlabel('Largura ( m )')
ax5.set_ylabel('Dissipação do Calor ( W )')
plt.show()


#Largura da aleta variando de 0 a 1m
tsteps_amb = np.linspace(0,35,500)
qsimulado_3 = np.array([])
for temperatura in tsteps_amb:
     n_sim, Qsem_sim, Qaleta_sim, Qtotal_sim, Asem_sim, Aaleta_sim = Calculo(har, harvent, diametro, comp, alt, aletas, larg, esp, k, vent, Toleo, temperatura)
     qsimulado_3 = np.append(qsimulado_3, [Qtotal_sim])
#PLOT CURVA TRANSFERENCIA DE CALOR VARIANDO ALTURA
plt.plot(tsteps_amb, qsimulado_3, label = 'Transferência de Calor')
plt.scatter(Tamb, Qtotal)
plt.grid()
plt.legend(loc=2)
plt.title('Variação da Temperatura do Ambiente (Ventilação Ligada)')
plt.xlabel('Temperatura ( ºC )')
plt.ylabel('Dissipação do Calor ( W )')
plt.show()


fig5 = plt.figure(facecolor = 'white')
vent = 0

plt.axis([0, 100, -5000, 10000])
plt.ion()
Perdas = 0
Variavel = 0
desliga_variavel = 100
for t in range(1,100):
    if (t > 65):
        Perdas = Perdas - 5*np.sqrt(t)
    else:
        Perdas = 700*np.sqrt(t)
        
    n, Qsem, Qaleta, Qtotal,Asem, Aaleta = Calculo(har, harvent, diametro, comp, alt, aletas, larg, esp, k, vent, Toleo, Tamb)
    Diferenc = Qtotal - Perdas 
    
    if (Diferenc < 0):
        Variavel = 1 #Liga a variavel que vai ligar o ventilador
        desliga_variavel = t + 50
        
    if (desliga_variavel == t):
        Variavel = 0
        
    if (Variavel == 0):
        vent = 0
        plt.scatter(t, Diferenc)
        plt.grid()
        plt.title('VENT OFF')
        plt.xlabel('Tempo')
        plt.ylabel('Diferença (Transferência - Perdas)')
        plt.pause(0.05)
    else:
        vent = 1
        plt.scatter(t, Diferenc)
        plt.grid()
        plt.title('VENT ON')
        plt.xlabel('Tempo')
        plt.ylabel('Diferença (Transferência - Perdas)')
        plt.pause(0.05)
        

















