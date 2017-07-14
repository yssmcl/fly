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
arqv_dot="$dir_fontes/dc-$nome.dot"
layouts=(circo dot fdp)

"$dir_fly/manage.py" graph_models "$opcoes" > "$arqv_dot" &&
sed -i 's/arrowtail=dot/arrowtail=open/g' "$arqv_dot"

for layout in "${layouts[@]}"
do
	if [ -f "$arqv_dot" ]
	then
		"$layout" "$arqv_dot" -Tpng > "$dir_doc/dc-$nome-$layout.png"
	else
		echo "Arquivo '$arqv_dot' não encontrado"
	fi
done

# MER
# Opções do DbVisualizer: Show One Link/Column [on], Links to Colums [off]
arqv_svg="$dir_fontes/mer.svg"
if [ -f "$arqv_svg" ]
then
	inkscape -z -e "$dir_doc/mer.png" -d256 "$arqv_svg" > /dev/null
else 
	echo "Arquivo '$arqv_svg' não encontrado"
fi

sed -i "/'django_extensions',/d" "$dir_fly/fly/settings.py"
