cd
if [ -d ./sondensucher]  # existiert Ordner Sondensucher
	then
        echo =====Sondensucher aktualisiert=====
   		cd sondensucher/
        git pull
   	else
		echo =====Ordner Skripte wird erstellt=====
		git clone https://github.com/woehrer12/sondensucher.git
fi