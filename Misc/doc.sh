#!/bin/bash

dir_fly="../Code/fly"
dir_fontes="../doc/fontes"
dir_doc="../doc"

if ! grep -q "'django_extensions'," "$dir_fly/fly/settings.py"
then
	sed -i "/INSTALLED_APPS = \[/a 'django_extensions'," "$dir_fly/fly/settings.py"
fi

# Diagrama de classes
nome="todos"
opcoes="--all-applications"
arquivo_dot="$dir_fontes/dc-$nome.dot"
layouts=(circo dot fdp)

"$dir_fly/manage.py" graph_models "$opcoes" > "$arquivo_dot" &&
sed -i 's/arrowtail=dot/arrowtail=open/g' "$arquivo_dot"

for layout in "${layouts[@]}"
do
	if [ -f "$arquivo_dot" ]
	then
		"$layout" "$arquivo_dot" -Tpng > "$dir_doc/dc-$nome-$layout.png"
	else
		echo "Arquivo '$arquivo_dot' não encontrado"
	fi
done

# MER
# Opções do DbVisualizer: Show One Link/Column [on], Links to Colums [off]
arquivo_svg="$dir_fontes/mer.svg"
if [ -f "$arquivo_svg" ]
then
	inkscape -z -e "$dir_doc/mer.png" -d256 "$arquivo_svg" > /dev/null
else 
	echo "Arquivo '$arquivo_svg' não encontrado"
fi

sed -i "/'django_extensions',/d" "$dir_fly/fly/settings.py"
