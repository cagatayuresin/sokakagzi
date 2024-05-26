# Sokak Ağzı Projesi

Sokak Ağzı, Urban Dictionary tarzında bir sözlük sitesidir. Kullanıcılar, çeşitli konular hakkında açıklamalar yazabilir, bu açıklamaları beğenebilir, beğenmeyebilir ve favorilerine ekleyebilirler. Proje, Django ve Tailwind CSS kullanılarak geliştirilmiştir.

## Özellikler

- Kullanıcı Kayıt ve Giriş
- Kullanıcı Profili Güncelleme
- Yeni Konu ve Açıklama Ekleme
- Açıklama Beğenme ve Beğenmeme
- Açıklama Favorileme
- Favoriler ve Kullanıcı Açıklamaları Sayfalaması
- Konu Arama
- Kullanıcı Avatarı Yükleme
- Kullanıcıya Özel Açıklama ve Favoriler Sayfaları

## Kurulum

### Gereksinimler

- Docker
- Docker Compose

### Adımlar

1. Bu projeyi yerel makinenize klonlayın:

   ```bash
   git clone https://github.com/kullanici/sokakagzi.git
   cd sokakagzi
   ```
   
2. Gerekli ortam değişkenlerini tanımlayın. Proje dizininde .env dosyasını oluşturun ve aşağıdaki değişkenleri ekleyin:

   ```env
     SECRET_KEY=your_secret_key
     DEBUG=True
     DB_NAME=your_db_name
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     EMAIL_HOST=your_email_host
     EMAIL_PORT=your_email_port
     EMAIL_USE_TLS=your_email_use_tls
     EMAIL_HOST_USER=your_email_host_user
     EMAIL_HOST_PASSWORD=your_email_host_password
     DEFAULT_FROM_EMAIL=your_default_from_email
     DJANGO_SUPERUSER_USERNAME=your_admin_username
     DJANGO_SUPERUSER_EMAIL=your_admin_email
     DJANGO_SUPERUSER_PASSWORD=your_admin_password
     SITE_DOMAIN=your_site_domain
     SITE_NAME=Sokak Agzi
     SITE_ID=1
     ```
3. Docker Compose ile projeyi başlatın:

   ```bash
   docker-compose up --build
   ```
4. Tarayıcınızı açın ve http://localhost:8000 adresine gidin.

## Kullanım

### Kayıt ve Giriş

Ana sayfada Kayıt Ol ve Giriş Yap butonlarını kullanarak kullanıcı kaydı oluşturabilir veya mevcut kullanıcıyla giriş yapabilirsiniz.

### Profil Güncelleme

Giriş yaptıktan sonra Profil sayfasına giderek kullanıcı adınızı, e-posta adresinizi ve avatarınızı güncelleyebilirsiniz.

### Konu ve Açıklama Ekleme

Yeni bir konu eklemek için ana sayfadaki Yeni Başlık butonunu kullanın.

Bir konunun detay sayfasına giderek yeni açıklamalar ekleyebilirsiniz.

### Açıklamaları Beğenme ve Favorileme

Her açıklamanın altında beğenme, beğenmeme ve favorileme butonları bulunmaktadır. Kendi açıklamalarınızı beğenemez veya favorilerinize ekleyemezsiniz.

### Favoriler ve Yazdıklarım

Favorilerim sayfasında favorilerinize eklediğiniz tüm açıklamaları görebilirsiniz.

Yazdıklarım sayfasında kendi yazdığınız tüm açıklamaları görebilirsiniz.

### Arama

Sayfanın üst kısmındaki arama çubuğunu kullanarak konular arasında arama yapabilirsiniz.

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir pull request oluşturun. Herhangi bir sorunla karşılaşırsanız, issue açmaktan çekinmeyin.

## Lisans
Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakın.