import os

def main():
  folder_to_show = list()

  try:
    my_folders = [x[0] for x in os.walk("..\\")]
    for i in my_folders:
      for j in i.split('\\'):
        if 'tomada' in j:
          folder_to_show.append(j)

  except:
    print('Ocorreu um erro ao tentar buscar arquivos...')


  if folder_to_show:
    # Exibe todas as pastas com o nome de tomada encontrada
    print(folder_to_show)


if __name__ == "__main__":
  main()