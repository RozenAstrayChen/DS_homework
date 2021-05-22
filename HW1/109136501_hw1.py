import requests
from bs4 import BeautifulSoup

def crawler_info(address):
    url = 'https://www.blockchain.com/eth/address/'+ address +'?view=standard'
    resp = requests.get(url); resp.encoding = 'utf-8'; resp.encoding = 'big5' 
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    info_spans = soup.find_all("div", class_="sc-8sty72-0 bFeqhe")
    
    infoes = []
    for info_span in info_spans:
        infoes.append(info_span.find('span').text)
    transaction_classes = soup.find_all("div", class_="sc-1fp9csv-0 koYsLf")

    transaction_classes.reverse()
    for transaction_class in transaction_classes:
        last_transaction = transaction_class.find("span", class_="sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC sc-85fclk-0 fhjukF")
        if last_transaction is not None:
            amout = last_transaction.text
            time = transaction_class.find("span", class_="sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC").text
            transaction = transaction_class.find_all("a", class_="sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk")[-1].text
            return infoes, time, transaction, amout
    
    return infoes, None, None, None

def show(info, time, transaction, amount, write=True, path="109136501_hw1_output.txt"):
    print('%s : %s' % (info[2], info[3]))
    print('%s : %s' % (info[4], info[5]))
    print('%s : %s' % (info[6], info[7]))
    print('%s : %s' % (info[8], info[9]))
    print('%s : %s' % (info[10], info[11]))
    print('%s : %s' % (info[12], info[13]))
    if time is not None:
        print('%s : %s' % ('Date', time))
        print('%s : %s' % ('To', transaction))
        print('%s : %s' % ('Amount', amount))
    print('------------------------------------')

    if write:
        f = open(path, "a", encoding='UTF-8')
        f.writelines('%s: %s\n' % (info[2], info[3]))
        f.writelines('%s: %s\n' % (info[4], info[5]))
        f.writelines('%s: %s\n' % (info[6], info[7]))
        f.writelines('%s: %s\n' % (info[8], info[9]))
        f.writelines('%s: %s\n' % (info[10], info[11]))
        f.writelines('%s: %s\n' % (info[12], info[13]))
        if time is not None:
            f.writelines('%s: %s\n' % ('Date', time))
            f.writelines('%s: %s\n' % ('To', transaction))
            f.writelines('%s: %s\n' % ('Amount', amount))
        f.writelines('--------------------------------------------------------------------------\n')
        f.close()
    

def hw1(input_path='ex_input_hw1.txt'):
    f = open(input_path, "r")
    mylist = f.read().splitlines() 
    f.close()
    # create file
    f = open('109136501_hw1_output.txt', "w", encoding='UTF-8')
    f.close()
    for ids in mylist:
        ids_list = []
        for i in range(0, 4):
            ids_list.append(ids)
            infos, time, transaction, amount = crawler_info(ids)
            
            show(infos, time, transaction, amount)
            ids = transaction
            if time is None:
                break
        f = open('109136501_hw1_output.txt', "a", encoding='UTF-8')
        for idx in range(0, len(ids_list)):
            f.writelines(ids_list[idx])
            if idx != len(ids_list)-1:
                f.writelines(' -> ')
        f.writelines('\n--------------------------------------------------------------------------\n')
        f.close()
        
        
hw1()