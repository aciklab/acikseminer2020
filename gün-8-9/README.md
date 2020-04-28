# Samba Sunucusu Kurulumu
Bu paket için önerilen işletim sistemi **Pardus 19.2 Server**dır
SSH yüklü olan bir uzak sunucuya göndermek isteniyorsa scp ile 
```
scp /bilgisayarınızdaki_paketin_yolu/samba-20200423-221809.deb kullanıcı_adı@sunucu_IP
```
ya da sftp ile gönderebilirsiniz.
```
sftp kullanıcı_adı@sunucu_IP
> put /bilgisayarınızdaki_paketin_yolu/samba-20200423-221809.deb
```
Samba sunucusu kurulumu için samba-20200423-221809.deb paketinin bulunduğu dizine gidilir ve aşağıdaki komut çalıştırılır
```
sudo apt install -y ./samba-20200423-221809.deb  
```
# Samba Domaini oluşturma
samba-20200423-221809.deb   paketini yükledikten sonra aşağıdaki komutla domain kurulumunu yapabilirsiniz.
`home.lab` oluşturmak istediğiniz domain, `Passw0rd` ise administrator kullanıcısının parolası. Bu değerleri değiştirerek kullanabilirsiniz
```
smb-create-domain home.lab Passw0rd
```

# Pardus makineyi Windows ya da Samba domainine ekleme
domainjoin.py komutunu pardus makinesi kopyaladıktan sonra aşağıdaki komut ile çalıştırılır
```
sudo python /kodun_bulunduğu_yol/domainjoin.py
```
istenilen bilgilere Windows Aktif Dizin (2016 ya da 2019 kullanabilirsiniz) ya da Samba(4.11.3 versiyonu) sunucunlarının ve domaindeki yekili kullanıcıların parolalarını vererek domaine alma işlemini yapabilirsiniz.

**ÖNEMLİ: domaine aldıktan sonra istemci makinesini yeniden başlatmak gerekir**
# Pardus makinesini domainden çıkarma
Aşağıdaki komut ile domaine dahil olan bir makineyi domainden çıkarabilirsiniz
```
sudo realm leave --remove
```
