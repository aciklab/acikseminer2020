#!/usr/bin/python
# -*- coding: utf-8 -*-

# Gerekli, modüller
#   getpass: kullanıcıdan parola alırken parolanın gozukmemesini saglar
#   subprocess: process ile linux komutlarını çağırıp çıktılarını almaya yarar
#   re: metin içeirsinde belirli şablonlara göre araya yapmaya yarar. Config dosyalarını değiştirirken için kullanılır.
import getpass, subprocess, re, os

# Domaine almak için kullanılan configuration dosyaları
f_dns = "/etc/resolv.conf"
f_hosts = "/etc/hosts"
f_samba = "/etc/samba/smb.conf"
f_realm = "/etc/realmd.conf"
f_kerberos = "/etc/krb5.conf"
f_ligtdm = "/etc/lightdm/lightdm.conf"
f_sudoers = "/etc/sudoers.d/domainadmins"
f_sssd = "/etc/sssd/sssd.conf"
PATH_IFUP = "/etc/network/if-up.d/dns-update"

# Samba client-server mantığıyla çalışır. Makineyis istemci olarak ayarlayabilmek için gerekir.
def addSAMBA(workgroup,realm):
    with open(f_samba, "w") as sambafile:
        sambafile.write("""
[global]
unix charset=UTF-8
workgroup = """ + workgroup + """
client signing = yes
client use spnego = yes
dedicated keytab file = /etc/krb5.keytab
kerberos method = secrets and keytab
realm = """ + realm + """
dns proxy = no
map to guest = Bad User
log file = /var/log/samba/log.%m
max log size = 1000
syslog = 0
panic action = /usr/share/samba/panic-action %d """)

# realmd servisi SSSD'yi otomatik bir şekilde yapılandırır. Böylece kullanıcı girişleri için mapping yapılır
def addREALM(realm):
	proc = subprocess.Popen("lsb_release -r | cut -d':' -f2 | xargs", stdout=subprocess.PIPE, shell=True)
	(version, err) = proc.communicate()
	proc = subprocess.Popen("lsb_release -i | cut -d':' -f2 | xargs", stdout=subprocess.PIPE, shell=True)
	(distname, err) = proc.communicate()
	if (distname=="Pardus" and "17" in version):
		with open(f_samba, "a") as sambafile:
			sambafile.write("""client min protocol = SMB2
client max protocol = SMB3""")
	with open(f_realm, "w") as realmfile:
		realmfile.write("""[users]
default-home = /home/%D/%U
default-shell = /bin/bash
[active-directory]
default-client = sssd
os-name = """ + distname + """
os-version = """ + version + """
[service]
automatic-install = no
[""" + realm + """]
fully-qualified-names = no
automatic-id-mapping = yes
user-principal = yes
manage-system = no""")

# Samba/AD sunucusu ile istemcimizin zamanını eşitler. Donanım saatini günceller.
def setTime(ntpserver):
    cmd=subprocess.Popen("ntpdate "+ntpserver, stdout=subprocess.PIPE, shell=True)
    cmd.communicate()
    cmd=subprocess.Popen("hwclock --systohc", stdout=subprocess.PIPE, shell=True)
    cmd.communicate()

# Domaine alabilmek için gerekli olan paketleri ve kütüphaneleri yükler
def installDependences():
    try:
        cmd = subprocess.Popen("DEBIAN_FRONTEND=noninteractive apt-get update",shell=True)
        cmd.communicate()

        cmd = subprocess.Popen("DEBIAN_FRONTEND=noninteractive apt-get install krb5-user samba sssd libsss-sudo ntpdate realmd packagekit adcli sssd-tools cifs-utils smbclient -y", shell=True)
        cmd.communicate()
        print("Gereksinimler yüklendi")
    except Exception as error:
        print("Hata:",error)

# DNS olarak AD/Samba sunucusunun IP adresi ayarlanmalıdır. 
def editDNS(domain_ip,domain):
     # DNS ayarlarını düzenle
    try:
        # resolv.conf dosyasının kilidini kaldırır
        cmd = subprocess.Popen("chattr -i " + f_dns,shell=True)
        cmd.communicate()
        # resolv.conf dns olarak domain sunucsunu verir
        f = open(f_dns, "w")
        text = """nameserver %s
search %s
domain %s
""" % (domain_ip, domain, domain)
        f.write(text)
        f.close()
        # resolv.conf dosyasını kilitler
        cmd = subprocess.Popen("chattr +i " + f_dns,shell=True)
        cmd.communicate()
        print("DNS başarıyla güncellendi")
    except Exception as error:
        print("Hata, DNS ayarlanamadı:",error)

# Domaindeki DNS'e kendisini kaydettirebilmek için, makine adının domain adresiyle birlikte düzenlenmesi gerekir
# makine adı "client1" ise "client1.ornek.lab" olarak güncellenir
def editHosts(client_hostname,domain):
    # host dosyasını düzenle
    cmd = subprocess.call("hostnamectl set-hostname " + client_hostname + "." + domain,shell=True)
    cmd = subprocess.Popen("sed -i '/127.0.1.1/d' " + f_hosts,shell=True)
    cmd.communicate()
    cmd = subprocess.Popen("sed -i '1 a\\127.0.1.1      %s.%s   %s' %s" % (client_hostname,domain,client_hostname,f_hosts) ,shell=True)
    cmd.communicate()

# Domaine almak için, domaindeki yetkili bir kullanıcı adı
#                                parolası
#                                domain sunucusunun IP adresi
# gerekmektedir. Bunları kullanıcıdan alıp main fonksiyona geri döndürür.
def getInputs():
    # Kullanıcıdan parametreleri al
    domain_ip = raw_input("Samba/AD IP Adresi: ")
    domain_admin = raw_input("Domain admin kullanıcısı: ")
    domain_admin_password = getpass.getpass(prompt='Domain admin kullanıcı parolası? ') 
    client_hostname = raw_input('Makinenin yeni adı(hostname): ') 
    
    # Domain bilgilerini çek, alınan domain ip adresinden domain ile ilgili diğer bilgiler çekilir
    domain_info = subprocess.check_output("samba-tool domain info " + domain_ip + " || true" ,shell=True)
    if domain_info == "":
        exit("Hata: " + domain_ip + " adresinde domain bilgisine ulaşılamadı.")
    domain = re.findall("Domain\s*:\s*(.*)", domain_info)[0]
    domain_netbios_name = re.findall("Netbios.*domain\s*:\s*(.*)", domain_info)[0]
    return domain_ip, domain_admin, domain_admin_password, client_hostname, domain, domain_netbios_name

# domain ile haberleşmeyi sağlayan bazı servisler özel karakterleri desteklemez
# Bilgisayarı domaine almak ya da domaindeki kullanıcılarla giriş yapabilmek için dil ayarlarından bazılarının ingilizce olması gerekir.
# Dil ayarlarını kalıcı olarak değiştirmek için /etc/default/locale dosyasını düzenler, mevcut oturum için dili ingilizceye çeker
def editLocales():
    # İngilizceyi aktifleştirir ve yükler
    cmd = subprocess.Popen("locale-gen", shell=True)
    cmd.communicate()
    # Kalıcı olarak bazı dil ayarlarını ingilizceye çeker
    cmd = subprocess.Popen("sed -i 's/#.*en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/g' /etc/locale.gen" ,shell=True)
    with open("/etc/default/locale", "w") as localefile:
        localefile.write("""LANG=tr_TR.UTF-8
LANGUAGE=
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="tr_TR.UTF-8"
LC_TIME="tr_TR.UTF-8"
LC_COLLATE="tr_TR.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="tr_TR.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="tr_TR.UTF-8"
LC_ADDRESS="tr_TR.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=""")
    # Mevcut oturumda dil ingilizceye çekilir
    cmd = subprocess.Popen("localectl set-locale LANG=en_US.UTF-8", shell=True)
    cmd.communicate()

# Ticket(bilet) kullanımı için varsayılan kerberos sunucusu olarak domain sunucusunu ekler
def krbDefaultRealm(domain):
    cmd = subprocess.Popen("sed -i '/default_realm/d' %s" % (f_kerberos),shell=True)
    cmd.communicate()
    cmd = subprocess.Popen("sed -i '/\[libdefaults\]/a default_realm = %s' %s" % (domain,f_kerberos) ,shell=True)
    cmd.communicate()

# Linuxta ev dizini bulunmuyorsa kullanıcı giriş yapamaz. Pam modülüne kullanıcı ilk giriş yaparken ev dizini eklenmesi için bir satir eklenir.
def addMkHomedir():
    if (subprocess.call('grep -w "session required pam_mkhomedir.so skel=\/etc\/skel umask=0077" %s' % ("/etc/pam.d/common-session"),shell=True) == 1):
        subprocess.Popen("echo 'session required pam_mkhomedir.so skel=/etc/skel umask=0077' >> /etc/pam.d/common-session",shell=True)

# Kullanıcı giriş ekranında tüm kullanıcıların çekilmemesi için
# kullanıcı adı listesinin drop-down-list olarak değil manuel yazılması için lightdm dosyasında iki satır yorumdan kaldırılır ve true yapılır
def editLightdmConf():
    if(os.path.isfile(f_ligtdm)):
        cmd = subprocess.Popen("sed -i 's/.*greeter-show-manual-login\s*=\s*false/greeter-show-manual-login=true/g' %s" % (f_ligtdm) ,shell=True)
        cmd.communicate()

        cmd = subprocess.Popen("sed -i 's/.*#greeter-hide-users\s*=\s*false/greeter-hide-users=true/g' %s" % (f_ligtdm) ,shell=True)
        cmd.communicate()

# Domaindeki bulunan "Domain Admins" grubu sudoers dosyasına eklenerek, bu gruba dahil olan tüm kullanıcıların makinede 
#   sudo yetkisine sahip olması sağlanır
def addSudoers(domain):
    with open(f_sudoers, "w") as sudofile:
        sudofile.write("""%s\\x20admins ALL=(ALL) ALL """ % domain)

# Makine domaine alınırken domainde bulunan DNS'e kaydı eklenir. Fakat istemcinin IP adresi değişirse bunun DNS'te güncellenmesi gerekir.
# Network yeniden her başlatıldığından ip adresinin DNS'de güncellenmesini  sağlar
def addDNSUpdateOnStart():
    with open(PATH_IFUP, "w") as ifupfile:
        ifupfile.write("""#!/bin/bash
net ads dns register -P""")
    command1="chown root:root "+ PATH_IFUP
    subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)

# SSSD conf'a linux politikaların çekilebilmesi için gerekli bir satır ekler 
def editSSSD():
    subprocess.Popen("rm -f /var/lib/sss/db/*", stdout=subprocess.PIPE, shell=True)
    with open(f_sssd, "a") as sssdfile:
        sssdfile.write("ad_gpo_access_control = permissive")
    subprocess.Popen("systemctl restart sssd", stdout=subprocess.PIPE, shell=True)

# Tüm ayarlamalar yapıldıktan sonra domaine dahil etme işlemi yapılır
def domainJoin(domain_admin_password,domain_admin,domain):
    # Realm komutu ile domaine dahil eder
    command="echo "+ domain_admin_password +" | realm join --user=\""+domain_admin+"@"+domain.upper()+"\" "+domain.lower()
    cmd = subprocess.Popen(command, shell=True)
    cmd.communicate()
    # net ads dns komutu ile makineti domain DNS'ine kaydeder
    command="echo "+ domain_admin_password +" | net ads dns register -U "+domain_admin+"@"+domain.upper()
    cmd = subprocess.Popen(command, shell=True)
    cmd.communicate()

def main():
    # Gereksinimleri yükler
    installDependences()
    # Gerekli bilgileri kullanıcıdan alır, domain bilgilerini ip adresinden üretir
    domain_ip, domain_admin, domain_admin_password, client_hostname, domain, domain_netbios_name = getInputs()
    
    # Kullanıcının DNS'ini domain sunucusu olarak ayarlar
    editDNS(domain_ip,domain)
    # Sunucu DNS'ine kendisini kaydettirebilmek için makine adını düzenler
    editHosts(client_hostname,domain)
    # Domain sunucusu ile zamanının eşitler
    setTime(domain_ip)

    # İstemcide bulunan sambanın konfigürasyon dosyasını düzenler 
    addSAMBA(domain_netbios_name,domain)
    # sssd'nin konfigürasyon dosyasını oluşturan realmd servisinin ayarları yapılır
    addREALM(domain)

    # Dil ayarlarından gerekli olanları ingilizceye çevirir
    editLocales()

    # Domaine dahil eder ve ip adresini domain DNS'ine ekler
    domainJoin(domain_admin_password,domain_admin,domain)

    # Bilet kullanımı için gerekli ayarlamaları yapar
    krbDefaultRealm(domain.upper())
    # Kullanıcının ilk girişinde ev dizinini oluşturur
    addMkHomedir()
    # Giriş ekranının performanslı çalışmasını sağlar
    editLightdmConf()
    # Domain admins grubunu sudoers'e ekler
    addSudoers(domain)
    # IP değişikliğinde bunun domain DNS'inde güncellenmesini sağlar
    addDNSUpdateOnStart()
    # SSSD ayar dosyasına gerekli ek ayarları ekler
    editSSSD()

    cmd = subprocess.Popen("realm permit -a", shell=True)
    cmd.communicate()
    
    # BU ISLEMLER TAMAMLANDIKTAN SONRA MAKINE YENIDEN BASLATILMALIDIR

if __name__ == "__main__":
    main()