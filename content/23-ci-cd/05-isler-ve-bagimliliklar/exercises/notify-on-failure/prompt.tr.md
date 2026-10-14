Hattın sonuna bir `notify` işi ekle:

- `deploy`'u beklesin.
- Yalnızca hatta bir şey **düştüğünde** çalışsın.
- Makine `ubuntu-latest`; tek adım: `echo` ile bir mesaj yazdır.

Dikkat: test düşerse `deploy` düşmez, **atlanır**. Koşul bunu da kapsamalı.
