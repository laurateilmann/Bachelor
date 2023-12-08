# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:06:24 2023

@author: ltei0004
"""


plt.figure()
plt.plot(x, y, 'o')
plt.title("Insert title", fontsize=16, family='Times New Roman', fontweight='bold')
plt.xlabel("x-label title", fontsize=14, family='Times New Roman')
plt.ylabel("y-label title", fontsize=14, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
plt.grid()