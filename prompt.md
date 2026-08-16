nano ~/.bashrc

source ~/.bashrc

echo "IyA9PT09PSBQcm9tcHQgcHJvZmlzc2lvbmFsIGNvbG9yaWRvID09PT09CgpSRVNFVD0nXFtcMDMzWzBtXF0nCkJPTEQ9J1xbXDAzM1sxbVxdJwpHUkVFTj0nXFtcMDMzWzMybVxdJwpCTFVFPSdcW1wwMzNbMzRtXF0nCllFTExPVz0nXFtcMDMzWzMzbVxdJwpDWUFOPSdcW1wwMzNbMzZtXF0nClJFRD0nXFtcMDMzWzMxbVxdJwpNQUdFTlRBPSdcW1wwMzNbMzVtXF0nCk9SQU5HRT0nXFtcMDMzWzM4OzU7MjA4bVxdJwoKX19idWlsZF9wcm9tcHQoKSB7CiAgICBsb2NhbCBleGl0X2NvZGU9JD8KCiAgICAjIC0tLS0gR2l0IC0tLS0KICAgIGxvY2FsIGdpdF9pbmZvPSIiCiAgICBsb2NhbCBicmFuY2gKICAgIGJyYW5jaD0kKGdpdCBzeW1ib2xpYy1yZWYgLS1zaG9ydCBIRUFEIDI+L2Rldi9udWxsKQogICAgaWYgWyAtbiAiJGJyYW5jaCIgXTsgdGhlbgogICAgICAgIGxvY2FsIHN0YXR1cz0iIgogICAgICAgIGlmICEgZ2l0IGRpZmYgLS1xdWlldCAyPi9kZXYvbnVsbDsgdGhlbgogICAgICAgICAgICBzdGF0dXM9IiR7c3RhdHVzfSoiCiAgICAgICAgZmkKICAgICAgICBpZiAhIGdpdCBkaWZmIC0tY2FjaGVkIC0tcXVpZXQgMj4vZGV2L251bGw7IHRoZW4KICAgICAgICAgICAgc3RhdHVzPSIke3N0YXR1c30rIgogICAgICAgIGZpCiAgICAgICAgaWYgWyAtbiAiJChnaXQgc3RhdHVzIC0tcG9yY2VsYWluIDI+L2Rldi9udWxsIHwgZ3JlcCAnXj8/JykiIF07IHRoZW4KICAgICAgICAgICAgc3RhdHVzPSIke3N0YXR1c30/IgogICAgICAgIGZpCiAgICAgICAgZ2l0X2luZm89IiAoJGJyYW5jaCRzdGF0dXMpIgogICAgZmkKCiAgICAjIC0tLS0gS3ViZXJuZXRlcyAtLS0tCiAgICBsb2NhbCBrOHNfaW5mbz0iIgogICAgaWYgY29tbWFuZCAtdiBrdWJlY3RsID4vZGV2L251bGwgMj4mMTsgdGhlbgogICAgICAgIGxvY2FsIGNvbnRleHQKICAgICAgICBjb250ZXh0PSQoa3ViZWN0bCBjb25maWcgY3VycmVudC1jb250ZXh0IDI+L2Rldi9udWxsKQogICAgICAgIGlmIFsgLW4gIiRjb250ZXh0IiBdOyB0aGVuCiAgICAgICAgICAgIGxvY2FsIG5hbWVzcGFjZQogICAgICAgICAgICBuYW1lc3BhY2U9JChrdWJlY3RsIGNvbmZpZyB2aWV3IC0tbWluaWZ5IC0tb3V0cHV0ICdqc29ucGF0aD17Li5uYW1lc3BhY2V9JyAyPi9kZXYvbnVsbCkKICAgICAgICAgICAgbmFtZXNwYWNlPSR7bmFtZXNwYWNlOi1kZWZhdWx0fQogICAgICAgICAgICBrOHNfaW5mbz0iIGs4czooJGNvbnRleHQvJG5hbWVzcGFjZSkiCiAgICAgICAgZmkKICAgIGZpCgogICAgUFMxPSIke0JPTER9JHtHUkVFTn1cdSR7UkVTRVR9QCR7Qk9MRH0ke0dSRUVOfVxoJHtSRVNFVH0gJHtDWUFOfVtcdF0ke1JFU0VUfVxuIgogICAgUFMxKz0iJHtCTFVFfVx3JHtZRUxMT1d9JHtnaXRfaW5mb30ke09SQU5HRX0ke2s4c19pbmZvfSR7UkVTRVR9XG4iCiAgICBQUzErPSIke01BR0VOVEF9XCQke1JFU0VUfSAiCn0KClBST01QVF9DT01NQU5EPV9fYnVpbGRfcHJvbXB0CgojID09PT09IEFsaWFzIHBlcnNvbmFsaXphZG9zID09PT09CmFsaWFzIGdsPSdnY2xvdWQgYXV0aCBsb2dpbicK" | base64 -d > ~/.bashrc


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
