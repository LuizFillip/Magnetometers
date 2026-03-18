# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 09:11:59 2026

@author: Luiz
"""

pathin = 'magnetometers/data/2015/SJG/'

# Função para verificar se uma linha é numérica
def is_numeric_line(line):
    parts = line.strip().split()
    return all(part.lstrip('-').isdigit() for part in parts)

# Função para ler o arquivo e extrair os dados
def read_text_file(filename):
    data = []

    with open(filename, 'r') as file:
        for line in file:
            if is_numeric_line(line):
             
                numbers = list(map(int, line.strip().split()))
                data.append(numbers)
            else:
                # Se quiser armazenar o texto também:
                # print("Linha de texto encontrada:", line.strip())
                pass

    return data

def fn2dn(fn):
    strc = fn.split('.')[0].lower()
    return dt.datetime.strptime(strc, '%b%d%y')


fn = 'dec1915.sjg'


def to_frame(infile):
    l =  infile 
    dn  = fn2dn(l.split('/')[-1])

    data = read_text_file(infile)
    
    cols = ['x', 'y', 'z', 'f']
    
    df = pd.DataFrame(data).iloc[:, :4]
    
    df.columns = cols 
    
    times = pd.date_range(
        dn, 
        freq = '1min', 
        periods = len(df)
        )
    
    df.index = times 
    
    return df 
