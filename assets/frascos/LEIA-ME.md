# Fotos dos frascos

Nomes exatos que o `index.html` procura (WebP, máx. 1000px de largura):

    sweet-reign.webp
    royal-bloom.webp
    midnight-grace.webp
    azure-mist.webp
    golden-aura.webp

Enquanto o arquivo não existir, o card mostra só o nome e o perfil olfativo —
nunca uma moldura vazia.

Converter: `cwebp -q 82 -resize 1000 0 foto.jpg -o sweet-reign.webp`
Pode subir o `.jpg` aqui que a conversão é um comando.

## mini/

`mini/` é gerado pelo mesmo script — são as miniaturas de 140px que aparecem
na lista de `pedido.html`. Não precisa subir nada aqui: saem do mesmo original.
