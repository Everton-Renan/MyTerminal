# MyTerminal
MyTerminal é uma ferramenta CLI (Command Line Interface) que facilita a criação de arquivos, diretórios, ambientes virtuais e a instalação de módulos Python diretamente pelo terminal.
## Avisos
**O arquivo data.json precisa não pode ter o nome ou o diretório alterado.**<br>
**Esta aplicação roda comandos direto no terminal, então utilize com cuidado.**<br>
**Este projeto foi criado apenas para fins de estudos.**

## Testado em
- Windows 11
- Kali Linux


<h3>Comando create</h3>
<p>Gerencia a criação de arquivos, diretórios e ambientes virtuais.</p>
<p>Argumentos Posicionais:</p>
<p>type - Escolhe o que será criado ex:.(file, venv, dir).</p>
<p>name - Escolhe o nome do arquivo, pasta ou ambiente virtual.</p>
<p>Sintaxe: create type name.</p>
<p>Flag -i para a instalação de módulos python junto com a criação do ambiente virtual.</p>
<p>Sintaxe: create venv name -i django flask</p>

<h3>Comando install</h3>
<p>Comando para a instalação de módulos python à ambientes virtuais já criados.</p>
<p>Argumentos posicionais:</p>
<p>name - Nome do ambiente virtual.</p>
<p>Sintaxe: install name django flask</p>

<h3>Comando select_folder</h3>
<p>Comando para a seleção da pasta em que o terminal irá trabalhar.</p>
<p>Sintaxe: select_folder</p>
<p>Flag -r para a restauração da última pasta salva no arquivo data.json.</p>
<p>Sintaxe: select_folder -r</p>
<p>Flag -p permite o envio do caminho pelo terminal.</p>
<p>Sintaxe: select_folder -p caminho/para/a/pasta</p>

<h3>Comando ls</h3>
<p>Comando para listar todos os itens da pasta atual.</p>
<p>Sintaxe: ls</p>

<h3>Comando cd</h3>
<p>Comando para alterar a pasta atual.</p>
<p>Argumentos posicionais:</p>
<p>dir - Nome do diretório que para qual deseja alterar.</p>
<p>Sintaxe: cd dir</p>
