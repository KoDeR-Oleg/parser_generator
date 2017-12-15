 #!/bin/bash

rm main.aux
rm main.idx
rm main_koi.ilg
rm main.ind
rm main.log
rm main.pdf
rm main.toc

xelatex main.tex
xelatex main.tex

iconv -f utf8 -t koi8 main.idx -o main_koi.idx
makeindex -s main.ist main_koi.idx
iconv -f koi8 -t utf8 main_koi.ind -o main.ind

xelatex main.tex

rm main.aux
rm main.idx
rm main_koi.ilg
rm main.ind
rm main.log
rm main.toc
rm main_koi.idx
rm main_koi.ind
