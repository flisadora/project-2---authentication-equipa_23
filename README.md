# Correr o projeto

## Server e Database
Utilizando o xampp:
1. Adicionar a pasta `server` do projeto a `/opt/lampp/htdocs`
2. Correr xampp
   1. `cd /opt/lampp`
   2. `sudo ./manager-linux-x64.run`
3. Em `localhost/dashboard`, selecionar phpMyAdmin
4. Importar ficheiro `HPWiki.sql` que se encontra na pasta database
    - emails e passwords:
      - isabella@hotmail.com: iLoveDobby_3
      - john@gmail.com: AvadaKedravaBellatrix
      - lili_martinha@gmail.com: AvadaKedravaBellatrix88

## Client
Na pasta client de cada uma das apps:
1. `npm install`
2. `npm start`

## UAP
`python3 uap.py`

## Requirements
pip install -r requirements.txt
