nano ~/.bashrc

source ~/.bashrc


# ===== Prompt profissional colorido =====

parse_git_branch() {
    local branch
    branch=$(git symbolic-ref --short HEAD 2>/dev/null) || return
    local status=""

    if ! git diff --quiet 2>/dev/null; then
        status="${status}*"
    fi
    if ! git diff --cached --quiet 2>/dev/null; then
        status="${status}+"
    fi
    if [ -n "$(git status --porcelain 2>/dev/null | grep '^??')" ]; then
        status="${status}?"
    fi

    echo " ($branch$status)"
}

parse_k8s_context() {
    command -v kubectl >/dev/null 2>&1 || return

    local context
    context=$(kubectl config current-context 2>/dev/null)
    [ -z "$context" ] && return

    local namespace
    namespace=$(kubectl config view --minify --output 'jsonpath={..namespace}' 2>/dev/null)
    namespace=${namespace:-default}

    echo " ⎈ ($context/$namespace)"
}

RESET='\[\033[0m\]'
BOLD='\[\033[1m\]'
GREEN='\[\033[32m\]'
BLUE='\[\033[34m\]'
YELLOW='\[\033[33m\]'
CYAN='\[\033[36m\]'
RED='\[\033[31m\]'
MAGENTA='\[\033[35m\]'
ORANGE='\[\033[38;5;208m\]'

PS1="${BOLD}${GREEN}\u${RESET}@${BOLD}${GREEN}\h${RESET} ${CYAN}[\t]${RESET}\n"
PS1+="${BLUE}\w${YELLOW}\$(parse_git_branch)${ORANGE}\$(parse_k8s_context)${RESET}\n"
PS1+="${MAGENTA}➜${RESET} "

export PS1

export PROMPT_COMMAND='if [ $? -ne 0 ]; then echo -ne "\033[31m"; fi'




# ===== Alias personalizados =====
alias gl='gcloud auth login'
alias glp='gcloud auth login && gcloud config set project meu-projeto-id'

alias gs='git status'
alias gp='git pull'
alias gc='git commit -m'
alias k='kubectl'
alias ll='ls -la'
alias cls='clear'


# ===== Alias: Git =====
alias g='git'
alias gs='git status'
alias ga='git add'
alias gaa='git add --all'
alias gc='git commit -m'
alias gca='git commit -a -m'
alias gp='git push'
alias gpl='git pull'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gb='git branch'
alias gl='git log --oneline --graph --decorate -n 20'
alias gd='git diff'
alias gds='git diff --staged'
alias gst='git stash'
alias gstp='git stash pop'
alias gcl='git clone'

# ===== Alias: gcloud =====
alias gcl-login='gcloud auth login'
alias gcl-list='gcloud projects list'
alias gcl-set='gcloud config set project'
alias gcl-current='gcloud config get-value project'
alias gcl-ls-instances='gcloud compute instances list'
alias gcl-ssh='gcloud compute ssh'
alias gcl-configs='gcloud config configurations list'

# ===== Alias: kubectl =====
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgd='kubectl get deployments'
alias kgn='kubectl get nodes'
alias kga='kubectl get all'
alias kdp='kubectl describe pod'
alias kds='kubectl describe svc'
alias kdd='kubectl describe deployment'
alias kl='kubectl logs'
alias klf='kubectl logs -f'
alias kex='kubectl exec -it'
alias kctx='kubectl config current-context'
alias kns='kubectl config set-context --current --namespace'
alias kaf='kubectl apply -f'
alias kdel='kubectl delete'

# ===== Alias: Helm =====
alias h='helm'
alias hls='helm list'
alias hi='helm install'
alias hu='helm upgrade'
alias hun='helm uninstall'
alias hs='helm search repo'
alias hro='helm rollback'
alias hst='helm status'

# ===== Alias: Python =====
alias py='python'
alias py3='python3'
alias pip='python -m pip'
alias venv='python -m venv venv'
alias activate='source venv/Scripts/activate'
alias runserver='python manage.py runserver'
alias reqs='pip install -r requirements.txt'
alias freeze='pip freeze > requirements.txt'
