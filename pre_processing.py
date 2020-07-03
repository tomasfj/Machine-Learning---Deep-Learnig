import os, os.path
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from PIL import Image

def count_images():
    DIR1 = './dataset/flor1'
    DIR2 = './dataset/flor2'
    DIR3 = './dataset/flor3'
    DIR4 = './dataset/flor4'
    DIR5 = './dataset/flor5'
    DIR6 = './dataset/flor6'
    DIR7 = './dataset/flor7'
    n_flor1 =len([name for name in os.listdir(DIR1) if os.path.isfile(os.path.join(DIR1, name))])
    n_flor2 =len([name for name in os.listdir(DIR2) if os.path.isfile(os.path.join(DIR2, name))])
    n_flor3 =len([name for name in os.listdir(DIR3) if os.path.isfile(os.path.join(DIR3, name))])
    n_flor4 =len([name for name in os.listdir(DIR4) if os.path.isfile(os.path.join(DIR4, name))])
    n_flor5 =len([name for name in os.listdir(DIR5) if os.path.isfile(os.path.join(DIR5, name))])
    n_flor6 =len([name for name in os.listdir(DIR6) if os.path.isfile(os.path.join(DIR6, name))])
    n_flor7 =len([name for name in os.listdir(DIR7) if os.path.isfile(os.path.join(DIR7, name))])
    print('Flor 1: %d' %n_flor1 )
    print('Flor 2: %d' %n_flor2 )
    print('Flor 3: %d' %n_flor3 )
    print('Flor 4: %d' %n_flor4 )
    print('Flor 5: %d' %n_flor5 )
    print('Flor 6: %d' %n_flor6 )
    print('Flor 7: %d' %n_flor7 )
    print('Total = %d' %(n_flor1 + n_flor2 + n_flor3 + n_flor4+ n_flor5+ n_flor6+ n_flor7))

    return([n_flor1, n_flor2, n_flor3, n_flor4, n_flor5, n_flor6, n_flor7])



# Load Data in '.csv' format: filename, class, learning_validation_test_set_flag
def make_csv_file(n_imagens):
    nomes_flores = ['flor1', 'flor2', 'flor3', 'flor4', 'flor5', 'flor6', 'flor7']

    with open('anotations.csv', mode='w') as csv_file:
        csv_file = csv.writer(csv_file, delimiter=',')

        for i in range(len(nomes_flores)):
            for j in range(n_imagens[i]):
                csv_file.writerow( [str(nomes_flores[i])+'_'+str(j)+'.jpg', i+1, 0] )


def split_dataset(n_imagens):
    nomes_flores = ['flor1', 'flor2', 'flor3', 'flor4', 'flor5', 'flor6', 'flor7']

    x = []

    for i in range(len(nomes_flores)):
        for j in range(n_imagens[i]):
            x.append([str(nomes_flores[i])+'_'+str(j)+'.jpg', i+1, -1])

    x = np.asarray(x)
    y = np.arange(len(x))

    # dividir em treino(80%) e teste+validação(20%)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    print('x_train: %d, x_test: %d, y_train: %d, y_test: %d' %(len(x_train), len(x_test), len(y_train), len(y_test)))

    # dividir teste+validação(20%) em teste(10%) e validação (10%)
    x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=42)
    print('x_val: %d, x_test: %d, y_val: %d, y_test: %d' %(len(x_val), len(x_test), len(y_val), len(y_test)))


    # learning/train = 0, validation = 1, test = 2
    for x in x_train:
        x[2] = 0
    
    for x in x_val:
        x[2] = 1

    for x in x_test:
        x[2] = 2

    data = np.concatenate((x_train, x_val, x_test))


    with open('anotations.csv', mode='w') as csv_file:
        csv_file = csv.writer(csv_file, delimiter=',')
        
        for i in data:
            csv_file.writerow( i )



# ------------------------------ #
# -- Mudar nome dos ficheiros -- #
# ------------------------------ #

path = os.path.join(os.getcwd(), 'dataset/flor3/')

def sorted_dir(folder):
    def getctime(name):
        path = os.path.join(folder, name)
        return os.path.getctime(path)
    return sorted(os.listdir(path), key=getctime)

def rename_files():
    i = 0
    for file_name in sorted_dir(path):
        _, ext = os.path.splitext(file_name)
        print (file_name + " - " + str(i)+ext)    
        os.rename(os.path.join(path,file_name), os.path.join(path, 'flor3_' + str(i) + ext))
        i += 1

        print(str(i-1) + " files.")

def resize():
    path = os.path.join(os.getcwd(), 'dataset/flores/')
    dirs = os.listdir( path )
    
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((64,64), Image.ANTIALIAS)
            imResize.save(f + '.jpg')


def half_dataset(size, folder, csv_name):

    n_imagens = count_images()

    nomes_flores = ['flor1', 'flor2', 'flor3', 'flor4', 'flor5', 'flor6', 'flor7']

    x = []

    for i in range(len(nomes_flores)):
        for j in range(n_imagens[i]):
            x.append([str(nomes_flores[i])+'_'+str(j)+'.jpg', i+1, -1])

    x = np.asarray(x)
    y = np.arange(len(x))

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)
    
    path = os.path.join(os.getcwd(), folder)
    dirs = os.listdir( path )

    for x in x_train:
        if os.path.exists(os.path.join(path, x[0])):
            os.remove( os.path.join(path, x[0]) )
        else:
            print("The file %s does not exist" %x[0]) 

    print('Tamanho do file: %d ' % len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) )


    x = x_test
    y = np.arange(len(x_test))

    # dividir em treino(80%) e teste+validação(20%)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    print('x_train: %d, x_test: %d, y_train: %d, y_test: %d' %(len(x_train), len(x_test), len(y_train), len(y_test)))

    # dividir teste+validação(20%) em teste(10%) e validação (10%)
    x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=42)
    print('x_val: %d, x_test: %d, y_val: %d, y_test: %d' %(len(x_val), len(x_test), len(y_val), len(y_test)))

    # learning/train = 0, validation = 1, test = 2
    for x in x_train:
        x[2] = 0
    
    for x in x_val:
        x[2] = 1

    for x in x_test:
        x[2] = 2

    data = np.concatenate((x_train, x_val, x_test))

    with open(csv_name, mode='w') as csv_file:
        csv_file = csv.writer(csv_file, delimiter=',')
        
        for i in data:
            csv_file.writerow( i )




# call functions

#count_images()

#---

# criar ficheiro .csv
#make_csv_file(count_images())

# dividir dados em treino(40%), teste(20%), validação(20%)
#split_dataset(count_images())

#---

#rename_files()

#---

#resize()

#---

half_dataset(0.5, 'dataset/flores_metade/', 'anotations_metade.csv')
half_dataset(0.25, 'dataset/flores_quarto/', 'anotations_quarto.csv')