import speedtest
from time import sleep
from os import system
from os.path import exists
from datetime import datetime
import pandas as pd


class SpeedTest:
    df = None
    def __init__(self):
        self.df = pd.DataFrame(columns=['Data Hora', 'Ping', 'Download', 'Upload'])

    def print_header(self):
        """Exibe o cabeçalho da aplicação"""
        system('clear')
        print('-----------------------------------------')
        print('       Teste - Velocidade Internet       ')
        print('-----------------------------------------\n\n')

        print('Presione Ctrl+C para parar a aplicação :)\n\n')

    def get_status_connection(self):
        """Verifica a conexão com a internet
        
        get_status_connection -> bool
        """
        dns_for_ping = 'www.google.com'

        return_ping = system('ping -c 1 ' + dns_for_ping)

        self.print_header()

        print('Testando a velocidade...\n')

        if return_ping == 0:
            return True
        return False
    
    def get_results(self):
        """Verifica quais os resultados do teste de velocidade
        get_results() -> dict
        """
        ping = 0
        download = 0
        upload = 0

        if self.get_status_connection():
            try:
                s = speedtest.Speedtest()
                s.get_best_server()
                s.download()
                s.upload()

                ping = s.results.dict()['ping']
                download = s.results.dict()['download'] / 1000000
                upload = s.results.dict()['upload'] / 1000000
            except:
                ping = 0
                download = 0
                upload = 0
        else:
            ping = 0
            download = 0
            upload = 0

        results = {'ping': round(ping), 'download': round(download), 'upload': round(upload)}

        return results

    def print_results(self, results):
        """Exibe os resultados do teste de velocidade"""
        ping = results['ping']
        download = results['download']
        upload = results['upload']

        self.print_header()

        if results['download']:
            print('---------------Resultados----------------')
            print('|-> Ping: %d' %ping)
            print('|-> Download: %d' %download)
            print('|-> Upload: %d' %upload)
            print('-----------------------------------------\n\n\n')
        else:
            print('*** Sem conexão com a internet ***\n\n\n')



    def write_file(self, results):
        """Escreve os resultados do teste de velocidade em um arquivo
        Keywords arguments:
        results -- dicionario com os resultados do teste de velocidade
        """
        ping = results['ping']
        download = results['download']
        upload = results['upload']

        name_archive_xlsx = 'temp/speed.xlsx'
        name_archive_txt = 'temp/speed.txt'
        flag_file = 'a'

        date_time = datetime.now()
        text_date_time = date_time.strftime('%d/%m/%Y %H:%M:%S')

        """Escreve o resultado em formato xlsx"""
        if exists(name_archive_xlsx):
            self.df = pd.read_excel(name_archive_xlsx, sheet_name='speed')
            
        self.df.loc[len(self.df)] = [text_date_time, ping, download, upload]
        self.df.to_excel(name_archive_xlsx, sheet_name='speed', index=False)

        """Escreve o resultado em formato txt"""
        if not exists(name_archive_txt):
            flag_file = 'w'
            
            with open(name_archive_txt, flag_file) as writer:
                writer.write('Data Hora|Ping|Download|Upload\n')

            flag_file = 'a'

        with open(name_archive_txt, flag_file) as writer:
            writer.write('%s|%d|%.2f|%.2f\n' %(text_date_time , ping, download, upload))

while True:
    try:
        time_sleep = 60

        speed_test = SpeedTest()
        
        speed_test.print_header()

        results = speed_test.get_results()

        speed_test.print_results(results)

        speed_test.write_file(results)

        for timer in range(time_sleep, 0, -1):
            speed_test.print_results(results)

            print('O poximo teste será realizado em %d segundos!' %timer)

            sleep(1)

    except KeyboardInterrupt:
        speed_test.print_header()

        print('Ctrl+C presionado. Aplicação sendo encerrada')
        print('Obrigado por utilizar a aplicação :):):)')
        exit(1)