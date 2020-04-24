# Openldap Kurulum ve Kullanım
Opendap dizin servisi kurulumu için slapd, ldap araçları için ldap-utils paketleri yüklenir
```
$ sudo apt update 
$ sudo apt install -y slapd ldap-utils
```
slapcat komutu ile kurulu boş dizin çıktısı görüntülenir
```
$ sudo slapcat
dn: dc=nodomain
objectClass: top
objectClass: dcObject
objectClass: organization
o: nodomain
dc: nodomain
structuralObjectClass: organization
entryUUID: f9de7768-1aa7-103a-8a8a-6b383f6b329b
creatorsName: cn=admin,dc=nodomain
createTimestamp: 20200424184847Z
entryCSN: 20200424184847.818438Z#000000#000#000000
modifiersName: cn=admin,dc=nodomain
modifyTimestamp: 20200424184847Z

dn: cn=admin,dc=nodomain
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator
userPassword:: e1NTSEF9VVlsRFJYYXdIcVF2bmN0cjRLQXg5RDB5SExPallTdHU=
structuralObjectClass: organizationalRole
entryUUID: f9e89b26-1aa7-103a-8a8b-6b383f6b329b
creatorsName: cn=admin,dc=nodomain
createTimestamp: 20200424184847Z
entryCSN: 20200424184847.884942Z#000000#000#000000
modifiersName: cn=admin,dc=nodomain
modifyTimestamp: 20200424184847Z
```
ldap yapılandırması için aşağıdaki komut çalıştırılır
```diff
dpkg-reconfigure slapd
┌───────────────────────┤ Configuring slapd ├──────────────────────────────────────────────┐
│                                						                                               │ 
│ If you enable this option, no initial configuration or database will be created for you. │ 
│                                                                                          │ 
│ Omit OpenLDAP server configuration?                                                      │ 
│                                                                                          │ 
│          <Yes>                           ->  <No>                                        │ 
│                                                                                          │ 
└──────────────────────────────────────────────────────────────────────────────────────────┘ 
┌────────────────────────────────────────────────────────────────────────────────┤ Configuring slapd ├──────────────────────────────────────────────────────────────────────────────┐
│ The DNS domain name is used to construct the base DN of the LDAP directory. For example, 'foo.example.org' will create the directory with 'dc=foo, dc=example, dc=org' as base DN.│ 
│                                                                                                   																                                               	│ 
│ DNS domain name:                                                                                                                                                               		│ 
│                                                                                                                                          																					│ 
│ ornek.ldap.com___________________________________________________________________________________________________________________________________________________________________	│ 
│                                                                                                                                          																					│ 
│                                                                                       <Ok>                                                                   											│ 
│                                                                                                                                                                                   │ 
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ 
 ┌──────────────────────────────────┤ Configuring slapd ├─────────────────────────────────┐
 │ Please enter the name of the organization to use in the base DN of your LDAP directory.│ 
 │                                                                                        │ 
 │ Organization name:                                                                     |
 │                                                                                        │ 
 │ ornek__________________________________________________________________________________│ 
 │                                                                                        │ 
 │                                          <Ok>                                          │ 
 │                                                                                        │ 
 └────────────────────────────────────────────────────────────────────────────────────────┘ 
┌─────────────────────────┤ Configuring slapd ├─────────────────────────┐
│ Please enter the password for the admin entry in your LDAP directory. │ 
│                                                                       │ 
│ Administrator password:                                               │ 
│                                                                       │ 
│ ********_____________________________________________________________	│ 
│                                                                       │ 
│                             ->  <Ok>                                  │ 
│                                                                       │ 
└───────────────────────────────────────────────────────────────────────┘ 
┌─────────────────────────────────────┤ Configuring slapd ├─────────────────────────────────────────────────┐
│ Please enter the admin password for your LDAP directory again to verify that you have typed it correctly. │ 
│                                                                                                           │ 
│ Confirm password:                                                                                         | 
│                                                                                                           │ 
│ ********________________________________________________________________________________________________ 	│ 
│                                                                                                           │ 
│                                               ->  <Ok>                                                    │ 
│                                                                                                           │ 
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘ 

┌─────────────────────────────────┤ Configuring slapd ├─────────────────────────────────────────────────────────────────────────────────────────────┐
│ HDB and BDB use similar storage formats, but HDB adds support for subtree renames. Both support the same configuration options.                   │ 
│                                                                                                                                                   │ 
│ The MDB backend is recommended. MDB uses a new storage format and requires less configuration than BDB or HDB.					       	                  │ 
│                                                                                                                                                   │ 
│ In any case, you should review the resulting database configuration for your needs. See /usr/share/doc/slapd/README.Debian.gz for more details.  	│ 
│                                                                                                                                                  	│ 
│ Database backend to use:                                                   																											                  │ 
│                                                                                                                                                  	│ 
│                                                                       BDB                                                                        	│ 
│                                                                       HDB                                                                        	│ 
│                                                                   ->  MDB                                                                        	│ 
│                                                                                                                                                  	│ 
│                                                                                                                                                  	│ 
│                                                                      <Ok>                                                                        	│ 
│                                                                                                                                                  	│ 
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
┌───────────────┤ Configuring slapd ├─────────────────────────────┐
│                                                               	│ 
│                                                               	│ 
│                                                               	│ 
│ Do you want the database to be removed when slapd is purged?  	│ 
│                                                               	│ 
│                <Yes>               ->  <No>                   	│ 
│                                                               	│ 
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────┤ Configuring slapd ├───────────────────────────────────────────────────────────────────────────────┐
│                                                                                                                         │
│ There are still files in /var/lib/ldap which will probably break the configuration process. If you enable this option,	│
│ the maintainer scripts will move the old database files out of the way before creating a new database.  			          │ 
│                                                                                                                         │ 
│ Move old database?                                                                                                      │ 
│                                                                                                                         │ 
│                   -> <Yes>                                                <No>								                          │ 
│                                                                                                                         │ 
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ 
```
Ayarlar yapılandırıldıktan sonra dizin özeti aşağıdaki gibi ayarladığınız şekilde gözükmeli. domain bilgilerinde **nodomain** yazmamalı
```
$ slapcat

dn: dc=ornek,dc=ldap,dc=com
objectClass: top
objectClass: dcObject
objectClass: organization
o: ornek
dc: ornek
structuralObjectClass: organization
entryUUID: f7bb731e-1741-103a-8f65-65fb6ccf9071
creatorsName: cn=admin,dc=ornek,dc=ldap,dc=com
createTimestamp: 20200420110102Z
entryCSN: 20200420110102.078755Z#000000#000#000000
modifiersName: cn=admin,dc=ornek,dc=ldap,dc=com
modifyTimestamp: 20200420110102Z

dn: cn=admin,dc=ornek,dc=ldap,dc=com
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator
userPassword:: e1NTSEF9STFGUjc3dmVKbkh1c0lSN0Y5a1VTOFgybGExeDNCOHg=
structuralObjectClass: organizationalRole
entryUUID: f7bc71c4-1741-103a-8f66-65fb6ccf9071
creatorsName: cn=admin,dc=ornek,dc=ldap,dc=com
createTimestamp: 20200420110102Z
entryCSN: 20200420110102.085332Z#000000#000#000000
modifiersName: cn=admin,dc=ornek,dc=ldap,dc=com
modifyTimestamp: 20200420110102Z
```

# ldap organizasyon oluşturma
organizasyon.ldif dosyası oluşturulur ve organizationalUnit türünde veri oluşturulur. Örnek iki organizasyonu aşağıdaki komut ile oluşturabilirsiniz. Terminal ekranında echo komutu yazılan, metni dosyaya yazma işlemi yapar.
```
echo "dn: ou=kisiler,dc=ornek,dc=ldap,dc=com
objectClass: organizationalUnit
ou: people

dn: ou=gruplar,dc=ornek,dc=ldap,dc=com
objectClass: organizationalUnit
ou: groups 
" > organizasyon.ldif
```
Oluşturulan ldiff ile belirtilen özelliklere sahip organizasyonlar, ldapadd komutu ile eklenir. 
```
ldapadd -x -D cn=admin,dc=ornek,dc=ldap,dc=com -W -f organizasyon.ldif
```

# Ldap grup oluşturma
grup.ldif adında bir dosya oluşturulur ve içerisinde türü posixGroup olan 2 adet veri oluşturulur. posixGroup linuxtaki kullanıcı gruplarını ifade eden sınıftır. Buna uygun olarak gidNumber (grup id'si) özelliğine sahiptir.
Gruba kullanıcı eklenmek istendiğinde memberUid özelliği kullanılabilir. 
```
echo "dn: cn=duygu,ou=gruplar,dc=ornek,dc=ldap,dc=com
objectClass: posixGroup
cn: duygu
gidNumber: 2000
memberUid: duygu

dn: cn=ali,ou=gruplar,dc=ornek,dc=ldap,dc=com
objectClass: posixGroup
cn: ali
gidNumber: 2001
memberUid: ali
" > grup.ldif
```
Oluşturulan ldiff ile belirtilen özelliklere sahip organizasyonlar, ldapadd komutu ile eklenir. 
```
ldapadd -x -D  cn=admin,dc=ornek,dc=ldap,dc=com -W -f grup.ldif 
```
# Ldap Kisi oluşturma
kisiler.ldif adında bir dosya oluşturulur ve içerisinde olan 2 adet veri oluşturulur. 
inetOrgPerson sınıfı openldaptaki standart bir insan türünü tanımlar. İş tanımı, telefonu, mail adresi gibi temel özellikleri içerir.
posixAccount sınıfı linuxtaki standart bir kullanıcı için gerekli olan özellikleri içerir. Kullanıcı id'si, login shell'i gibi
shadowAccount sınıfı linuxta kullanıcının parola girerek kimlik doğrulaması için gerekli olan sınıftır (/etc/shadow içerisindeki bilgileri içerir)
```
echo "dn: uid=duygu,ou=kisiler,dc=ornek,dc=ldap,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: duygu
sn: olmez
loginShell: /bin/bash
uidNumber: 2000
gidNumber: 2000
homeDirectory: /home/duygu
mobile: 5551132434

dn: uid=veli,ou=kisiler,dc=ornek,dc=ldap,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: ali
sn: veli
loginShell: /bin/bash
uidNumber: 2001
gidNumber: 2001
homeDirectory: /home/ali
" > kisiler.ldif
ldapadd -x -D  cn=admin,dc=ornek,dc=ldap,dc=com -W -f kisiler.ldif 
```
# Ldap kisi sorgusu
* openldaptaki kökten itibaren tüm kullanıcıları bulur
ldapsearch -x -b "dc=ornek,dc=ldap,dc=com" -H ldap://127.0.0.1 "objectClass=inetOrgPerson" -

* openldaptaki kökten itibaren telefon numarası boş olmayan kullanıcıları bulur
ldapsearch -x -b "dc=ornek,dc=ldap,dc=com" -H ldap://127.0.0.1 "mobile=*" -
