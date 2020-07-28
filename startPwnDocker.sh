#!/bin/sh

echo "Launching pwndocker"

cat > /tmp/.pwnDockerBashAliases << :EOF
gropper () { ropper -f "\$1" --nocolor | grep "\$2"; }
export PS1="\n--------------------\n\w \T \$?\n\\\\$ \[\$(tput sgr0)\]"
:EOF

sg docker 'cd $(pwd); docker run -d --rm -h banana --name banana -v /tmp/.pwnDockerBashAliases:/root/.bash_aliases  -v $(pwd):/ctf/work -p 23946:23946 --cap-add=SYS_PTRACE skysider/pwndocker@sha256:7a91fcee7f34679a40bef80f82a2872298530b0c78c2e0ac9fd183c15fe60ba2 >/dev/null 2>&1'
sg docker 'docker exec -it banana /bin/bash'
