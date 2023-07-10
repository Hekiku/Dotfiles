# gnome-terminal
alias c='clear'

# control ls command output
alias ll='ls -lX --group-directories-first'
alias la='ls -lAX --group-directories-first'

# control cd command behavior
alias cdh='cd ~'
alias cd..='cd ..'
alias ...='cd ../../../'

# update debian linux server
alias update='sudo apt update'
alias upgrade='sudo apt upgrade'
alias upgradable='apt list --upgradable'
alias search='apt search'

# apt management
alias install='sudo apt install'
alias remove='sudo apt remove'
alias broken='sudo apt --fix-broken install'
alias aremove='sudo apt autoremove'

# snap management
alias slist='snap list'
alias sfind='snap find'
alias sinstall='sudo snap install'
alias srefresh='sudo snap refresh'
alias sremove='sudo snap remove'

# shutdown command
alias reboot='sudo reboot'
alias poweroff='sudo poweroff'
alias suspend='sudo suspend'

# resource usage
alias free='free -m'
alias df='df -h --exclude=squashfs'

# xampp
alias xamppon='sudo /opt/lampp/lampp start'
alias xamppoff='sudo /opt/lampp/lampp stop'

# extra features
alias clock='tty-clock -csS'

