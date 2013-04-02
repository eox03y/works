if &term =~ "xterm-debian" || &term =~ "xterm-xfree86"
set t_Co=16
set t_Sf=^[[3%dm
set t_Sb=^[[4%dm
set t_kb=^H
fixdel
endif

if has("syntax")
syntax on " Default to no syntax highlightning 
endif

set ruler
set tabstop=4
set shiftwidth=4
set smartindent

