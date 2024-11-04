# Visualização de objetos 3D com Projeção Ortogonal e Perspectiva em Python

## Bibliotecas Utilizadas

- [pyGame](https://www.pygame.org/)
- sys
- math

## Como Usar

1. Abra o terminal e execute o comando `python grupo6.py <objeto.obj>`, onde `<objeto.obj>` é o nome do arquivo .obj que deseja renderizar. Arquivos muito grandes podem comprometer o desempenho do programa. Para fácil visualização, utilize um dos 3 objetos fornecidos neste repositório.

2. Uma janela irá abrir com a visualização dos objetos. O objeto da esquerda (azul) utiliza projeção ortogonal, enquanto o da direita (vermelho) utiliza perspectiva. 

<img src="https://i.imgur.com/FpqCcPY.png">

## Comandos do Teclado

- `f`: Alternar o modo de preenchimento (On / Off)
- `p`: Alternar o modo de exibição dos pontos (On / Off)
- `l`: Alternar o modo de exibição das linhas (On / Off)
- `r`: Alternar o modo de rotação automática (On / Off)
- `shift + r`:  Reseta a rotação do objeto para a inicial
- `numpad 1-9`: Coloca o objeto na posição correspondente (igual ao teclado numérico)
- `setas`: Move os objetos
- `scroll`: Altera o zoom
- `,`: Diminui a distância entre os objetos
- `.`: Aumenta a distância entre os objetos
- `1`: Alterna a exibição do objeto da projeção ortogonal
- `2`: Alterna a exibição do objeto da projeção em perspectiva
- `numpad +`: Rotaciona o objeto
- `numpad -`: Retorna a rotação do objeto


![](https://github.com/NicolasArvani/python-projecoes/blob/main/simulacao.gif)

#### Créditos

Projeto feito para a matéria de computação gráfica (COG), do Instituto Federal de São Paulo (IFSP), campus Salto.

Grupo 6:
- [Nicolas Arvani](https://github.com/nicolasarvani)
- [Isabella Bicudo de Souza](https://github.com/isabellabsouza)
- Erick Henrique de Araújo Moreira
- Fernanda Miyuki Egawa
- Gustavo Milan Cardoso
- Maria Eduarda Guedes