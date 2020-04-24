#!/usr/bin/python
# -*- coding: utf-8 -*-
# sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
import json, datetime, os, sys, ldap
from ldap.controls import SimplePagedResultsControl
import ldap.modlist as modlist

server_ip_adress = "192.168.1.10"
domain_dot_format = "ornek.ldap.com"
## split "." lara göre metni parcalar, aralara ",dc=" koyarak join ile parcaları birlestirir
domain_dc_format = "dc=" + ",dc=".join(domain_dot_format.split("."))
port = "389"
user_dn = "cn=admin,dc=ornek,dc=ldap,dc=com"
password = "Passw0rd"

# Samba baglantısı kurulur. Global degiskene atanır. Sistemin her yerinden erisilebilir
def setSambaConnection():
    print("setSambaConnection")
    global ldap_connection
    ## try içersisnde herhangibir hata alinirsa except kısmında çıktı olarak hatayı yazdirir
    try:
        host =  server_ip_adress + ':' + port
        ## varsayilan olarak openldap guvensiz olan ldap(389), samba ldaps(636)'i kullanir.
        if port == "389":
            host = 'ldap://' + host
        elif port == "636":
            host = 'ldaps://' + host
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap_connection = ldap.initialize(host)
        ldap_connection.protocol_version = ldap.VERSION3
        ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
        ldap_connection.set_option(ldap.OPT_NETWORK_TIMEOUT, 20.0)
        ldap_connection.simple_bind_s(user_dn, password)
    except Exception as e:
        ## Baglantida hata aldıysa ekrana çıktı verir ve programı kapatır
        print("Samba/AD sunucusuna baglanamadi")
        sys.exit(e)
    ## Hata alnadıysa ekrana çıktı verir
    print("Samba/AD sunucusuna baglandi")



# Daha önce kurulan baglantı global olarak tanımlanır. Kullanıcı adı ve soyadı alarak basit bir kullanıcı ekler.
def addUser(username,surname):
    global ldap_connection
    # dn ile birlikte verinin tam yolu belirlenir
    dn = "uid=" + username + ",ou=kisiler," + domain_dc_format
    # modlist ile nesnenin ozellikleri (sınıfının semasına gore) veri listesi oluşturulur
    modlist = {
        "objectClass": ["inetOrgPerson"], # Sınıfı inetOrgPerson, hangi ozelliklere sahip olacagını belirtir
        "cn": [ username ],               # Nesneye verilen isim (tc ya da isim verilebilir)
        "sn": [ surname ],                # soyadı
        }
    # oluşdurulan ozellik listesi ile, belirtilen dn'de ldap modülündeki add_s fonksiyonu ile kullanıcı eklenir
    result = ldap_connection.add_s(dn, ldap.modlist.addModlist(modlist))

# yukarudaki fonksiyon ile aynı işi yapar. 1 yerine 100 kullanıcı ekler
def addMoreUser(username,surname):
    global ldap_connection
    dn = "uid=" + username + ",ou=kisiler," + domain_dc_format
    for number in range(100):
        modlist = {
            "objectClass": ["inetOrgPerson"],
            "cn": [ username+str(number) ],
            "sn": [ surname+str(number) ],
            }
        result = ldap_connection.add_s(dn, ldap.modlist.addModlist(modlist))

# Basit bir sorgu yapar
#   filter hengi verilerin aranacagi (orneğin kullanıcılar ve telefon numarası bos olmayanlar)
#   attrs hangi ozelliklerin cekileceği (adı ve soyadı)
#   base_dn aramanın agacın neresinde yapılacagını belirtir
def search(filter,attrs,base_dn):
    global ldap_connection
    result = ldap_connection.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs)
    print(result)
    # dönen dictionary array'indeki verileri for dönerek daha basit bir hale getirir. Key olarak kullanılar dn'leri siler
    results = [entry for dn, entry in result if isinstance(entry, dict)]
    print results
    return results

# Ldap sorgusunda 1000'den fazla veri sorgu cok uzun surer ya da limit asildi seklinde hata verir.
# Bu fonksiyon donen sorgunun çıktılarını biner biner alır, birbirinin sonuna ekler.
#   filter hengi verilerin aranacagi (orneğin kullanıcılar ve telefon numarası bos olmayanlar)
#   attrs hangi ozelliklerin cekileceği (adı ve soyadı)
#   base_dn aramanın agacın neresinde yapılacagını belirtir
def getSambaUsers(filter,attrs,base_dn):
    print("getSambaUsers")
    global ldap_connection
    ldapUsers = []
    page_control = SimplePagedResultsControl(True, size=1000, cookie='')

    response = ldap_connection.search_ext(base_dn,ldap.SCOPE_SUBTREE,filter,attrs,serverctrls=[page_control])
    try:
        pages = 0
        while True:
            pages += 1
            rtype, rdata, rmsgid, serverctrls = ldap_connection.result3(response)
            ldapUsers.extend(rdata)
            controls = [control for control in serverctrls if control.controlType == SimplePagedResultsControl.controlType]
            if not controls:
                print('The server ignores RFC 2696 control')
                break
            if not controls[0].cookie:
                break
            page_control.cookie = controls[0].cookie
            response = ldap_connection.search_ext(base_dn,ldap.SCOPE_SUBTREE,filter, attrs,serverctrls=[page_control])

    except:
        print()

    # dönen dictionary array'indeki verileri for dönerek daha basit bir hale getirir. Key olarak kullanılar dn'leri siler
    results = [entry for dn, entry in ldapUsers if isinstance(entry, dict)]
    return results

def main():
    ## Define Globals
    global ldap_connection

    # ldap baglantısı kurar. bunu ldap_connection degiskenine atar
    setSambaConnection()
    
    # basit bir kullanıcı ekleme
    addUser("ayse","demir")

    # kok dizinden baslayarak tüm kullanıcıları arama
    search("objectClass=inetOrgPerson",["cn","sn"],domain_dc_format)

    # kok dizinden baslayarak tüm mobil ozelligi bos olmayan kullanıcıları arama
    search("(&(objectClass=inetOrgPerson)(mobile=*))",["cn","sn"],domain_dc_format)

    # ldap baglantısı kapatılır
    ldap_connection.unbind()

if __name__ == '__main__':
    sys.exit(main())
