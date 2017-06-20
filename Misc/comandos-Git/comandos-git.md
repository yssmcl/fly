```git
git init
git remote add origin <URL-repositório>.git
git add -A
git commit -m "<mensagem>"
git push -u origin master
```

| Comando                                       | Descrição
| -------                                       | ---------
| `git init`                                    | Inicializa repositório
| `git status`                                  | Exibe status da área de preparação
| `git add <arquivos>`                          | Adiciona arquivos à área de preparação
| `git add -A`                                  | Adiciona todos os arquivos (recém-criados e modificados) à área de preparação
| `git commit -m "<mensagem>"`                  | Adiciona arquivos ao repositório local
| `git log`                                     | Exibe log de commits
|                                               | |
|                                               | |
| `git clone <URL-repositório>.git`             | Clona repositório
| `git fetch`                                   | Baixa commits do repositório remoto para o repositório local
| `git remote add origin <URL-repositório>.git` | Adiciona repositório remoto principal
| `git push -u <remoto> <local>`                | Upa mudanças feitas no repositório local para o repositório remoto
| `git pull <remoto> <local>`                   | Puxa mudanças feitas no repositório remoto para o repositório local ‒ equivalente a: `git fetch <remoto> && git merge origin/<local>`
|                                               | |
|                                               | |
| `git branch <branch>`                         | Cria branch
| `git branch -d <branch>`                      | Deleta branch `<branch>`
| `git branch -u <remoto>`                      | Configura upstream para `<remoto>`
| `git checkout <branch>`                       | Muda para `<branch>`
| `git merge <branch>`                          | Realiza merge de `<branch>` com `master`
|                                               | |
|                                               | |
| `git diff <arquivos>`                         | Compara arquivos do diretório de trabalho com os arquivos da área de preparação
| `git show <hash>`                             | Mostra os diffs do commit `<hash>`
| `git checkout -- <arquivo>`                   | A versão do arquivo no diretório de trabalho é substituída pela versão do repositório local
| `git reset [HEAD] <arquivos>`                 | Retira arquivos da área de preparação
| `git reset <hash>`                            | Apaga os commits posteriores ao commit `<hash>`, logo o HEAD commit se torna o commit `<hash>` (desfaz commits)
| `git rm <arquivo>`                            | Deleta o arquivo do diretório de trabalho ‒ equivalente a: `rm <arquivo> && git add <arquivo>`
| `git stash`                                   | Armazena mudanças no diretório de trabalho temporariamente
| `git stash pop`                               | Recupera mudanças armazenadas
